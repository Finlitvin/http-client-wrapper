import pytest
from pytest_httpx import HTTPXMock

from httpx import RequestError

from client.errors import HTTPCommunicationError
from client.errors import HTTPRequestError
from client.client import HTTPClient
from client.models import HTTPResponse
from client.hooks import raise_on_4xx_5xx


def test_request_get(
    http_client: HTTPClient,
    httpx_mock: HTTPXMock,
    application_json_headers: dict,
    json_dict: dict,
    json_bytes: bytes,
):
    method = "POST"
    url = ""

    httpx_mock.add_response(
        url=url,
        headers=application_json_headers,
        json=json_dict,
    )
    response: HTTPResponse = http_client.request(method, url)

    assert response.status_code == 200
    assert response.headers.get(
        "content-type"
    ) == application_json_headers.get("content-type")
    assert response.content == json_bytes
    assert response.text() == json_bytes.decode("utf-8")
    assert response.json() == json_dict


def test_request_post(
    http_client: HTTPClient,
    httpx_mock: HTTPXMock,
    application_json_headers: dict,
    json_dict: dict,
    json_bytes: bytes,
):
    method = "POST"
    url = ""

    httpx_mock.add_response(
        method=method,
        url=url,
        headers=application_json_headers,
        json=json_dict,
    )

    response: HTTPResponse = http_client.request(method, url, json=json_dict)

    assert response.status_code == 200
    assert response.headers.get(
        "content-type"
    ) == application_json_headers.get("content-type")
    assert response.content == json_bytes
    assert response.text() == json_bytes.decode("utf-8")
    assert response.json() == json_dict


def test_http_communication_error(
    http_client: HTTPClient, httpx_mock: HTTPXMock
):
    method = "POST"
    url = ""
    error_str = "Request error"

    httpx_mock.add_exception(RequestError(error_str))
    with pytest.raises(HTTPCommunicationError) as exc:
        _ = http_client.request(method, url)

    assert str(exc.value) == error_str


def test_http_status_error_with_exception(
    http_client: HTTPClient,
    httpx_mock: HTTPXMock,
    application_json_headers: dict,
    json_dict: dict,
    json_bytes: bytes,
):
    method = "POST"
    url = ""
    error_str = "Error"
    status_code = 404

    httpx_mock.add_response(
        status_code=status_code,
        method=method,
        headers=application_json_headers,
        json=json_dict,
    )

    with pytest.raises(HTTPRequestError) as exc:
        _ = http_client.request(
            method=method,
            url=url,
            event_hooks={"response": [raise_on_4xx_5xx]},
        )

    assert exc.value.message == error_str
    assert exc.value.response.status_code == status_code
    assert exc.value.response.headers.get(
        "content-type"
    ) == application_json_headers.get("content-type")
    assert exc.value.response.content == json_bytes
    assert exc.value.response.text() == json_bytes.decode("utf-8")
    assert exc.value.response.json() == json_dict
