import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.errors import FailureCategory, JobExtractionError
from src.models import JobPageContent

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
    if job_url:
        job_url = job_url.strip()

    if not job_url:
        raise JobExtractionError(FailureCategory.INVALID_URL, "Job URL is missing")
    if not _is_valid_url(job_url):
        raise JobExtractionError(FailureCategory.INVALID_URL, f"Invalid URL: {job_url}")

    headers = {"User-Agent": "Litty/1.0"}

    try:
        response = requests.get(job_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout as error:
        raise JobExtractionError(
            FailureCategory.INACCESSIBLE,
            "Request timed out after 10 seconds",
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


def parse_job_page(html: str) -> JobPageContent:
    soup = BeautifulSoup(html, "html.parser")

    metadata = _extract_metadata(soup)
    job_posting = _extract_job_posting(soup)

    for tag in soup.find_all(NON_CONTENT_TAGS):
        tag.decompose()

    page_text = _tidy_text(soup.get_text(separator="\n"))

    return JobPageContent(
        metadata=metadata,
        page_text=page_text,
        job_posting=job_posting,
    )


def _is_valid_url(url: str) -> bool:
    try:
        parsed_url = urlparse(url)

        return parsed_url.scheme in ("http", "https") and bool(parsed_url.hostname)
    except ValueError:
        return False


def _extract_metadata(soup: BeautifulSoup) -> dict[str, str]:
    metadata = {}

    if soup.title and soup.title.string:
        metadata["title"] = soup.title.string.strip()

    for key, attrs in META_TAGS.items():
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            metadata[key] = tag["content"].strip()

    return metadata


def _extract_job_posting(soup: BeautifulSoup) -> dict | None:
    tags = soup.find_all("script", type="application/ld+json")

    for tag in tags:
        try:
            data = json.loads(tag.get_text())
        except json.JSONDecodeError:
            continue

        if isinstance(data, dict) and "@graph" in data:
            data = data["@graph"]

        if isinstance(data, dict):
            candidates = [data]
        elif isinstance(data, list):
            candidates = data
        else:
            continue

        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue

            job_type = candidate.get("@type")

            if isinstance(job_type, str):
                job_types = [job_type]

            elif isinstance(job_type, list):
                job_types = job_type

            else:
                continue

            # "https://schema.org/JobPosting" -> "JobPosting"
            if any(
                type_name.rstrip("/").split("/")[-1] == "JobPosting"
                for type_name in job_types
                if isinstance(type_name, str)
            ):
                return candidate

    return None


def _tidy_text(text: str) -> str:
    lines = text.splitlines()
    tidy_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(tidy_lines)
