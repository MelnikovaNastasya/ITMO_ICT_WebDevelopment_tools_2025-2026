import asyncio

from task1.common import LIMIT, WORKERS, Measurement, calculate_sum, print_measurement, split_range, timed


async def calculate_sum_async(start: int, end: int) -> int:
    await asyncio.sleep(0)
    return calculate_sum(start, end)


async def calculate_all(limit: int, workers: int) -> int:
    ranges = split_range(limit, workers)
    partial_results = await asyncio.gather(
        *(calculate_sum_async(start, end) for start, end in ranges)
    )
    return sum(partial_results)


def run(limit: int = LIMIT, workers: int = WORKERS) -> Measurement:
    return timed("asyncio", lambda: asyncio.run(calculate_all(limit, workers)))


if __name__ == "__main__":
    print_measurement(run(), LIMIT)

