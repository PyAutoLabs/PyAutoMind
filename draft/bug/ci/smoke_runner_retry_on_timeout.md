# Retry a timed-out script once in the shared runner, before failing the suite

Type: bug
Target: ci
Repos:
- @PyAutoHands
Difficulty: small
Autonomy: supervised
Priority: low
Status: deprioritised 2026-08-26 — see banner
Epic: jax-compile-stall
Campaign: bug/ci/jax_vmap_jit_compile_stall.md (interim mitigation — not a phase; superseded in priority by phases 3 and 4)
Filed: 2026-08-26

## DEPRIORITISED 2026-08-26 — do not start this ahead of phase 3

Filed the same day and deprioritised the same day, on the human's objection that
retrying a failing test papers over the crack. That objection is right, and this
campaign's own history is the argument for it: the defect has been quarantined
three times and diagnosed zero times, and this ledger's § "This is why
quarantining is the wrong end state" says why. A retry is a fourth kind of paper
— it removes the symptom without the diagnosis, and with it the pressure to look.

The one thing this prompt offered that quarantine does not is evidence: paired
same-commit observations at scale. That justification also weakened the day it
was written — the 2026-08-26 re-run produced such a pair by hand (TIMEOUT 300s
then PASS 41.2s, same commit), and phase 3 now has a deterministic 16/16
reproducer that needs no pairing at all.

**Kept, not deleted**, for two reasons: the reasoning is worth having on record if
the board treadmill becomes intolerable before phase 3 lands, and the
visible-retry design here (both attempt durations in the report, never a bare
`PASS`) is the right shape if anyone ever does build it. Revisit only if phase 3
stalls **and** the manual re-run cost is actually hurting — and never as a
substitute for the root cause.

## Why this is filed

Interim mitigation for the `jax-compile-stall` epic's *operational* cost, not for
the defect. The epic ledger
[`jax_vmap_jit_compile_stall.md`](jax_vmap_jit_compile_stall.md) records that
exactly one member of `multi_dataset/jax_likelihood/` hangs to the 300s smoke cap
per run, and that **which** member rotates run to run:

| Run | Date | Leg | Stalled |
|---|---|---|---|
| 32680155872 | 08-24 | 3.12 | `mge.py` |
| 32741347675 | 08-24 | 3.13 | `rectangular_mge.py` |
| 32849006683 | 08-25 | 3.13 | `mge_group.py` |

Three of the last five `Smoke Tests` runs on `autogalaxy_workspace_test` main
were red on first attempt from this alone. Each is a RED `ws_ci` row on the Heart
board and a Slack `#ci` alert, cleared by a human re-running the job. That
treadmill is the stall's main day-to-day cost now, and the root cause is blocked
(phase 3 needs the phase 1b enabler — see the ledger's 2026-08-25 entry).

**Quarantine is not the alternative.** The rotation is exactly why: parking the
script that stalled just lets the next run pick a different one, while stripping
coverage of the heaviest JAX paths. See the ledger's § "This is why quarantining
is the wrong end state".

## The change

`autohands/build_util.py`, `execute_script`: a script that raises
`subprocess.TimeoutExpired` is re-run **once** before being recorded as a
TIMEOUT. Scope it to timeouts only — a `CalledProcessError` is a deterministic
failure and must still fail fast on the first attempt.

Every workspace inherits this through the shared runner
(`.github/scripts/run_smoke.py` is a thin shim over `run_python.py`), so **no
workspace script is touched and no entry leaves `smoke_tests.txt`**. That is the
fix locus this epic requires: user-facing workspace scripts are documentation.

## The retry must be visible, never silent

A silent retry would turn this from mitigation into concealment, and would
destroy the evidence the epic needs.

- The `ScriptResult` records that a retry happened, the outcome of each attempt,
  and **both** durations — a first-attempt 300s cap followed by a 20s pass is the
  bimodality, and it should be readable straight off the report.
- The console prints something distinguishable (`RETRY PASS (20.1s, first
  attempt capped at 300s)`), never a bare `PASS`.
- A script that caps on **both** attempts is recorded as TIMEOUT and fails the
  suite exactly as today.

## Second benefit: it is an experiment, not just a workaround

Today each stall is a single sample. A retry makes every occurrence a paired
observation in the same job, on the same runner, at the same commit — which is
the comparison the epic has been unable to run at scale. A stall that clears on
retry confirms the per-run bimodality; one that repeats on the same script is a
much stronger signal than anything in the ledger so far. Whoever picks up phase 3
should mine these reports.

## Watch for

- **The job time budget.** One retry adds up to a full cap (300s) to a run that
  already spent one. Confirm the reusable workflow's job timeout has headroom for
  two capped scripts, or the mitigation trades a red gate for a killed job.
- **`no_run.yaml` / release-cap paths.** `execute_script` is shared with the
  mega-run at an 1800s cap; a retry there costs far more. Decide deliberately
  whether the retry is cap-agnostic or smoke-only, and say which in the code.
- **The notebook path** (`_classify_notebook_run`) has its own timeout branch.
  State whether it is in scope rather than leaving the two to drift.

## Acceptance

- A single timed-out script no longer reds the suite when its retry passes.
- The report and console both show the retry and both attempt durations.
- A script that caps twice still fails the suite, and a non-timeout failure still
  fails on the first attempt.
- Tests cover: retry-passes, retry-also-times-out, non-timeout failure not
  retried.
- No workspace script, `smoke_tests.txt` entry or `no_run.yaml` entry changed.

## Not a fix

This does not diagnose or fix the stall, and the code comment should say so and
point at the epic ledger. Removing it is part of phase 3's close-out.
