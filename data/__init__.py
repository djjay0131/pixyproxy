# data/__init__.py
"""
This module initializes the data layer of the PixyProxy system. 

It loads environment variables from a .env file, retrieves the database connection string, and creates a DbContext instance that will be used throughout the data layer to interact with the database.

The DbContext instance is created with the connection string and is responsible for managing database connections and transactions.

Author: djjay
Date: 2024-03-20
"""

import os
import threading
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()

# Database Configuration
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True,
}

# Create a thread-local storage
local_storage = threading.local()

db_pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=10, **config)

# Provide a global function to fetch the current context
def get_current_db_context():
    return getattr(local_storage, "db_context", None)
