PixyProxy is a system that offers API endpoints for creating images from prompts, storing the metadata and content of these images, listing image details, and delivering image content. 

The system is a Python-based FastAPI REST API that manages images generated from LLM prompts. Each image is identified by a GUID for public use and an integer ID for internal use. The image data, filename, prompt used for its generation, and timestamps are also associated with each image.

The API allows users to provide a prompt to generate an image and retrieve one or more images with their details.

The API is divided into four layers:

1. `/data` layer: This is the database layer using a repository pattern. MySQL stores relational data, and a folder called /imges to stores the images. This layer also converts models to dictionaries and vice versa for efficiency. SQL commands use named parameters, and initialization logic is in an `init.py` module.

2. `/service` layer: This layer handles image prompt requests. Incoming models from the web layer are revalidated using pydantic. All exceptions, whether from the database or service layer, are handled using a general `ImagePromptException` format.

3. `/core` layer: This layer focuses on models and exceptions, all extending `ImagePromptException`.

4. `/web` layer: This is the resource layer handling image prompts. It uses a dependency pattern to ensure authenticated access to methods and includes a dependency for universal logging of all requests.

The API supports operations like searching by prompt, filename, GUID, fetching an image by GUID, and fetching all image details within pagination limits. These endpoints return JSON responses.

The system also implements universal request logging in the format `YYYY-MM-DD HH:min:sec,ms {{LoggingLevel}} {{request-id}} [thread-id] [method:line number] REQUEST START  (or REQUEST END)`. The request-id is generated from host-datetime-threadid. All exceptions are handled by a single exception handler.