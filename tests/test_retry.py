# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
import time
import pytest
from hcc.retry import retry_function, RetryPolicy
from .test_utilities import Counter, assert_runtime

BASE_DELAY = 100
MAX_RETRIES = 5


def setup_function():
    Counter.reset()


def test_retry_function_with_exceptions_fail():
    Counter.reset()

    def always_fail():
        Counter.next()
        raise Exception("Always fail")  # pylint: disable=broad-exception-raised

    start_time = time.time()
    with pytest.raises(Exception, match="Always fail"):
        retry_function(
            func=always_fail,
            is_retry_needed=lambda x: True,
            max_retry_count=MAX_RETRIES,
            retry_policy=RetryPolicy.LINEAR,
            base_delay=BASE_DELAY,
        )
    end_time = time.time()

    assert Counter.count == MAX_RETRIES
    expected_runtime = (MAX_RETRIES - 1) * (BASE_DELAY / 1000)
    actual_runtime = end_time - start_time
    assert_runtime(expected_runtime, actual_runtime)


def test_retry_function_with_exceptions_eventual_success():
    Counter.reset()

    def succeed_on_third_time():
        val = Counter.next()
        if val == 3:
            return val
        raise Exception("Fail on first two attempts")  # pylint: disable=broad-exception-raised

    start_time = time.time()
    response = retry_function(
        func=succeed_on_third_time,
        is_retry_needed=lambda x: False,  # Exceptions are always retried
        max_retry_count=MAX_RETRIES,
        retry_policy=RetryPolicy.LINEAR,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()

    assert response == 3
    expected_runtime = (3 - 1) * (BASE_DELAY / 1000)
    actual_runtime = end_time - start_time
    assert_runtime(expected_runtime, actual_runtime)
