# web/routers/image.py
"""
This file defines the routes for the Image API. It includes routes for creating, retrieving, and getting the content of images.

Author: djjay
Date: 2024-03-20
"""
from typing import List
from fastapi import APIRouter, Depends
from core.models import ImageDetailCreate, ImageDetail
from service.image_service import ImageServiceInterface
from web.dependencies import get_image_service

router = APIRouter()

# Route to create a new image
@router.post("/", response_model=ImageDetail)
def create_image(image_detail: ImageDetailCreate, 
                 service: ImageServiceInterface = Depends(get_image_service)):
    return service.create_image(image_detail)

# Route to get the details of an image by its GUID
@router.get("/{guid}", response_model=ImageDetail)
def get_image_details_by_guid(guid: str, 
                              service: ImageServiceInterface = Depends(get_image_service)):
    return service.get_image_details_by_guid(guid)

# Route to get the details of all images
@router.get("/", response_model=List[ImageDetail])
def get_all_image_details(service: ImageServiceInterface = Depends(get_image_service)):
    return service.get_all_image_details()

# Route to get the content of an image by its GUID
@router.get("/{guid}/content")
def get_image_content(guid: str, service: ImageServiceInterface = Depends(get_image_service)):
    return service.get_image_content(guid)