# Likelihood lifecycle phase 0B PR 3b: re-key dashboard trends on the v3 identity, re-point legacy-name writers, delete the results_layout.py old-path shim

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- dashboard
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `scripts/misc/tooling/results_layout.py` is deleted and nothing imports it; every lint `--check` step passes; no script under `scripts/` writes a results path outside the §3.7 mirrored tree (a grep/test asserts it); the dashboard trend series and README tables render from the mirrored tree with a documented old-id → v3-id mapping so no published history is lost
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 0
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-24

Split out of 0B PR 3 (catalogue builder, issue https://github.com/PyAutoLabs/autolens_profiling/issues/442) by human ruling 2026-10-24: PR 3 shipped the `profiling-summary@3` builder but deliberately stopped short of two scope items, recorded in its PR body.

## What

1. **Re-key trend series** — `build_dashboard.py` and `build_readme.py` still read through the temporary `results_layout.py` legacy view because their trend series ids and README tables are keyed by pre-move file names. Re-key them on the v3 identity (`likelihood`/`instrument`/`setup_id`/`host_class`/`model_variant`/`measurement`), carrying an explicit old-id → new-id map so published history is continuous; then delete `results_layout.py`.
2. **Re-point legacy-name writers** — ~30 scripts write by legacy name outside `resolve_output_paths` (versioned summaries, vmap probes, `sweep.py`/`aggregate.py`, HPC submits) and are coupled to readers that parse legacy names. Route them through `resolve_output_paths` (or its mirrored-tree equivalent) together with their readers. No profiling may be run to verify: use dry-run/path-only modes or unit tests on the path builders; anything only verifiable by a real run is listed for the next RAL batch (human go per batch, CPU arrays on `ral` only).

## Out of scope

Re-measuring anything; the Pulse re-pin (PR 4 of 0B); `scripts/misc/` grouping (PR 5).
