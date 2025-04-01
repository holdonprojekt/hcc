# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from unittest import TestCase
from unittest.mock import Mock
from hcc import retry_function


class TestLogRetry(TestCase):
    def test_logging_on_retry_function_success(self):
        mock_func = Mock()
        mock_func.side_effect = ["Success"]

        with self.assertLogs("hcc.retry", level="INFO") as context:
            _ = retry_function(
                func=mock_func,
                is_retry_needed=lambda x: x != "Success",
                max_retry_count=5,
            )

            expected_log = "INFO:hcc.retry:Attempt 1/5 returning with: Success"
            self.assertEqual(len(context.output), 1)
            self.assertEqual(context.output[0], expected_log)

    def test_logging_on_retry_function_exception(self):
        mock_func = Mock()
        mock_func.side_effect = [Exception("Error"), "Success"]

        with self.assertLogs("hcc.retry", level="INFO") as context:
            _ = retry_function(
                func=mock_func,
                is_retry_needed=lambda x: x != "Success",
                max_retry_count=5,
            )

            expected_log = "WARNING:hcc.retry:Attempt 1/5 failed with exception: Error"
            self.assertEqual(len(context.output), 2)
            self.assertEqual(context.output[0], expected_log)

    def test_logging_on_retry_function_exception_return(self):
        mock_func = Mock()
        mock_func.side_effect = [Exception("Error")]

        with (
            self.assertLogs("hcc.retry", level="INFO") as context,
            self.assertRaises(Exception),
        ):
            _ = retry_function(
                func=mock_func,
                is_retry_needed=lambda x: x != "Success",
                max_retry_count=1,
            )

            expected_log = (
                "WARNING:hcc.retry:Attempt 1/1 returning with exception: Error"
            )
            self.assertEqual(len(context.output), 1)
            self.assertEqual(context.output[0], expected_log)

    def test_logging_on_retry_function_error(self):
        mock_func = Mock()
        mock_func.side_effect = ["Error", "Success"]

        with self.assertLogs("hcc.retry", level="INFO") as context:
            _ = retry_function(
                func=mock_func,
                is_retry_needed=lambda x: x != "Success",
                max_retry_count=5,
            )

            expected_log = "INFO:hcc.retry:Attempt 1/5 failed with error result: Error"
            self.assertEqual(len(context.output), 2)
            self.assertEqual(context.output[0], expected_log)

    def test_logging_on_retry_function_error_return(self):
        mock_func = Mock()
        mock_func.side_effect = ["Error"]

        with self.assertLogs("hcc.retry", level="INFO") as context:
            _ = retry_function(
                func=mock_func,
                is_retry_needed=lambda x: x != "Success",
                max_retry_count=1,
            )

            expected_log = "INFO:hcc.retry:Attempt 1/1 returning with: Error"
            self.assertEqual(len(context.output), 1)
            self.assertEqual(context.output[0], expected_log)
