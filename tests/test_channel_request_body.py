# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from typing import Any, Optional
from unittest.mock import patch, Mock
import pytest
import requests
from hcc import Channel, DataType, JsonType


def run_test(
    method: str,
    data: Optional[DataType] = None,
    json: Optional[JsonType] = None,
) -> requests.PreparedRequest:
    with patch("requests.Session.send") as mock_send:
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}
        mock_send.return_value = mock_response

        url = "https://mockserver.com/success"

        captured_calls: list[requests.PreparedRequest] = []

        original_prepare_request = requests.Session.prepare_request

        def capture_prepare_request(request: requests.Request) -> Any:
            prepared_request = original_prepare_request(requests.Session(), request)
            captured_calls.append(prepared_request)
            return prepared_request

        with patch(
            "requests.Session.prepare_request",
            side_effect=capture_prepare_request,
        ):
            channel = Channel(url=url, max_retry_count=1)
            method_to_call = getattr(channel, method)
            _ = method_to_call(**{"data": data, "json": json})

    return captured_calls.pop()


def test_channel_post_request_body_data():
    prepared_request = run_test(
        method="post",
        data={"key": "value"},
    )
    assert prepared_request.body == "key=value"
    assert not prepared_request.headers["Content-Type"] == "application/json"


def test_channel_post_request_body_json():
    prepared_request = run_test(
        method="post",
        json={"key": "value"},
    )
    assert prepared_request.body == b'{"key": "value"}'
    assert prepared_request.headers["Content-Type"] == "application/json"


def test_channel_post_request_body_neiher():
    with pytest.raises(Exception):
        _ = run_test(
            method="post",
        )


def test_channel_post_request_body_both():
    with pytest.raises(Exception):
        _ = run_test(
            method="post",
            data={"key": "value"},
            json={"key": "value"},
        )


def test_channel_put_request_body_data():
    prepared_request = run_test(
        method="put",
        data={"key": "value"},
    )
    assert prepared_request.body == "key=value"
    assert not prepared_request.headers["Content-Type"] == "application/json"


def test_channel_put_request_body_json():
    prepared_request = run_test(
        method="put",
        json={"key": "value"},
    )
    assert prepared_request.body == b'{"key": "value"}'
    assert prepared_request.headers["Content-Type"] == "application/json"


def test_channel_put_request_body_neiher():
    with pytest.raises(Exception):
        _ = run_test(
            method="put",
        )


def test_channel_put_request_body_both():
    with pytest.raises(Exception):
        _ = run_test(
            method="put",
            data={"key": "value"},
            json={"key": "value"},
        )


def test_channel_patch_request_body_data():
    prepared_request = run_test(
        method="patch",
        data={"key": "value"},
    )
    assert prepared_request.body == "key=value"
    assert not prepared_request.headers["Content-Type"] == "application/json"


def test_channel_patch_request_body_json():
    prepared_request = run_test(
        method="patch",
        json={"key": "value"},
    )
    assert prepared_request.body == b'{"key": "value"}'
    assert prepared_request.headers["Content-Type"] == "application/json"


def test_channel_patch_request_body_neiher():
    with pytest.raises(Exception):
        _ = run_test(
            method="patch",
        )


def test_channel_patch_request_body_both():
    with pytest.raises(Exception):
        _ = run_test(
            method="patch",
            data={"key": "value"},
            json={"key": "value"},
        )
