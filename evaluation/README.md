# Evaluation

How we prove Litty works.

The targets are defined in [PROBLEM_STATEMENT.md](../PROBLEM_STATEMENT.md#acceptance-criteria). This document explains how they are measured.

## Evaluation Set

Before tuning anything, build a set of at least 20 real job descriptions.

| Fit verdict | Minimum |
| --- | --- |
| `STRONG` | 5 |
| `MODERATE` | 5 |
| `WEAK` | 5 |
| `NOT_SUITABLE` | 3 |

Include the seven roles assessed on 26 October 2026 and every scenario in [test-cases.md](test-cases.md).

Label each job description by hand:

* Every requirement, marked `REQUIRED` or `DESIRABLE`.
* The match status of each requirement.
* The evidence IDs supporting each match.
* The overall fit verdict.

Freeze the labels before evaluation. A label changes only with a recorded reason, never to make Litty pass.

The labels reference real candidate evidence, so the real dataset stays out of the public repository. Only synthetic examples are committed.

## How Targets Are Measured

| Target | Measurement |
| --- | --- |
| Unsupported claims | Manually review every claim in every generated CV, cover letter and chat answer against its cited evidence. |
| Chat behaviour | Run the chat test cases and check each answer, refusal and suggestion card against its expected outcome. |
| Evidence traceability | Check by code that every factual claim has a valid evidence reference. |
| Exact facts and attribution | Check names, titles, dates, numbers and employer/project attribution against the profile. |
| Requirements recall | Correctly identified labelled requirements divided by all labelled requirements. |
| Requirements precision | Correctly identified labelled requirements divided by all requirements identified by Litty. |
| `REQUIRED` recall | Measure recall separately for `REQUIRED` requirements. |
| Match status | Compare Litty’s `MATCH`, `PARTIAL`, `MISSING` and `UNKNOWN` classifications with human labels. |
| Fit verdict | Compare Litty’s verdict with the labelled verdict. |
| Repeatability | Run every job three times and compare requirements, statuses, verdicts, suggestions and scores. |
| Alignment and ceiling | Recalculate both using deterministic code from the final document. |
| Speed | Record each workflow step for every job. Report p50 and p95. |

If an AI model judges whether a claim is supported, measure its results against human-reviewed labels too.

## Factual Accuracy

99.9% factual accuracy is the aspiration.

With zero errors across approximately 3,000 independently reviewed claims, the one-sided 95% upper confidence bound on the error rate is approximately 0.1%.

Release 1 will not have that many claims. Its release gate is therefore zero unsupported claims.

Every report must state:

* Number of claims reviewed.
* Number of errors found.
* Observed error rate.
* 95% upper confidence bound on the error rate.

The confidence bound is an estimate, not proof of universal accuracy.

## Reports

Both reports are generated from the final complete evaluation run.

### `evaluation-report.md`

Contains:

* Every metric compared with its target.
* Results by fit category.
* A table of mismatch categories.
* Failures found.
* Root causes.
* Changes made or deliberately not made.
* Factual accuracy results and confidence bound.

### `usage-report.md`

Contains:

* p50 and p95 time per workflow step.
* Number of model calls.
* Input and output tokens.
* Cost per job.
* Comparison with one existing CV tool using the same inputs and evaluation criteria.

## Reproducibility

One command must reproduce every number in both reports.

* **Recompute:** every number is recomputed from the saved outputs of the final run. This must match exactly.
* **Rerun:** calling the model again gives results close to the originals, but not identical, because model output can vary. How close is measured by the repeatability target.

The evaluation must use the frozen dataset, labels, prompts, configuration and recorded software versions.

Every evaluation run must record its inputs and versions so that results can be traced and compared.
