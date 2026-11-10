# Evaluation

How we prove Litty works. The targets are in the [problem statement](../PROBLEM_STATEMENT.md#acceptance-criteria). This document explains how they are measured.

## Evaluation set

Before tuning anything, build a set of at least 20 real job descriptions:

| Fit | At least |
| --- | --- |
| `STRONG` | 5 |
| `MODERATE` | 5 |
| `WEAK` | 5 |
| `NOT_SUITABLE` | 3 |

Include the seven roles assessed on 26 October 2026, and every case in [test-cases.md](test-cases.md).

Label each job by hand:

* every requirement, marked `REQUIRED` or `DESIRABLE`
* the match status of each requirement, with the evidence IDs behind it
* the fit verdict.

Then freeze the labels. A label changes only with a logged reason, never to make Litty pass.

The labels point to real profile evidence, so the real dataset stays out of the public repository. Only made up examples are committed.

## How each target is measured

| Target | How |
| --- | --- |
| Unsupported claims | Every claim in every generated CV and cover letter is reviewed by hand against its cited evidence. |
| Citations, exact facts, right employer | Checked by code against the profile. |
| Recall and precision | Requirements found by Litty compared with the labelled requirements. |
| Match status and fit verdict | Compared with the labels. |
| Same job run three times | Run each job three times and compare. |
| Alignment and ceiling | Computed by code from the final document. |
| Speed | Time each step on every job. Report p50 and p95. |

If an AI is used to judge whether claims are supported, that judge is measured against human labels too.

## About 99.9%

99.9% factual accuracy is the aspiration. Proving it takes about 3,000 reviewed claims with zero errors. Release 1 will not have that many, so the gate is zero unsupported claims. Report how many claims were reviewed and the 95% upper bound on the error rate.

## Reports

Both are written from the final full run.

| Report | Contents |
| --- | --- |
| `evaluation_report.md` | Every metric against its target, a table of mismatch categories, failures found, root causes, and what was changed or deliberately not changed. |
| `usage_report.md` | p50 and p95 time per step, model calls, input and output tokens, cost per job, and a comparison with one existing CV tool. |

One command must reproduce every number in both reports.
