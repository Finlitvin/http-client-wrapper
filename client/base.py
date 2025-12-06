from typing import Any
from abc import ABC
from abc import abstractmethod


class HTTPResponseInterface(ABC):
    """Абстрактный интерфейс для HTTP ответа"""

    @abstractmethod
    def __init__(
        self,
        status_code: int,
        content: str | bytes,
        headers: dict[str, str],
        json_data: Any | None = None,
    ):
        pass

    @abstractmethod
    def json(self) -> Any:
        pass

    @abstractmethod
    def text(self) -> str:
        pass


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
    ) -> HTTPResponseInterface:
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
            HTTPResponseInterface: Объект ответа
        """
        pass
