It seems like we would need the following use cases to make our API useful:
Remember that guids are used to identify prompts.

* Create an image.  When we create an image, we must specify  content for the prompt that will be used to create the image.  

* Get Image Details by GUID.  Provide a GUID to an image and return the GUID, filename, prompt and timestamps.  JSON format.

* Get All Image Details.  Return all details for all images including the GUID, filename, and prompt.  JSON format.

* Retrieve an image. Provide a GUID to an image and retrieve the image bytes in the body of the response.



