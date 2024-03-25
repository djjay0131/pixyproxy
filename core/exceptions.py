"""
This module defines custom exceptions for the PixyProxy system.
These exceptions are used to handle and communicate specific error conditions that can occur in the core, data, service, and web layers of the system.

Author: djjay
Date: 2024-03-20
"""

# Core exceptions
class ImageException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Data layer exceptions
class DBConnectionError(ImageException):
    def __init__(self):
        super().__init__("A connection to the database could not be established.")

class RecordNotFoundError(ImageException):
    def __init__(self):
        super().__init__("The requested record was not found.")

class ImageNotFoundError(ImageException):
    def __init__(self):
        super().__init__("The requested image was not found.")

class ConstraintViolationError(ImageException):
    def __init__(self):
        super().__init__("A database constraint was violated.")

# Service layer exceptions
class DataValidationError(ImageException):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidOperationError(ImageException):
    def __init__(self, message: str):
        super().__init__(message)

# Web layer exceptions
class BadRequestError(ImageException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message)

class EndPointNotFoundError(ImageException):
    def __init__(self, message: str = "Endpoint not found"):
        super().__init__(message)

# HTTP status codes for exceptions
EXCEPTION_STATUS_CODES = {
    ImageException: 500,  # Internal Server Error
    DBConnectionError: 500,  # Internal Server Error
    RecordNotFoundError: 404,  # Not Found
    ImageNotFoundError: 404,  # Not Found
    ConstraintViolationError: 409,  # Conflict
    DataValidationError: 400,  # Bad Request
    InvalidOperationError: 400,  # Bad Request
    BadRequestError: 400,  # Bad Request
    EndPointNotFoundError: 404,  # Not Found
    InvalidOperationError: 403,  # Forbidden
}