# Refactor conductor — the first default-auto agent

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

## Why

Demonstrated need, not symmetry: a "refactor agent" bullet has sat in
`@PyAutoMind/ideas.md` since before this series was conceived, and `/refactor`
today is merely `start_dev` pre-tagged with the work-type. Refactoring is also
the **most autonomy-friendly work-type** — behaviour-preserving by definition,
so the test suite + review faculty form a near-complete gate — which makes it
the right proving ground for the `--auto` machinery before feature/bug work
earns the same treatment.

## What

Add `@PyAutoBrain/agents/conductors/refactor/` following the Build Agent's
shape (Tier line, `AGENTS.md`, deterministic entrypoint, capability audit):

1. **Plans no-behaviour-change work**: selects the next `refactor/*` Mind task
   (or plans a named one), emits a `RefactorDecision` mirroring the
   FeatureDecision shape, with an explicit behaviour-preservation argument
   (what invariant, which tests witness it).
2. **Mines candidates**: can sweep review-faculty FINDINGS,
   simplification-review output, and `ideas.md` refactor bullets into proposed
   `refactor/<target>/` prompts (via intake — it files, it does not bypass).
3. **Runs at `safe` by default** under `--auto`, per the work-type cap in
   `AUTONOMY.md` — the first conductor whose normal mode is autonomous, ending
   at PR-open with the review verdict attached.
4. Re-point the `/refactor` verb from the work-type-entry shim to the
   conductor; update the routing table in `PyAutoBrain/AGENTS.md` and
   `PyAutoMind/ROUTING.md`.

## Boundaries

- Consults faculties only (sizing, review, memory when it lands, vitals for
  risky work) — never another conductor.
- A refactor that changes any public API or observable behaviour is
  misclassified: the conductor re-routes it to feature/bug rather than
  proceeding at `safe`.
- Whether an "optimize agent" (the adjacent ideas.md bullet) is this
  conductor's second mode or its own thing is a scope decision for the plan —
  do not silently absorb it.

Blocked-by: 4_auto_dev_mode.md (and transitively 1–3). Mark the ideas.md
bullet `[formalised -> feature/autonomy/6_refactor_conductor.md]` when issued.
