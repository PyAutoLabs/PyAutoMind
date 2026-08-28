# Bundles phase 1 — `Themes:` keyword list and theme-keyed (cross-repo) auto-bundling

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-27

## Original request (verbatim)

> what is the premise of grouping?, they feel a bit random but I guess its hard
> to know how to group really. it feels like they are grouped on the source code
> library rather than the task and its scientific context, where the latter
> would generally be more cross repo
>
> i think we want 1 and 2?
>
> could even be multiple key words in bullet points to help more?

## Context

The Bundles section shipped 2026-08-27 (record
`complete/2026/08/dashboard-bundles.md`, PyAutoBrain#309). Its auto-bundler
groups on `Target:` only — a mechanical key (one worktree per repo), not a
topical one — so proposals read as "three things that live in autoarray", not
"three things about MGE". The useful grouping is scientific/topical and is
routinely cross-repo; the `start_bundle` contract already allows that (one
shared worktree per repo, parallel across repos).

## Scope

1. **`Themes:` header** — optional light-header key in the same list form as
   `Repos:`:

   ```
   Themes:
   - mge
   - jax-gradient
   - interferometer
   ```

   Small, controlled, human-editable vocabulary documented in `REFERENCE.md`
   (seed from the epic slugs and the obvious clusters: `mge`, `point-source`,
   `jax-compile`, `jax-gradient`, `ci-smoke`, `dashboard`, `assistants`,
   `cti`, …). Unknown keywords render a ⚠️ like unknown epic/bundle slugs so
   the list never rots into free-text tags. Intake assigns them at
   formalisation going forward (`_intake.py` formalise step).
2. **Renderer** (`PyAutoBrain/agents/conductors/intake/_intake.py`
   `auto_bundles`) — deterministic, keyed on themes, cross-repo allowed:
   - **first bullet = primary theme** = the grouping key; every prompt lands in
     at most one auto bundle (no duplicates across cards);
   - **remaining bullets = affinity**: within a primary-theme pool, packing
     prefers members with the highest keyword overlap (Jaccard over the whole
     list), so a large pool splits by what the work is about rather than by
     filename order; ties broken by priority, then `Target`, then path;
   - `Target` remains the fallback grouping key for prompts with no themes;
   - keep every existing exclusion, the size cap, min 2, the top-8 display and
     pinned/auto ordering. Card title = primary theme (+ the shared secondary
     keywords, if any); members show their repo.
3. **One-off backfill** — an Opus sweep reads each of the ~132 `draft/` prompts
   and writes a `Themes:` list where clear (1–3 keywords, primary first; leave
   absent when unclear); reviewable as a single diff, committed by the human.
   Never overwrite an existing value.
4. Tests for primary-theme grouping, affinity-driven packing, cross-repo
   members, fallback-to-Target, unknown-keyword warning, and that the existing
   Target-only fixture still renders identically when no prompt carries themes.

Deferred to phase 2 (`bundle_nightly_claude_pass.md`): assigning theme lists to
new drafts automatically and Claude-proposed cross-theme bundles — the
affinity keywords are exactly the signal that pass uses.
