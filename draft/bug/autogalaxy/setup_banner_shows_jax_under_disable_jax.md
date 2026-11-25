# Setup banner shows the designated JAX setup when `PYAUTO_DISABLE_JAX=1` forces NumPy

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- hpc-gpu
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Witness: With `PYAUTO_DISABLE_JAX=1` (or JAX not installed) and `setup="auto"` resolving to a JAX designation, the `Setup:` line reports what actually runs, e.g. `Setup:    numpy · CPU · dense · fp64   (rule imaging/mge · designated JAX; JAX disabled)`, and `Parallel:` agrees. Includes a test.
Review-minutes: 10
Unattended: no
Lane: any
Filed: 2026-11-25
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md

## Context

Found by the 5F PR2 worker under the workspace smoke profile (`PYAUTO_DISABLE_JAX=1`). `use_jax_from` correctly falls back to numpy (`autogalaxy/analysis/setup_util.py`), but the banner (`setup_banner_from`) prints the designated `JAX · CPU · dense`. The banner's job is to keep the user in the loop, so it should say what runs.
