# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from typing import Optional, List, Any
from unittest.mock import patch, Mock
from hcc import Channel, DataType

MAX_RETRY_COUNT = 5


def run_test(
    method: str,
    url: str,
    side_effects: List[Mock],
    data: Optional[DataType] = None,
):
    with patch(f"hcc.channel.requests.{method}") as mock_method:
        mock_method.side_effect = side_effects
        channel = Channel(url=url, max_retry_count=MAX_RETRY_COUNT)
        method_to_call = getattr(channel, method)
        kwargs: dict[str, Any] = {"data": data}
        if method in ["post", "put", "patch"]:
            response = method_to_call(**kwargs)
        else:
            response = method_to_call()
        return response, mock_method


def test_channel_get_success():
    response, mock_get = run_test(
        method="get",
        url="https://mockserver.com/success",
        side_effects=[Mock(status_code=200)],
    )
    assert response.status_code == 200
    assert mock_get.call_count == 1


def test_channel_get_fail():
    response, mock_get = run_test(
        method="get",
        url="https://mockserver.com/fail",
        side_effects=[Mock(status_code=500)] * MAX_RETRY_COUNT,
    )
    assert response.status_code == 500
    assert mock_get.call_count == MAX_RETRY_COUNT


def test_channel_get_success_on_third_time():
    response, mock_get = run_test(
        method="get",
        url="https://mockserver.com/success_on_third_time",
        side_effects=[
            Mock(status_code=500),
            Mock(status_code=500),
            Mock(status_code=200),
        ],
    )
    assert response.status_code == 200
    assert mock_get.call_count == 3


def test_channel_post_success():
    response, mock_post = run_test(
        method="post",
        url="https://mockserver.com/success",
        side_effects=[Mock(status_code=201)],
        data={},
    )
    assert response.status_code == 201
    assert mock_post.call_count == 1


def test_channel_post_fail():
    response, mock_post = run_test(
        method="post",
        url="https://mockserver.com/fail",
        side_effects=[Mock(status_code=500)] * MAX_RETRY_COUNT,
        data={},
    )
    assert response.status_code == 500
    assert mock_post.call_count == MAX_RETRY_COUNT


def test_channel_post_success_on_third_time():
    response, mock_post = run_test(
        method="post",
        url="https://mockserver.com/success_on_third_time",
        side_effects=[
            Mock(status_code=500),
            Mock(status_code=500),
            Mock(status_code=201),
        ],
        data={},
    )
    assert response.status_code == 201
    assert mock_post.call_count == 3


def test_channel_put_success():
    response, mock_put = run_test(
        method="put",
        url="https://mockserver.com/success",
        side_effects=[Mock(status_code=201)],
        data={},
    )
    assert response.status_code == 201
    assert mock_put.call_count == 1


def test_channel_put_fail():
    response, mock_put = run_test(
        method="put",
        url="https://mockserver.com/fail",
        side_effects=[Mock(status_code=500)] * MAX_RETRY_COUNT,
        data={},
    )
    assert response.status_code == 500
    assert mock_put.call_count == MAX_RETRY_COUNT


def test_channel_put_success_on_third_time():
    response, mock_put = run_test(
        method="put",
        url="https://mockserver.com/success_on_third_time",
        side_effects=[
            Mock(status_code=500),
            Mock(status_code=500),
            Mock(status_code=201),
        ],
        data={},
    )
    assert response.status_code == 201
    assert mock_put.call_count == 3


def test_channel_delete_success():
    response, mock_delete = run_test(
        method="delete",
        url="https://mockserver.com/success",
        side_effects=[Mock(status_code=200)],
    )
    assert response.status_code == 200
    assert mock_delete.call_count == 1


def test_channel_delete_fail():
    response, mock_delete = run_test(
        method="delete",
        url="https://mockserver.com/fail",
        side_effects=[Mock(status_code=500)] * MAX_RETRY_COUNT,
    )
    assert response.status_code == 500
    assert mock_delete.call_count == MAX_RETRY_COUNT


def test_channel_delete_success_on_third_time():
    response, mock_delete = run_test(
        method="delete",
        url="https://mockserver.com/success_on_third_time",
        side_effects=[
            Mock(status_code=500),
            Mock(status_code=500),
            Mock(status_code=200),
        ],
    )
    assert response.status_code == 200
    assert mock_delete.call_count == 3


def test_channel_patch_success():
    response, mock_patch = run_test(
        method="patch",
        url="https://mockserver.com/success",
        side_effects=[Mock(status_code=200)],
        data={},
    )
    assert response.status_code == 200
    assert mock_patch.call_count == 1


def test_channel_patch_fail():
    response, mock_patch = run_test(
        method="patch",
        url="https://mockserver.com/fail",
        side_effects=[Mock(status_code=500)] * MAX_RETRY_COUNT,
        data={},
    )
    assert response.status_code == 500
    assert mock_patch.call_count == MAX_RETRY_COUNT


def test_channel_patch_success_on_third_time():
    response, mock_patch = run_test(
        method="patch",
        url="https://mockserver.com/success_on_third_time",
        side_effects=[
            Mock(status_code=500),
            Mock(status_code=500),
            Mock(status_code=200),
        ],
        data={},
    )
    assert response.status_code == 200
    assert mock_patch.call_count == 3
