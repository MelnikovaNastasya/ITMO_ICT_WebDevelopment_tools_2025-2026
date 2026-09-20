import asyncio

from task1.async_sum import calculate_all
from task1.common import calculate_sum, expected_sum, split_range
from task1.threading_sum import run as run_threads


def test_calculate_sum() -> None:
    assert calculate_sum(1, 100) == 5050


def test_ranges_cover_numbers_once() -> None:
    ranges = split_range(10, 3)
    values = [number for start, end in ranges for number in range(start, end + 1)]
    assert values == list(range(1, 11))


def test_threading_result() -> None:
    assert run_threads(10_000, 4).result == expected_sum(10_000)


def test_async_result() -> None:
    assert asyncio.run(calculate_all(10_000, 4)) == expected_sum(10_000)

