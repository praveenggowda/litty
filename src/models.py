from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field

Source = Literal["page_text", "job_posting", "metadata"]


@dataclass
class JobPageContent:
    metadata: dict[str, str]
    job_posting: dict | None = None
    page_text: str = ""


class ExtractedFact(BaseModel):
    value: str
    quote: str = Field(description="Exact text copied from the source, not paraphrased")
    source: Source


class Requirement(BaseModel):
    text: str = Field(
        description="The requirement copied exactly as written on the page"
    )
    priority: Literal["REQUIRED", "DESIRABLE"]
    source: Source


class JobAnalysis(BaseModel):
    job_title: ExtractedFact | None
    company: ExtractedFact | None
    location: ExtractedFact | None
    role_overview: ExtractedFact | None = Field(
        description="The advert's own sentence or paragraph summarising the role, "
        "copied exactly"
    )
    responsibilities: list[str] = Field(
        description="Each responsibility copied exactly as written on the page"
    )
    requirements: list[Requirement] = Field(
        description="Every requirement the advert states, each one separately"
    )
