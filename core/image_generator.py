import os

from typing import Literal
from openai import OpenAI

import core
from .models import ImageDetail, ImageDetailCreate
from data.image_repository import ImageRepositoryInterface
import httpx
import time
import base64
import json

class ImageGenerator:
    def __init__(self, repository: ImageRepositoryInterface, base_url='http://aitools.cs.vt.edu:7860/openai/v1',
                 api_key='aitools'):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.repo = repository

        # Ensure the images directory exists
        if not os.path.exists('images'):
            os.makedirs('images')        

    def generate_image(self, image_create_request: ImageDetailCreate, model: str = "dall-e-3",
                   style: Literal["vivid", "natural"] = "vivid",
                   quality: Literal["standard", "hd"] = "hd",
                   size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024") -> ImageDetail:
        # Call OpenAI
        response = self.client.images.generate(prompt=image_create_request.prompt, 
                                            model=model,
                                            style=style,
                                            quality=quality,
                                            size=size,
                                            response_format='b64_json')

        # Get the base64 encoded image data from the OpenAI response
        image_data_b64 = response.data[0].b64_json

        # Decode the base64 data to get the image content
        image_content = base64.b64decode(image_data_b64)

        # Generate a filename and a GUID
        timestamp = int(time.time())
        filename = f"{image_create_request.prompt.replace(' ', '_')[:27]}_{timestamp}.png"
        guid = core.make_guid()

        # Save the contents of the image underneath the images folder
        with open(os.path.join('images', filename), 'wb') as f:
            f.write(image_content)

        # Using self.repo, save the guid, filename and prompt to the database
        image_detail = self.repo.create_image(image_create_request.prompt, guid, filename)

        # Return the ImageDetail object
        return image_detail