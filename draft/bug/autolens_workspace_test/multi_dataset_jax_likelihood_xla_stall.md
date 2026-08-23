# multi_dataset/jax_likelihood scripts hang to the timeout cap (XLA compile stall)

Type: bug
Target: autolens_workspace_test
Repos:
- @autolens_workspace_test
- @PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-08-22 (backfilled from git)

## Why this is filed now

Filed 2026-08-22 after `multi_dataset/jax_likelihood/mge.py` was parked out of
the PR smoke gate (autolens_workspace_test#262) to unblock the pynufft removal
(#261). Parking removes the symptom from CI; **this prompt is what stops the
underlying stall from going quiet.** The whole
`multi_dataset/jax_likelihood/` family is now absent from the PR gate.

## The bug

Scripts in this family intermittently stop making progress and run to whatever
timeout cap applies, instead of completing in their normal tens of seconds.

Already recorded for the sibling, in `config/build/no_run.yaml:87`:

> `multi_dataset/jax_likelihood/delaunay.py` — NEEDS_FIX 2026-08-01 — hangs to
> the 1800s release cap in 3 of 5 release-integrate runs since 07-31 (18s when
> it passes; **intermittent XLA compile stall, family-wide** — ag_test
> `rectangular.py` also hit); quarantined to unblock the 2026-08-01 release;
> see autolens_workspace_test#245

`mge.py` now shows the identical signature at the 300s smoke cap:

- 4/4 job failures on #261 — Python 3.12 and 3.13, twice each including a
  re-run — always `TIMEOUT (300s) multi_dataset/jax_likelihood/mge.py`,
  always 23/24 passed.
- Runs green standalone in **32 s** under its declared `ENV: jax
  full_datasets` profile, simulating its dataset from scratch as CI does. So
  it is not cap margin; it stops progressing.
- Not caused by #261: that diff is three files, none in `smoke_tests.txt`, and
  `mge.py` references nothing it changed.
- Not dataset contamination: `mge.py` is the only gate script touching
  `dataset/multi_dataset/lens_sersic`, and the runner gives each script its own
  subprocess.

Reproduced only in CI so far — never locally in isolation — which points at the
compile stall being load- or environment-sensitive rather than a code defect in
any one script.

## Scope

The family is now almost entirely quarantined, which is the real cost:

- `delaunay.py` — NEEDS_FIX in `no_run.yaml` (release), #245
- `delaunay_mge` — SLOW in `no_run.yaml`
- `shared_preloads.py` — SLOW in `no_run.yaml`, and disabled in
  `smoke_tests.txt` since 2026-07-22
- `mge.py` — disabled in `smoke_tests.txt` 2026-08-22 (this filing).
  Deliberately **not** added to `no_run.yaml`: every observed failure is at the
  300 s smoke cap and there is no release-cap evidence, so release coverage is
  intentionally left intact.

## Task

1. Characterise the stall rather than the scripts. It is family-wide and has
   also hit `ag_test rectangular.py`, so a per-script speedup is not the fix.
   Establish whether it is an XLA/jaxlib compile deadlock, a runner resource
   limit, or a threading interaction — a hung run's stack (py-spy or
   `faulthandler` on SIGTERM at the cap) would settle it far faster than more
   timing data.
2. Consider making the runner dump a stack trace on timeout instead of just
   reporting `TIMEOUT`. Today a hang produces no evidence at all, which is why
   this has been quarantined three times without a diagnosis.
3. Once fixed, un-quarantine the family: re-enable `mge.py` and
   `shared_preloads.py` in `smoke_tests.txt` and clear the `no_run.yaml`
   entries that cite #245.

## Acceptance

- A root cause for the stall, or an explicit decision that it is an
  infrastructure limit to be worked around rather than fixed.
- A hung script leaves diagnostic evidence behind.
- The `multi_dataset/jax_likelihood/` family is back under CI coverage, or its
  absence is a recorded deliberate choice rather than an accumulation of
  one-off quarantines.
