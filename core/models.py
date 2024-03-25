# data/models.py
"""
This module defines the data models used in the PixyProxy system. 

The `ImageDetailCreate` model represents the data needed to create a new image, including the filename and the prompt used for its generation.

The `ImageDetail` model extends `ImageDetailCreate` and includes additional fields that are set by the system when an image is created, such as the unique ID, GUID, and timestamp.

Author: djjay
Date: 2024-03-20
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str