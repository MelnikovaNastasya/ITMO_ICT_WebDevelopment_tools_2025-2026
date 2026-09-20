import multiprocessing as mp

from task1.common import LIMIT, WORKERS, Measurement, calculate_sum, print_measurement, split_range, timed


def run(limit: int = LIMIT, workers: int = WORKERS) -> Measurement:
    ranges = split_range(limit, workers)

    def operation() -> int:
        with mp.Pool(processes=workers) as pool:
            return sum(pool.starmap(calculate_sum, ranges))

    return timed("multiprocessing", operation)


if __name__ == "__main__":
    mp.freeze_support()
    print_measurement(run(), LIMIT)

