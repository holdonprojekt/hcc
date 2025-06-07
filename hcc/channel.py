"""This module defines the Channel class, which provides methods for making HTTP requests.


The Channel class provides methods for sending HTTP requests (GET, POST, PUT, DELETE, PATCH)
and automatically retries requests in case of failure, based on a configurable retry policy.
"""

from typing import Any, Callable, Optional, Dict
import logging
import requests
from .retry import retry_function, RetryPolicy
from .custom_data_types import DataType, JsonType, HeaderType
from .exceptions import (
    ConnectTimeout,
    RequestError,
    JSONDecodeError,
    ReadTimeout,
    RequestException,
    UnknownRequestException,
)


logger = logging.getLogger("hcc.request")


class Channel:
    """The Channel class is a wrapper around the requests library that simplifies
    making HTTP requests with retry functionality.

    It provides methods for sending GET, POST, PUT, DELETE, and PATCH requests, with automatic retry
    in case of failure (determined by status codes). The class supports configurable timeout, retry
    policies, and delay between retries.

    The Channel class takes the following parameters:
        url: The URL to which the requests will be sent.
        timeout: The timeout for the requests (default is 2.0 seconds).
        max_retry_count: The maximum number of retries for failed requests (default is 5).
                         If set to None, there is no limit on the number of retries.
        retry_policy: The retry policy for failed requests (default is None).
        base_delay: The base delay for retries in milliseconds (default is None).

    Typical usage example:
    ```python
    from hcc import Channel

    channel = Channel(url="https://api.example.com")
    response = channel.get()
    print(response.json())
    ```
    """

    def __init__(
        self,
        *,
        url: str,
        timeout: float = 2.0,
        max_retry_count: Optional[int] = 5,
        retry_policy: Optional[RetryPolicy] = None,
        base_delay: Optional[int] = None,
    ):
        self.url = url
        self.timeout = timeout
        self.max_retry_count = max_retry_count
        self.retry_policy = retry_policy
        self.base_delay = base_delay
        self.success_status_codes = [200, 201]
        self.is_retry_needed: Callable[[requests.Response], bool] = (
            lambda response: response.status_code not in self.success_status_codes
        )
        logger.info(
            (
                "Channel created: id: %s, URL: %s, timeout: %s, "
                "max_retry_count: %s, retry_policy: %s, base_delay: %s"
            ),
            id(self),
            self.url,
            self.timeout,
            self.max_retry_count,
            self.retry_policy,
            self.base_delay,
        )

    def get(
        self,
        *,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[HeaderType] = None,
    ) -> requests.Response:
        """The get method sends a GET request.

        Args:
            params: The query parameters for the request (default is an empty dictionary).
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.

        Raises:
            Exception: If the maximum retry count is reached and the request still fails.
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        logger.info(
            "GET request: channel: %s, params: %s, headers: %s",
            id(self),
            params,
            headers,
        )
        response = retry_function(
            func=lambda: self._make_request(
                "get",
                self.url,
                timeout=self.timeout,
                params=params,
                headers=headers,
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay,
        )
        logger.info("GET response: %s", response)
        return response

    def post(
        self,
        *,
        data: Optional[DataType] = None,
        json: Optional[JsonType] = None,
        headers: Optional[HeaderType] = None,
    ) -> requests.Response:
        """The post method sends a POST request.

        Args:
            data: The data to be sent in the body of the request (default is None).
                Either this or `json` should be provided.
            json: The JSON data to be sent in the body of the request (default is None).
                Either this or `data` should be provided.
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.

        Raises:
            Exception: If the maximum retry count is reached and the request still fails.
        """
        assert data is not None or json is not None, (
            "Either data or json must be provided"
        )
        assert data is None or json is None, "Only one of data or json can be provided"
        if json:
            data = None
        if headers is None:
            headers = {}
        logger.info(
            "POST request: channel: %s, data: %s, json: %s, headers: %s",
            id(self),
            data,
            json,
            headers,
        )
        response = retry_function(
            func=lambda: self._make_request(
                "post",
                self.url,
                timeout=self.timeout,
                data=data,
                json=json,
                headers=headers,
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay,
        )
        logger.info("POST response: %s", response)
        return response

    def put(
        self,
        *,
        data: Optional[DataType] = None,
        json: Optional[JsonType] = None,
        headers: Optional[HeaderType] = None,
    ) -> requests.Response:
        """The put method sends a PUT request.

        Args:
            data: The data to be sent in the body of the request (default is None).
                Either this or `json` should be provided.
            json: The JSON data to be sent in the body of the request (default is None).
                Either this or `data` should be provided.
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.

        Raises:
            Exception: If the maximum retry count is reached and the request still fails.
        """
        assert data is not None or json is not None, (
            "Either data or json must be provided"
        )
        assert data is None or json is None, "Only one of data or json can be provided"
        if json:
            data = None
        if headers is None:
            headers = {}
        logger.info(
            "PUT request: channel: %s, data: %s, json: %s, headers: %s",
            id(self),
            data,
            json,
            headers,
        )
        response = retry_function(
            func=lambda: self._make_request(
                "put",
                self.url,
                timeout=self.timeout,
                data=data,
                json=json,
                headers=headers,
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay,
        )
        logger.info("PUT response: %s", response)
        return response

    def delete(
        self,
        *,
        headers: Optional[HeaderType] = None,
    ) -> requests.Response:
        """The delete method sends a DELETE request.

        Args:
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.

        Raises:
            Exception: If the maximum retry count is reached and the request still fails.
        """
        if headers is None:
            headers = {}
        logger.info(
            "DELETE request: channel: %s, headers: %s",
            id(self),
            headers,
        )
        response = retry_function(
            func=lambda: self._make_request(
                "delete",
                self.url,
                timeout=self.timeout,
                headers=headers,
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay,
        )
        logger.info("DELETE response: %s", response)
        return response

    def patch(
        self,
        *,
        data: Optional[DataType] = None,
        json: Optional[JsonType] = None,
        headers: Optional[HeaderType] = None,
    ) -> requests.Response:
        """The patch method sends a PATCH request.

        Args:
            data: The data to be sent in the body of the request (default is None).
                Either this or `json` should be provided.
            json: The JSON data to be sent in the body of the request (default is None).
                Either this or `data` should be provided.
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.

        Raises:
            Exception: If the maximum retry count is reached and the request still fails.
        """
        assert data is not None or json is not None, (
            "Either data or json must be provided"
        )
        assert data is None or json is None, "Only one of data or json can be provided"
        if json:
            data = None
        if headers is None:
            headers = {}
        logger.info(
            "PATCH request: channel: %s, data: %s, json: %s, headers: %s",
            id(self),
            data,
            json,
            headers,
        )
        response = retry_function(
            func=lambda: self._make_request(
                "patch",
                self.url,
                timeout=self.timeout,
                data=data,
                json=json,
                headers=headers,
            ),
            is_retry_needed=self.is_retry_needed,
            max_retry_count=self.max_retry_count,
            retry_policy=self.retry_policy,
            base_delay=self.base_delay,
        )
        logger.info("PATCH response: %s", response)
        return response

    def request(
        self,
        *,
        method: str,
        params: Optional[Dict[str, str]] = None,
        data: Optional[DataType] = None,
        json: Optional[JsonType] = None,
        headers: Optional[HeaderType] = None,
    ) -> requests.Response:
        """The request method sends a request with the specified method.

        Args:
            method: The HTTP method to be used (GET, POST, PUT, DELETE, PATCH).
            params: The query parameters for the request (default is an empty dictionary).
            data: The data to be sent in the body of the request (default is None).
                Either this or `json` should be provided.
            json: The JSON data to be sent in the body of the request (default is None).
                Either this or `data` should be provided.
            headers: The headers for the request (default is an empty dictionary).

        Returns:
            The HTTP response from the first successful or last request.

        Raises:
            Exception: If the maximum retry count is reached and the request still fails.
        """
        method = method.upper()
        if method == "GET":
            return self.get(params=params, headers=headers)
        if method == "POST":
            return self.post(data=data, json=json, headers=headers)
        if method == "PUT":
            return self.put(data=data, json=json, headers=headers)
        if method == "DELETE":
            return self.delete(headers=headers)
        if method == "PATCH":
            return self.patch(data=data, json=json, headers=headers)
        raise ValueError(f"Unsupported method: {method}")

    def _make_request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """The _make_request private method sends a request and transforms exceptions if necessary.

        In `request` 2.32.3 the following exceptions are exported from the package.
        Their mapping is the following:
        - `ConnectionError`: is not mapped because it's a superclass of `ConnectTimeout`
            (and some not exported exceptions)
        - `ConnectTimeout`: mapped to `hcc.ConnectTimeout`
        - `FileModeWarning`: mapped to `hcc.RequestError`
        - `HTTPError`: mapped to `hcc.RequestError`
        - `JSONDecodeError`: mapped to `hcc.JSONDecodeError`
        - `ReadTimeout`: mapped to `hcc.ReadTimeout`
        - `RequestException`: mapped to `hcc.RequestException` (and put last because it's
            a superclass of all of `requests` package's exceptions)
        - `Timeout`: is not mapped because it's an ancestor class of `ConnectTimeout` and
            `ReadTimeout`
        - `TooManyRedirects`: mapped to `hcc.RequestError`
        - `URLRequired`: is not mapped because it's not used anymore
            (see: https://github.com/psf/requests/issues/6877)

        Args:
            method: The HTTP method to be used (GET, POST, PUT, DELETE, PATCH).
            url: The URL to which the requests will be sent.
            **kwargs: Additional arguments for the request, such as timeout, data, json, headers.

        Returns:
            The HTTP response from the request.

        Raises:
            Exception: If the request fails.
        """
        try:
            return requests.request(method, url, **kwargs)  # pylint: disable=missing-timeout
        except requests.ConnectTimeout as e:
            raise ConnectTimeout from e
        except (
            requests.FileModeWarning,
            requests.HTTPError,
            requests.TooManyRedirects,
        ) as e:
            raise RequestError from e
        except requests.JSONDecodeError as e:
            raise JSONDecodeError from e
        except requests.ReadTimeout as e:
            raise ReadTimeout from e
        except requests.RequestException as e:
            raise RequestException from e
        except Exception as e:
            raise UnknownRequestException from e
