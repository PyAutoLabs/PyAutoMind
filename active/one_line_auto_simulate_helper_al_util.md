# One-line auto-simulate helper: al.util.dataset.simulate_if_needed

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
- HowToGalaxy
- HowToLens
- PyAutoHands
- workspaces
Difficulty: too-large
Autonomy: supervised
Priority: normal
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md
Status: formalised
Issued: 2026-11-01
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/669
Consequence: glance
Witness: after the sweep, `grep -rn "subprocess.run" --include=*.py` next to `should_simulate` returns zero hits in every workspace, and `check_dataset_allowlist` reports the same number of guarded call sites before and after.
Review-minutes: 3
Unattended: needs-slicing

Phases: (1) PyAutoArray helper + docstring + test; (2) PyAutoHands guard recognises simulate_if_needed; (3) after release, one sweep PR per workspace repo.

Workspace scripts auto-simulate their dataset with an 8-line block that exposes
`subprocess`/`sys` to users who only need to know "simulate if missing":

```python
if al.util.dataset.should_simulate(str(dataset_path)):
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "scripts/simulator/lens_x2.py"],
        check=True,
    )
```

Replace it with one line:

```python
al.util.dataset.simulate_if_needed(dataset_path, simulator="scripts/simulator/lens_x2.py")
```

## Library (PyAutoArray, first)

Add to `autoarray/util/dataset_util.py`, beside `should_simulate`:

```python
def simulate_if_needed(dataset_path, simulator):
    if not should_simulate(str(dataset_path)):
        return
    import subprocess
    import sys
    subprocess.run([sys.executable, str(simulator)], check=True)
```

- Keep subprocess isolation (do NOT use runpy — simulator JAX/matplotlib state must not leak into the caller).
- Accept str or Path for both args.
- Update the `should_simulate` docstring's usage example to point at the helper.
- Unit test: mock subprocess.run; called when should_simulate is True, not called when False.
- Confirm it is reachable as `al.util.dataset.simulate_if_needed` / `ag.` / `aa.` (check how `util.dataset` is re-exported).

## PyAutoHands guard

`autohands/check_dataset_allowlist.py` `should_simulate_sites` (~line 238) AST-scans
for `should_simulate(...)` call sites to prove a capped run cannot rmtree committed
files. Extend it to also match `simulate_if_needed` (first arg = dataset path),
with a test, so swept scripts stay covered by the guard.

## Workspace sweep (after the library release)

Replace the pattern across every workspace (autolens/autogalaxy/autofit workspaces,
*_workspace_test, HowToLens/HowToGalaxy, assistants), one PR per repo. Mechanical
rewrite; keep the dataset_path and simulator path exactly as in each script.
Regenerate notebooks where the repo generates them. Smoke-test a sample per repo.
Watch for variants (extra argv, different indentation, `aa.`/`ag.` prefixes) and
leave any non-standard block untouched, listing it in the PR.

<!-- formalised by the Intake (Conception) Agent on 2026-11-01 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/0d2c73d2-cd73-44f6-9692-7e6c5ddba6dd/scratchpad/simulate_if_needed.md -->
