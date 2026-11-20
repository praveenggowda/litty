from enum import StrEnum


class FailureCategory(StrEnum):
    # Fetch & HTML validation
    INVALID_URL = "INVALID_URL"
    INACCESSIBLE = "INACCESSIBLE"
    UNSUPPORTED_CONTENT = "UNSUPPORTED_CONTENT"

    # Pre-analysis content check
    EMPTY_CONTENT = "EMPTY_CONTENT"

    # LLM execution & structured output
    LLM_ERROR = "LLM_ERROR"
    LLM_PARSE_ERROR = "LLM_PARSE_ERROR"


class LittyError(Exception):
    def __init__(
        self,
        category: FailureCategory,
        message: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.status_code = status_code


class JobExtractionError(LittyError):
    """Raised when a job page can't be fetched or parsed."""


class JobAnalysisError(LittyError):
    """Raised when the advert can't be analysed into a JobAnalysis."""
