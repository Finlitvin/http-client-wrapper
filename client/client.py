from typing import Any

from httpx import Client
from httpx import RequestError
from httpx import HTTPStatusError
from httpx import InvalidURL
from httpx import CookieConflict
from httpx import StreamError

from .base import HTTPClientInterface
from .models import HTTPResponse
from .errors import HTTPCommunicationError
from .errors import HTTPCookieConflict
from .errors import HTTPInvalidURL
from .errors import HTTPRequestError
from .errors import HTTPStreamError


class HTTPClient(HTTPClientInterface):
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: dict[str, str] | None = None,
        **kwargs,
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
            event_hooks=kwargs.pop("event_hooks", None) or self.__event_hooks,
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
                raise HTTPCommunicationError(str(exc))

            except HTTPStatusError as exc:
                raise HTTPRequestError(
                    message="Error",
                    response=HTTPResponse(
                        status_code=exc.response.status_code,
                        content=exc.response.content,
                        headers=dict(exc.response.headers),
                        json_data=exc.response.json()
                        if exc.response.headers.get("content-type")
                        == "application/json"
                        else None,
                    ),
                )

            except InvalidURL as exc:
                raise HTTPInvalidURL(exc)

            except CookieConflict as exc:
                raise HTTPCookieConflict(exc)

            except StreamError as exc:
                raise HTTPStreamError(exc)
