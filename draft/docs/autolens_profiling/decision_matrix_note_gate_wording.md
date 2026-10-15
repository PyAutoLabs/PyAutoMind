# Decision-matrix note: stop describing gate 60 as current; link the Pulse knowledge

Type: docs
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: safe
Priority: normal
Consequence: notify
Status: formalised

Follow-up from `complete/2026/10/interferometer-route-gate-phase2.md` (autolens_profiling#419 /
PR #420), review finding F3.

1. `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` may still describe the
   fixed `interferometer_numba_nnz_per_source_max: 60` gate as the current default. Since
   PyAutoArray#632 (`17caf228`) the packaged default is `null` (the two-constant cost model). Check
   the note and, where it presents gate 60 as current, mark it as historical and point to
   `results/notes/interferometer_route_gate_aris_2026_10.md`. Do not rewrite the 2026-09
   measurements themselves.
2. Add a pointer from `wiki/campaigns/interferometer_likelihood.md` to the PyAutoPulse task's
   Knowledge section and its two decision records. Use a link only, and never copy the prose:
   - https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_large_mask_aris.md
   - https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/adaptsplit-zero-weight-delaunay-only.md
   - https://github.com/PyAutoLabs/PyAutoPulse/blob/main/decisions/interferometer-route-gate-cost-model.md

Done when `check_wiki.py --check` and the other lint.yml checks pass, and no note in
autolens_profiling presents gate 60 as the current default.
