from dataclasses import replace
from types import SimpleNamespace

import pytest
from anthropic import AnthropicError
from pydantic import ValidationError

from src.errors import FailureCategory, JobAnalysisError
from src.job_analysis import MAX_FIELD_CHARS, analyse_job_page
from src.models import JobAnalysis, JobPageContent

ALL_TAGS = ("<metadata>", "<job_posting>", "<page_text>")


class FakeMessages:
    def __init__(
        self,
        response: SimpleNamespace | None = None,
        error: Exception | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.last_call: dict | None = None

    def parse(self, **kwargs) -> SimpleNamespace | None:
        self.last_call = kwargs
        if self.error:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, messages: FakeMessages) -> None:
        self.messages = messages


def _empty_analysis() -> JobAnalysis:
    return JobAnalysis(
        job_title=None,
        company=None,
        location=None,
        role_overview=None,
        responsibilities=[],
        requirements=[],
    )


def _client_returning(
    parsed_output: JobAnalysis | None,
    stop_reason: str = "end_turn",
) -> FakeClient:
    response = SimpleNamespace(parsed_output=parsed_output, stop_reason=stop_reason)
    return FakeClient(FakeMessages(response=response))


def _client_raising(error: Exception) -> FakeClient:
    return FakeClient(FakeMessages(error=error))


def _full_job_page() -> JobPageContent:
    return JobPageContent(
        metadata={"title": "Software Engineer"},
        job_posting={"@type": "JobPosting", "title": "Software Engineer"},
        page_text="We are hiring a Software Engineer.",
    )


def _sent_user_message(client: FakeClient) -> str:
    assert client.messages.last_call is not None
    return client.messages.last_call["messages"][0]["content"]


class TestAnalyseJobPage:
    # Message content

    def test_message_includes_all_three_sources(self):
        client = _client_returning(_empty_analysis())

        analyse_job_page(_full_job_page(), client)
        message = _sent_user_message(client)

        assert "<metadata>" in message
        assert "<job_posting>" in message
        assert "<page_text>" in message

    @pytest.mark.parametrize(
        ("field", "empty_value", "missing_tag"),
        [
            ("metadata", {}, "<metadata>"),
            ("job_posting", None, "<job_posting>"),
            ("page_text", "", "<page_text>"),
            ("page_text", "   ", "<page_text>"),
        ],
        ids=[
            "no-metadata",
            "no-job-posting",
            "empty-page-text",
            "whitespace-page-text",
        ],
    )
    def test_omits_empty_source(self, field, empty_value, missing_tag):
        client = _client_returning(_empty_analysis())
        job_page = replace(_full_job_page(), **{field: empty_value})

        analyse_job_page(job_page, client)
        message = _sent_user_message(client)

        assert missing_tag not in message
        for tag in ALL_TAGS:
            if tag != missing_tag:
                assert tag in message

    def test_drops_long_job_posting_fields_but_keeps_description(self):
        client = _client_returning(_empty_analysis())

        long_description = "A" * (MAX_FIELD_CHARS + 100)
        long_tracking_blob = "B" * (MAX_FIELD_CHARS + 100)

        job_page = JobPageContent(
            metadata={},
            job_posting={
                "@type": "JobPosting",
                "title": "Software Engineer",
                "description": long_description,
                "tracking_blob": long_tracking_blob,
            },
            page_text="Some job",
        )

        analyse_job_page(job_page, client)
        message = _sent_user_message(client)

        assert "Software Engineer" in message
        assert long_description in message
        assert "tracking_blob" not in message
        assert long_tracking_blob not in message

    # Result and errors

    def test_returns_the_analysis_from_the_model(self):
        analysis = _empty_analysis()
        client = _client_returning(analysis)

        result = analyse_job_page(_full_job_page(), client)

        assert result is analysis

    def test_anthropic_error_becomes_llm_error(self):
        sdk_error = AnthropicError("boom")
        client = _client_raising(sdk_error)

        with pytest.raises(JobAnalysisError) as exc_info:
            analyse_job_page(_full_job_page(), client)

        assert exc_info.value.category == FailureCategory.LLM_ERROR
        assert exc_info.value.__cause__ is sdk_error

    def test_validation_error_becomes_llm_parse_error(self):
        with pytest.raises(ValidationError) as validation_info:
            JobAnalysis.model_validate({})
        validation_error = validation_info.value
        client = _client_raising(validation_error)

        with pytest.raises(JobAnalysisError) as exc_info:
            analyse_job_page(_full_job_page(), client)

        assert exc_info.value.category == FailureCategory.LLM_PARSE_ERROR
        assert exc_info.value.__cause__ is validation_error

    def test_missing_parsed_output_becomes_llm_parse_error(self):
        client = _client_returning(parsed_output=None, stop_reason="max_tokens")

        with pytest.raises(JobAnalysisError) as exc_info:
            analyse_job_page(_full_job_page(), client)

        assert exc_info.value.category == FailureCategory.LLM_PARSE_ERROR
