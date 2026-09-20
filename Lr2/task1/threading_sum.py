import threading

from task1.common import LIMIT, WORKERS, Measurement, calculate_sum, print_measurement, split_range, timed


def run(limit: int = LIMIT, workers: int = WORKERS) -> Measurement:
    ranges = split_range(limit, workers)
    partial_results = [0] * workers

    def worker(index: int, start: int, end: int) -> None:
        partial_results[index] = calculate_sum(start, end)

    def operation() -> int:
        threads = [
            threading.Thread(target=worker, args=(index, start, end))
            for index, (start, end) in enumerate(ranges)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return sum(partial_results)

    return timed("threading", operation)


if __name__ == "__main__":
    print_measurement(run(), LIMIT)

