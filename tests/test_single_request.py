# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=W0611
from typing import Any
from unittest.mock import patch as mock_patch, Mock
import requests
from hcc import Channel, get, post, put, delete, patch  # type: ignore # noqa: F401


def assert_equal_requests(method: str):
    with mock_patch("requests.Session.send") as mock_send:
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}
        mock_send.return_value = mock_response

        url = "https://mockserver.com/success"
        params = {"q": "test"}
        json = {"key": "value"}
        headers = {"Authorization": "Bearer token"}

        if method in ["post", "put", "patch"]:
            kwargs = {"json": json, "headers": headers}
        elif method == "delete":
            kwargs = {"headers": headers}
        else:
            kwargs = {"params": params, "headers": headers}

        captured_calls: list[requests.PreparedRequest] = []

        original_prepare_request = requests.Session.prepare_request

        def capture_prepare_request(request: requests.Request) -> Any:
            prepared_request = original_prepare_request(requests.Session(), request)
            captured_calls.append(prepared_request)
            return prepared_request

        with mock_patch(
            "requests.Session.prepare_request",
            side_effect=capture_prepare_request,
        ):
            channel = Channel(url=url)
            channel_method = getattr(channel, method)
            _ = channel_method(**kwargs)
            prepared_request_channel = captured_calls.pop()

            single_request_method = globals()[method]
            _ = single_request_method(url=url, **kwargs)
            prepared_request_single_request = captured_calls.pop()

        assert (
            prepared_request_channel.__dict__
            == prepared_request_single_request.__dict__
        )


def test_single_request_get():
    assert_equal_requests("get")


def test_single_request_post():
    assert_equal_requests("post")


def test_single_request_put():
    assert_equal_requests("put")


def test_single_request_delete():
    assert_equal_requests("delete")


def test_single_request_patch():
    assert_equal_requests("patch")
