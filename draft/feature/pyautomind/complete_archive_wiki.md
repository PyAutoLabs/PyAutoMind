# Token-light wiki index over the complete/ archive

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Depends on

`feature/pyautomind/lifecycle_state_split.md` (Phase 1) — this needs
`complete/YYYY/MM/<slug>.md` per-task rich records to exist first. **Do not
issue this until Phase 1 nears shipping** (`feedback_no_bulk_issue_queues`).

## Problem

Once `complete/` holds hundreds of per-task records, an agent still can't look
up "have we hit this before / what did we learn about X" without reading many
files. We want the `autolens_assistant/wiki` model — a **curated markdown index
with `[[wiki-links]]`, not RAG / embeddings** ("RAG is dead") — so lookup is
token-light: read one index page, follow one or two links, done.

## Model to emulate — autolens_assistant/wiki

Study `autolens_assistant/wiki/` before designing:
- `wiki/README.md` — the "when to read / when to write which" table.
- `wiki/literature/index.md` — the token-light top-level nav: grouped
  `[[slug]]` links with one-line hooks, nothing more.
- `wiki/literature/AGENTS.md` — the page schema (concepts/entities/sources page
  types, `[[wiki-link]]` cross-refs) the assistant is told to follow.
- Its provenance split: `core/` generated from source, `literature/`
  hand-curated, `project/` append-only journal.

## Goal

Build `complete/index.md` + supporting index pages so an agent can navigate the
finished-work archive cheaply.

- **`complete/index.md`** — the entry point. Grouped `[[links]]` with one-line
  hooks (by theme: JAX/perf, release/build, samplers, lensing science, Mind/
  Brain infra, …), plus a "by date" pointer to the `YYYY/MM/` tree.
- **Per-record front-matter / tags** — each `complete/YYYY/MM/<slug>.md` gains a
  small tag block (theme, repos touched, key traps) so the index generator can
  bucket it. Cross-link related records with `[[slug]]` (analogous to how the
  auto-memory `MEMORY.md` + `[[name]]` links already work — reuse that idiom).
- **`complete/AGENTS.md`** — schema + "how an agent should search the archive"
  rules (read index → follow links → grep a dated bucket only if needed).
  Wire a pointer into the top-level AGENTS.md router so the archive is
  discoverable.

## Generation + drift

- A generator (`scripts/lifecycle.py` extended, or a sibling) that (re)builds
  `complete/index.md` from the per-record tags — deterministic, so it can run in
  `--check` mode and fail CI on drift (mirrors `spawn_drift` / the Phase-1
  lifecycle check). Hybrid allowed: generated skeleton + a hand-curated
  "highlights / hard-won traps" section that survives regeneration (like the
  assistant wiki's curated vs generated split).
- Decide: fully-generated index (cheap, mechanical) vs curated (richer, ages).
  Recommend **generated skeleton + curated highlights band**.

## Open questions to settle at plan time

- Granularity: one flat `index.md`, or `index.md` + per-theme sub-index pages
  (only if the archive is big enough to warrant it)?
- Does the memory faculty (`/memory`, PyAutoMemory) already cover "what did we
  learn" such that this index should *link out* to memories rather than
  duplicate them? Reconcile with `PyAutoBrain` Memory Faculty so the archive
  index and long-term memory don't fork.

## Original request (verbatim)

> As a follow up, I think we probbaly want to then build a wiki or indexing
> scheme for the complete folder so its really easy for an agent to look up old
> issues in a token light way, analogous to the wiki features used in
> autolens_assistant (e.g. RAG is dead). This is actually quite a large task so
> do some deep research on the plan.
