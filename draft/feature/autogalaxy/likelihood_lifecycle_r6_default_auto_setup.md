# Likelihood lifecycle R6: flip the default to `setup="auto"`, then sweep `use_jax=` out of the workspaces

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- PyAutoArray
- PyAutoFit
- autolens_workspace
- autogalaxy_workspace
- HowToLens
- HowToGalaxy
- autolens_workspace_test
- autogalaxy_workspace_test
Themes:
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: A fresh `al.AnalysisImaging(dataset=dataset)` with no `setup=` and no `use_jax=` resolves `setup="auto"` at fit start (banner shows "Automatic compute setup"), and the workspace start_here scripts carry no `use_jax=` argument.
Epic: likelihood-lifecycle
Phase: 6 (R6 rollout)
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-25

## Request (human, 2026-11-25, verbatim)

"Do those and go to next epic step" — the next epic step being the R6 default flip + `use_jax` sweep, after release 2026.11.25.1 shipped `setup="auto"` opt-in with the "would choose" banner.

## Context

- Ruling R6 (2026-11-16): one release with `setup="auto"` opt-in and a "would choose" banner (done: 2026.11.25.1), then the default flips.
- Today the dataset analyses default to `use_jax=True, setup=None`; `use_jax` is honoured only when `setup` is `None`, a resolved setup sets the backend.
- Follow-ups recorded for the flip: slim the numpy operator attach in `AnalysisDataset` so it delegates to PyAutoArray `sparse_operator_for`; decide `lazy_sparse_operator` default (`off` this release) and `number_of_cores` default (`1`).
- Workspace scripts pass `use_jax=` in ~355 files (autolens_workspace 170, autogalaxy_workspace 52, HowToLens 4, HowToGalaxy 13, autolens_workspace_test 74, autogalaxy_workspace_test 42).

## Out of scope

- New profiling or rule changes (`setup_rules.yaml`).
- autolens_assistant docs (separate follow-up `draft/feature/autolens_assistant/hpc_setup_flag_and_wiki_auto_setup.md`).
