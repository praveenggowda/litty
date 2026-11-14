import pytest
import requests.exceptions

from src.errors import FailureCategory, JobExtractionError
from src.job_extraction import fetch_job_page

JOB_URL = "https://example.com"


class FakeResponse:
    def __init__(self, text="", content_type="text/html", status_code=200):
        self.text = text
        self.headers = {"Content-Type": content_type}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(response=self)


class TestFetchJobPage:
    @pytest.mark.parametrize(
        "job_url",
        [
            "",
            "        ",
            None,
        ],
    )
    def test_rejects_missing_url(self, job_url):
        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(job_url)

        assert exc_info.value.category == FailureCategory.INVALID_URL
        assert str(exc_info.value) == "Job URL is missing"

    @pytest.mark.parametrize(
        "job_url",
        [
            "not-a-url",
            "ftp://example.com",
            "file:///etc/passwd",
            "javascript:alert(1)",
            "https://",
            "http://[invalid",
        ],
    )
    def test_rejects_invalid_url(self, job_url):
        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(job_url)

        assert exc_info.value.category == FailureCategory.INVALID_URL
        assert str(exc_info.value) == f"Invalid URL: {job_url}"

    @pytest.mark.parametrize(
        "error, expected_message",
        [
            (requests.exceptions.Timeout(), "Request timed out after 10 seconds"),
            (requests.exceptions.SSLError(), "SSL handshake failed"),
            (requests.exceptions.ConnectionError(), "Connection failed"),
            (requests.exceptions.TooManyRedirects(), "Too many redirects"),
            (
                requests.exceptions.RequestException(),
                "Request failed: RequestException",
            ),
        ],
        ids=["timeout", "ssl", "connection", "redirects", "generic"],
    )
    def test_maps_request_failure_to_inaccessible(
        self, monkeypatch, error, expected_message
    ):
        def fake_get(*args, **kwargs):
            raise error

        monkeypatch.setattr("src.job_extraction.requests.get", fake_get)

        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(JOB_URL)

        assert exc_info.value.category == FailureCategory.INACCESSIBLE
        assert str(exc_info.value) == expected_message
        assert exc_info.value.__cause__ is error

    @pytest.mark.parametrize(
        "content_type", ["application/pdf", "application/json", ""]
    )
    def test_rejects_unsupported_content_type(self, monkeypatch, content_type):
        def fake_get(*args, **kwargs):
            return FakeResponse(content_type=content_type)

        monkeypatch.setattr("src.job_extraction.requests.get", fake_get)

        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(JOB_URL)

        assert exc_info.value.category == FailureCategory.UNSUPPORTED_CONTENT
        assert (
            str(exc_info.value)
            == f"Expected text/html, got {content_type or 'no content type'}"
        )

    @pytest.mark.parametrize("status_code", [403, 404, 500])
    def test_maps_http_error_to_inaccessible(self, monkeypatch, status_code):
        def fake_get(*args, **kwargs):
            return FakeResponse(status_code=status_code)

        monkeypatch.setattr("src.job_extraction.requests.get", fake_get)

        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(JOB_URL)

        assert exc_info.value.category == FailureCategory.INACCESSIBLE
        assert exc_info.value.status_code == status_code
        assert str(exc_info.value) == f"HTTP {status_code}"

    def test_returns_html(self, monkeypatch):
        def fake_get(*args, **kwargs):
            return FakeResponse(
                text="<p>Hi</p>", content_type="text/html; charset=utf-8"
            )

        monkeypatch.setattr("src.job_extraction.requests.get", fake_get)

        assert fetch_job_page(f"  {JOB_URL}  ") == "<p>Hi</p>"


# TODO: TestParseJobPage
# - empty or blank html -> empty metadata, empty page_text, job_posting None
# - title, description and og: tags extracted; missing ones absent
# - JSON-LD JobPosting found directly, inside @graph, and with @type as list/URL
# - malformed JSON-LD or only non-JobPosting types -> job_posting None
# - script and style text not in page_text
# - blank lines and indentation tidied in page_text
# - header and footer text kept (hidden blockers, e.g. "must hold DV clearance")
