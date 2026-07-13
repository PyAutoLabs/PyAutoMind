# Weak lensing PYAUTO_SMALL_DATASETS support

Type: feature
Target: weak
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Weak lensing PYAUTO_SMALL_DATASETS support. Extend the PYAUTO_SMALL_DATASETS=1 smoke-mode mechanism (autoarray/util/dataset_util.py — 15x15 array cap + should_simulate delete-and-regenerate, honoured by Mask2D.circular / Grid2D.uniform) to weak-lensing datasets so workspace-test smoke runs of scripts/weak/ are fast. Weak datasets are catalogue-shaped (N background galaxies, not pixels), so the lever is the galaxy count: cap the number of positions drawn by SimulatorShearYX.via_tracer_random_positions_from (e.g. 200 -> ~25) when the env var is active, mirroring the imaging cap convention and constants in aa.util.dataset. NOTE (2026-07-09, user direction): the should_simulate auto-simulation pattern for scripts/weak/{fit,modeling}.py ships with series step 6 (weak-viz-profiles, PyAutoLens#581) — this task only needs to verify the env-var path regenerates a SMALL catalogue through that pattern. Keep the cap OUT of via_tracer_from (explicit user grid) and note the weak path uses Grid2DIrregular so existing uniform-grid caps never touch it. Gotcha from prior work: these env-var mutations can bite inside decorators — trace the full call path before assuming where the cap lands. Env var wiring for smoke runs already exists via PyAutoBuild config/build/env_vars.yaml; no os.environ mutation in scripts.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
