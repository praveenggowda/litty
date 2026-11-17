from pathlib import Path

from anthropic import Anthropic

from src.job_analysis import analyse_job_page
from src.job_extraction import parse_job_page

html = Path("tests/fixtures/real/ashby_checkout_e88f77c7.html").read_text()
analysis = analyse_job_page(parse_job_page(html), Anthropic())
print(analysis.model_dump_json(indent=2))
