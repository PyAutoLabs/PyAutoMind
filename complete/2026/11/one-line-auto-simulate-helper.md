## one-line-auto-simulate-helper
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/669
- completed: 2026-11-01
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/670
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/329

- Scope shipped: phases 1–2 only. Phase 3 (workspace sweep) re-filed as `draft/feature/workspaces/simulate_if_needed_workspace_sweep.md`, which waits for the PyAutoArray release carrying #670.
- PyAutoArray#670 (merge `c7da8b0f`): `simulate_if_needed(dataset_path, simulator)` in `autoarray/util/dataset_util.py`. Subprocess (`sys.executable`, `check=True`), not runpy; str or Path; returns whether the simulator ran. `should_simulate` docstring example points at it. Tests mock `subprocess.run`; `test_autoarray/util` 148 passed; CI 3/3 legs green.
- PyAutoHands#329 (merge `70f87b47`): `check_dataset_allowlist` leg 2 matches `DELETING_CALLS = ("should_simulate", "simulate_if_needed")`, taking the first positional argument or the `dataset_path=` keyword. 4 new tests; CI 3/3 legs green.
- Trap: PyAutoHands CI runs the tenant-firewall check (`repos_sync.py --check --only "tenant firewall (organ code)"`). Naming a library repo (`PyAutoArray`) in an organ code comment fails it, even though all tests pass. Run it locally before pushing organ code.
- Process note: the PRs were opened directly from the cloud session rather than via `/ship_library`. The `pending-release` label and Mind link on #670 were added at `/prm` close-out.
- Unverified: `al.`/`ag.util.dataset` re-export of the helper was assumed from the existing `al.util.dataset.should_simulate` usage, not checked in PyAutoGalaxy/PyAutoLens. Check it in the phase 3 sweep.

## Original prompt

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
