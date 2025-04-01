"""hcc package initialization.

This package provides the Channel class for making HTTP requests with retry functionality.
"""

import logging.config
import yaml

from .channel import Channel
from .single_request import get, post, put, delete, patch
from .retry import retry_function, RetryPolicy
from .custom_data_types import DataType, JsonType, HeaderType

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
]


def initialize_logging():
    """Initialize logging using the configuration file."""
    with open("log_config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)


initialize_logging()
