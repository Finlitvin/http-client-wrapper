from datetime import datetime
from httpx import Response
from httpx import Request


def log_request(request: Request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")


def log_response(response: Response):
    request = response.request
    print(
        f"Response event hook: {request.method} {request.url} - Status {response.status_code}"
    )


def add_timestamp(request: Request):
    request.headers["x-request-timestamp"] = datetime.now(tz=datetime.utc).isoformat()


def raise_on_4xx_5xx(response: Response):
    response.raise_for_status()
