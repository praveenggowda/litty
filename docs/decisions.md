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
* **Decision:** Each run takes one job. Everything else (master CV, evidence and templates) is saved in the profile beforehand. How the job is given is set out in 007.
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

### 007. Job input: URL or pasted text

* **Date:** 12 November 2026
* **Question:** How does the candidate give Litty the job, and what happens when it cannot be read?
* **Options:** URL only; URL first with pasted text only as a fallback; URL and pasted text together; exactly one of URL or pasted text.
* **Decision:**
    1. A run starts with exactly one of a job URL or pasted job text.
    2. If a URL is given, Litty tries to extract the job description.
    3. The candidate can replace extracted text with pasted text.
    4. A complete description names a specific role, gives enough context to understand it, and has at least one identifiable responsibility or requirement. Skills, technology stack, experience and desirable skills are extracted when present but are not mandatory.
    5. A page that does not identify one specific job (careers homepage, several vacancies) is its own outcome: Litty asks which role the candidate wants.
    6. Pasted text goes through the same completeness and untrusted input checks.
    7. PDF job descriptions are out of Release 1 scope.
    8. The run record keeps the final accepted job text and its source.
* **Why:** One source per run avoids contradictions. Some jobs arrive without a URL (recruiter emails, messages). Extraction can be wrong even when it succeeds, so the candidate needs a way to correct it.
* **How we would know it was wrong:** Candidates often have to paste text after a successful extraction, or valid job descriptions are regularly rejected as incomplete.

### 008. Agent-first UI

* **Date:** 12 November 2026
* **Question:** How does the candidate use Litty?
* **Options:** A traditional app with forms and pages; a blank chatbot; an agent-first experience with structured workflow states.
* **Decision:**
    1. Two primary areas: **Litty Agent**, the conversation where a job is run, and **Profile**, where professional information, the master CV and templates are managed. Documents and history are reachable, but their navigation is not decided yet.
    2. The agent is not a blank chatbot. It shows structured states, clear progress, review screens and approval buttons.
    3. The backend stays a controlled workflow (006). Agent-first UI does not mean autonomous execution.
    4. One conversation is one job run. A run can have several attempts.
    5. Five stages are shown to the candidate, with the eight internal workflow steps underneath. Prepare suggested changes belongs under Review changes.
    6. Litty continues automatically from reading the job to assessing fit, but only when the job text passes validation. There is no extra approval checkpoint (002).
    7. The extracted job description is shown, and the candidate can view it or replace it with pasted text. Replacing it before review invalidates the previous assessment and starts a new attempt. The old attempt is kept.
    8. Requirements are shown with neutral indicators and `REQUIRED` or `DESIRABLE` labels before fit is assessed. After assessment, `MATCH`, `PARTIAL`, `MISSING` and `UNKNOWN` are shown distinctly, never by colour alone.
    9. Chat answers questions about the current job, profile and assessment only. All trust rules apply to chat answers. Unrelated requests are declined politely.
    10. Workflow actions always use explicit buttons. A new fact mentioned in chat is saved only through Add fact with candidate confirmation. A change requested in chat becomes a suggestion card that needs normal approval.
    11. Chat behaviour is part of the evaluation and regression tests.
    12. Release 1 is single user: no My Account. No Settings until there are settings to manage.
    13. The product tagline is "An AI agent that helps your real experience shine."
* **Why:** The conversation makes one job run feel like a guided story, while buttons and workflow states keep every decision explicit and every action controlled.
* **How we would know it was wrong:** Candidates try to do most things through chat and find the buttons frustrating, or chat answers start drifting from the evidence.

### 009. Reading job pages: generic handling and one fallback

* **Date:** 16 November 2026
* **Question:** Job pages vary widely. How does Litty handle them without adding code for each site?
* **Options:** Site-specific extraction rules for each careers site or ATS; generic extraction with one fallback when no usable advert is found.
* **Decision:**
    1. Extraction is deterministic. Analysis uses AI.
    2. Each page is read into three separate sources: page metadata, the JSON-LD `JobPosting`, and visible page text. They are kept separate because they can be incomplete, outdated or contradictory.
    3. Only generic transformations are applied: HTML is converted to clean text, long or duplicated values are limited, and visible page text is the primary source when sources disagree. Conflicts are reported, never resolved silently.
    4. When no usable advert is found, Litty asks the candidate to paste the job text (007). This single fallback covers pages that need JavaScript, pages behind a login or bot protection, adverts inside an iframe, and pages we have not seen before. Completeness validation (007, point 4) decides this, not detection of each page type.
    5. Non-HTML responses such as PDFs are rejected as unsupported content and the candidate is asked to paste the text.
    6. A new kind of page becomes an evaluation case, not a code change, unless it reveals a gap that affects a whole category of pages.
    7. Deferred: site-specific data hidden in ATS scripts (for example salary or experience level), detecting closed adverts, pages with several vacancies (007, point 5), and adverts not in English.
* **Why:** Real pages showed visible text holding the whole advert, visible text holding none of it (the advert only in JSON-LD), JSON-LD with outdated dates, JSON-LD with values in the wrong fields, and key facts only in hidden ATS data. Rules per site would grow without end. One fallback keeps Litty predictable and honest about what it could not read.
* **How we would know it was wrong:** Candidates often have to paste text for common careers sites, or valid adverts are regularly reported as incomplete.

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
* The candidate replaces the job text during or after review. What happens? (Before review is decided in 008.)
* Litty judges a job description incomplete and the candidate disagrees. Can they continue anyway, with a warning?
* After "which role?", is that role's text taken from the same page, or must the candidate give its own URL or text?
* A job page loads normally but says the job is closed. Is it treated as inaccessible (expired)?
* What happens with a job description that is not in English?
* How is "enough context to understand it" tested? It needs labelled examples that pass and fail.

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
