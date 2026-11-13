from src.errors import FailureCategory

FRIENDLY_MESSAGES: dict[FailureCategory, str] = {
    FailureCategory.INVALID_URL: "That doesn't look like a valid job link. Please check the URL and try again.",
    FailureCategory.INACCESSIBLE: "I couldn't reach that job page. It may be down, private or blocking access. Please try again later.",
    FailureCategory.UNSUPPORTED_CONTENT: "That link doesn't point to a web page I can read. Please use the job posting's page URL.",
}

DEFAULT_FRIENDLY_MESSAGE = "Something went wrong while reading that job link."
