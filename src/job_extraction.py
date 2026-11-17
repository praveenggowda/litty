import json
from html import unescape
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.errors import FailureCategory, JobExtractionError
from src.models import JobPageContent

REQUEST_TIMEOUT_SECONDS = 10
USER_AGENT = "Litty/1.0"

NON_CONTENT_TAGS = [
    "script",
    "style",
    "noscript",
    "svg",
    "canvas",
    "template",
    "meta",
    "link",
    "head",
]

META_TAGS = {
    "description": {"name": "description"},
    "og:title": {"property": "og:title"},
    "og:description": {"property": "og:description"},
}


def fetch_job_page(job_url: str) -> str:
    job_url = _validate_url(job_url)
    return _download_html(job_url)


def parse_job_page(html: str) -> JobPageContent:
    soup = BeautifulSoup(html, "html.parser")

    metadata = _extract_metadata(soup)
    job_posting = _extract_job_posting(soup)
    page_text = _extract_page_text(soup)  # must run last: it removes tags from the soup

    return JobPageContent(
        metadata=metadata,
        job_posting=job_posting,
        page_text=page_text,
    )


def _validate_url(job_url: str | None) -> str:
    job_url = (job_url or "").strip()

    if not job_url:
        raise JobExtractionError(FailureCategory.INVALID_URL, "Job URL is missing")
    if not _is_valid_url(job_url):
        raise JobExtractionError(FailureCategory.INVALID_URL, f"Invalid URL: {job_url}")

    return job_url


def _is_valid_url(url: str) -> bool:
    try:
        parsed_url = urlparse(url)

        return parsed_url.scheme in ("http", "https") and bool(parsed_url.hostname)
    except ValueError:
        return False


def _download_html(job_url: str) -> str:
    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(
            job_url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.exceptions.Timeout as error:
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            f"Request timed out after {REQUEST_TIMEOUT_SECONDS} seconds",
        ) from error
    except requests.exceptions.SSLError as error:
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            "SSL handshake failed",
        ) from error
    except requests.exceptions.ConnectionError as error:
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            "Connection failed",
        ) from error
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            f"HTTP {status_code}",
            status_code,
        ) from error
    except requests.exceptions.TooManyRedirects as error:
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            "Too many redirects",
        ) from error
    except requests.exceptions.RequestException as error:
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            f"Request failed: {type(error).__name__}",
        ) from error

    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type.lower():
        raise JobExtractionError(
            FailureCategory.UNSUPPORTED_CONTENT,
            f"Expected text/html, got {content_type or 'no content type'}",
        )

    return response.text


def _extract_metadata(soup: BeautifulSoup) -> dict[str, str]:
    metadata = {}

    if soup.title and soup.title.string:
        metadata["title"] = soup.title.string.strip()

    for key, attrs in META_TAGS.items():
        tag = soup.find("meta", attrs=attrs)
        content = tag.get("content") if tag else None
        if isinstance(content, str) and content.strip():
            metadata[key] = content.strip()

    return metadata


def _extract_job_posting(soup: BeautifulSoup) -> dict | None:
    for tag in soup.find_all("script", type="application/ld+json"):
        for item in _parse_json_ld(tag.get_text()):
            if _is_job_posting(item):
                return _clean_job_posting(item)

    return None


def _parse_json_ld(raw_json: str) -> list[dict]:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return []

    if isinstance(data, dict) and "@graph" in data:
        data = data["@graph"]

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def _is_job_posting(item: dict) -> bool:
    schema_type = item.get("@type")

    if isinstance(schema_type, str):
        schema_types = [schema_type]
    elif isinstance(schema_type, list):
        schema_types = schema_type
    else:
        return False

    return any(
        type_name.rstrip("/").split("/")[-1] == "JobPosting"
        for type_name in schema_types
        if isinstance(type_name, str)
    )


def _clean_job_posting(job_posting: dict) -> dict:
    description = job_posting.get("description")

    if isinstance(description, str):
        job_posting["description"] = _html_to_text(description)

    return job_posting


def _html_to_text(markup: str) -> str:
    text = unescape(markup)
    text = BeautifulSoup(text, "html.parser").get_text(separator="\n")
    return _tidy_text(text)


def _extract_page_text(soup: BeautifulSoup) -> str:
    for tag in soup.find_all(NON_CONTENT_TAGS):
        tag.decompose()

    return _tidy_text(soup.get_text(separator="\n"))


def _tidy_text(text: str) -> str:
    lines = text.splitlines()
    tidy_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(tidy_lines)
