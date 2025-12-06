import json
from collections.abc import Generator

import pytest

from client.client import HTTPClient


@pytest.fixture
def http_client() -> Generator[HTTPClient]:
    http_client = HTTPClient("https://test.com")
    yield http_client


@pytest.fixture
def application_json_headers() -> dict[str, str]:
    return {"content-type": "application/json"}


@pytest.fixture
def json_dict() -> dict[str, str]:
    return {"key": "value"}


@pytest.fixture
def json_bytes(json_dict: dict[str, str]) -> bytes:
    json_bytest = json.dumps(json_dict, separators=(": ", ":")).encode("utf-8")
    return json_bytest
