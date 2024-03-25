Lets build the data layer for the following system and database schema.
Let's use DB-API to do this with a MYSQL backend.
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

Here is the database schema to use:
```

CREATE TABLE `images` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `guid` VARCHAR(36) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `prompt` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Images_U1` (`guid`),
  KEY `Images_I1` (`filename`),
  KEY `Images_I2` (`created_at`),
  KEY `Images_I3` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```
Let's generate:
* a list of files needed to cleanly implement the provided Mysql version of the database
* complete code for the data layer using a repository pattern with interfaces, models, and exceptions

- Don't forget to separate initialisation code into data/__init__.py
- In the initialization code, let create a database connection context that will manage a pool of connections.  The context class should have the ability to begin, commit, and rollback transactions, as well as the ability to create a database cursor 
- Let's assume use of python-dotenv to read in configuration items 
- Include a sample .env file with any configuration items needed
- specify types and salient docstrings for all public function signatures
- Make sure the code is smartly commented when necessary, and all methods are implemented completely. 
- Provide a description at the top of each file that includes the authors name (djjay), and today's date.
- Create the database connections as a connection pool stored in the data/__init__.py file.

Let's make sure to cover the following use cases for our system:
```
Use Case 1: Create an Image
- Description: This use case allows users to create an image by providing a prompt. The system will generate an image based on the provided prompt.
- Steps:
  1. User provides a prompt.
  2. System generates an image based on the prompt.
  3. System stores the image, prompt, and associated metadata.
  4. System returns the GUID of the created image.

Use Case 2: Get ImageDetails by GUID
- Description: This use case allows users to retrieve the details of an image by providing its GUID.
- Steps:
  1. User provides a GUID.
  2. System fetches the image details associated with the provided GUID.
  3. System returns the ImageDetails including GUID, filename, prompt, and timestamps of the image in JSON format.

Use Case 3: Get All ImageDetails
- Description: This use case allows users to retrieve the details of all images stored in the system.
- Steps:
  1. User requests all image details.
  2. System fetches all image details.
  3. System returns the ImageDetails of all images, including the GUID, filename, and prompt, in JSON format.

Use Case 4: Retrieve an Image
- Description: This use case allows users to retrieve an image by providing its GUID.
- Steps:
  1. User provides a GUID.
  2. System fetches the image associated with the provided GUID.
  3. System returns the image bytes in the body of the response.

```


## Response

This is a large task, so I'll break it down into steps:

1. Create the necessary files and directories.
2. Define the database connection context in `data/__init__.py`.
3. Define the Image model in `data/models.py`.
4. Define the ImageRepository interface and its MySQL implementation in `data/repositories.py`.
5. Define the ImagePromptException in `data/exceptions.py`.
6. Create a sample `.env` file.

Here's the code:

```python
# data/__init__.py
"""
Data layer initialization module.
Author: djjay
Date: YYYY-MM-DD
"""
import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

class DatabaseContext:
    """
    Database context that manages a pool of connections.
    """
    def __init__(self):
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    def begin(self):
        """
        Begins a new transaction.
        """
        return self.cnxpool.get_connection()

    def commit(self, cnx):
        """
        Commits the current transaction.
        """
        cnx.commit()

    def rollback(self, cnx):
        """
        Rolls back the current transaction.
        """
        cnx.rollback()

    def cursor(self, cnx):
        """
        Creates a new cursor.
        """
        return cnx.cursor()

db_context = DatabaseContext()
```

```python
# data/models.py
"""
Data layer models module.
Author: djjay
Date: YYYY-MM-DD
"""
from datetime import datetime

class Image:
    """
    Image model.
    """
    def __init__(self, id: int, guid: str, filename: str, prompt: str, created_at: datetime, updated_at: datetime):
        self.id = id
        self.guid = guid
        self.filename = filename
        self.prompt = prompt
        self.created_at = created_at
        self.updated_at = updated_at
```

```python
# data/repositories.py
"""
Data layer repositories module.
Author: djjay
Date: YYYY-MM-DD
"""
from abc import ABC, abstractmethod
from .models import Image
from . import db_context

class ImageRepository(ABC):
    """
    Image repository interface.
    """
    @abstractmethod
    def create_image(self, image: Image) -> None:
        pass

    @abstractmethod
    def get_image_by_guid(self, guid: str) -> Image:
        pass

    @abstractmethod
    def get_all_images(self) -> list[Image]:
        pass

class MySQLImageRepository(ImageRepository):
    """
    MySQL implementation of the ImageRepository interface.
    """
    def create_image(self, image: Image) -> None:
        cnx = db_context.begin()
        cursor = db_context.cursor(cnx)
        try:
            cursor.execute(
                "INSERT INTO images (guid, filename, prompt) VALUES (%s, %s, %s)",
                (image.guid, image.filename, image.prompt)
            )
            db_context.commit(cnx)
        except:
            db_context.rollback(cnx)
            raise
        finally:
            cursor.close()
            cnx.close()

    def get_image_by_guid(self, guid: str) -> Image:
        cnx = db_context.begin()
        cursor = db_context.cursor(cnx)
        try:
            cursor.execute(
                "SELECT id, guid, filename, prompt, created_at, updated_at FROM images WHERE guid = %s",
                (guid,)
            )
            row = cursor.fetchone()
            return Image(*row)
        finally:
            cursor.close()
            cnx.close()

    def get_all_images(self) -> list[Image]:
        cnx = db_context.begin()
        cursor = db_context.cursor(cnx)
        try:
            cursor.execute(
                "SELECT id, guid, filename, prompt, created_at, updated_at FROM images"
            )
            return [Image(*row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            cnx.close()
```

```python
# data/exceptions.py
"""
Data layer exceptions module.
Author: djjay
Date: YYYY-MM-DD
"""
class ImagePromptException(Exception):
    """
    Base exception for image prompt errors.
    """
    pass
```

```dotenv
# .env
DB_HOST=localhost
DB

_NAME

=pixyproxy
DB_USER=root
DB_PASSWORD=secret
```

This code assumes that you have a MySQL server running on localhost with a database named "pixyproxy" and a user "root" with password "secret". Please replace these values with your actual database configuration.