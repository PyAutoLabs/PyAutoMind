# Workspace hygiene sweep (refs, config, docstrings) — 2026-11-04

Type: refactor
Target: autolens_workspace, autofit_workspace, HowToLens, HowToGalaxy, autoreduce_workspace
Consequence: judge
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/620

Human, 2026-11-04: "codex cleared can we do the things now?" — the hygiene items deferred in the
health review until the Codex HowTo link work landed.

1. refs: 3 genuine dead references in autolens_workspace (simultaneous.py:728 subhalo path,
   point_solver/pairing.py:111 and :259 profiling paths). The other 16 refs findings are scanner
   false positives (sibling-repo and runtime paths) → Brain bug.
2. config: mirror output.dataset_identity + dataset_identity_sha256 into autofit_workspace;
   PyAutoLens output.fit_dill is a legacy key with no reader — do not mirror.
3. docstrings: merge the 180 adjacent top-level docstring boundaries, regenerate notebooks.
