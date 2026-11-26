## likelihood-lifecycle-r6-default-auto
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/759
- completed: 2026-11-26
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/715
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1800
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/760
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/894
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/373
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/715
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1800
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/760
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/894
- epic: likelihood-lifecycle (R6 phase A)
- remainder re-filed: draft/feature/autolens_workspace/likelihood_lifecycle_r6b_workspace_use_jax_sweep.md (phase B, gated on the release)

R6 phase A (scope merged; phase B re-filed): the defaults flip after the 2026.11.25.1 opt-in release.

- **Analyses (Galaxy + Lens):** `use_jax=None, setup="auto"` by default via a pickle-safe sentinel (`setup_util.SETUP_DEFAULT`, `setup_and_use_jax_from`). Precedence: `setup` passed → as given (`None` = opt-out); else explicit `use_jax` → manual opt-out with the would-choose banner; else auto. A defaulted auto that cannot choose falls back to the constructor backend with a warning; `raise_if_setup_unresolved` skips defaulted analyses so pre-fit `log_likelihood_function` calls keep working.
- **Searches (Fit):** `number_of_cores="auto"` everywhere except GridSearch (kept at 1 by ruling: auto hung the suite via the grid's Process job pool; bug draft `draft/bug/autofit/grid_search_number_of_cores_auto_hangs.md`). Zeus pool attaches only while sampling; the interpolator's DynestyStatic pinned to 1. Fit suite time 325.7 s vs main 337 s.
- **Array:** `lazy_sparse_operator: "auto"`; fixed the numba imaging sparse data_vector for several mappers (exposed by the lazy default; control test in PyAutoLens).
- **autolens_workspace_test#373:** the interferometer sparse-operator assertion script pins lazy off on its dense reference.
- Operator attach was already a single `dataset.apply_setup(setup)` call; nothing left to slim.

Checks: suites green with JAX (Array 2614, Fit 4391, Galaxy 1679, Lens 1177) and on a CI-faithful no-JAX venv (2149/4064/1595/1112, 0 failed); Heart smoke 7/8 → 8th fixed by #373; all PR CI green before merge.

Traps:
- Masking JAX with `sys.modules['jax'] = None` is NOT a faithful no-JAX leg: scipy's array_api_compat then crashes (`'NoneType' object has no attribute 'Array'`), failing ~50–100 tests even on main. Reproduce CI instead: uv venv, `pip install ./<repo>[optional]` for Nerves/Array/Fit/Galaxy/Lens, uninstall the jax family (`jax jaxlib jaxnnls optax chex jax_zero_contour blackjax nufftax tfp-nightly`), run with `env -u PYTHONPATH`.
- Heart smoke's "N/M workspaces passed" line can come from a script failure only visible in `~/.pyauto-heart/smoke-runtime/<ws>/smoke.log` (grep FAIL), not in the per-workspace results JSON.

## Original prompt

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
Issued: 2026-11-25

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
