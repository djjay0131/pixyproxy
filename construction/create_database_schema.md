I think it might be time to consider how we are storing data in the database schema for this system:
```
You are an expert in rewriting software architect instructions into a
readable useful system description, suitable for further processing by a LLM.

You are to write a system description that will be used to build the system. The system description
as specified by your architect is as follows:
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

Rewrite that system prompt, without losing detail, but in a way that is more
readable and useful for further processing by a LLM.
```


Let's generate a database schema that upholds requirements and conforms with Mysql that holds:
- all the necessary tables and indices for Images and searching for Images
- names all constraints
- every entity should have an id integer and a string guid. 
- At the start of the file set up for all tables to be properly fully internationalized
- Change all the names for constraints and indices.  
  - unique constraints should be named tablename_U{n} where N is an ordinal digit.  
  - Foreign constraints should be tablename_F{n}, and
  - indices should be named tablename_I{n} 

Here is a sample schema to start with:
```
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid VARCHAR(36) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);  
```

Split this into 3 files.

/data/scripts/create.sql:
- Creates the database, named pixyproxy, user name  pixyproxy, and password pixyproxy.  Include a drop and create statement that checks if the database exists first.

/data/scripts/schema.mysql:
- Creates the database schema.

/data/scripts/create_db.ps1:
- A powershell file that will execute the 2 scripts, it will connect to mysql using root and no password.  


## Response

Here are the two SQL scripts for creating the database and the database schema:

1. `/data/scripts/create_database.sql`:

```sql
-- This script creates the database
-- It takes the database name, user name, and password as parameters

CREATE DATABASE IF NOT EXISTS ${database_name};
CREATE USER IF NOT EXISTS '${username}'@'localhost' IDENTIFIED BY '${password}';
GRANT ALL PRIVILEGES ON ${database_name}.* TO '${username}'@'localhost';
FLUSH PRIVILEGES;
```

2. `/data/scripts/create_schema.sql`:

```sql
-- This script creates the database schema
-- It takes the database name as a parameter

USE ${database_name};

-- Set up for all tables to be properly fully internationalized
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

CREATE TABLE IF NOT EXISTS Images (
    id INT AUTO_INCREMENT,
    guid VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT Images_U1 UNIQUE (guid),
    INDEX Images_I1 (filename),
    INDEX Images_I2 (prompt(10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

These scripts assume that you are running them with a MySQL client that supports parameter substitution, such as `mysql -u root -p < /data/scripts/create_database.sql`. Replace `${database_name}`, `${username}`, and `${password}` with your actual database name, username, and password.

The `Images` table includes an `id` column as the primary key, a `guid` column with a unique constraint, and `filename` and `prompt` columns with indices for searching. The `created_at` and `updated_at` columns store timestamps. The table uses the `utf8mb4` character set and the `utf8mb4_unicode_ci` collation for full internationalization.