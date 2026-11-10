# Architecture

How Litty is built.

> **Status:** not designed yet. Design starts after the [data model](data-model.md) and the [workflow](workflow.md) are settled.

## Principles

* Build the simplest system that satisfies the [trust rules](../PROBLEM_STATEMENT.md#trust-rules).
* Use AI only where a step needs language understanding. Use plain code for everything that can be checked exactly.
* The step that writes a claim never approves it. Claims are checked separately.
* Write the workflow as plain code first. Adopt a framework only when the code shows a need for one.
* Adopt retrieval, extra agents or new tools only when an evaluation result justifies it.

## Questions this document will answer

* What are the main components, and what is each one responsible for?
* How does data flow between them?
* Where are the profile, runs and generated documents stored?
* How are trust rules enforced: which checks are exact, and which need judgement?
* How are model calls made, retried and recorded?
