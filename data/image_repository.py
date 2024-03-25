# data/image_repository.py
"""
This module defines the ImageRepositoryInterface, an abstract base class (ABC) for image repositories in the PixyProxy system.

The ImageRepositoryInterface declares two methods: `create_image` and `get_image_details_by_guid`.

The `create_image` method is expected to create a new image record in the database and return its GUID.

The `get_image_details_by_guid` method is expected to retrieve the details of an image from the database using its GUID.

Concrete implementations of this interface should provide specific logic for interacting with the database or other data sources.

Author: djjay
Date: 2024-03-20
"""

from typing import List

from fastapi import Response
from data import get_current_db_context
from data.database_context import DatabaseContext
from core.models import ImageDetail, ImageDetailCreate
from core.exceptions import ImageNotFoundError
from core.image_columns import ImageColumns 
import os
from pathlib import Path

from abc import ABC, abstractmethod


class ImageRepositoryInterface:
    """
    Interface for the ImageRepository.
    Author: djjay
    Date: 2022-03-30
    """

    def create_image(self, guid: str, filename: str, prompt: str) -> ImageDetail:
        """
        Creates an image.

        Parameters:
        guid (str): The GUID of the image.
        filename (str): The filename of the image.
        prompt (str): The prompt used to generate the image.

        Returns:
        Image: The created image.
        """
        pass

    def get_image_by_guid(self, guid: str) -> ImageDetail:
        """
        Gets an image by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        Image: The image.
        """
        pass

    def get_all_image_details(self) -> List[ImageDetail]:
        """
        Gets all image details.

        Returns:
        List[Image]: The details of all images.
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
    
class MySQLImageRepository(ImageRepositoryInterface):
    def create_image(self, prompt: str, guid: str, filename: str) -> ImageDetail:
        """
        Creates an image in the database and returns its ImageDetail.

        Parameters:
        prompt (str): The prompt for the image.

        Returns:
        ImageDetail: The ImageDetail of the created image.
        """
        # Create the image details record in the database
        query = """
        INSERT INTO images (guid, filename, prompt)
        VALUES (%s, %s, %s)
        """
        values = (guid, filename, prompt)
        db = get_current_db_context()
        db.cursor.execute(query, values)

        # Create an ImageDetail object and return it
        image_detail = ImageDetail(guid=guid, filename=filename, prompt=prompt)
        return image_detail
    

    def get_image_details_by_guid(self, guid: str) -> ImageDetail:
        """
        Gets image details by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        Image: The image details.

        Raises:
        ImageNotFoundException: If no image with the provided GUID exists.
        """
        query = """
        SELECT id, guid, filename, prompt, created_at, updated_at
        FROM images
        WHERE guid = %s
        """

        db = get_current_db_context()
        db.cursor.execute(query, (guid,))
        result = db.cursor.fetchone()
        if result is None:
            raise ImageNotFoundError(f"No image found with GUID {guid}")
        image_detail = ImageDetail(guid=result[ImageColumns.GUID], filename=result[ImageColumns.FILENAME], prompt=result[ImageColumns.PROMPT])
        return image_detail

    def get_all_image_details(self) -> list[ImageDetail]:
        """
        Gets all image details.

        Returns:
        list[Image]: The details of all images.
        """
        query = """
        SELECT guid, filename, prompt
        FROM images
        """

        db = get_current_db_context()
        db.cursor.execute(query)
        results = db.cursor.fetchall()
        return [ImageDetail(guid=result[ImageColumns.GUID], filename=result[ImageColumns.FILENAME], prompt=result[ImageColumns.PROMPT]) for result in results]

    def get_image_content(self, guid: str) -> bytes:
        """
        Retrieves an image by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        bytes: The image bytes.

        Raises:
        ImageNotFoundException: If no image with the provided GUID exists.
        FileNotFoundError: If the image file does not exist.
        """
        # Fetch the filename from the database
        query = """
        SELECT filename
        FROM images
        WHERE guid = %s
        """
        db = get_current_db_context()
        db.cursor.execute(query, (guid,))
        result = db.cursor.fetchone()
        if result is None:
            raise ImageNotFoundError(f"No image found with GUID {guid}")

        filename = result[ImageColumns.FILENAME]

        # Construct the file path
        app_root = os.getcwd()
        images_dir = os.path.join(app_root, 'images')
        file_path = Path(os.path.join(images_dir, filename))

        # Check if the file exists
        if not file_path.is_file():
            raise FileNotFoundError(f"No file found at {file_path}")


        # Read and return the file bytes
        with open(file_path, 'rb') as file:
            return Response(file.read(), media_type='image/png')