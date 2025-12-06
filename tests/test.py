import pytest
from pytest_httpx import HTTPXMock

from httpx import RequestError

from client.errors import HTTPCommunicationError
from client.errors import HTTPRequestError
from client.client import HTTPClient
from client.models import HTTPResponse
from client.hooks import raise_on_4xx_5xx


def test_request_get(http_client: HTTPClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"key": "value"},
        headers={"Content-Type": "application/json"},
    )
    response: HTTPResponse = http_client.request("GET", "")

    assert response.status_code == 200
    assert response.content == b'{"key":"value"}'
    assert response.headers == {
        "content-length": "15",
        "content-type": "application/json",
    }
    assert response.json() == {"key": "value"}
    assert response.text() == '{"key":"value"}'


def test_request_post(http_client: HTTPClient, httpx_mock: HTTPXMock):
    request_data = {"key": "value"}

    httpx_mock.add_response(
        method="POST",
        headers={"Content-Type": "application/json"},
        json=request_data,
    )

    response: HTTPResponse = http_client.request("POST", "", json=request_data)

    assert response.status_code == 200

    result = response.json()
    assert result == request_data


def test_http_request_error(http_client: HTTPClient, httpx_mock: HTTPXMock):
    httpx_mock.add_exception(RequestError("Request error"))
    with pytest.raises(HTTPCommunicationError) as exc:
        _ = http_client.request("GET", "")
    assert str(exc.value) == "Request error"


def test_http_status_error_with_exception(http_client: HTTPClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=404,
        method="POST",
        headers={"Content-Type": "application/json"},
        json={},
    )

    with pytest.raises(HTTPRequestError) as exc:
        _ = http_client.request(
            method="POST", url="", event_hooks={"response": [raise_on_4xx_5xx]}
        )

    assert exc.value.message == "Error"
