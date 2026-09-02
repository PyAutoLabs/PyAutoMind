# Phase 5 dev leg: prepare the mesh gradient-search array for PositionsLH…

Type: feature
Target: workspaces
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: jax-inference-profiling

Phase 5 dev leg: prepare the mesh gradient-search array for PositionsLH at factor 1e5 / threshold auto — verify the multi_start_prodigy leaf scripts honour SEARCHES_POSITIONS / _THRESHOLD / _FACTOR through _setup.py, add a `submit_search_multi_start_prodigy_phase5_positions_array.sh` under hpc/batch_gpu/ (cells × seeds per Cortex phase 16), include the one-cell Nautilus tauto0.2 f1e5 control task, and dry-run one task with AUTOLENS_PROFILING_SMOKE=1. No submission — dispatch is a Cortex phase-16 act after phase 12 is ruled.

Gate: this prompt is gated on PyAutoCortex phase 16
(`phases/inference_programme/phase5_mesh_gradient_positions_on.md`, state `planned`)
having been READ BY THE HUMAN — the array's cells, arms and seeds come from that
phase's dispatch plan, and it also records two open questions the array's shape
depends on (there is no `multi_start_prodigy_autoconv` leaf for any mesh cell, and
no measured step rate for any mesh cell at 256 lanes, so a probe arm precedes the
sizing). Not a `Blocked-by:` — a Cortex phase is not a GitHub ref.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from user-intake -->
