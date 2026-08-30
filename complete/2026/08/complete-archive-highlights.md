## complete-archive-highlights (the Highlights band of complete/index.md curated — 30 lesson hooks under five themes)
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/368
- completed: 2026-08-29
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/371
- prompt: draft/feature/pyautomind/complete_archive_wiki.md (bundle `mind-workflow`)
- summary: The token-light archive index shipped with lifecycle-state-split (2026-07); what this prompt still owed was the editorial pass. The `<!-- CURATED -->` band of `complete/index.md` now carries 30 records under JAX/numerics/perf · release/build/CI drift · samplers/inference · lensing science · Mind/Brain infrastructure, each with a one-line hook that states the reusable lesson, not the task. `complete/AGENTS.md` describes the link form the generator actually emits (markdown links, not `[[wiki-links]]`) and what earns a Highlights line. One test proves a curated band survives `lifecycle.py index` regeneration byte-for-byte.
- validation: `lifecycle.py index --check` OK; `lifecycle.py check` OK; PyAutoMind suite 282 passed (new `tests/test_lifecycle_index.py`, control-tested — a trailing blank line in the band fails it).

## Traps and findings
- `index --check` is a byte-for-byte round trip of the whole file including the band, so the band must be exactly what `_render_index` re-emits — whitespace included. Regenerate and commit the generated file, never hand-tune the surroundings.
- `complete/AGENTS.md` promised `[[slug]]` links while `lifecycle.py` emits `[slug](path)`; nothing resolves `[[...]]` under `complete/`. Doc fixed to the machinery, not the other way round.
- Not done, worth a prompt if wanted: the Brain memory faculty (`agents/faculties/memory/_memory.py`) greps all 1223 records and never reads `index.md` first — the band is a cheaper entry point it does not yet consult. Per-record tag blocks and per-theme sub-index pages were dropped as scope; 1223 records is not yet the size that warrants them.
- Seeds the curation dropped and why: `04/skip-degenerate-radial-caustic` (four metadata lines, no body), `04/history-rewrite-guard` (rollout mechanics; the rule lives in every AGENTS.md), the two firewall allowlist records (narrow one-off decisions), `08/overflow-flood-refs-smc-cell` (status dump; lesson carried by the clipper/step-scaling records).

## Original prompt

# Token-light wiki index over the complete/ archive

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-07-13 (backfilled from git)
Issued: 2026-08-29

## Depends on

`feature/pyautomind/lifecycle_state_split.md` (Phase 1) — this needs
`complete/YYYY/MM/<slug>.md` per-task rich records to exist first. **Do not
issue this until Phase 1 nears shipping** (`feedback_no_bulk_issue_queues`).

## 2026-08-09 — SUBSTANTIALLY SHIPPED; only the curation is left

Checked by the draft/ sweep. Phase 1 shipped
([[lifecycle-state-split]], monolithic `complete.md` retired 2026-07-16, issue #81),
so the dependency above is long satisfied — **and most of what this prompt asks for
shipped with it.**

`complete/index.md` exists on `main` and already is the token-light index this
prompt specifies:

- **952 records** linked, grouped by dated bucket.
- Its own header states the lookup protocol this prompt describes almost verbatim
  — *"read this, follow one or two links, and only then grep a dated bucket."*
- **Generated**, by `scripts/lifecycle.py index`, with `index --check` gating
  staleness in CI — so it cannot rot.
- It has the curated band: `<!-- CURATED:START -->` … `<!-- CURATED:END -->`,
  documented as surviving regeneration.
- `complete/AGENTS.md` § "How to look something up (token-light — RAG is dead)"
  carries the same doctrine this prompt opens with.

**What is actually left is the curation, not the machinery.** The Highlights band
is empty — it reads `_(curate hard-won records here — survives regeneration.)_`.
So the remaining work is the editorial pass: pick the hard-won records worth
surfacing and write the one-line hooks, in the `autolens_assistant/wiki` style
this prompt says to study.

Re-scope before issuing: drop the "build the index" legs, keep the "curate it"
legs, and re-read § "Model to emulate" against what `lifecycle.py index` already
generates rather than against a blank slate. `Difficulty:` medium is now
generous.

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
