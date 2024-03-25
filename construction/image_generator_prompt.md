Let's build an image generator that uses a large language model with image generation support.  

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

This is the method that will invoke the generator code
```python
    def create_image(self, image: ImageDetailCreate) -> ImageDetail:
        try:
            image = ImageDetailCreate(**image.dict())
        except ValidationError as e:
            raise ConstraintViolationError(str(e))

        # Generate a filename and a GUID
        timestamp = int(time.time())
        filename = f"{image.prompt.replace(' ', '_')[:27]}_{timestamp}.jpg"
        guid = core.make_guid()

        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                image_detail = self.image_repo.create_image(image.prompt, guid, filename)
                db.commit_transaction()
                # Create an ImageDetail object and return it
                return image_detail
            except ImageException as e:
                db.rollback()
                raise e
```
Here are the models:

```python
class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str

```

Here is some starter code for the class:

```python
class ImageGenerator:

    def __init__(self, repository: ImageRepositoryInterface, base_url='http://aitools.cs.vt.edu:7860/openai/v1',
                 api_key='aitools', ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.repo = repository

    def generate_image(self, image_create_request: ImageDetailCreate, model: str = "dall-e-3",
                    style: Literal["vivid", "natural"] = "vivid",
                    quality: Literal["standard", "hd"] = "hd",
                    size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024") -> ImageDetail:

        # call open AI
        # get the image url from the OpenAI response
        # using httpx or requests, get the contents of the image url
        # save the contents of the image underneath the images folder
        # make a guid for the image
        # using self.repo, save the guid, filename and prompt to the database
        # e.g.   return self.repo.generate_image(guid, folder_filename, image_create_request)
```

The comments are pseudocode for the generate_image method.

Implement the rest of the generate image class as well as any changes to the create image method from the service class.

