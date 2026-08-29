# Bundles phase 2 — nightly Claude pass: theme-fill new drafts + proposed bundles

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
- dashboard
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: parked
Filed: 2026-08-27
Unblocked: phase 1 shipped 2026-08-28 — complete/2026/08/bundle-themes.md (PyAutoBrain#312, PyAutoMind#366)

## Premise

**Rules render, Claude labels.** Phase 1 makes the auto-bundler deterministic
over a `Themes:` keyword list. This phase adds the judgment rules cannot supply,
without making the render non-reproducible or burning tokens on the page itself.

## Scope

1. **Nightly workflow** in `PyAutoMind/.github/workflows/` (precedent:
   `morning_status.yml`, which already runs Claude on a cron) that:
   - reads every `draft/` prompt **without** a `Theme:` and writes one where
     clear, using the `REFERENCE.md` vocabulary — **write only when absent,
     never overwrite a human value** (the one softening of the "nothing
     rewrites prompt files" rule; a bot commit, reviewable in the log);
   - proposes bundles that **cross themes** when several prompts read as one
     piece of work, written to `PyAutoMind/bundles_proposed.md` (same schema as
     `bundles.md` plus `- rationale:` in Claude's words), replaced wholesale
     each night — a proposal, never a record. Pinning = copying an entry into
     `bundles.md`.
   - commits with the bot identity and dispatches `pages_dashboard.yml`
     explicitly (GITHUB_TOKEN pushes trigger nothing).
2. **Renderer** merges `bundles_proposed.md` below pinned and above the
   deterministic auto proposals, with an origin tag (`pinned` / `claude` /
   `auto`); members of a Claude proposal leave the auto pool like pinned ones.
   Deterministic auto bundles remain the floor when the pass fails or is
   skipped.
3. Guard rails: skip silently when nothing is un-themed and the backlog hash is
   unchanged; cap proposals (e.g. 8); never touch `active/`, `epics.md` or
   registry files; `lifecycle.py check` must stay green after the commit.
4. Tests for the merge order/origin tags and the never-overwrite rule (the
   theme-fill step must be a pure "absent → value" transform under test).

## 2026-08-29 — PARKED at bundle `mind-workflow` plan time

Checked before issuing. Both legs have lost their driver:
- **Theme-fill**: the intake formaliser already writes `Themes:` at filing time
  (`PyAutoBrain/agents/conductors/intake/_intake.py`, `_render_header`), and
  the backfill covered 130/136. Only 7 hand-filed drafts lacked a theme on
  2026-08-29 — filled by hand in the same commit as this note. A nightly Claude
  run is the wrong tool for a workload that is near zero on an ordinary day.
- **Cross-theme proposals**: no demand yet. The deterministic auto-bundler
  renders 8 proposals today and the first bundle ever run is the one that
  parked this prompt. Revisit when bundles have been run several times and a
  grouping a rule cannot find has actually been wanted.
Un-park when either driver returns; the renderer hooks (`parse_bundles`'s
`origin` stamp, `_auto_excluded`) and `ledger_merge.LEDGER_FILES` are the three
places phase 2 would touch.
