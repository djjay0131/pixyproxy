# main.py
"""
This file sets up the FastAPI application for the PixyProxy system. It includes the necessary middleware and exception handlers.

Author: djjay
Date: 2024-03-20
"""

import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.exceptions import EXCEPTION_STATUS_CODES, ImageException
from web.middleware import LoggingMiddleware, RequestIdMiddleware
from web.routers import image_router
from fastapi import HTTPException

# Create a new FastAPI application
app = FastAPI(
    title="PixyProxy",
    description="API endpoints for image creation from prompts, storage of image metadata and content, listing of image details, and delivery of image content.",
    version="1.0.0",
)

# Include the images router
app.include_router(image_router.router, prefix="/image")

# Add the RequestIdMiddleware to the middleware stack
app.add_middleware(RequestIdMiddleware)

# Add the LoggingMiddleware to the middleware stack
app.add_middleware(LoggingMiddleware)

# Exception handler for generic exceptions
@app.exception_handler(Exception)
def handle_generic_exception(request: Request, exc: Exception):
    status_code = 500  # Default status code for generic exceptions
    stack_trace = traceback.format_exc()
    return JSONResponse(status_code=status_code, content={"detail": str(exc), "stack_trace": stack_trace})

# Exception handler for ImageException
@app.exception_handler(ImageException)
def handle_image_exception(request: Request, exc: ImageException):
    status_code = EXCEPTION_STATUS_CODES.get(type(exc), 500)
    stack_trace = traceback.format_exc()
    return JSONResponse(status_code=status_code, content={"detail": str(exc), "stack_trace": stack_trace})