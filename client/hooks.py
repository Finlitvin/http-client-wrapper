from datetime import datetime
from httpx import Response
from httpx import Request


def log_request(request: Request) -> None:
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")


def log_response(response: Response) -> None:
    request = response.request
    print(
        f"Response event hook: {request.method} {request.url} - Status {response.status_code}"
    )


def add_timestamp(request: Request) -> None:
    request.headers["x-request-timestamp"] = datetime.now(tz=datetime.utc).isoformat()


def raise_on_4xx_5xx(response: Response) -> None:
    response.read()
    response.raise_for_status()
