"""This module defines custom data types used throughout the application.

Type Aliases:
    HeaderType: Represents HTTP headers.
    JsonType: Represents any JSON-compatible data type, that can be sent in an HTTP request body.
    DataType: Represents any data type, that can be sent in an HTTP request body.
"""

from typing import Any, Iterable, Mapping, TypeAlias


DataType: TypeAlias = (
    Iterable[bytes]
    | str
    | bytes
    # TODO Add support for SupportsRead
    # | SupportsRead[str | bytes]
    | list[tuple[Any, Any]]
    | tuple[tuple[Any, Any], ...]
    | Mapping[Any, Any]
)

JsonType: TypeAlias = Any

HeaderType: TypeAlias = Mapping[str, str]
