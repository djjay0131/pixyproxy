# service/image_service.py
"""
This module defines the ImageServiceInterface and its implementation, ImageService.

The ImageServiceInterface is an abstract base class that outlines the methods any image service should implement. These methods include creating an image, retrieving an image by its GUID, retrieving all image details, and retrieving the content of an image by its GUID.

The ImageService class is a concrete implementation of the ImageServiceInterface. It uses an image repository to interact with the database. Each method starts a database transaction, performs the necessary operations, and then either commits the transaction if everything went well or rolls it back in case of an exception.

Author: djjay
Date: 2024-03-30
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError
from core import image_generator
from core.exceptions import ConstraintViolationError, DataValidationError, ImageException, InvalidOperationError
from data.database_context import DatabaseContext
from data import db_pool, local_storage
from data.image_repository import ImageRepositoryInterface
from core.models import ImageDetail, ImageDetailCreate
from typing import List

class ImageServiceInterface:
    """
    Interface for the ImageService.
    Author: djjay
    Date: 2022-03-30
    """

    def create_image(self, image_detail: ImageDetailCreate) -> ImageDetail:
        """
        Creates an image.

        Parameters:
        image_detail (ImageDetailCreate): The details of the image to be created.

        Returns:
        Image: The created image.
        """
        pass

    def get_image_details_by_guid(self, guid: str) -> ImageDetail:
        """
        Gets an image by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        ImageDetail: The details of the image.
        """
        pass

    def get_all_image_details(self) -> List[ImageDetail]:
        """
        Gets all image details.

        Returns:
        List[ImageDetail]: The details of all images.
        """
        pass

    def get_image_content(self, guid: str) -> bytes:
        """
        Gets the content of an image by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        bytes: The content of the image.
        """
        pass

class ImageService(ImageServiceInterface):
    def __init__(self, image_repo: ImageRepositoryInterface, image_generator: image_generator):
        self.image_repo = image_repo
        self.image_generator = image_generator

    def create_image(self, image: ImageDetailCreate) -> ImageDetail:
        try:
            image = ImageDetailCreate(**image.dict())
        except ValidationError as e:
            raise ConstraintViolationError(str(e))

        with DatabaseContext() as db:
            db.begin_transaction()
            # Generate the image and save it to the database
            image_detail = self.image_generator.generate_image(image)
            db.commit_transaction()

        return image_detail

    def get_image_details_by_guid(self, guid: str) -> ImageDetail:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                image = self.image_repo.get_image_details_by_guid(guid)
                db.commit_transaction()
                return image
            except ImageException as e:
                db.rollback()
                raise DataValidationError("Invalid GUID provided.") from e

    def get_image_content(self, guid: str) -> bytes:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                image = self.image_repo.get_image_content(guid)
                db.commit_transaction()
                return image
            except ImageException as e:
                db.rollback()
                raise DataValidationError("Invalid GUID provided.") from e
            
    def get_all_image_details(self) -> List[ImageDetail]:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                images = self.image_repo.get_all_image_details()
                db.commit_transaction()
                return images
            except ImageException as e:
                db.rollback()
                raise InvalidOperationError("Unable to retrieve all image details.") from e