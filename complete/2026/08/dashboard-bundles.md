## dashboard-bundles
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/309
- completed: 2026-08-27
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/310
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/365

- Dashboard **Bundles** section: sets of independent prompts for one Fable-orchestrated session (Opus subagents implement); every task still renders in its usual section. Rendered between Backlog and Recent in md + html.
- `PyAutoMind/bundles.md` = human-pinned registry (epics.md-style schema, born empty); optional `Bundle: <slug>` prompt header mirrors `Epic:`.
- Auto proposals are render-only and deterministic: group by Target; exclude epic members / `Blocked-by:` / `human-required` / `too-large` / pinned; small=1, medium=2, large=4 pts, cap 8, ≤4 members, ≤1 large, min 2; top 8 shown by urgency with a "Showing N of M" footer. Refresh rides the existing nightly `dashboard_refresh.yml`.
- `PyAutoBrain/skills/start_bundle` = the orchestration contract: one `/start_dev` + issue + PR per member, one shared worktree per repo, architect plans / subagents implement. Paragraph added to `skills/WORKFLOW.md`.
- Traps: Mind PR's dashboard freshness check renders with Brain `main` → merge the Brain renderer PR first. `Blocked-by:` always counts as unresolved (renderer is offline). Shipped on human RED ack (unrelated Heart reasons).
- Deferred: phase 2 optional Claude refinement of the auto proposals, only if the rules-based bundles feel dumb.

## Original prompt

# Dashboard "Bundles" — grouping tasks for Fable-orchestrated multi-task sessions

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
Issued: 2026-08-27

## Original request (verbatim)

> I am slowly moving to a model where Fable orchestrates larger tasks with opus.
> I therefore think we need a grouping mechanism on the pyautomind dashboard,
> where similar tasks which make sense to be done in on go with fable as an
> orchestrator make sense. This should not change the dashboard as it is, seeing
> all tasks listed individually is still highly valueable and makes sense when I
> want to do one at a time. I think we need a group section, and a sensible
> mechanism which will update the grouped tasks regularly (every night?).

## Approved design (2026-08-27)

A **bundle** is a set of independent prompts that make sense in one Fable
session, with Opus subagents executing the members. Distinct from an **epic**
(ordered, phase-gated, one phase at a time). Every task still appears in its
usual dashboard section — a bundle is an additional view, never a replacement.

1. **`PyAutoMind/bundles.md` registry** — holds only human-**pinned** bundles,
   schema like `epics.md`: `## <slug>` then `- title:` / `- members:` (prompt
   paths) / `- rationale:` / `- status:`. Optional `Bundle: <slug>` prompt
   header mirrors `Epic:` so a human can force membership. Nothing ever
   rewrites prompt files automatically.
2. **Render-only auto-bundling** in
   `PyAutoBrain/agents/conductors/intake/_intake.py` — deterministic, computed
   at dashboard-render time, never written to the registry. Rules: same
   `Target` repo; exclude `Epic:` members, unresolved `Blocked-by:`,
   `Autonomy: human-required`, `Difficulty: too-large`; size cap (≤ 1 large +
   3 small, or ≤ 4 medium); minimum 2 members; pinned members leave the auto
   pool. Refresh rides the existing nightly `dashboard_refresh.yml` — no new
   schedule.
3. **New "Bundles" H2** in `dashboard.md` + `dashboard.html`, placed between
   Backlog and Recent. One card per bundle (pinned first, then auto): members
   table (size / priority / status), total size, and a one-tap **Fable
   orchestration prompt** with copy button (HTML), analogous to the epic
   resume prompt. Existing sections unchanged.
4. **Brain orchestration contract** — `start_bundle` skill (or
   `start_dev --bundle <slug>`) describing: one issue per member (keeps the
   no-bulk-issue rule), shared worktree per repo, per-task PRs so `/prm` works
   unchanged, Fable plans / Opus executes. Plus a paragraph in
   `PyAutoBrain/skills/WORKFLOW.md`.

Deferred (phase 2, only if auto bundles feel dumb): an optional Claude
refinement pass over the deterministic proposals.
