"""hcc package initialization.

This package provides the Channel class for making HTTP requests with retry functionality.
"""

import logging

from .channel import Channel
from .single_request import get, post, put, delete, patch
from .retry import retry_function, RetryPolicy
from .custom_data_types import DataType, JsonType, HeaderType
from .exceptions import (
    HccRequestError,
    ConnectTimeout,
    RequestError,
    JSONDecodeError,
    ReadTimeout,
    RequestException,
    UnknownRequestException,
)

__all__ = [
    "Channel",
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "retry_function",
    "RetryPolicy",
    "DataType",
    "JsonType",
    "HeaderType",
    "HccRequestError",
    "ConnectTimeout",
    "RequestError",
    "JSONDecodeError",
    "ReadTimeout",
    "RequestException",
    "UnknownRequestException",
]


def initialize_logging():
    """Initialize logging for the hcc package."""
    logging.getLogger("hcc").addHandler(logging.NullHandler())


initialize_logging()
