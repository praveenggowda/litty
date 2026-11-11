# Architecture

How Litty is built.

> **Status:** Not designed yet. Architecture design begins after the [data model](data-model.md) and [workflow](workflow.md) are agreed.

## Principles

1. Build the simplest system that satisfies Litty’s [trust requirements](../PROBLEM_STATEMENT.md#trust-rules).
2. Use AI where language understanding and reasoning are needed. Use deterministic code wherever possible.
3. The component that generates a claim must not approve it. Validation must happen independently.
4. Design and implement the workflow in plain code first. Adopt a workflow framework only when a demonstrated need justifies it.
5. Introduce retrieval, additional agents or external tools only when evaluation results demonstrate a need.
6. Keep business rules independent of the AI model and orchestration framework.

## Questions This Document Will Answer

* What are the main components, and what is each responsible for?
* How does data flow between components?
* Where are profiles, evidence, workflow runs and generated documents stored?
* How are trust requirements enforced? Which checks are deterministic, and which require AI-assisted judgement?
* How are model calls managed, retried and recorded?
* How does the system handle failures, interruptions and workflow recovery?
* How are security, privacy and access controls enforced?
