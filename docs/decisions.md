# Decisions

Every significant decision about Litty, with the reason behind it.

Each entry records the question, the options, the choice, why, and how we would know it was wrong.

Status is one of:

* **Accepted:** decided.
* **Proposed:** a default we follow until it is decided.

## Accepted

### 001. The job is the only input

* **Date:** 9 November 2026
* **Decision:** each run takes one job, as a URL first or as pasted text if the URL cannot be read. Everything else (master CV, evidence, templates) is saved in the profile beforehand.
* **Why:** the candidate should not upload the same documents for every job.

### 002. One approval point

* **Date:** 9 November 2026
* **Decision:** the candidate approves, edits or rejects each change at step 3. There is no approval step for the extracted requirements.
* **Why:** one clear checkpoint keeps the flow fast. Mistakes in reading the job are measured in evaluation, not pushed onto the candidate.

### 003. Cover letter is offered after the CV

* **Date:** 9 November 2026
* **Decision:** the cover letter is offered once the CV is ready, not chosen up front.
* **Why:** it keeps the input to one thing, and the letter must stay consistent with the approved CV.

### 004. Master CV is never overwritten

* **Date:** 10 November 2026
* **Decision:** the master CV stays unchanged. A tailored CV is a separate document and never becomes evidence by itself.
* **Why:** otherwise tailored wording could quietly turn into "truth" for the next job.

## Proposed

| Question | Default until decided |
| --- | --- |
| Master CV and profile disagree. Which is right? | Neither. Show the conflict and let the candidate decide. |
| Are new facts from review saved to the profile? | Only with consent, one fact at a time. |
| Can job titles change to match the job? | No. Titles are reproduced exactly. |
| Can the summary paragraph be rewritten? | Only through an approved change. |
| The template is not ATS friendly. Keep it or fix it? | Keep it and warn. |
| Are the speed targets right? | Use them as written. Measure one existing tool first as a baseline. |
| Is Litty a workflow or an agent? | A graph workflow: the steps are known, so code decides the order, not a model. |
| How big is one evidence item? | Not yet decided. |
| A change fails the trust check repeatedly. What happens? | Not yet decided. |
| Which steps need AI? | Not yet decided. Record one entry per step. |

## Template

```markdown
### 00N. Title

* **Date:**
* **Question:**
* **Options:**
* **Decision:**
* **Why:**
* **How we would know it was wrong:**
```
