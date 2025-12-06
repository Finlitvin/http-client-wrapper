from typing import Generator

import pytest

from client.client import HTTPClient


@pytest.fixture
def http_client() -> Generator[HTTPClient]:
    http_client = HTTPClient("https://test_url")
    yield http_client
