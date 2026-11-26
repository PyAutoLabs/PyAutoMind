# Remove the temporary R6 sweep pins (mixed factor graphs, weak) after the release

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Gate: the release carrying PyAutoLabs/PyAutoFit#1801, PyAutoGalaxy#761, PyAutoLens#896 (R6 pre-release fixes).
Filed: 2026-11-26

## Ask

The R6 phase B sweep (autolens_workspace#692, autogalaxy_workspace#285) pinned backends where the R6 defaults broke before the pre-release fixes landed. After the release, remove the pins and their explanatory notes so the examples use the default setup:
- autolens_workspace `multi_dataset/features/imaging_and_point_source/modeling.py`, `multi_dataset/features/imaging_and_interferometer/modeling.py` (`use_jax=True` on the analyses);
- autogalaxy_workspace `multi_dataset/features/imaging_and_interferometer/modeling.py`, `multi_dataset/features/pixelization/modeling.py`;
- autolens_workspace weak scripts `weak/modeling.py`, `weak/likelihood_function.py`, `weak/real_data/a2744.py`, `weak/features/strong_lensing/modeling.py` (`use_jax=False`), and the stale comment near line 195 of `weak/modeling.py` saying the weak fit is a NumPy calculation.
Run each in test mode against the released stack; regenerate their notebooks from inside each repo.
