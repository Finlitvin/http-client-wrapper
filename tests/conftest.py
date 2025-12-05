from typing import Generator

import pytest

from main import HttpClient


@pytest.fixture
def http_client() -> Generator[HttpClient]:
    http_client = HttpClient("https://jsonplaceholder.typicode.com")
    yield http_client
