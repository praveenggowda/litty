# Litty — Build Plan

## Phases

### Phase 1: Agent Core (terminal)
- Personal profile config
- freehire job search tool
- Claude scoring and verdict output
- Terminal interface

### Phase 2: CV and Cover Letter
- CV upload and parsing
- RAG: embed profile documents into a vector store
- Semantic matching against job descriptions
- Tailored CV and cover letter generation in your voice

### Phase 3: Evaluation
- Verdict accuracy tracking
- Hallucination rate monitoring
- Score drift detection

### Phase 4: Monitoring
- LLM call tracing with Langfuse
- Token cost and latency per run

### Phase 5: Web UI
- Simple web interface
- Multi-user support

## Tech stack

- Python
- Anthropic SDK (Claude as the agent brain with tool use)
- freehire API (job search)
- pgvector or Chroma (vector store for RAG in Phase 2)
- FastAPI (web UI in Phase 5)
- Langfuse (monitoring in Phase 4)

## Project structure

```
litty/
  profile_example.py   # template showing the profile structure
  profile_private.py   # your personal profile (gitignored, never committed)
  tools.py             # freehire search tool definition
  agent.py             # main agent loop with Claude and tool use
  main.py              # entry point
  requirements.txt
```

## Status

Phase 1 in progress.
