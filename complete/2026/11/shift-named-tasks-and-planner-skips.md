- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/667
- prs: https://github.com/PyAutoLabs/PyAutoBrain/pull/668 (merged 2026-11-17)
- epic: autonomous-orchestrators, M3.6b
- what shipped: R5 (option a) — one-slice-per-epic and phase order bind only `Phase:` tasks (a `Phase:` counts by its leading number; an unnumbered label is still a phase), a side task orders itself by `Blocked-by:` and its rejection names the blocker. `batch brief --check` runs the watcher's gates (claims on Mind's local origin/main, then `plan`) and prints "will not start — <reason>" per named task; the watcher records the same in `backlog_gates.named` for the digest's Not started line (a named task with no draft says so). R2 — a `coordination:`/`conflict-override:` line frees a repo only for the task it names. A shift's dip skips drafts with no `Witness:` (counted; named and resumed exempt). `brief --new` with no goal epic/tag writes `backlog: scoped`, `tiers: notify, glance`. `brief --check` applies the organ rule to named tasks (`_brief.organ_findings`: refuse on the shift's own code, pass with a line, warn on no telling path). Docs: AUTONOMY.md "Human rulings R5 and R2", batch AGENTS.md, skills/batch/batch.md.
- evidence: 7 witness tests fail on main 8f36ae6, pass (46 in tests/test_batch_named_tasks.py); Brain 2309 passed; skill line counts OK; Fable 5.2 review x4, FINDINGS fixed each round (organ-rule path reading); first CI run red on the tenant firewall (instance names in organ code and tests), fixed in c07b315, then green; shadow row merged-unchanged (stage 2, human-/prm). Real Mind: organ survey 14 refused / 17 warned / 18 passed of 317 drafts.
- follow-up: `Blocked-by:` never clears after its blocker ships; a queued `judge` task is outside the `brief --new` default scope (name it in the brief); spawn-gate reasons (max-workers, tokens, pause) still read plain "not started"; the organ rule passes a prompt that names only other paths even if its fix lands in watcher code; run the firewall check locally before Brain pushes (the suite does not).

## Original prompt

# M3.6b Named tasks and the planner: per-epic limit on phases only, a reason for every task not started

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-17
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/667
Epic: autonomous-orchestrators
Phase: 10
Consequence: glance
Witness: `python -m pytest tests/test_batch*.py -q` passes with new tests that fail on today's main: (1) a brief naming an epic's `Phase:` task and a same-epic task with no `Phase:` dispatches both; (2) two `Phase:` tasks of one epic: the second is not started, and both `brief --check` output and the digest's "Not started" line give the reason; (3) a side task with `Blocked-by:` naming the phase prompt waits for it; (4) a backlog draft with no `Witness:` is skipped and counted in the digest; (5) a draft whose repo is claimed in `active.md` by another task is not dispatched and is counted; (6) `brief --new` writes `backlog: scoped` with the backlog-reach scope, not `fill-idle`; (7) a named task in the intake renderer passes the organ rule at `--check` with a line saying why
Lane: any
Unattended: never

## Why

In shift 2026-11-16-pm:

- `_batch.py` rejects a second task of the same epic ("epic … already in this batch"). The
  wall-estimate bug carries the likelihood-lifecycle tag, so it took phase 5A's place. The
  rejection reached neither `plan`, the digest nor the tick log: the digest just says 5A was
  "Not started".
- Only one worker asked the human on GitHub: PyAutoFit#1777, asked 18:38Z, answered 18:42Z,
  never resumed. Its question (repo claimed by another task, no file overlap) could have been
  settled before dispatch.
- 152 backlog drafts were skipped because PyAutoArray is claimed by one active task; PyAutoFit
  is held the same way.
- `--new` defaulted to `fill-idle`; the chat chose `tiers: notify, glance` without asking.
- The organ rule needed the human's "PyAutoBrain fixes are fine".
- 115 drafts have no `Witness:`; the backlog picks without one were excluded by hand.

Human rulings, 2026-11-17:

- **R5 (option a):** the per-epic limit applies to tasks with a `Phase:` number only. Order
  between a side task and a phase is written as `Blocked-by:`. Every named task that will not
  start is listed with its reason at `brief --check` and in the digest.
- **R2:** the planner does not dispatch a task whose repo is claimed by another active task;
  the digest counts those skipped.

## What

1. The per-epic limit counts only tasks with a `Phase:` number (R5). A side task and the next
   phase can share a shift; ordering between them is `Blocked-by:`.
2. Every named task that will not start gets one line with its reason, at `brief --check` and
   in the digest.
3. The planner does not dispatch a task whose repo another active task claims, named or
   backlog (R2), and the digest counts them.
4. The backlog dip skips drafts with no `Witness:` itself and counts them in the digest.
5. `brief --new` defaults the backlog scope from the 2026-11-16 backlog-reach ruling (queue
   first, then `Difficulty: small` single-repo tasks).
6. A named task in a renderer (the intake dashboard code) is not the watcher, writer or
   release path: `--check` says so and passes the organ rule.

## Out of scope

- How long-lived `active.md` claims shut out the backlog (infrastructure review).
- The readiness pass that turns gates into rulings before a shift (M3.3).
- Restarting answered tasks (M3.6c).
