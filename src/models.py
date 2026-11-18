from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field


@dataclass
class JobPageContent:
    metadata: dict[str, str]
    job_posting: dict | None = None
    page_text: str = ""


class ExtractedFact(BaseModel):
    value: str
    quote: str = Field(description="Exact text copied from the source, not paraphrased")
    source: Literal["page_text", "job_posting", "metadata"]


class JobAnalysis(BaseModel):
    job_title: ExtractedFact | None
    company: ExtractedFact | None
    location: ExtractedFact | None
    responsibilities: list[str] = Field(
        description="Each responsibility copied exactly as written on the page"
    )
