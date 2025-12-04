import json
from typing import Any
from abc import ABC, abstractmethod


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
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | bytes | str | None = None,
        json_data: Any | None = None,
        timeout: float = 30.0,
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



    

