# data/db_context.py
"""
This module defines the DbContext class for the PixyProxy system.

The DbContext class is responsible for managing database connections and transactions. It uses a connection pool to efficiently manage connections to the MySQL database.

The class provides methods to get a cursor for executing SQL commands, start a transaction, and commit or rollback a transaction.

Author: djjay
Date: 2024-03-20
"""
# data/db_context.py
from data import local_storage, db_pool

class DatabaseContext:
    def __init__(self):
        self._cursor = None

    def __enter__(self):
        self.conn = db_pool.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)
        # Store the context in thread-local storage
        local_storage.db_context = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.conn.rollback()  # Rollback transaction if an exception was raised
            self.cursor.close()
            self.conn.close()  # Close the connection regardless of exception status
        finally:
            # Remove context from local storage
            del local_storage.db_context

    @property
    def cursor(self):
        return self._cursor

    # Exposing transactional methods for use in service layer
    def begin_transaction(self):
        self.conn.start_transaction()

    def commit_transaction(self):
        self.conn.commit()

    def rollback_transaction(self):
        self.conn.rollback()

    @cursor.setter
    def cursor(self, value):
        self._cursor = value
