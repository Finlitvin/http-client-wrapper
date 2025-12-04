import json
import logging
from typing import Any
from abc import ABC
from abc import abstractmethod

from httpx import Client
from httpx import RequestError
from httpx import HTTPStatusError
from httpx import InvalidURL
from httpx import CookieConflict
from httpx import StreamError

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s]: %(message)s"
)

class HTTPResponse:
    """Класс для HTTP-ответа"""

    def __init__(
        self,
        status_code: int,
        content: str | bytes,
        headers: dict[str, str],
        json_data: Any | None = None
    ):
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self._json = json_data
    
    def json(self) -> Any:
        if self._json is not None:
            return self._json
        
        if isinstance(self.content, bytes):
            content_str = self.content.decode('utf-8')
        else:
            content_str = self.content
        self._json = json.loads(content_str)

        return self._json
    
    def text(self) -> str:
        if isinstance(self.content, bytes):
            return self.content.decode('utf-8')
        return self.content


class HTTPClientInterface(ABC):
    """Абстрактный интерфейс для HTTP клиента"""

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        timeout: int | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs
    ) -> HTTPResponse:
        """Выполняет HTTP запрос
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
            url: URL для запроса
            headers: Заголовки запроса
            params: Query параметры
            data: Тело запроса (form-encoded или bytes/str)
            json_data: JSON данные для тела запроса
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
    ):
        self.__base_url = base_url
        self.__timeout = timeout
        self.__headers = headers

    def request(
        self,
        method: str,
        url: str,
        timeout: int | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs
    ) -> HTTPResponse:
        with Client(
            base_url=self.__base_url,
            headers=headers or self.__headers,
            timeout=timeout or self.__timeout,
        ) as client:
            try:
                response = client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    **kwargs
                )

                return HTTPResponse(
                    status_code=response.status_code,
                    content=response.content,
                    headers=dict(response.headers),
                    json_data=response.json() if response.headers.get('content-type') == 'application/json' else None
                )

            except RequestError as exc:
                raise Exception(exc)
            
            except HTTPStatusError as exc:
                raise Exception(exc)
            
            except InvalidURL as exc:
                raise Exception(exc)
            
            except CookieConflict as exc:
                raise Exception(exc)
            
            except StreamError as exc:
                raise Exception(exc)



if __name__ == "__main__":
    http_client = HttpClient("https://jsonplaceholder.typicode.com")

    try:
        response = http_client.request(
            "GET",
            "/posts/1"
        )
        logging.info(response.text())
    except Exception as exc:
        logging.error(f"{exc}")