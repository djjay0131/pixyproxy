You are an expert in writing FastAPI system use cases.
Each use case should briefly describe the operation at hand.

The system we are building is a prompt management system and has a system description:
```
We're building a system named PixyProxy, which is a Python-based FastAPI REST API. Its primary function is to manage images generated from LLM prompts. Each image is uniquely identified by a GUID for public identification and an integer ID for internal use. The image data, filename, the prompt used for its creation, and timestamps are all associated with each image.

Users can interact with the API by providing a prompt to generate an image and retrieve one or more images along with their details.

The API is structured into four distinct layers:

1. `/data` layer: This is the database layer that uses a repository pattern. It uses MySQL for storing relational data and a folder called /images for storing the images. This layer is also responsible for converting models to dictionaries and vice versa for efficiency. SQL commands in this layer use named parameters, and the initialization logic is contained in an `init.py` module.

2. `/service` layer: This layer processes image prompt requests. It revalidates incoming models from the web layer using pydantic. Any exceptions, whether from the database or service layer, are handled using a general `ImagePromptException` format.

3. `/core` layer: This layer is focused on models and exceptions, all of which extend `ImagePromptException`.

4. `/web` layer: This is the resource layer that handles image prompts. It uses a dependency pattern to ensure authenticated access to methods and also includes a dependency for universal logging of all requests.

The API provides endpoints that support operations such as searching by prompt, filename, GUID, fetching an image by GUID, and fetching all image details within pagination limits. These endpoints return JSON responses.

The system also implements universal request logging in the format `YYYY-MM-DD HH:min:sec,ms {{LoggingLevel}} {{request-id}} [thread-id] [method:line number] REQUEST START  (or REQUEST END)`. The request-id is generated from host-datetime-threadid. All exceptions are managed by a single exception handler.
```

Write system use cases for the following system:
```
It seems like we would need the following use cases to make our API useful:
Remember that guids are used to identify prompts.

* Create an image.  When we create an image, we must specify  content for the prompt that will be used to create the image.  

* Get Image Details by GUID.  Provide a GUID to an image and return the GUID, filename, prompt and timestamps.  JSON format.

* Get All Image Details.  Return all details for all images including the GUID, filename, and prompt.  JSON format.

* Retrieve an image. Provide a GUID to an image and retrieve the image bytes in the body of the response.
```
