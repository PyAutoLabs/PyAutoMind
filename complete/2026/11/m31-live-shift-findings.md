Fixes from the M3.1 live shifts of 2026-11-14 (PyAutoMind#570/#571), plus close-out clean-up items 1–2. Shipped as PyAutoBrain#638 (9a7072afd), merged 2026-11-16 on `ci-verdict` GREEN with Heart dev-ship GREEN. Issue PyAutoBrain#637.

**Fixed:**
- **Re-dispatch reserve:** at most +1 session, once per shift.
- **Crashed label:** a killed task that is never re-dispatched reads "Crashed — not re-dispatched".
- **Parked tasks:** a task parked on a question isn't started again until a brief names it or a later shift finishes it.
- **Repo claims:** claims on Mind origin/main are respected, except where marked `coordination:`. An unreadable `active.md` fails closed.
- **Calibration gate:** also reads the local origin/main ref. The 16-minute gap on 11-14 was in the lead, not the gate.
- **Backlog reach (human ruling 2026-11-16):** queue first, then only small single-repo tasks. Recorded in AUTONOMY.md.
- **Organ excludes by rule:** no dips into Brain, Mind or Hands.
- **Token reserve:** median of comparable shifts, capped at budget/2.
- **PR keys** enforced.
- **Unattended close-out** removes the worktree and branch, or says why.
- **In-turn merges** retire their queue entry.

**Witness:**
- 15 new offline tests.
- Brain suite: 2031 passed. The 1 failure is environmental.
- Dry run, branch vs base (`Science/scratch/m3_1_prep/findings_637/dryrun.md`).

**Review:** independent Opus returned FINDINGS. Three were fixed in c0e4d72, including the uncapped token reserve that could freeze a shift. Follow-up: answering a question doesn't clear the hold by itself; M3.5 (questions inbox) owns that.

## Original prompt

# M3.1 live shifts 2026-11-14 (pm2 + pm3): findings

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Consequence: glance
Priority: high
Status: draft
Filed: 2026-11-14
Epic: autonomous-orchestrators (programme M3.1 → M3.2)
Lane: any

Shift A `batches/2026-11-14-pm2.md` (PyAutoMind#570) and shift B `batches/2026-11-14-pm3.md`
(PyAutoMind#571) ran on Brain 7be8e94. They exercised: an unattended library merge (PyAutoLens#861),
kill → re-dispatch (B), backlog dips, question pushes, /drop, and back to back shifts with no re-pick
of a named task. Not seen live: a merge-cap refusal (B's two PRs were refused earlier, on
decision-taken) and a token-cap refusal of a spawn (the session cap bound first both times).

1. **Re-dispatch has no reserved session.** In A, the killed worker stayed "crashed — awaiting
   re-dispatch", because the 4th session went to a backlog dip after the first task finished in
   ~25 min. Reserve one session for re-dispatch, or let a re-dispatch bypass `max-sessions` up to
   +1.
2. **A killed, never re-dispatched task reads "Not started" in the digest** (A's
   `galaxy_duplicate_pytree…`). It should read as crashed and not re-dispatched, with the reason.
3. **A parked task stays pickable.** `markdown_regeneration_sigma_min` parked in A on a question
   (autolens_workspace#669) but its prompt stayed in `draft/` with no claim, and it was on B's
   wait list. The human /dropped it. A parked-on-question task must not be startable until the
   question is answered (see M3.5 questions inbox).
4. **Repo claims across shifts are not checked at plan time.** B's `model_bullet_parameter_count_drift`
   started twice (once killed, once re-dispatched), then parked because autolens_workspace was
   claimed by A's backlog pick `cluster_regime_narrative` (PR #671 open). F4 excludes claimed
   *tasks*. It should also skip tasks whose repos are claimed in `active.md` on origin/main.
5. **Calibration-gate lag.** A's `review-minutes-actual` was pushed ~19:57Z and the canonical Mind
   was fast-forwarded, but B's 20:11 tick still refused "missing". B first dispatched at 20:14.
   Find which ref the gate reads (the once-per-shift Mind fetch?) and make a fresh record count
   within one tick.
6. **Dips reach beyond queue.md.** A dipped `cluster_regime_narrative` (not in queue.md, medium,
   three repos) after the queue's startable entries ran out. The human approved "simple real work
   from the queue". **Human ruling 2026-11-16:** queue first, then only `Difficulty: small`
   single-repo backlog tasks; anything bigger must be queued by the human. Enforce it in the planner
   for `backlog: scoped` and record the ruling in AUTONOMY.md (authorized).
7. **Brief excludes drift.** Organ drafts filed after a brief is written are not excluded. The
   lead added 9 to B by hand. The planner should exclude PyAutoBrain/PyAutoMind/PyAutoHands
   targets by rule (a shift never changes its own watcher, writer or release path), not by list.
8. **Token cap never refused a spawn.** B ended at 498k of 400k: workers ~125k each, a killed
   worker still costs, and close-outs ran over the budget as ruled. Re-check the reservation maths
   so the cap binds before the session cap when it is meant to.

9. **Worker wrote a bare `pr:` key in its active.md row** (`cluster-regime-narrative`), so `lifecycle.py check` drifted and /prm would find nothing to merge. The lead renamed it to `workspace-pr:`. The worker template, or the writer's validation, should enforce the PR keys (REFERENCE.md "The PR keys").

Witness: one offline test per item 1–5, 7, 8 and 9 that fails on 7be8e94. Item 6 now has a test too: a medium or multi-repo backlog draft is never dipped.
