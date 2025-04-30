"""This module defines exceptions used inside this package."""


class HccRequestError(IOError):
    """
    Base class for all request related exceptions raised by `hcc`.
    """


class ConnectTimeout(HccRequestError):
    """
    Wrapper around the `requests.ConnectTimeout` exception.
    """


class RequestError(HccRequestError):
    """
    Wrapper around the otherwise unwrapped exceptions from the `requests` package.
    """


class JSONDecodeError(HccRequestError):
    """
    Wrapper around the `requests.JSONDecodeError` exception.
    """


class ReadTimeout(HccRequestError):
    """
    Wrapper around the `requests.ReadTimeout` exception.
    """


class RequestException(HccRequestError):
    """
    Wrapper around the `requests.RequestException` (superclass) exception.
    """


class UnknownRequestException(HccRequestError):
    """
    Exception for all unrecognizable request related errors.
    """
