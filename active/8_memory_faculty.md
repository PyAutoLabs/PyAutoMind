# Memory faculty — one read-only consult for PyAutoMemory + autolens_assistant

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

## Why

Feature, bug and intake conductors each describe "consult PyAutoMemory" in
prose, and WORKFLOW.md tells every skill to do it ad-hoc — the same
duplication vitals was created to remove for Heart. A memory faculty makes the
consult uniform and machine-invokable, and it is the prerequisite for the
science→task pipeline (`9_scholar_intake.md`): scholar mode needs a
disciplined read surface, not bulk-loading wikis.

## What

Add `@PyAutoBrain/agents/faculties/memory/`:

1. Given a topic/question (e.g. "prior work on delaunay pixelization
   regularization"), return a **cited digest**: relevant PyAutoMemory sub-wiki
   pages, autolens_assistant skill/wiki pages, prior Mind `complete.md`
   entries — pointers plus a short synthesis, never wholesale page dumps.
2. Follow the faculty shape: read-only, judges and stops, sensor organs are
   Memory and the assistant workspaces. Do not couple to Memory's internal
   layout — resolve sub-wikis at query time (the standing rule).
3. Rewire the consumers: Feature/Bug conductors and the WORKFLOW.md "consult
   Memory before substantial planning" step point at the faculty instead of
   restating the procedure.

## Boundaries

- **Privacy seam**: PyAutoMemory is personal. The faculty's digests flow into
  Mind prompts and issues on private/organism repos — fine — but anything that
  later lands in public user-facing repos (workspace tutorials, docs) must not
  carry PyAutoMemory references. State this in the faculty's AGENTS.md.
- Operational history stays Mind's (complete.md, issues); the faculty may read
  it but the boundary prose in ORGANISM.md is unchanged.
- Not a RAG build-out — no indexes, no embeddings, no new infra. Grep + the
  wikis' own structure, same as a careful human session.

Blocked-by: 1_autonomy_contract.md only (independent of 2–7; can run in
parallel with them).
