from pytest_httpx import HTTPXMock

from main import HttpClient 
from main import HTTPResponse


def test_request_get(http_client: HttpClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response()
    response: HTTPResponse = http_client.request("GET", "")

    assert response.status_code == 200


def test_request_post(http_client: HttpClient, httpx_mock: HTTPXMock):
    request_data = {"key": "value"}

    httpx_mock.add_response(
        method="POST",
        headers={"Content-Type": "application/json"},
        json=request_data,
    )

    response: HTTPResponse = http_client.request(
        "POST", "", json=request_data
    )

    assert response.status_code == 200

    result = response.json()
    assert result == request_data
