# Bundles phase 2 — nightly Claude pass: theme-fill new drafts + proposed bundles

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Blocked-by: draft/feature/pyautomind/bundle_theme_grouping.md

## Premise

**Rules render, Claude labels.** Phase 1 makes the auto-bundler deterministic
over a `Theme:` header. This phase adds the judgment rules cannot supply,
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
