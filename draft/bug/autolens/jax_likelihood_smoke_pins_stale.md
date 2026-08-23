# autolens_workspace_test jax_likelihood pins: 4 scripts fail smoke on main

Type: bug
Target: autolens
Repos:
- @PyAutoLens
Difficulty: low
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-08-19 (backfilled from git)

## Finding (2026-08-19, control-tested during lazy-heavy-imports #1505)

`pyauto-heart smoke autolens_test` fails 4/24 on canonical main (verified twice,
worktree and canonical identical):

- `imaging/jax_likelihood/lp.py` — vmap result is ~half the hardcoded pin
  `-1.34797827e09`. This is the positions-LH penalty-doubling: the unmerged fix
  `fb1aefe0b` ("sum PositionsLH penalties instead of doubling the last entry")
  sits in the orphan worktree `~/Code/PyAutoLabs-wt/positions-lh-penalty-accumulation`
  (PyAutoLens). The pin was calibrated against the doubling behaviour — landing
  that fix and re-pinning must happen together.
- `interferometer/jax_likelihood/rectangular.py` — misses pin `-3164.286252` by
  0.0124% vs rtol 1e-4 (stale-pin drift).
- `interferometer/jax_likelihood/mge.py`, `multi_dataset/jax_likelihood/mge.py` —
  same stale-pin family.

## Task

Adjudicate the orphan positions-LH worktree (land or discard `fb1aefe0b`), then
recalibrate the four scripts' hardcoded pins against current main and widen
tolerances where the value is legitimately environment-sensitive. Every
workspace_test smoke sweep reads 20/24 until this lands.
