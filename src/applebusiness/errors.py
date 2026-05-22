from pydantic import BaseModel

__all__ = ["ClientError", "ErrorResponse", "ErrorResponseError"]


class ErrorResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/errorresponse"""

    errors: list[ErrorResponseError]


class ErrorResponseError(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/errorresponse/error-data.dictionary"""

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
        error_response: ErrorResponse | None,
        raw_response: dict | str | None = None,
    ):
        self.status = status
        self.error_response = error_response
        self.raw_response = raw_response

    def __str__(self):
        if self.error_response is None:
            return f"API request failed with status {self.status} and invalid or missing error details: {self.raw_response!r}"
        details = "; ".join(
            f"{error.title} ({error.code}): {error.detail}"
            for error in self.error_response.errors
        )
        return f"API request failed with status {self.status}: {details}"

    def __repr__(self):
        return (
            f"ClientError(status={self.status}, error_response={self.error_response!r})"
        )
