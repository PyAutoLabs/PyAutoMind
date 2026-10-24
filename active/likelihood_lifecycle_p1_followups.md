# Likelihood lifecycle follow-ups after phases 0B and 1B: point-source --output-path, cluster source-plane assert, coverage/parity, single §3.3 source, guard default-arg roots, pinned-check order test

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the point_source image/source runtime scripts write to `--output-path` when given; `cluster/source_plane/likelihood_breakdown.py` passes its decomposition assert on a freshly simulated dataset (or a library bug prompt is filed and the script is unchanged); `coverage_matrix` excludes parity from `current_records_unplanned`; `catalogue_lifecycle` reads `catalogue/provisional_designations.json`; the write guard catches a results root passed as a default argument; an AST test asserts every sweep-driven leaf calls `record_pinned_check` after its last row write; every lint --check step passes
Review-minutes: 20
Unattended: never
Epic: likelihood-lifecycle
Phase: 1
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-24
Issued: 2026-10-24
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/454

Human request 2026-10-24: "prm, then do all still to do in one go, then we start phase 2". Plan approved in chat (A + B).

## What (one PR)
1. `scripts/point_source_image/image_plane/likelihood_runtime.py` and `scripts/point_source_source/source_plane/likelihood_runtime.py` place their row through `place_output_path` directly and ignore `--output-path`. Route them through `resolve_output_paths` like every other cell (found by the #453 review).
2. `scripts/cluster/source_plane/likelihood_breakdown.py` (~line 499): the step-by-step log-likelihood fails its check against production `FitPositionsSource` on a freshly simulated dataset, so its `fit.png` is never reached on the laptop. Diagnose first. If the script's decomposition is stale, fix it here. If PyAutoLens is wrong, stop, file a separate library bug prompt, and leave the script alone.
3. `scripts/misc/tooling/coverage_matrix.py` (~line 221): exclude `measurement == "parity"` from `current_records_unplanned` (#451 review).
4. `catalogue_lifecycle.py` reads `catalogue/provisional_designations.json` instead of a hard-coded copy of §3.3 (#451 review).
5. `test_results_write_destinations.py`: catch a results root passed as a default argument (`def f(r=RESULTS_ROOT): r/"breakdown"`) (#449 review residual).
6. An AST test that every sweep-driven leaf (`sweep_layout.CELLS`) calls `record_pinned_check` after its last row write, which locks in the #453 timeout rule (#453 re-review suggestion).

## Out of scope
1A (`/eyes` human sign-off) runs alongside, in the session. No measurement artefacts are touched, no RAL jobs run, nothing is re-measured.
