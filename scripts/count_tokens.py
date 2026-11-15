import json
import re
from difflib import SequenceMatcher
from pathlib import Path

import anthropic

from src.job_extraction import parse_job_page

client = anthropic.Anthropic()

html = Path("tests/fixtures/real/shieldpay_senior_net_engineer.html").read_text()
job_page = parse_job_page(html)


def _count_tokens(text: str) -> int:
    return client.messages.count_tokens(
        model="claude-haiku-5-5",
        messages=[{"role": "user", "content": text}],
    ).input_tokens


def _compare_texts(json_ld: str, page_text: str) -> None:
    def normalise(text: str) -> str:
        return " ".join(text.lower().split())

    json_ld = normalise(json_ld)
    page_text = normalise(page_text)

    similarity = SequenceMatcher(None, json_ld, page_text).ratio()
    print(f"Similarity: {similarity:.2%}")

    json_ld_sentences = set(re.split(r"(?<=[.!?])\s+", json_ld))

    page_sentences = set(re.split(r"(?<=[.!?])\s+", page_text))

    print("\nOnly in JSON-LD:")

    for sentence in sorted(json_ld_sentences - page_sentences):
        print(f"- {sentence}")

    print("\nOnly in page text:")

    for sentence in sorted(page_sentences - json_ld_sentences):
        print(f"- {sentence}")


_compare_texts(job_page.job_posting["description"], job_page.page_text)

print("Metadata:", _count_tokens(json.dumps(job_page.metadata)))
print("JSON-LD:", _count_tokens(json.dumps(job_page.job_posting)))
print("Page text:", _count_tokens(job_page.page_text))

combined_content = {
    "metadata": job_page.metadata,
    "job_posting": job_page.job_posting,
    "page_text": job_page.page_text,
}

print("Combined:", _count_tokens(json.dumps(combined_content)))
