import socket
from unittest.mock import patch

import pytest

from shared.parser_logic import UnsafeUrlError, extract_title, validate_public_url


def test_extract_title() -> None:
    assert extract_title("<html><title>  Test page </title></html>") == "Test page"


def test_extract_missing_title() -> None:
    assert extract_title("<html><body>Hello</body></html>") == "Без заголовка"


def test_rejects_non_http_url() -> None:
    with pytest.raises(UnsafeUrlError):
        validate_public_url("file:///etc/passwd")


@patch("shared.parser_logic.socket.getaddrinfo")
def test_rejects_private_address(getaddrinfo) -> None:
    getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))]
    with pytest.raises(UnsafeUrlError):
        validate_public_url("http://localhost/test")
