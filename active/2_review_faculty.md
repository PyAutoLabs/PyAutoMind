# Review faculty — an automatic branch-review verdict conductors consult

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft

## Why

"Do hard tasks autonomously, rely on testing and review, human validates at the
end" only works if review is a first-class automatic gate — symmetric with how
the vitals faculty wraps Heart. Today code review happens ad-hoc in the human's
session; nothing machine-checkable stands between an autonomous implementation
and its PR.

## What

Add `@PyAutoBrain/agents/faculties/review/` — a read-only faculty that, given a
task worktree / feature branch:

1. Runs the harness code-review capability (`/code-review` at high effort) plus
   a verification pass (drive the affected flow, not just tests) over the diff
   against the target branch.
2. Returns a verdict: **CLEAN** (ship), **FINDINGS** (list, ranked; autonomous
   runs must resolve or downgrade to a human checkpoint), **BLOCKED** (could
   not review — treat as human-required).
3. Follows the faculty shape: `AGENTS.md` with a `Tier:` line, deterministic
   entrypoint, never dispatches or mutates. Its "sensor" is the diff + the
   review tooling, the way vitals' sensor is Heart.

Wire the consult into the ship path so `ship_*` in autonomous mode requires
`review == CLEAN` alongside the Heart gate (the gate composition itself is
defined in `3_autonomous_ship_gate.md`).

## Boundary decision (adversarial finding — settled, record it in the AGENTS.md)

A diff review is a **side-effect-free opinion**, which is the definition of a
faculty — it does **not** belong in Heart. Heart is the organism-state
observer (repo state, CI, PRs, deep install checks on main); it never looks at
feature branches and stays the sole authority on *release* readiness. The
review faculty gates the **dev workflow's** ship step only. Do not extend
Heart, and do not let this faculty grow release opinions.

Blocked-by: 1_autonomy_contract.md (verdict semantics must match the contract's
checkpoint table).
