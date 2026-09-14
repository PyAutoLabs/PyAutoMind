# Clear Heart profiling-drift YELLOW: regenerate re-pinned MGE result JSONs and keep SLQ records out of pinned_drift

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- heart
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: `python3 PyAutoHeart/heart/checks/profiling_drift.py` reports 0 drifted results; the three runtime MGE cells print "Pinned-value check PASSED" and write `"pinned_drift": []`; matrix_free JSONs carry SLQ records under a new key with `pinned_drift: []`; `build_readme.py --check` passes
Review-minutes: 10
Filed: 2026-09-14

User request (verbatim, 2026-09-14):

"""
can you fix the PyAutoHeart being red
"""
(follow-up "continue" → diagnose and fix the remaining Heart YELLOW reasons; plan approved 2026-09-14.)

## Context

Heart reports 6 drifted profiling results (123 scanned). Triage 2026-09-14 (Brain profiling agent + file
reads) found no real drift:

- `results/runtime/imaging/{mge,mge_mass_jax,pixelization_numba_mge_mass}/*_hst_v2026.8.17.1.json`:
  commit 446f8f1 (#235, 2026-09-08) re-pinned the literals (lp radial bins [4,2,1] -> [4,2,2]) but
  committed the pre-re-pin discovery JSONs; each file's `got` equals today's pin. Drift 0.02% / 1e-5 %.
- `results/breakdown/imaging/matrix_free_{delaunay,delaunay_nn,rectangular}_hpc_a100_fp64_matrix_free.json`:
  the Cholesky pins PASSED (1e-13). The `pinned_drift` rows are SLQ (p=16 m=40) estimates with
  `"rtol": null` that `scripts/imaging/likelihood_breakdown/matrix_free.py` (~L1201-1233) appends
  unconditionally ("recorded, never a fault"). Heart's contract (PyAutoHeart PR #38) is "empty
  pinned_drift = all matched", so every non-empty list counts as drift. SLQ error is deterministic
  Lanczos truncation bias (rect 16.6%), so no tolerance is appropriate.

## Fix

1. Re-run the three runtime cells from the repo root with no `--config-name` (preserves filenames):
   `OMP_NUM_THREADS=1 NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib python3 scripts/imaging/likelihood_runtime/{mge,mge_mass_jax,pixelization_numba_mge_mass}.py`.
   Commit the regenerated JSONs (timings will differ from the WSL reference host; the pin check is the
   witness, not the timings — keep the timing rows honest, do not hand-edit).
2. In `matrix_free.py`, move the unconditional SLQ comparison records out of `_drift_records` into
   their own JSON key (e.g. `slq_pin_comparison`) so `pinned_drift` only carries `check_pinned` failures.
   Apply the same transform to the three committed A100 JSONs (move the rtol:null rows to the new key,
   leave `pinned_drift: []`); do not re-run the A100 legs (RAL access not required; the exact pins reproduce).
3. Regenerate README dashboards (`build_readme.py`) — lint runs `--check`.
Never bisect or edit a library from this repo (design_lock_in.md "record-and-flag, never adjudicate").
