# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# ruff: noqa: E731
import time
from typing import Callable
from hcc import retry_function, RetryPolicy
from .test_utilities import Counter, assert_runtime, assert_runtime_interval

BASE_DELAY = 100
MAX_RETRIES = 5
RETRY_NUMBER_SUCCESS = 3
RETRY_NEEDED_SUCCESS: Callable[[int], bool] = (
    lambda result: result < RETRY_NUMBER_SUCCESS
)
RETRY_NEEDED_FAIL: Callable[[int], bool] = lambda result: result < 10


def setup_function():
    Counter.reset()


def test_retry_function_success_immediate():
    start_time = time.time()
    response = retry_function(
        func=Counter.next,
        is_retry_needed=RETRY_NEEDED_SUCCESS,
        retry_policy=RetryPolicy.IMMEDIATE,
        max_retry_count=MAX_RETRIES,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()
    assert response == RETRY_NUMBER_SUCCESS
    assert end_time - start_time < 0.1


def test_retry_function_fail_immediate():
    start_time = time.time()
    response = retry_function(
        func=Counter.next,
        is_retry_needed=RETRY_NEEDED_FAIL,
        retry_policy=RetryPolicy.IMMEDIATE,
        max_retry_count=MAX_RETRIES,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()
    assert response == MAX_RETRIES
    assert end_time - start_time < 0.1


def test_retry_function_success_linear():
    start_time = time.time()
    response = retry_function(
        func=Counter.next,
        is_retry_needed=RETRY_NEEDED_SUCCESS,
        retry_policy=RetryPolicy.LINEAR,
        max_retry_count=MAX_RETRIES,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()
    assert response == RETRY_NUMBER_SUCCESS
    assert_runtime(
        (RETRY_NUMBER_SUCCESS - 1) * BASE_DELAY / 1000, end_time - start_time
    )


def test_retry_function_fail_linear():
    start_time = time.time()
    response = retry_function(
        func=Counter.next,
        is_retry_needed=lambda result: result < 10,
        retry_policy=RetryPolicy.LINEAR,
        max_retry_count=MAX_RETRIES,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()
    assert response == MAX_RETRIES
    assert_runtime((MAX_RETRIES - 1) * BASE_DELAY / 1000, end_time - start_time)


def test_retry_function_success_jitter():
    start_time = time.time()
    response = retry_function(
        func=Counter.next,
        is_retry_needed=RETRY_NEEDED_SUCCESS,
        retry_policy=RetryPolicy.JITTER,
        max_retry_count=MAX_RETRIES,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()
    assert response == RETRY_NUMBER_SUCCESS
    expected_runtime_middle = (RETRY_NUMBER_SUCCESS - 1) * BASE_DELAY / 1000
    assert_runtime_interval(
        expected_runtime_middle * 0.5,
        expected_runtime_middle * 1.5,
        end_time - start_time,
    )


def test_retry_function_fail_jitter():
    start_time = time.time()
    response = retry_function(
        func=Counter.next,
        is_retry_needed=RETRY_NEEDED_FAIL,
        retry_policy=RetryPolicy.JITTER,
        max_retry_count=MAX_RETRIES,
        base_delay=BASE_DELAY,
    )
    end_time = time.time()
    assert response == MAX_RETRIES
    expected_runtime_middle = (MAX_RETRIES - 1) * BASE_DELAY / 1000
    assert_runtime_interval(
        expected_runtime_middle * 0.5,
        expected_runtime_middle * 1.5,
        end_time - start_time,
    )
