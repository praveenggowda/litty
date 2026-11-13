from urllib.parse import urlparse

import requests

from src.errors import FailureCategory, JobExtractionError


def extract_job_description(job_url: str) -> str:
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

    html = response.text
    return html


def _is_valid_url(url: str) -> bool:
    try:
        parsed_url = urlparse(url)

        return parsed_url.scheme in ("http", "https") and bool(parsed_url.hostname)
    except ValueError:
        return False
