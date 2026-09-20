from dataclasses import dataclass
from time import perf_counter

LIMIT = 10_000_000_000_000
WORKERS = 4


@dataclass(frozen=True)
class Measurement:
    approach: str
    result: int
    seconds: float


def calculate_sum(start: int, end: int) -> int:
    """Возвращает сумму целых чисел на включительном отрезке [start, end]."""
    if start > end:
        return 0
    return (start + end) * (end - start + 1) // 2


def split_range(limit: int, parts: int) -> list[tuple[int, int]]:
    """Делит диапазон 1..limit на parts непересекающихся частей."""
    if limit < 1:
        raise ValueError("limit должен быть положительным")
    if parts < 1:
        raise ValueError("parts должен быть положительным")

    base, remainder = divmod(limit, parts)
    ranges: list[tuple[int, int]] = []
    start = 1
    for index in range(parts):
        size = base + (1 if index < remainder else 0)
        end = start + size - 1
        ranges.append((start, end))
        start = end + 1
    return ranges


def expected_sum(limit: int) -> int:
    return limit * (limit + 1) // 2


def print_measurement(measurement: Measurement, limit: int) -> None:
    print(f"Подход: {measurement.approach}")
    print(f"Сумма чисел от 1 до {limit}: {measurement.result}")
    print(f"Правильный результат: {measurement.result == expected_sum(limit)}")
    print(f"Время: {measurement.seconds:.6f} сек.")


def timed(approach: str, operation) -> Measurement:
    started = perf_counter()
    result = operation()
    return Measurement(approach, result, perf_counter() - started)

