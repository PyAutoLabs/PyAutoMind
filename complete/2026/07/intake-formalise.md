## intake-formalise
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/32 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/33 (merged)
- notes: |
    Added `intake formalise` — retroactive conception for the backlog (once
    codenamed repair; renamed because raw prompts are intended word-vomit
    awaiting conception, not defects). Selects census records with missing
    header fields; Type/Target from the taxonomy folder (authoritative),
    Difficulty/Autonomy/Priority via the shared sizing faculty; inserts only
    the missing lines, prose byte-verbatim (CRLF files read/written
    newline-preserving — caught an LF-normalisation bug on 5 files during the
    live run and fixed before commit). Re-home suggestions reported (36),
    never acted on. Ran on the live Mind: 83/83 formalised, hygiene 77 → 0,
    dashboard regenerated with all columns populated (sizing says 50
    too-large / 18 large — honest signal those prompts need splitting at
    start_dev). Heart YELLOW on unrelated science-stack items, acknowledged.
