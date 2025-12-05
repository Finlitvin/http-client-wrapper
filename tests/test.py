from main import HttpClient, HTTPResponse


def test_request_get(http_client: HttpClient):
    response: HTTPResponse = http_client.request(
        "GET",
        "/posts/1",
    )

    assert response.status_code == 200
