import threading
from time import perf_counter

import requests

from task2.common import ParsedPage, URLS, extract_title, save_as_task, split_urls


def parse_and_save(url: str) -> ParsedPage:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    page = ParsedPage(url=url, title=extract_title(response.text))
    save_as_task(page, "threading")
    print(f"[threading] {page.title} <- {url}")
    return page


def parse_chunk(urls: list[str]) -> None:
    for url in urls:
        try:
            parse_and_save(url)
        except Exception as error:
            print(f"[threading] Ошибка {url}: {error}")


def main() -> None:
    started = perf_counter()
    chunks = split_urls(URLS, min(4, len(URLS)))
    threads = [threading.Thread(target=parse_chunk, args=(chunk,)) for chunk in chunks]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Общее время threading: {perf_counter() - started:.3f} сек.")


if __name__ == "__main__":
    main()

