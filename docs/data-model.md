# Data Model

How Litty represents the candidate's professional information.

> **Status:** draft. What is written here is decided. Open points are listed at the end and tracked in [decisions.md](decisions.md).

## The idea

The profile is the foundation. CVs are documents generated from it.

Evidence is not one big block of text. It is broken into small items, each with its own ID, so every claim in a CV can point to exactly the item that supports it.

## Profile

| Category | Examples |
| --- | --- |
| Identity | Name, contact details |
| Employment | Employers, job titles, dates, responsibilities |
| Projects | Work projects and personal projects |
| Skills | Languages, frameworks, tools |
| Achievements | Results and numbers, e.g. "reduced response time by 35%" |
| Qualifications | Degrees and certifications |
| STAR stories | Situation, Task, Action, Result |
| Incidents | Production incidents and how they were resolved |
| Preferences | Career goals and constraints |
| Documents | Master CV, CV template, cover letter template |

## Evidence item

Every evidence item has:

| Field | Meaning |
| --- | --- |
| `id` | Unique and stable. Never reused. |
| `source` | Where it came from: `master_cv`, `profile`, or `added_in_review`. |
| `type` | Role, bullet, achievement, skill, qualification, STAR story, incident, and so on. |
| `employer` or `project` | What it belongs to, where it applies. |
| `period` | Start and end dates, where they apply. |
| `text` | The evidence itself, exactly as the candidate gave it. |

Example, with made up data:

```yaml
- id: acme-bullet-03
  source: master_cv
  type: achievement
  employer: Acme Ltd
  period: 2022-03 to 2025-06
  text: "Reduced API response time by 35% by introducing Redis caching"

- id: star-sso-portal
  source: profile
  type: star_story
  employer: Acme Ltd
  period: 2024
  text: "Situation: ... Task: ... Action: ... Result: ..."
```

Because each item carries its employer and period, rules 3 and 4 in the [problem statement](../PROBLEM_STATEMENT.md#trust-rules) can be checked by plain code.

## Rules for the data

* The master CV is never overwritten.
* A tailored CV never becomes evidence by itself.
* A fact added during review is saved only when the candidate approves it, with `source: added_in_review` and the date.
* Real profile data never goes into the repository. Only made up examples do.

## Open points

* How big is one evidence item: a whole job, one bullet, or one sentence?
* How are evidence items extracted from the master CV, and who confirms them?
* What happens when the master CV and the rest of the profile disagree?
* How is a profile version identified, so a run record can point to it?
