"""This module defines methods for making HTTP requests.

When making multiple requests towards an URL, consider using the `Channel` class.
"""

from typing import Optional, Dict
import requests

from .channel import Channel
from .retry import RetryPolicy
from .custom_data_types import DataType, JsonType, HeaderType


def get(
    *,
    url: str,
    params: Optional[Dict[str, str]] = None,
    headers: Optional[HeaderType] = None,
    timeout: float = 2.0,
    max_retry_count: Optional[int] = 5,
    retry_policy: Optional[RetryPolicy] = None,
    base_delay: Optional[int] = None,
) -> requests.Response:
    """The get method sends a GET request.

    Args:
        url: The URL to which the requests will be sent.
        params: The query parameters for the request (default is an empty dictionary).
        headers: The headers for the request (default is an empty dictionary).
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy for failed requests (default is None).
        base_delay: The base delay for retries in milliseconds (default is None).

    Returns:
        The HTTP response from the first successful or last request.

    Raises:
        Exception: If the maximum retry count is reached and the request still fails.
    """
    return Channel(
        url=url,
        timeout=timeout,
        max_retry_count=max_retry_count,
        retry_policy=retry_policy,
        base_delay=base_delay,
    ).get(
        params=params,
        headers=headers,
    )


def post(
    *,
    url: str,
    data: Optional[DataType] = None,
    json: Optional[JsonType] = None,
    headers: Optional[HeaderType] = None,
    timeout: float = 2.0,
    max_retry_count: Optional[int] = 5,
    retry_policy: Optional[RetryPolicy] = None,
    base_delay: Optional[int] = None,
) -> requests.Response:
    """The post method sends a POST request.

    Args:
        url: The URL to which the requests will be sent.
        data: The data to be sent in the body of the request (default is None).
            Either this or `json` should be provided.
        json: The JSON data to be sent in the body of the request (default is None).
            Either this or `data` should be provided.
        headers: The headers for the request (default is an empty dictionary).
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy for failed requests (default is None).
        base_delay: The base delay for retries in milliseconds (default is None).

    Returns:
        The HTTP response from the first successful or last request.

    Raises:
        Exception: If the maximum retry count is reached and the request still fails.
    """
    return Channel(
        url=url,
        timeout=timeout,
        max_retry_count=max_retry_count,
        retry_policy=retry_policy,
        base_delay=base_delay,
    ).post(
        data=data,
        json=json,
        headers=headers,
    )


def put(
    *,
    url: str,
    data: Optional[DataType] = None,
    json: Optional[JsonType] = None,
    headers: Optional[HeaderType] = None,
    timeout: float = 2.0,
    max_retry_count: Optional[int] = 5,
    retry_policy: Optional[RetryPolicy] = None,
    base_delay: Optional[int] = None,
) -> requests.Response:
    """The put method sends a PUT request.

    Args:
        url: The URL to which the requests will be sent.
        data: The data to be sent in the body of the request (default is None).
            Either this or `json` should be provided.
        json: The JSON data to be sent in the body of the request (default is None).
            Either this or `data` should be provided.
        headers: The headers for the request (default is an empty dictionary).
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy for failed requests (default is None).
        base_delay: The base delay for retries in milliseconds (default is None).

    Returns:
        The HTTP response from the first successful or last request.

    Raises:
        Exception: If the maximum retry count is reached and the request still fails.
    """
    return Channel(
        url=url,
        timeout=timeout,
        max_retry_count=max_retry_count,
        retry_policy=retry_policy,
        base_delay=base_delay,
    ).put(
        data=data,
        json=json,
        headers=headers,
    )


def delete(
    *,
    url: str,
    headers: Optional[HeaderType] = None,
    timeout: float = 2.0,
    max_retry_count: Optional[int] = 5,
    retry_policy: Optional[RetryPolicy] = None,
    base_delay: Optional[int] = None,
) -> requests.Response:
    """The delete method sends a DELETE request.

    Args:
        url: The URL to which the requests will be sent.
        headers: The headers for the request (default is an empty dictionary).
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy for failed requests (default is None).
        base_delay: The base delay for retries in milliseconds (default is None).

    Returns:
        The HTTP response from the first successful or last request.

    Raises:
        Exception: If the maximum retry count is reached and the request still fails.
    """
    return Channel(
        url=url,
        timeout=timeout,
        max_retry_count=max_retry_count,
        retry_policy=retry_policy,
        base_delay=base_delay,
    ).delete(
        headers=headers,
    )


def patch(
    *,
    url: str,
    data: Optional[DataType] = None,
    json: Optional[JsonType] = None,
    headers: Optional[HeaderType] = None,
    timeout: float = 2.0,
    max_retry_count: Optional[int] = 5,
    retry_policy: Optional[RetryPolicy] = None,
    base_delay: Optional[int] = None,
) -> requests.Response:
    """The patch method sends a PATCH request.

    Args:
        url: The URL to which the requests will be sent.
        data: The data to be sent in the body of the request (default is None).
            Either this or `json` should be provided.
        json: The JSON data to be sent in the body of the request (default is None).
            Either this or `data` should be provided.
        headers: The headers for the request (default is an empty dictionary).
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy for failed requests (default is None).
        base_delay: The base delay for retries in milliseconds (default is None).

    Returns:
        The HTTP response from the first successful or last request.

    Raises:
        Exception: If the maximum retry count is reached and the request still fails.
    """
    return Channel(
        url=url,
        timeout=timeout,
        max_retry_count=max_retry_count,
        retry_policy=retry_policy,
        base_delay=base_delay,
    ).patch(
        data=data,
        json=json,
        headers=headers,
    )
