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