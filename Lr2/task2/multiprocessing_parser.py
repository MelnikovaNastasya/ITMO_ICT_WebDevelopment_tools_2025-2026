import multiprocessing as mp
from time import perf_counter

import requests

from task2.common import ParsedPage, URLS, extract_title, save_as_task, split_urls


def parse_and_save(url: str) -> ParsedPage:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    page = ParsedPage(url=url, title=extract_title(response.text))
    save_as_task(page, "multiprocessing")
    print(f"[multiprocessing] {page.title} <- {url}")
    return page


def parse_chunk(urls: list[str]) -> None:
    for url in urls:
        try:
            parse_and_save(url)
        except Exception as error:
            print(f"[multiprocessing] Ошибка {url}: {error}")


def main() -> None:
    started = perf_counter()
    chunks = split_urls(URLS, min(4, len(URLS)))
    processes = [mp.Process(target=parse_chunk, args=(chunk,)) for chunk in chunks]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print(f"Общее время multiprocessing: {perf_counter() - started:.3f} сек.")


if __name__ == "__main__":
    mp.freeze_support()
    main()

