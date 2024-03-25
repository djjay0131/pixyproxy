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