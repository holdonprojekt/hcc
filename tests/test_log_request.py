# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from unittest import TestCase
from unittest.mock import patch, Mock
import requests
from hcc import Channel


class TestLogRequest(TestCase):
    url = "https://mockserver.com/success"
    timeout = 2.0
    max_retry_count = 5
    retry_policy = None
    base_delay = None
    params = {"param1": "value1", "param2": "value2"}
    headers = {"header1": "value1", "header2": "value2"}
    json = {"key": "value"}

    def test_logging_on_new_channel(self):
        with patch("requests.Session.send") as mock_send:
            mock_response = Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"message": "success"}
            mock_send.return_value = mock_response

            with self.assertLogs("hcc.request", level="INFO") as context:
                _ = Channel(
                    url=self.url,
                    timeout=self.timeout,
                    max_retry_count=self.max_retry_count,
                    retry_policy=self.retry_policy,
                    base_delay=self.base_delay,
                )
                expected_log = (
                    r"^INFO:hcc.request:Channel created: id: \d+, "
                    + r"URL: "
                    + self.url
                    + r", "
                    + r"timeout: "
                    + str(self.timeout)
                    + r", "
                    + r"max_retry_count: "
                    + str(self.max_retry_count)
                    + r", "
                    + r"retry_policy: "
                    + str(self.retry_policy)
                    + r", "
                    + r"base_delay: "
                    + str(self.base_delay)
                    + r"$"
                )
                self.assertEqual(len(context.output), 1)
                self.assertRegex(context.output[0], expected_log)

    def test_logging_on_get_request(self):
        with patch("requests.Session.send") as mock_send:
            mock_response = Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"message": "success"}
            mock_send.return_value = mock_response

            channel = Channel(url=self.url)

            with self.assertLogs("hcc.request", level="INFO") as context:
                channel.get(params=self.params, headers=self.headers)

                expected_request_log = (
                    r"^INFO:hcc.request:GET request: "
                    + r"channel: \d+, "
                    + r"params: "
                    + str(self.params)
                    + r", "
                    + r"headers: "
                    + str(self.headers)
                    + r"$"
                )
                expected_response_log = r"^INFO:hcc.request:GET response: .+$"

                self.assertEqual(len(context.output), 2)
                self.assertRegex(context.output[0], expected_request_log)
                self.assertRegex(context.output[1], expected_response_log)

    def test_logging_on_post_request(self):
        with patch("requests.Session.send") as mock_send:
            mock_response = Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"message": "success"}
            mock_send.return_value = mock_response

            channel = Channel(url=self.url)

            with self.assertLogs("hcc.request", level="INFO") as context:
                channel.post(json=self.json, headers=self.headers)

                expected_request_log = (
                    r"^INFO:hcc.request:POST request: "
                    + r"channel: \d+, "
                    + r"data: None, "
                    + r"json: "
                    + str(self.json)
                    + r", "
                    + r"headers: "
                    + str(self.headers)
                    + r"$"
                )
                expected_response_log = r"^INFO:hcc.request:POST response: .+$"

                self.assertEqual(len(context.output), 2)
                self.assertRegex(context.output[0], expected_request_log)
                self.assertRegex(context.output[1], expected_response_log)

    def test_logging_on_put_request(self):
        with patch("requests.Session.send") as mock_send:
            mock_response = Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"message": "success"}
            mock_send.return_value = mock_response

            channel = Channel(url=self.url)

            with self.assertLogs("hcc.request", level="INFO") as context:
                channel.put(json=self.json, headers=self.headers)

                expected_request_log = (
                    r"^INFO:hcc.request:PUT request: "
                    + r"channel: \d+, "
                    + r"data: None, "
                    + r"json: "
                    + str(self.json)
                    + r", "
                    + r"headers: "
                    + str(self.headers)
                    + r"$"
                )
                expected_response_log = r"^INFO:hcc.request:PUT response: .+$"

                self.assertEqual(len(context.output), 2)
                self.assertRegex(context.output[0], expected_request_log)
                self.assertRegex(context.output[1], expected_response_log)

    def test_logging_on_delete_request(self):
        with patch("requests.Session.send") as mock_send:
            mock_response = Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"message": "success"}
            mock_send.return_value = mock_response

            channel = Channel(url=self.url)

            with self.assertLogs("hcc.request", level="INFO") as context:
                channel.delete(headers=self.headers)

                expected_request_log = (
                    r"^INFO:hcc.request:DELETE request: "
                    + r"channel: \d+, "
                    + r"headers: "
                    + str(self.headers)
                    + r"$"
                )
                expected_response_log = r"^INFO:hcc.request:DELETE response: .+$"

                self.assertEqual(len(context.output), 2)
                self.assertRegex(context.output[0], expected_request_log)
                self.assertRegex(context.output[1], expected_response_log)

    def test_logging_on_patch_request(self):
        with patch("requests.Session.send") as mock_send:
            mock_response = Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.json.return_value = {"message": "success"}
            mock_send.return_value = mock_response

            channel = Channel(url=self.url)

            with self.assertLogs("hcc.request", level="INFO") as context:
                channel.patch(json=self.json, headers=self.headers)

                expected_request_log = (
                    r"^INFO:hcc.request:PATCH request: "
                    + r"channel: \d+, "
                    + r"data: None, "
                    + r"json: "
                    + str(self.json)
                    + r", "
                    + r"headers: "
                    + str(self.headers)
                    + r"$"
                )
                expected_response_log = r"^INFO:hcc.request:PATCH response: .+$"

                self.assertEqual(len(context.output), 2)
                self.assertRegex(context.output[0], expected_request_log)
                self.assertRegex(context.output[1], expected_response_log)
