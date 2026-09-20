import asyncio
from time import perf_counter
import ssl
import certifi
import aiohttp

from task2.common import ParsedPage, URLS, extract_title, save_as_task


async def parse_and_save(url: str, session: aiohttp.ClientSession) -> ParsedPage | None:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
        page = ParsedPage(url=url, title=extract_title(html))
        await asyncio.to_thread(save_as_task, page, "asyncio")
        print(f"[asyncio] {page.title} <- {url}")
        return page
    except Exception as error:
        print(f"[asyncio] Ошибка {url}: {error}")
        return None


async def run() -> None:
    timeout = aiohttp.ClientTimeout(total=20)
    headers = {"User-Agent": "TimeFlow-Lab2/1.0"}

    ssl_context = ssl.create_default_context(
        cafile=certifi.where()
    )

    connector = aiohttp.TCPConnector(
        ssl=ssl_context
    )

    async with aiohttp.ClientSession(
        timeout=timeout,
        headers=headers,
        connector=connector
    ) as session:
        await asyncio.gather(
            *(parse_and_save(url, session) for url in URLS)
        )


def main() -> None:
    started = perf_counter()
    asyncio.run(run())
    print(f"Общее время asyncio: {perf_counter() - started:.3f} сек.")


if __name__ == "__main__":
    main()

