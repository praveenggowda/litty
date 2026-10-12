import subprocess


def search_jobs(query, country, seniority, skills, visa, limit):
    cmd = ["freehire", "search", query,
           "--country", country,
           "--seniority", seniority,
           "--skills", skills,
           "--limit", str(limit)
           ]

    if visa:
        cmd.append("--visa")

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
