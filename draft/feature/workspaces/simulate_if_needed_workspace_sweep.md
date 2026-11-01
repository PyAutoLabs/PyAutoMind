# Sweep workspaces onto al.util.dataset.simulate_if_needed (one PR per repo)

Type: feature
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- HowToLens
- HowToGalaxy
- assistants
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: after the sweep, `grep -rn "subprocess.run" --include=*.py` next to `should_simulate` returns zero hits in every workspace, and `check_dataset_allowlist` reports the same number of guarded call sites before and after.
Review-minutes: 3
Unattended: needs-slicing
Blocked-by: PyAutoArray release carrying https://github.com/PyAutoLabs/PyAutoArray/pull/670 (pending-release)
Filed: 2026-11-01

- Status: split out of `one-line-auto-simulate-helper` at close-out. Phases 1–2 shipped in `complete/2026/11/one-line-auto-simulate-helper.md` (PyAutoArray#670, PyAutoHands#329); this is phase 3, what remains.

Replace the 8-line auto-simulate block in every workspace script:

```python
if al.util.dataset.should_simulate(str(dataset_path)):
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "scripts/simulator/lens_x2.py"],
        check=True,
    )
```

with the one-liner shipped in PyAutoArray#670:

```python
al.util.dataset.simulate_if_needed(dataset_path, simulator="scripts/simulator/lens_x2.py")
```

- Start only after the PyAutoArray release that carries #670 has published; workspaces pin released libraries.
- First confirm `al.util.dataset.simulate_if_needed` and `ag.util.dataset.simulate_if_needed` resolve. The re-export was assumed at close-out, not verified.
- Do one PR per repo (autolens/autogalaxy/autofit workspaces, *_workspace_test, HowToLens/HowToGalaxy, assistants). This is a mechanical rewrite: keep the dataset_path and simulator path exactly as in each script.
- Regenerate notebooks where the repo generates them. Smoke-test a sample per repo.
- Watch for variants (extra argv, different indentation, `aa.`/`ag.` prefixes). Leave any non-standard block untouched and list it in the PR.
- Run `check_dataset_allowlist` before and after in each repo: the guarded call-site count must not drop. PyAutoHands#329 already makes the guard recognise `simulate_if_needed`.
