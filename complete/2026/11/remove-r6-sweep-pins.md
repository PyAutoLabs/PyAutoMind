## remove-r6-sweep-pins
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/698
- completed: 2026-11-26
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/765
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/699
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/286
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/142
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/198
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/765
- epic: likelihood-lifecycle (post-R6 release follow-up)

After release 2026.11.26.1 the temporary R6 phase B pins came out: analyses in the mixed factor-graph examples (autolens imaging+point, imaging+interferometer; autogalaxy imaging+interferometer, pixelization) no longer pass `use_jax=True` (the graph's own `FactorGraphModel(use_jax=True)`, from July, stays and defaulted analyses adopt it), and the weak scripts drop `use_jax=False` and the #614 notes. `weak/features/strong_lensing/modeling.py` keeps its July-era imaging `use_jax=False`; the weak factor adopts NumPy.

Human-added scope ("do the 3 left alones"): `weak/start_here.py` dropped its July-era `use_jax=False` + #614 prose (search stays Nautilus); "from the next release" prose rewritten in 9 autolens_workspace, 4 autogalaxy_workspace, 1 HowToLens script and 2 assistant pages (hpc.md re-stamped via `audit_skill_apis.py --write-provenance` after wiki-currency failed on the content hash); PyAutoGalaxy `adopt_backend` log line now says "so all its factors share one backend" instead of "as their default setups disagree" (wrong when the graph's use_jax sets the backend).

Validation: all edited scripts run in PYAUTO_TEST_MODE=1 (banners confirm adoption), targeted Heart smoke PASS, test_autogalaxy 1692 passed, notebooks regenerated (only matching ones changed), ci-verdict GREEN on all five.

## Original prompt

# Remove the temporary R6 sweep pins (mixed factor graphs, weak) after the release

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-11-26
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
