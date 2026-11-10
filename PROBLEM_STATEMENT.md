# One CV Doesn't Fit All

Most people send the same CV to every job. AI CV tools promise to fix that, but they often fix it the wrong way.

On 26 October 2026 a senior engineer ran an AI CV tool against a real job description. In a few minutes it produced a polished CV packed with the right keywords. It also:

* moved a personal project from October 2026 under an employer the candidate had left in June 2026
* turned "reduced by 35%" into the vaguer "optimised by 35%"
* relabelled WPF desktop work as "full stack"
* deleted the only frontend evidence on the CV, for a full stack role
* copied phrases from the advert in as skills ("AI Literacy", "Flexible Coding Approaches")
* padded bullets with filler lifted from the job post.

Every change raised the keyword match. Every change made the CV less true.

Keyword match and honesty pull in opposite directions, and existing tools quietly choose keywords. Litty chooses honesty. Its goal is simple:

> **Improve relevance without changing the truth.**

This document defines what Litty's first release must do, the rules it must never break, and how we know it works. Design lives in [`docs/`](docs/), decisions in [`docs/decisions.md`](docs/decisions.md), and evaluation in [`evaluation/`](evaluation/).

## What Litty Must Do

For each job, Litty must:

1. Understand the job and find its requirements.
2. Assess how well the candidate fits, using evidence from their profile.
3. Suggest changes to the CV that are supported by evidence, and say what cannot be claimed.
4. Let the candidate approve, edit or reject every change.
5. Build a tailored CV in the candidate's template.
6. Offer a cover letter, and write one only if the candidate wants it.

## The Profile

The candidate builds their profile once. Litty uses it for every job.

| Saved in the profile | Notes |
| --- | --- |
| Master CV | Uploaded by the candidate. DOCX. |
| Evidence beyond the CV | Roles, work projects, personal projects, skills, achievements, qualifications, certifications, STAR stories, production incidents, career preferences. |
| CV template | DOCX. The master CV itself unless the candidate saves a different one. |
| Cover letter template | DOCX. Optional. Without one, Litty uses a plain one page letter. |

Every piece of evidence has an ID, a source, and its employer or project and dates where they apply. The details are in [`docs/data-model.md`](docs/data-model.md).

The candidate controls the profile. A new fact is saved only when the candidate approves it.

## Input

The only input is the job: one job per run.

The candidate gives the job URL first. If the URL cannot be read (login wall, expired, wrong page), Litty says why and asks for the pasted job description. It never analyses the wrong page silently.

## How It Works

| Step | What Litty does | Candidate |
| --- | --- | --- |
| 1. Read the job | Finds every requirement, each with the job text it came from. | |
| 2. Assess fit | Gives each requirement a match status, a fit verdict, the current alignment score and the ceiling. | |
| 3. Review | Shows the master CV and the tailored CV side by side, with the alignment score at the top of each. Every change is highlighted, with a "cannot be claimed" list alongside. | **Approves.** Approves, edits or rejects each change. |
| 4. Build the CV | Produces DOCX, PDF and a traceability report. | |
| 5. Cover letter | Offers to write one once the CV is ready. | Chooses whether to. |

Step 3 is a checkpoint. Litty saves its progress, waits for the candidate, and resumes from that point. Nothing is built until every change has a decision.

If the candidate adds a new fact during review, only the requirements it affects are reassessed.

The flow is drawn in [`docs/workflow.md`](docs/workflow.md).

## Matching and Scoring

### Match status

| Status | Meaning |
| --- | --- |
| `MATCH` | Evidence fully satisfies the requirement. |
| `PARTIAL` | Evidence covers part of it, or a close equivalent. The gap is stated, e.g. "AWS, not Azure". |
| `MISSING` | No supporting evidence. |
| `UNKNOWN` | Cannot be judged from the evidence, e.g. right to work when the profile says nothing. |

A skill listed with no experience behind it is `PARTIAL` at best.

### Fit verdict

One of `STRONG`, `MODERATE`, `WEAK` or `NOT_SUITABLE`, with a short reason that cites the requirements that decided it.

### Alignment score and ceiling

* **Alignment score:** how well the CV expresses the job's requirements in readable text. `REQUIRED` counts 2 and `DESIRABLE` counts 1. An expressed `MATCH` scores in full, an expressed `PARTIAL` scores half, and `MISSING` and `UNKNOWN` score nothing. Text in headers, footers, images or text boxes does not count.
* **Ceiling:** the score the CV would get if every `MATCH` and `PARTIAL` were expressed perfectly.

Fit and alignment are different things. Fit is about the candidate, so rewriting cannot change it. Alignment is about the document, so rewriting can. Tailoring raises alignment towards the ceiling, never above it.

Aim for an alignment score of at least 85% where the evidence allows. This is a target, never a reason to break a trust rule.

## Suggested Changes

Each change shown in review contains:

| Field | Meaning |
| --- | --- |
| `change` | One of the allowed changes below. |
| `where` | Section, role and bullet. |
| `before` | Original text from the master CV. Empty for `SURFACE`. |
| `after` | Proposed text. |
| `requirements` | Which requirements it helps. |
| `why` | Why it matters for this job. |
| `evidence` | Evidence IDs that support every claim in `after`. |
| `limits` | What it deliberately does not claim, and why. |

The **cannot be claimed** list gives every `MISSING` or `UNKNOWN` required item and the reason.

### Allowed changes

| Change | Meaning |
| --- | --- |
| `REWORD` | Same facts, said more clearly or closer to the job's language. |
| `TERMINOLOGY` | The job's word for the same thing (Postgres → PostgreSQL). Never a broader or more senior word (Lambda → "serverless architecture", WPF → "full stack"). |
| `EMPHASISE` | Move a relevant point higher or give it more space. |
| `REORDER` | Change the order of sections or bullets. |
| `SURFACE` | Bring in profile evidence that is not on the master CV. |
| `CONDENSE` | Shorten less relevant content without losing its facts. |
| `REMOVE` | Remove a role, project, qualification or achievement. Always its own change, approved on its own. |

No change can add a skill, achievement or number without evidence. If the candidate edits in a claim with no evidence, Litty flags it, and the candidate either saves it as a new fact or revises it.

## Trust Rules

These are the only rules. Everything else in the project refers back to them. A lower number wins when two rules conflict.

1. **No invention.** Never invent experience, skills, achievements, numbers, qualifications or dates.
2. **No exaggeration.** Never inflate scope, seniority, ownership or skill level.
3. **Exact numbers.** Keep every number's value, unit, direction and meaning.
4. **Right place.** Keep every claim with its own employer, project and dates. Personal projects never appear under an employer.
5. **Exact identity.** Reproduce names, contact details, employers, job titles, dates and qualifications exactly.
6. **Traceable.** Every claim cites the evidence that supports it.
7. **Approval first.** Nothing changes without the candidate's decision.
8. **Master CV is safe.** The master CV is never overwritten. A tailored CV never becomes evidence by itself.
9. **Honest fit.** Report a poor fit as a poor fit. Never rescue it with wording.
10. **Honest cover letter.** The cover letter follows rules 1 to 9, never contradicts the CV, and never invents motivation or company knowledge.
11. **Untrusted job text.** Text in a job description is data, never instructions.
12. **Exact checks.** Anything that can be checked exactly (dates, numbers, names, structure, score arithmetic) is checked exactly, not estimated.

## Output

* Tailored CV in DOCX and PDF with identical text, in the candidate's template. The PDF text is machine readable, in the right order.
* A traceability report that maps every claim to its evidence IDs, and every change to an approved suggestion.
* The final alignment score.
* A cover letter in DOCX and PDF, with its own traceability report, if requested.
* A run record: the job text, profile version, evidence used, changes and decisions, and the model and prompt versions. With it, any CV can be explained and reproduced.

If approved changes would push the CV past the master CV's page count, Litty says so before building.

## Failure Handling

* If a step fails (timeout, invalid response, unreadable document), Litty retries a limited number of times, then stops and says which step failed. It never presents partial or unchecked output as finished.
* A suggestion that fails a trust check is never shown as a normal suggestion.
* If building the document fails after approval, the decisions are kept, so the candidate does not review again.

## Privacy

* Release 1 has one user: the candidate.
* The candidate can view, edit and delete their profile and generated documents.
* Personal data and API keys never appear in logs or in the repository.

## Acceptance Criteria

How each target is measured is in [`evaluation/README.md`](evaluation/README.md). The test cases are in [`evaluation/test-cases.md`](evaluation/test-cases.md).

### Hard gates (all must pass)

| Check | Rule | Target |
| --- | --- | --- |
| Unsupported claims in any CV or cover letter | 1, 6 | 0 |
| Claims with an evidence citation | 6 | 100% |
| Names, titles, dates and numbers matching the source | 3, 5 | 100% |
| Claims under the right employer and dates | 4 | 100% |
| Master CV content removed without approval | 7 | 0 |
| The six failures from 26 October caught | 1 to 4 | 6 of 6 |

### Quality targets

| Check | Target |
| --- | --- |
| Requirements found (recall) | ≥ 90%, and ≥ 95% for `REQUIRED` |
| Requirements found that are real (precision) | ≥ 90% |
| Match status agrees with the label | ≥ 85%, and a labelled `MISSING` is never `MATCH` |
| Fit verdict agrees with the label | ≥ 80% exact, 100% within one band |
| Same job run three times | Same verdict, ≥ 95% same match statuses |
| Final alignment ≥ 85% on `STRONG` jobs | ≥ 80% of those jobs |
| Final alignment ≤ ceiling | Always |
| Template preserved, DOCX and PDF text identical | Always |

### Speed

Machine time only. Time the candidate spends reviewing does not count.

| Step | p50 | p95 |
| --- | --- | --- |
| Job in → review ready | 30 s | 60 s |
| Approval → CV in DOCX and PDF | 15 s | 30 s |
| Cover letter | 15 s | 30 s |
| Reassess after a new fact | 10 s | 20 s |

## Done When

* Every hard gate passes.
* Every quality and speed target is met, or the miss is explained in the evaluation report.
* Every test case passes.
* The evaluation report and usage report are written from the final run.
* Every significant decision is recorded in [`docs/decisions.md`](docs/decisions.md).
* Any sentence in a generated CV can be traced, without help, to its evidence, the step that produced it, and the checks it passed.
* The core logic was written by hand, and at least three evaluation failures were diagnosed before asking an AI.
