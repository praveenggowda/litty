# Data Model

How Litty represents the candidate’s professional information.

> **Status:** Draft. Confirmed decisions are documented here. Open questions are tracked in [decisions.md](decisions.md).

## The Idea

The professional profile is the foundation of Litty. CVs are documents generated from it.

Evidence is not stored as one large block of text. It is broken into individually identifiable items so every factual claim in a generated CV can point to the evidence that supports it.

The profile contains structured professional information, while evidence provides the supporting facts.

## Profile

| Category | Examples |
| --- | --- |
| Identity | Name, contact details |
| Employment | Employers, job titles, dates, responsibilities |
| Projects | Work projects and personal projects |
| Skills | Languages, frameworks, tools |
| Achievements | Results and measurable outcomes |
| Qualifications | Degrees and certifications |
| STAR stories | Situation, Task, Action, Result |
| Incidents | Production incidents and resolutions |
| Preferences | Career goals and constraints |
| Documents | Master CV, CV template, cover letter template |

## Evidence Item

Every evidence item has:

| Field | Meaning |
| --- | --- |
| `id` | Unique and stable. Never reused. |
| `source` | Where it came from: `master_cv`, `profile` or `added_by_candidate` (a new fact confirmed during a run, through review or Add fact in chat). |
| `type` | Role, responsibility, achievement, skill, qualification, STAR story, incident, etc. |
| `employer` or `project` | What it belongs to, where applicable. |
| `period` | Start and end dates, where applicable. |
| `text` | The evidence itself, preserving the candidate’s original meaning. |
| `status` | `UNCONFIRMED`, `CANDIDATE_CONFIRMED`, `INDEPENDENTLY_VERIFIED` or `SUPERSEDED`. |

Each evidence item should represent one independently verifiable factual assertion.

Related evidence items can be grouped under an employment record, project or STAR story.

## Example

Made-up data:

```yaml
- id: acme-achievement-03
  source: master_cv
  type: achievement
  employer: Acme Ltd
  period: 2022-03 to 2025-06
  text: "Reduced API response time by 35% by introducing Redis caching"
  status: CANDIDATE_CONFIRMED

- id: star-sso-portal
  source: profile
  type: star_story
  employer: Acme Ltd
  period: 2024
  text: "Situation: ... Task: ... Action: ... Result: ..."
  status: CANDIDATE_CONFIRMED
```

## Rules for the Data

1. The master CV is never overwritten.
2. A tailored CV never becomes evidence by itself.
3. New facts added during a run are saved only after candidate confirmation, with source `added_by_candidate`, the date and the run they came from.
4. Every evidence item retains its original source and context.
5. Superseded evidence is retained for historical traceability.
6. Each workflow run references the exact profile version used.
7. Real profile data never goes into the repository. Only made-up examples are used.

## Open Questions

1. How are evidence items extracted from the master CV, and who confirms them?
2. How are conflicts between the master CV and the rest of the profile resolved?
3. How is a profile version identified and linked to a workflow run?
4. How are related evidence items grouped under employment, projects and STAR stories?
