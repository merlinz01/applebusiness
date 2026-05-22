from pydantic import BaseModel

__all__ = [
    "ClientError",
    "ErrorResponseItem",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "TooManyRequestsError",
]


class ErrorResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/errorresponse"""

    errors: list[ErrorResponseItem]


class ErrorResponseItem(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/errorresponse/errors-data.dictionary"""

    code: str
    detail: str
    id: str | None = None
    source: dict | None = None
    status: str
    title: str
    links: dict | None = None
    meta: dict | None = None


class ClientError(Exception):
    def __init__(
        self,
        status: int,
        error_responses: list[ErrorResponseItem] | None,
        raw_response: dict | str | None = None,
    ):
        self.status = status
        self.error_responses = error_responses
        self.raw_response = raw_response

    def __str__(self):
        if self.error_responses is None:
            return f"API request failed with status {self.status} and invalid or missing error details: {self.raw_response!r}"
        details = "; ".join(
            f"{error.title} ({error.code}): {error.detail}"
            for error in self.error_responses
        )
        return f"API request failed with status {self.status}: {details}"

    def __repr__(self):
        return f"ClientError(status={self.status}, error_response={self.error_responses!r})"


class BadRequestError(ClientError):
    pass


class UnauthorizedError(ClientError):
    pass


class ForbiddenError(ClientError):
    pass


class NotFoundError(ClientError):
    pass


class TooManyRequestsError(ClientError):
    pass


_status_code_to_exception = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    429: TooManyRequestsError,
}
