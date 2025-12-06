import logging

from client.base import HTTPClientInterface
from client.errors import HTTPCommunicationError
from client.errors import HTTPInvalidURL
from client.errors import HTTPRequestError
from client.client import HTTPClient
from client.hooks import raise_on_4xx_5xx

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(levelname)s]: %(message)s"
)


class TestClient:
    def __init__(self, http_client: HTTPClientInterface):
        self.__client = http_client

    def get_post(self, post_id):
        try:
            response = self.__client.request("GET", f"/posts/{post_id}")

            return response
        except HTTPCommunicationError as exc:
            logging.error(f"{exc}")
            raise Exception(exc)

        except HTTPRequestError as exc:
            logging.error(f"{exc}")
            raise Exception(exc)

        except HTTPInvalidURL as exc:
            logging.error(f"{exc}")
            raise Exception(exc)


if __name__ == "__main__":
    http_client = HTTPClient(
        "https://jsonplaceholder.typicode.com",
        event_hooks={"response": [raise_on_4xx_5xx]},
    )

    test_client = TestClient(http_client)

    try:
        response = test_client.get_post(1)
        logging.info(response.json())

    except Exception:
        pass
