import pytest
import requests.exceptions

from src.errors import FailureCategory, JobExtractionError
from src.job_extraction import fetch_job_page, parse_job_page

JOB_URL = "https://example.com"


class FakeResponse:
    def __init__(
        self, text: str = "", content_type: str = "text/html", status_code: int = 200
    ) -> None:
        self.text = text
        self.headers = {"Content-Type": content_type}
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(response=self)


def _real_response(body: bytes, content_type: str) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response._content = body
    response.headers["Content-Type"] = content_type
    response.encoding = requests.utils.get_encoding_from_headers(response.headers)
    return response


def _get_returning(
    monkeypatch: pytest.MonkeyPatch, response: FakeResponse | requests.Response
) -> None:
    monkeypatch.setattr(
        "src.job_extraction.requests.get", lambda *args, **kwargs: response
    )


def _get_raising(monkeypatch: pytest.MonkeyPatch, error: Exception) -> None:
    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr("src.job_extraction.requests.get", fail)


class TestFetchJobPage:
    # Errors

    @pytest.mark.parametrize(
        "job_url",
        [
            "",
            "        ",
            None,
        ],
        ids=["empty", "whitespace", "none"],
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
        ids=["no_scheme", "ftp", "file", "javascript", "no_host", "malformed"],
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
        _get_raising(monkeypatch, error)

        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(JOB_URL)

        assert exc_info.value.category == FailureCategory.INACCESSIBLE
        assert str(exc_info.value) == expected_message
        assert exc_info.value.__cause__ is error

    @pytest.mark.parametrize(
        "content_type",
        ["application/pdf", "application/json", ""],
        ids=["pdf", "json", "missing"],
    )
    def test_rejects_unsupported_content_type(self, monkeypatch, content_type):
        _get_returning(monkeypatch, FakeResponse(content_type=content_type))

        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(JOB_URL)

        assert exc_info.value.category == FailureCategory.UNSUPPORTED_CONTENT
        assert (
            str(exc_info.value)
            == f"Expected text/html, got {content_type or 'no content type'}"
        )

    @pytest.mark.parametrize("status_code", [403, 404, 500])
    def test_maps_http_error_to_inaccessible(self, monkeypatch, status_code):
        _get_returning(monkeypatch, FakeResponse(status_code=status_code))

        with pytest.raises(JobExtractionError) as exc_info:
            fetch_job_page(JOB_URL)

        assert exc_info.value.category == FailureCategory.INACCESSIBLE
        assert exc_info.value.status_code == status_code
        assert str(exc_info.value) == f"HTTP {status_code}"

    # Success

    def test_returns_html(self, monkeypatch):
        _get_returning(
            monkeypatch,
            FakeResponse(text="<p>Hi</p>", content_type="text/html; charset=utf-8"),
        )

        assert fetch_job_page(f"  {JOB_URL}  ") == "<p>Hi</p>"

    @pytest.mark.parametrize(
        ("html", "content_type", "encoding"),
        [
            ("<p>It’s £90k</p>", "text/html", "utf-8"),
            ("<p>It’s £90k</p>", "text/html; charset=utf-8", "utf-8"),
            ("<p>Café £90k</p>", "text/html; charset=iso-8859-1", "iso-8859-1"),
        ],
        ids=["no-charset", "declared-utf8", "declared-latin1"],
    )
    def test_decodes_html_using_the_right_encoding(
        self, monkeypatch, html, content_type, encoding
    ):
        _get_returning(monkeypatch, _real_response(html.encode(encoding), content_type))

        assert fetch_job_page(JOB_URL) == html


class TestParseJobPage:
    # Input

    @pytest.mark.parametrize("html", ["", "     "], ids=["empty", "whitespace"])
    def test_rejects_blank_html(self, html):
        with pytest.raises(JobExtractionError) as exc_info:
            parse_job_page(html)

        assert exc_info.value.category == FailureCategory.EMPTY_CONTENT

    # Metadata

    def test_extracts_metadata(self):
        html = """
            <html>
              <head>
                <title>  Senior .NET Engineer - Acme  </title>
                <meta name="description" content="Join our platform team.">
                <meta property="og:title" content="Senior .NET Engineer">
                <meta property="og:description" content="Build reliable services.">
              </head>
              <body><p>Job details</p></body>
            </html>
            """

        job_page = parse_job_page(html)

        assert job_page.metadata == {
            "title": "Senior .NET Engineer - Acme",
            "description": "Join our platform team.",
            "og:title": "Senior .NET Engineer",
            "og:description": "Build reliable services.",
        }

    def test_skips_missing_or_empty_metadata(self):
        html = """
            <html>
              <head>
                <meta name="description" content="">
                <meta property="og:title" content="   ">
              </head>
              <body><p>Job details</p></body>
            </html>
            """

        job_page = parse_job_page(html)

        assert job_page.metadata == {}

    # Job posting

    @pytest.mark.parametrize(
        "json_ld",
        [
            '{"@type": "JobPosting", "title": "Senior .NET Engineer"}',
            '{"@graph": [{"@type": "WebPage"}, {"@type": "JobPosting", "title": "Senior .NET Engineer"}]}',
            '{"@type": ["JobPosting"], "title": "Senior .NET Engineer"}',
            '{"@type": "https://schema.org/JobPosting", "title": "Senior .NET Engineer"}',
        ],
        ids=["direct", "graph", "type_list", "type_url"],
    )
    def test_extracts_job_posting(self, json_ld):
        html = f'<script type="application/ld+json">{json_ld}</script>'

        job_page = parse_job_page(html)

        assert job_page.job_posting["title"] == "Senior .NET Engineer"

    @pytest.mark.parametrize(
        "json_ld",
        [
            "{bad json",
            '{"@type": "Organization", "name": "Acme"}',
        ],
        ids=["bad_json", "non_job_posting"],
    )
    def test_ignores_invalid_or_non_job_posting_json_ld(self, json_ld):
        html = (
            f'<script type="application/ld+json">{json_ld}</script><p>Job details</p>'
        )

        job_page = parse_job_page(html)

        assert job_page.job_posting is None

    # Page text

    def test_removes_non_content_tags_from_page_text(self):
        html = """
        <html>
          <head><title>Senior .NET Engineer</title></head>
          <body>
            <script>trackVisitor();</script>
            <style>.job { color: red; }</style>
            <noscript>Please enable JavaScript</noscript>
            <p>Build reliable services.</p>
          </body>
        </html>
        """

        job_page = parse_job_page(html)

        assert job_page.page_text == "Build reliable services."

    def test_tidies_whitespace_in_page_text(self):
        html = """
        <body>
            <h1>   Senior .NET Engineer   </h1>


            <p>
                Build reliable services.
            </p>
        </body>
        """

        job_page = parse_job_page(html)

        assert job_page.page_text == "Senior .NET Engineer\nBuild reliable services."

    def test_keeps_header_and_footer_text(self):
        html = """
        <body>
          <header>Location: London, on site</header>
          <p>Build reliable services.</p>
          <footer>Note: you must already hold DV clearance.</footer>
        </body>
        """

        job_page = parse_job_page(html)

        assert "Location: London, on site" in job_page.page_text
        assert "you must already hold DV clearance" in job_page.page_text
