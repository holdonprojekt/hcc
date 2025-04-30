# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from unittest.mock import patch
import pytest
import requests
from hcc.exceptions import (
    ConnectTimeout,
    RequestError,
    JSONDecodeError,
    ReadTimeout,
    RequestException,
    UnknownRequestException,
)
from hcc.single_request import get


@pytest.mark.parametrize(
    "requests_exception, hcc_exception",
    [
        (requests.ConnectTimeout, ConnectTimeout),
        (requests.FileModeWarning, RequestError),
        (requests.HTTPError, RequestError),
        (requests.TooManyRedirects, RequestError),
        (requests.JSONDecodeError, JSONDecodeError),
        (requests.ReadTimeout, ReadTimeout),
        (requests.RequestException, RequestException),
        (Exception, UnknownRequestException),
    ],
)
def test_exception(requests_exception: type[Exception], hcc_exception: type[Exception]):
    with patch("hcc.channel.requests.request") as mock_method:
        if requests_exception is requests.JSONDecodeError:
            mock_method.side_effect = requests_exception("fake_msg", "fake_doc", 0)
        else:
            mock_method.side_effect = requests_exception()

        with pytest.raises(hcc_exception):
            _ = get(url="https://mockserver.com/success")
