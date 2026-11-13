from enum import StrEnum


class FailureCategory(StrEnum):
    INVALID_URL = "INVALID_URL"
    INACCESSIBLE = "INACCESSIBLE"
    UNSUPPORTED_CONTENT = "UNSUPPORTED_CONTENT"


class JobExtractionError(Exception):
    def __init__(
        self,
        category: FailureCategory,
        message: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.status_code = status_code
