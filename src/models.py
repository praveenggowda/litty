from dataclasses import dataclass


@dataclass
class JobPageContent:
    metadata: dict[str, str]
    page_text: str
    job_posting: dict | None = None
