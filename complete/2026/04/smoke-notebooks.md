## smoke-notebooks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/110
- completed: 2026-04-30
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/46, https://github.com/PyAutoLabs/autogalaxy_workspace/pull/50, https://github.com/PyAutoLabs/autolens_workspace/pull/111
- doc: Jammy2211/admin_jammy@18bc6fb (skills/smoke_test/SKILL.md)
- notes: Adds `smoke_notebooks.txt` registry + notebook execution loop in `run_smoke.py`. Notebooks execute via `jupyter nbconvert` written to `/tmp` (notebooks/ on disk untouched). On failure the runner regenerates the single failing notebook from its `.py` source via PyAutoBuild's `py_to_notebook` and retries once — full-workspace regen stays in `generate.py`. autogalaxy_workspace and autolens_workspace gained their first-ever CI smoke workflow (modeled on `_test`); autofit_workspace's existing workflow extended. autogalaxy/autolens CI green on first run; autofit smoke red on the pre-existing `Gaussian.model_data_from() got an unexpected keyword argument 'xp'` PyAutoFit example bug (independent fix in flight).

## Original prompt

Smoke tests currently run on python scripts, but we want to know on the normal workspaces notebooks
are always running ok.

For each, can you add two smoke tests on notebooks:

autofit_workspace: overview/overivew_1 and searches/mcmc.ipynb

autogalaxy_workspace and autolens_workspace: imaging/modeling.ipynb (with test mode) and interferometer/simulator.ipynb