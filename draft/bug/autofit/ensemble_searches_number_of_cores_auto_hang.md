# Emcee and Zeus hang (or fail) with the R6 default number_of_cores="auto"

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-26

## Finding

Release-integrate rehearsal PyAutoHeart run 45805219063 (v2026.11.26.1.dev89801, library mains with R6 PyAutoFit#1800 / 67164d229) failed four scripts:
- `autofit_workspace_test/scripts/searches/Emcee.py`: TIMEOUT at 1800s.
- `autofit_workspace_test/scripts/searches/Zeus.py`: FAIL after 20-30s, stuck at `Sampling progress 0%`.
- `autofit_workspace/scripts/plot/emcee_plotter.py`: TIMEOUT at 1800s.
- `autofit_workspace/scripts/cookbooks/search.py`: TIMEOUT at 1800s.

Each test script runs two searches. The first passes `number_of_cores=1` and passes. The second (Emcee.py:139, Zeus.py:150) uses the defaults, which R6 changed to `number_of_cores="auto"`.

Reproduced locally on 2026-11-26 (Python 3.13, canonical mains). Emcee.py hangs inside `autofit/non_linear/parallel/sneaky.py` (SneakyPool `__init__` at :242 and `run` at :167), with workers blocked in `multiprocessing/connection.py _recv`. This is a pool deadlock, not slowness.

It is the same family as `draft/bug/autofit/grid_search_number_of_cores_auto_hangs.md`, where GridSearch hit a nested job-pool hang under "auto". That draft only covers GridSearch.

## Why it matters

Every user who constructs `af.Emcee()` or `af.Zeus()` with default settings would hang once this is released. It blocks the next release, alongside `active/likelihood_lifecycle_r6d_prerelease_fixes.md`.

## Ask

Make the SneakyPool path safe under "auto", or resolve "auto" to a safe count for the ensemble samplers. Then add a PyAutoFit test that runs Emcee and Zeus with default `number_of_cores` past the first iteration. That test would have caught this, because test_emcee.py and test_zeus.py only changed the expected default value.

Witness: `Emcee.py` and `Zeus.py` in `autofit_workspace_test`, and `emcee_plotter.py` and `cookbooks/search.py` in `autofit_workspace`, pass on the integrate profile.
