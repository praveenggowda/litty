from src.errors import FailureCategory

DEFAULT_FRIENDLY_MESSAGE = "Something went wrong while reading that job link."

FRIENDLY_MESSAGES: dict[FailureCategory, str] = {
    FailureCategory.INVALID_URL: "That doesn't look like a valid job link. Please check the URL and try again.",
    FailureCategory.INACCESSIBLE: "I couldn't reach that job page. It may be down, private or blocking access. Please try again later.",
    FailureCategory.UNSUPPORTED_CONTENT: "That link doesn't point to a web page I can read. Please use the job posting's page URL.",
    FailureCategory.EMPTY_CONTENT: "I couldn't find any job advert text on that page. Please paste the advert text instead.",
    FailureCategory.LLM_ERROR: "The analysis service is unavailable right now. Please try again in a moment.",
    FailureCategory.LLM_PARSE_ERROR: "I read the job page but couldn't analyse the advert. Please try again in a moment.",
    FailureCategory.ANALYSIS_FAILED: "I read the job page but couldn't analyse the advert. Please try again in a moment.",
}


def friendly_message_for(category: FailureCategory) -> str:
    return FRIENDLY_MESSAGES.get(category, DEFAULT_FRIENDLY_MESSAGE)
