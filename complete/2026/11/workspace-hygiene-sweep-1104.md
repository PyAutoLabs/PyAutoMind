Pre-release workspace hygiene sweep (deferred from the 2026-11-04 health review), merged 2026-11-04.

- refs: 3 genuine dead references fixed in autolens_workspace (subhalo `start_here.py` path in
  multi_dataset slam/simultaneous.py; two autolens_profiling paths in guides/point_solver/pairing.py). The other 16
  `refs` findings were scanner false positives → draft/bug/pyautobrain/hygiene_refs_false_positives_cross_repo_and_runtime.md.
- config: autofit_workspace mirrors output.dataset_identity + dataset_identity_sha256. PyAutoLens output.fit_dill
  deliberately not mirrored (legacy, no reader) — remaining `config` finding is judged, not drift.
- docstrings: 180 adjacent top-level docstring boundaries merged (autolens_workspace 26, HowToLens 100, HowToGalaxy 36,
  autoreduce_workspace 18); AST check confirmed code identical and prose unchanged; 11 HowToLens raw/plain pairs
  merged as raw only where the plain block had no backslash. Notebooks regenerated.
- Found along the way: `autohands generate` deletes start_here.ipynb when ipynb-py-convert is missing, and a stale
  *_assistant checkout rewrites every notebook's Gemini context → draft/bug/pyautohands/generate_missing_converter_deletes_start_here.md.

## Original prompt

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
