import json
from typing import Any

from .base import HTTPResponseInterface


class HTTPResponse(HTTPResponseInterface):
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
        return str(self.status_code)
