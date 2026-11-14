import argparse
import logging
import sys

from src.errors import JobExtractionError
from src.job_extraction import fetch_job_page, parse_job_page
from src.user_messages import DEFAULT_FRIENDLY_MESSAGE, FRIENDLY_MESSAGES

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hey, I'm Litty! 🔥 Drop a job link and let's get your CV lit."
    )

    parser.add_argument(
        "job_url", help="URL of the job posting you want Litty to analyse"
    )
    args = parser.parse_args()

    html = fetch_job_page(args.job_url)
    job_page = parse_job_page(html)
    logger.info(
        "Extracted %d characters, %d metadata fields, job posting found: %s from %s",
        len(job_page.page_text),
        len(job_page.metadata),
        job_page.job_posting is not None,
        args.job_url,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        main()
    except JobExtractionError as error:
        logger.error(
            "Job extraction failed [%s]: %s (cause: %r)",
            error.category,
            error,
            error.__cause__,
        )
        print(
            FRIENDLY_MESSAGES.get(error.category, DEFAULT_FRIENDLY_MESSAGE),
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)
