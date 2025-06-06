import pytest
from unittest.mock import patch as mock_patch, Mock
import hcc


@pytest.mark.parametrize(
    "method",
    ["get", "post", "put", "delete", "patch", "GET", "POST", "PUT", "DELETE", "PATCH"],
)
def test_single_requests(method: str):
    with mock_patch(f"hcc.channel.Channel.{method.lower()}") as mock:
        mock.return_value = Mock(status_code=200)

        request_kwargs = {
            "method": method,
            "url": "https://mockserver.com/success",
            "params": {"q": "test"},
            "json": {"key": "value"},
            "data": None,
            "headers": {"Authorization": "Bearer token"},
        }

        hcc.request(**request_kwargs)
        _, kwargs = mock.call_args

        assert kwargs.items() <= request_kwargs.items()


@pytest.mark.parametrize(
    "method",
    ["get", "post", "put", "delete", "patch", "GET", "POST", "PUT", "DELETE", "PATCH"],
)
def test_channel_requests(method: str):
    with mock_patch(f"hcc.channel.Channel.{method.lower()}") as mock:
        mock.return_value = Mock(status_code=200)

        request_kwargs = {
            "method": method,
            "params": {"q": "test"},
            "json": {"key": "value"},
            "data": None,
            "headers": {"Authorization": "Bearer token"},
        }

        channel = hcc.Channel(url="https://mockserver.com/success")
        channel.request(**request_kwargs)
        _, kwargs = mock.call_args

        assert kwargs.items() <= request_kwargs.items()


def test_unsupported_requests():
    with pytest.raises(ValueError):
        request_kwargs = {
            "method": "options",
            "url": "https://mockserver.com/success",
            "params": {"q": "test"},
            "json": {"key": "value"},
            "data": None,
            "headers": {"Authorization": "Bearer token"},
        }

        hcc.request(**request_kwargs)

    with pytest.raises(ValueError):
        request_kwargs = {
            "method": "options",
            "params": {"q": "test"},
            "json": {"key": "value"},
            "data": None,
            "headers": {"Authorization": "Bearer token"},
        }

        channel = hcc.Channel(url="https://mockserver.com/success")
        channel.request(**request_kwargs)
