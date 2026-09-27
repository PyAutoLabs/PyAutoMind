# Local smoke env creation fails: smoke_install.sh flat pip chain vs the grouped layout

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_workspace
- autolens_workspace_test
- HowToLens
- euclid_strong_lens_modeling_pipeline
- autogalaxy_workspace
- autogalaxy_workspace_test
- HowToGalaxy
- autofit_workspace
- autofit_workspace_test
- HowToFit
- autocti_workspace
- autocti_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: on the grouped layout, `pyauto-heart smoke --prepare-only autolens` with the cached env moved aside creates a fresh env and exits 0 (today it fails at `pip install ./PyAutoNerves`); and the reusable Smoke Tests workflow on a flat CI checkout stays green for one workspace per family.
Review-minutes: 10
Unattended: ready
Observed 2026-09-27: `pyauto-heart smoke --prepare-only` fails locally for autolens_workspace, autolens_workspace_test and HowToLens. Each workspace's `.github/scripts/smoke_install.sh` runs a flat `pip install ./PyAutoNerves ./PyAutoFit ./PyAutoArray ./PyAutoGalaxy ./PyAutoLens` chain, and those paths do not exist in the grouped canonical layout (organs/PyAutoNerves, fit/PyAutoFit, array/PyAutoArray, galaxy/PyAutoGalaxy, lens/PyAutoLens). Heart runs that script LOCALLY, so it is not CI-only. Workaround used today: reuse the cached envs in `~/.pyauto-heart/smoke-envs/<ws>/py3.12` with Hands' run_python.py.

Impact: local smoke env (re)creation is broken for everyone on the grouped layout, and a stale cached env silently hides dependency changes (a new floor or extra in a library pyproject never reaches the env Heart smokes against).

## Evidence (read-only verification, PyAutoHeart main c67bca0)

- `heart/smoke.py:314-317` (`_install_environment`): `installer = workspace / ".github" / "scripts" / "smoke_install.sh"`; if it is a file, `_run(["bash", installer], cwd=organism_root, env=env)` and return. So the script's relative `./PyAuto*` paths resolve against the organism root.
- The workspace itself is found via `_workspace.repo_path(organism_root, spec.directory)` (heart/_workspace.py:192), which resolves grouped checkouts through Brain's `agents/_repo_paths.py` — Heart already knows the real paths; the shell script does not.
- `lens/autolens_workspace/.github/scripts/smoke_install.sh`: `pip install ./PyAutoNerves ./PyAutoFit ./PyAutoArray ./PyAutoGalaxy ./PyAutoLens` then `pip install "./PyAutoArray[optional]" "./PyAutoGalaxy[optional]" "./PyAutoLens[optional]"`. Its header says it runs "with cwd at the checkout root (the dependency chain is cloned beside `workspace/`)" — the flat CI layout.
- `ls /home/jammy/Code/PyAutoLabs/PyAutoFit` etc.: no such file or directory.
- The legacy no-installer fallback in the same function (`smoke.py:322-324`, `local_targets = [f"./{repo}" for repo in spec.chain]`) has the same flat assumption.
- This was explicitly deferred to "phase 3" by complete/2026/09/workspace-location-contracts.md and complete/2026/09/workspace-resolver-fanout.md ("the smoke_install.sh flat pip chain ... a shared CI+local script whose two callers would need different layouts") and was not picked up when the physical move landed.

## Affected files / repos

All 12 workspace installers carry the flat `pip install ./PyAuto*` chain:
- lens/autolens_workspace, lens/autolens_workspace_test, lens/HowToLens, lens/euclid_strong_lens_modeling_pipeline
- galaxy/autogalaxy_workspace, galaxy/autogalaxy_workspace_test, galaxy/HowToGalaxy
- fit/autofit_workspace, fit/autofit_workspace_test, fit/HowToFit
- cti/autocti_workspace, cti/autocti_workspace_test
(each `.github/scripts/smoke_install.sh`), plus PyAutoHeart `heart/smoke.py` (`_install_environment`, legacy fallback).

## Suggested fix direction

CI (the reusable Smoke Tests workflow, flat checkout with the chain cloned beside `workspace/`) MUST keep working unchanged — do not introduce a universal `root / manifest.path` rule. Options:
1. Heart passes the path map: before running the installer, Heart resolves each chain repo via `_workspace.repo_path` (Brain's `agents/_repo_paths.py` / the `repos.yaml` body map) and exports e.g. `PYAUTO_PATH_PyAutoFit=/abs/fit/PyAutoFit` (or one `PYAUTO_REPO_PATHS` map); the script uses `${PYAUTO_PATH_PyAutoFit:-./PyAutoFit}` so CI's flat default is untouched.
2. Heart builds a throwaway flat shim dir of symlinks (`PyAutoFit -> fit/PyAutoFit`, ...) and runs the installer with cwd there — zero workspace edits, one Heart change.
3. Apply the same resolution to the legacy `./{repo}` fallback.
Also consider: Heart should refuse to silently reuse a cached env when (re)creation fails, so a stale env cannot hide dependency changes.
