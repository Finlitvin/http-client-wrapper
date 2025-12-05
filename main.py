import json
import logging
from typing import Any
from typing import Callable
from abc import ABC
from abc import abstractmethod

from httpx import Client
from httpx import Response
from httpx import RequestError
from httpx import HTTPStatusError
from httpx import InvalidURL
from httpx import CookieConflict
from httpx import StreamError

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s][%(levelname)s]: %(message)s"
)


class HTTPRequestError(Exception):
    pass


class HTTPCommunicationError(Exception):
    pass


class HTTPInvalidURL(Exception):
    pass


class HTTPCookieConflict(Exception):
    pass


class HTTPStreamError(Exception):
    pass


class HTTPResponse:
    """Класс для HTTP-ответа"""

    def __init__(
        self,
        status_code: int,
        content: str | bytes,
        headers: dict[str, str],
        json_data: Any | None = None,
    ):
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self._json = json_data

    def json(self) -> Any:
        if self._json is not None:
            return self._json

        if isinstance(self.content, bytes):
            content_str = self.content.decode("utf-8")
        else:
            content_str = self.content
        self._json = json.loads(content_str)

        return self._json

    def text(self) -> str:
        if isinstance(self.content, bytes):
            return self.content.decode("utf-8")
        return self.content

    def __str__(self) -> str:
        return f"HTTPResponse(status_code={self.status_code})"


class HTTPClientInterface(ABC):
    """Абстрактный интерфейс для HTTP клиента"""

    @abstractmethod
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: dict[str, str] | None = None,
    ):
        pass

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        timeout: int | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> HTTPResponse:
        """Выполняет HTTP запрос

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
            url: URL для запроса
            headers: Заголовки запроса
            params: Query параметры
            json: JSON данные для тела запроса
            timeout: Таймаут запроса в секундах
            **kwargs: Дополнительные параметры для конкретной реализации

        Returns:
            HTTPResponse: Объект ответа
        """
        pass


class HttpClient(HTTPClientInterface):
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: dict[str, str] | None = None,
        **kwargs
    ):
        self.__base_url = base_url
        self.__timeout = timeout
        self.__headers = headers
        self.__event_hooks = kwargs.pop("event_hooks", None)

    def request(
        self,
        method: str,
        url: str,
        timeout: int | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> HTTPResponse:
        with Client(
            base_url=self.__base_url,
            headers=headers or self.__headers,
            timeout=timeout or self.__timeout,
            event_hooks=kwargs.pop("event_hooks", None) or self.__event_hooks
        ) as client:
            try:
                response = client.request(
                    method=method, url=url, params=params, json=json, **kwargs
                )

                return HTTPResponse(
                    status_code=response.status_code,
                    content=response.content,
                    headers=dict(response.headers),
                    json_data=response.json()
                    if response.headers.get("content-type") == "application/json"
                    else None,
                )

            except RequestError as exc:
                raise HTTPCommunicationError(exc)

            except HTTPStatusError as exc:
                raise HTTPRequestError(exc)

            except InvalidURL as exc:
                raise HTTPInvalidURL(exc)

            except CookieConflict as exc:
                raise HTTPCookieConflict(exc)

            except StreamError as exc:
                raise HTTPStreamError(exc)


class TestClient:
    def __init__(self, http_client: HTTPClientInterface):
        self.__client = http_client

    def get_post(self, post_id):
        try:
            response = self.__client.request("GET", f"/post/{post_id}")

            return response
        except HTTPCommunicationError as exc:
            logging.error(f"1 {exc}")
            raise Exception(exc)
        
        except HTTPRequestError as exc:
            logging.error(f"2 {exc}")
            raise Exception(exc)

        except HTTPInvalidURL as exc:
            logging.error(f"3 {exc}")
            raise Exception(exc)


def raise_on_4xx_5xx(response: Response):
    response.raise_for_status()


if __name__ == "__main__":
    http_client = HttpClient(
        "https://jsonplaceholder.typicode.com",
        event_hooks={"response": [raise_on_4xx_5xx]}
    )

    test_client = TestClient(http_client)

    try:
        response = test_client.get_post(1)
        logging.info(response.json())

    except Exception:
        pass
