# Decisions

Every significant decision about Litty, with the reason behind it.

Each entry records the question, options, decision, why, and how we would know it was wrong.

## Status

* **Accepted:** Decided and agreed.
* **Proposed:** Default we follow until formally decided.
* **Open:** Not yet decided.

## Accepted

### 001. The job is the only input

* **Date:** 9 November 2026
* **Question:** What does the candidate provide for each run?
* **Options:** Upload everything for every job; or maintain a persistent profile and provide only the job.
* **Decision:** Each run takes one job, as a URL first or pasted text if the URL cannot be read. Everything else (master CV, evidence and templates) is saved in the profile beforehand.
* **Why:** The candidate should not upload the same documents for every job.
* **How we would know it was wrong:** Candidates regularly need to re-upload information or cannot keep their profile up to date.

### 002. One approval point

* **Date:** 9 November 2026
* **Question:** When does the candidate review Litty’s work?
* **Options:** Approve extracted requirements and recommendations separately; or have one approval checkpoint.
* **Decision:** The candidate approves, edits or rejects each recommendation at step 3. There is no separate approval step for extracted requirements.
* **Why:** One clear checkpoint keeps the flow simple. Extraction accuracy is measured through evaluation.
* **How we would know it was wrong:** Incorrect requirement extraction regularly leads to misleading recommendations that the candidate cannot easily identify.

### 003. Cover letter is offered after the CV

* **Date:** 9 November 2026
* **Question:** When should the candidate choose whether to generate a cover letter?
* **Options:** Ask upfront; or offer it after the CV is ready.
* **Decision:** Offer the cover letter once the CV is ready.
* **Why:** It keeps the initial input simple, and the letter must remain consistent with the approved CV.
* **How we would know it was wrong:** Candidates regularly want to provide cover-letter-specific information upfront.

### 004. Master CV is never overwritten

* **Date:** 10 November 2026
* **Question:** Should tailored CVs replace the master CV?
* **Options:** Update the master CV; or keep tailored documents separate.
* **Decision:** The master CV stays unchanged. A tailored CV is a separate document and never becomes evidence by itself.
* **Why:** Otherwise, tailored wording could quietly become accepted as truth for the next job.
* **How we would know it was wrong:** Maintaining separate documents creates significant duplication or prevents candidates from managing their professional profile effectively.

### 005. Evidence is the foundation of every claim

* **Date:** 11 November 2026
* **Question:** What supports factual claims in generated documents?
* **Options:** Use generated CVs as future context; or require claims to reference profile evidence.
* **Decision:** Every factual claim must trace back to identifiable evidence in the candidate’s profile or an explicitly approved new fact.
* **Why:** Litty must never treat previously generated wording as proof that something happened.
* **How we would know it was wrong:** Claims cannot be reliably traced to their original evidence.

### 006. Workflow order is controlled by code

* **Date:** 11 November 2026
* **Question:** Should an AI agent decide the execution order?
* **Options:** Autonomous agent; sequential workflow; graph workflow.
* **Decision:** Use a graph workflow. The steps and transitions are known, so code controls execution rather than an autonomous model.
* **Why:** Litty requires predictable execution, approval checkpoints, conditional paths and recovery.
* **How we would know it was wrong:** The workflow becomes difficult to maintain, extend or recover without introducing a framework or orchestration mechanism.

## Proposed

| Question | Default until decided |
| --- | --- |
| Master CV and profile disagree. Which is right? | Neither. Show the conflict and let the candidate decide. |
| Are new facts from review saved to the profile? | Only with consent, one fact at a time. |
| Can job titles change to match the job? | No. Titles are reproduced exactly. |
| Can the summary paragraph be rewritten? | Only through an approved change. |
| The template is not ATS friendly. Keep it or fix it? | Keep it and warn. |
| Are the speed targets right? | Use them as written. Measure one existing tool first as a baseline. |
| How big is one evidence item? | One independently verifiable factual assertion. |
| How are generated claims validated? | Separately from the component that generates them. |
| How is profile history maintained? | Each workflow run references an immutable profile version. |

## Open

* A change fails the trust check repeatedly. What happens?
* Which steps need AI, and which use deterministic code? Record one decision per step.
* How are evidence items extracted from the master CV, and who confirms them?

## Decision Template

```markdown
### 00N. Title

* **Date:**
* **Question:**
* **Options:**
* **Decision:**
* **Why:**
* **How we would know it was wrong:**
```
