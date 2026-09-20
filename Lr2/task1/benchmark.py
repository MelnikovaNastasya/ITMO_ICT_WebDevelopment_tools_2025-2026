import csv
from pathlib import Path

from task1.async_sum import run as run_async
from task1.multiprocessing_sum import run as run_processes
from task1.threading_sum import run as run_threads


def main() -> None:
    measurements = [run_threads(), run_processes(), run_async()]
    output = Path(__file__).resolve().parents[1] / "results" / "task1_times.csv"
    output.parent.mkdir(exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["approach", "seconds", "result"])
        for item in measurements:
            writer.writerow([item.approach, f"{item.seconds:.6f}", item.result])
            print(f"{item.approach}: {item.seconds:.6f} сек.; сумма={item.result}")
    print(f"Результаты сохранены: {output}")


if __name__ == "__main__":
    main()

