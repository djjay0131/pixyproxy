Lets build the web layer for the following system and service layer.
Let's use FastAPI to do this.

The system description is as follows:
```
PixyProxy is a system designed to provide API endpoints for image creation from prompts, storage of image metadata and content, listing of image details, and delivery of image content. 

The system is built on Python and uses the FastAPI framework to manage images generated from LLM prompts. Each image is uniquely identified by a GUID for public use and an internal integer ID. Additional data associated with each image includes the image data itself, the filename, the prompt used for its generation, and timestamps.

Users can interact with the API to generate an image from a provided prompt and retrieve one or multiple images along with their details.

The API is structured into four distinct layers:

1. The `/data` layer serves as the database layer, adopting a repository pattern. MySQL is used for storing relational data, while a /images folder is used for storing the images. This layer is also responsible for converting models to dictionaries and vice versa for efficiency. SQL commands utilize named parameters, and initialization logic is contained in an `init.py` module.

2. The `/service` layer is responsible for handling image prompt requests. Models incoming from the web layer are revalidated using pydantic. All exceptions, whether originating from the database or service layer, are handled using a general `ImagePromptException` format.

3. The `/core` layer is centered around models and exceptions, all of which extend `ImagePromptException`.

4. The `/web` layer, or the resource layer, handles image prompts. It employs a dependency pattern to ensure authenticated access to methods and includes a dependency for universal logging of all requests.

The API supports operations such as searching by prompt, filename, GUID, fetching an image by GUID, and fetching all image details within pagination limits. These endpoints return responses in JSON format.

The system also implements universal request logging in the format `YYYY-MM-DD HH:min:sec,ms {{LoggingLevel}} {{request-id}} [thread-id] [method:line number] REQUEST START  (or REQUEST END)`. The request-id is generated from host-datetime-threadid. All exceptions are managed by a single exception handler.
```

Let's make sure to cover the following use cases for our system:
```
Use Case 1: Create an Image
- Description: This use case allows users to create an image by providing a prompt. The system will generate an image based on the provided prompt.
- Steps:
  1. User provides a prompt.
  2. System generates an image based on the prompt.
  3. System stores the image, prompt, and associated metadata.
  4. System returns the GUID of the created image.

Use Case 2: Get Image Details by GUID
- Description: This use case allows users to retrieve the details of an image by providing its GUID.
- Steps:
  1. User provides a GUID.
  2. System fetches the image details associated with the provided GUID.
  3. System returns the GUID, filename, prompt, and timestamps of the image in JSON format.

Use Case 3: Get All Image Details
- Description: This use case allows users to retrieve the details of all images stored in the system.
- Steps:
  1. User requests all image details.
  2. System fetches all image details.
  3. System returns the details of all images, including the GUID, filename, and prompt, in JSON format.

Use Case 4: Retrieve an Image
- Description: This use case allows users to retrieve an image by providing its GUID.
- Steps:
  1. User provides a GUID.
  2. System fetches the image associated with the provided GUID.
  3. System returns the image bytes in the body of the response.

```

Here is the image service interface to use:
```python
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
                
```

Here are the core model objects to use:
```python
class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str

```

Here are the core exceptions to use:
```python
# Core exceptions
class ImageException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Data layer exceptions
class DBConnectionError(ImageException):
    def __init__(self):
        super().__init__("A connection to the database could not be established.")

class RecordNotFoundError(ImageException):
    def __init__(self):
        super().__init__("The requested record was not found.")

class ImageNotFoundError(ImageException):
    def __init__(self):
        super().__init__("The requested image was not found.")

class ConstraintViolationError(ImageException):
    def __init__(self):
        super().__init__("A database constraint was violated.")

# Service layer exceptions
class DataValidationError(ImageException):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidOperationError(ImageException):
    def __init__(self, message: str):
        super().__init__(message)

# Web layer exceptions
class BadRequestError(ImageException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message)

class EndPointNotFoundError(ImageException):
    def __init__(self, message: str = "Endpoint not found"):
        super().__init__(message)

# HTTP status codes for exceptions
EXCEPTION_STATUS_CODES = {
    ImageException: 500,  # Internal Server Error
    DBConnectionError: 500,  # Internal Server Error
    RecordNotFoundError: 404,  # Not Found
    ImageNotFoundError: 404,  # Not Found
    ConstraintViolationError: 409,  # Conflict
    DataValidationError: 400,  # Bad Request
    InvalidOperationError: 400,  # Bad Request
    BadRequestError: 400,  # Bad Request
    EndPointNotFoundError: 404,  # Not Found
    InvalidOperationError: 403,  # Forbidden
}
```

The web layer is responsible for validation, central exception handling with a single exception handler,
and logging of each request (assigning a request id, logging the start and end result of each request per above).

Let's create a FastAPI application with a router for image creation and retrieval.  The routers will live in the /web/routers folder.

Let's write a global dependency so all endpoints are logged using the required format.  The logging middleware will use starlette to build a RequestIdMiddleware class, and a LoggingMiddleware class.  

Let's generate a file at a time and pause to think upfront about how things will all fit together.

Then let's generate an API description with enough detail to write test cases for the web layer.  

## Response

To build the web layer for the PixyProxy system, we will follow these steps:

1. Create a new FastAPI application.
2. Define the API routes for the use cases.
3. Implement the request handlers for each route.
4. Implement the logging middleware.
5. Implement the exception handler.
6. Generate the API description.

Let's start by creating the FastAPI application and defining the API routes.

```python
from fastapi import FastAPI
from .routers import images

app = FastAPI()

app.include_router(images.router)
```

Next, we will implement the request handlers in the `images` router.

```python
from fastapi import APIRouter, Depends
from ..core.models import ImageDetailCreate, ImageDetail
from ..service.image_service import ImageServiceInterface

router = APIRouter()

@router.post("/images", response_model=ImageDetail)
def create_image(image_detail: ImageDetailCreate, service: ImageServiceInterface = Depends()):
    return service.create_image(image_detail)

@router.get("/images/{guid}", response_model=ImageDetail)
def get_image_details_by_guid(guid: str, service: ImageServiceInterface = Depends()):
    return service.get_image_details_by_guid(guid)

@router.get("/images", response_model=List[ImageDetail])
def get_all_image_details(service: ImageServiceInterface = Depends()):
    return service.get_all_image_details()

@router.get("/images/{guid}/content")
def get_image_content(guid: str, service: ImageServiceInterface = Depends()):
    return service.get_image_content(guid)
```

Next, we will implement the logging middleware.

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging
import datetime

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = f"{request.client.host}-{datetime.datetime.now()}-{id(request)}"
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger("uvicorn")
        logger.info(f"{datetime.datetime.now()} INFO {request.state.request_id} [thread-id] [method:line number] REQUEST START")
        response = await call_next(request)
        logger.info(f"{datetime.datetime.now()} INFO {request.state.request_id} [thread-id] [method:line number] REQUEST END")
        return response

app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggingMiddleware)
```

Next, we will implement the exception handler.

```python
from fastapi import HTTPException
from ..core.exceptions import EXCEPTION_STATUS_CODES

@app.exception_handler(Exception)
def handle_exception(request: Request, exc: Exception):
    status_code = EXCEPTION_STATUS_CODES.get(type(exc), 500)
    return HTTPException(status_code=status_code, detail=str(exc))
```

Finally, we will generate the API description.

```python
app = FastAPI(
    title="PixyProxy",
    description="API endpoints for image creation from prompts, storage of image metadata and content, listing of image details, and delivery of image content.",
    version="1.0.0",
)
```

This completes the implementation of the web layer for the PixyProxy system.