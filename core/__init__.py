# data/__init__.py
# This file contains utility functions for the data module.
# Author: djjay
# Date: 2024-02-20

import uuid

def make_guid() -> str:
    """
    Generates a new GUID.

    Returns:
    str: The generated GUID.
    """
    return str(uuid.uuid4()).replace('-', '')