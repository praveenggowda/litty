import argparse
import json
import logging
import sys
from dataclasses import asdict

from anthropic import Anthropic

from src.errors import LittyError
from src.job_analysis import analyse_job_page
from src.job_extraction import fetch_job_page, parse_job_page
from src.user_messages import DEFAULT_FRIENDLY_MESSAGE, friendly_message_for

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    output = run_job_analysis_pipeline(args.job_url, no_llm=args.no_llm)
    print(output)


def run_job_analysis_pipeline(
    job_url: str,
    *,
    no_llm: bool = False,
    client: Anthropic | None = None,
) -> str:
    html = fetch_job_page(job_url)
    job_page = parse_job_page(html)

    logger.info(
        "Extracted %d characters, %d metadata fields, job posting found: %s from %s",
        len(job_page.page_text),
        len(job_page.metadata),
        job_page.job_posting is not None,
        job_url,
    )

    if no_llm:
        return json.dumps(asdict(job_page), indent=2, ensure_ascii=False)

    job_analysis = analyse_job_page(job_page, client or Anthropic())

    requirements = job_analysis.requirements
    required = sum(1 for r in requirements if r.priority == "REQUIRED")
    logger.info(
        "Analysed job: title found: %s, company found: %s, location found: %s, "
        "overview found: %s, %d responsibilities, "
        "%d requirements (%d required, %d desirable)",
        job_analysis.job_title is not None,
        job_analysis.company is not None,
        job_analysis.location is not None,
        job_analysis.role_overview is not None,
        len(job_analysis.responsibilities),
        len(requirements),
        required,
        len(requirements) - required,
    )

    return job_analysis.model_dump_json(indent=2)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hey, I'm Litty! 💡 Drop a job link and let's get your CV lit."
    )
    parser.add_argument(
        "job_url", help="URL of the job posting you want Litty to analyse"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Stop after reading the page and show what was extracted, without calling the model",
    )

    return parser.parse_args(argv)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        main()
    except LittyError as error:
        logger.error(
            "Litty failed [%s]: %s (cause: %r)",
            error.category,
            error,
            error.__cause__,
        )
        print(friendly_message_for(error.category), file=sys.stderr)
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected error")
        print(DEFAULT_FRIENDLY_MESSAGE, file=sys.stderr)
        sys.exit(1)
