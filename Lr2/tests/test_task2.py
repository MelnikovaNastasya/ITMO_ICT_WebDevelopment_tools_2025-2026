from task2.common import extract_title, split_urls


def test_extract_title() -> None:
    assert extract_title("<html><title> Test   page </title></html>") == "Test page"


def test_split_urls_preserves_all_urls() -> None:
    urls = ["a", "b", "c", "d", "e"]
    chunks = split_urls(urls, 3)
    assert sorted(url for chunk in chunks for url in chunk) == urls

