from .base import HTTPResponseInterface


class HTTPRequestError(Exception):
    """Ошибка при"""

    def __init__(self, message: str, response: HTTPResponseInterface):
        self.message = message
        self.response = response


class HTTPCommunicationError(Exception):
    pass


class HTTPInvalidURL(Exception):
    pass


class HTTPCookieConflict(Exception):
    pass


class HTTPStreamError(Exception):
    pass
