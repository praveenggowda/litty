from src.profile_private import PROFILE
from src.tools import search_jobs


def main() -> None:
    jobs = search_jobs(
        query=PROFILE["target_roles"][0],
        country="GB",
        seniority="senior",
        skills=",".join(PROFILE["primary_stack"]),
        visa=False,
        limit=10
    )

    print(jobs)


if __name__ == "__main__":
    main()
