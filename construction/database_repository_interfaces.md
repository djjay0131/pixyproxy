```python
class ImageRepositoryInterface(ABC):
    @abstractmethod
    def create_image(self, prompt: str) -> str:
        """
        Creates an image in the database and returns its GUID.

        Parameters:
        image (Image): The image to create.

        Returns:
        str: The GUID of the created image.
        """
        pass

    @abstractmethod
    def get_image_details_by_guid(self, guid: str) -> Image:
        """
        Gets image details by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        Image: The image details.
        """
        pass

    @abstractmethod
    def retrieve_image(self, guid: str) -> bytes:
        """
        Retrieves an image by GUID.

        Parameters:
        guid (str): The GUID of the image.

        Returns:
        bytes: The image bytes.
        """
        pass
```