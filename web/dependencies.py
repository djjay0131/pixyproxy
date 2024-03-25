
from fastapi import Depends

from data.image_repository import ImageRepositoryInterface, MySQLImageRepository
from service.image_service import ImageServiceInterface, ImageService
from core.image_generator import ImageGenerator

def get_image_repository() -> ImageRepositoryInterface:
    return MySQLImageRepository()

def get_image_generator(repo: ImageRepositoryInterface = Depends(get_image_repository)) -> ImageGenerator:
    return ImageGenerator(repo)

def get_image_service(repo: ImageRepositoryInterface = Depends(get_image_repository), 
                      generator: ImageGenerator = Depends(get_image_generator)) -> ImageServiceInterface:
    return ImageService(repo, generator)

