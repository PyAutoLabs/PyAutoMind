# normalise-auto-simulate-guard-idiom

- shipped: verified on autolens_workspace main `9974f891` (the prompt never left `draft/`)
- follows: [[auto-simulate-guard-targets]] (autolens_workspace#359 → #364, autogalaxy_workspace#175) and the `should_simulate` migration (autolens_workspace#354)
- repos:
  - autolens_workspace

## Summary

The prompt asks for four hand-rolled auto-simulate guards to be converted to
`al.util.dataset.should_simulate`, with one specific caution about not dropping a
stricter check while doing it. All four are converted on main, and the caution was
honoured — more carefully than the prompt asked.

Recorded 2026-08-09 by the draft/ sweep. No work is owed.

## Verified against autolens_workspace main (`9974f891`), 2026-08-09

Against the prompt's § Proposed work:

1. **All four idiom-B sites converted — DONE.** `cluster/likelihood_function.py`,
   `interferometer/features/pixelization/many_visibilities_preparation.py`,
   `imaging/features/advanced/subhalo/sensitivity/slam_source_parametric.py` and
   `…/slam_source_pixelized.py` all call `should_simulate` now. A repo-wide sweep
   finds **zero** remaining hand-rolled `data.fits … .exists()` simulator guards
   (492 files use the standard idiom).

2. **The `mass.csv` check was preserved — DONE, and better than specified.** The
   prompt warned "do not silently drop it" and offered two ways out. The shipped
   form takes the first *and* fixes an ordering subtlety the prompt did not raise:

   ```python
   if (
       al.util.dataset.should_simulate(str(dataset_path))
       or not (dataset_path / "mass.csv").exists()
   ):
   ```

   with a comment recording that `should_simulate` is evaluated **first** so its
   `PYAUTO_SMALL_DATASETS` rebuild always runs. Written the other way round, a
   present `mass.csv` would short-circuit past the capped-rebuild side effect —
   which is precisely the failure the conversion exists to prevent.

3. **Re-running under the capped profile** — not independently re-run here; that
   needs a real execution environment.

4. **`required_files=[...]` on `should_simulate` — NOT taken.** PyAutoArray's
   `should_simulate(dataset_path)` still has the single argument. This leg was
   explicitly optional in the prompt ("consider whether…", and it would have made
   the task library+workspace rather than workspace-only). The `mass.csv` clause
   living in the script is the alternative the prompt allowed.

**Not the same class, correctly left alone:** two `if not data_fits_path.exists():`
sites survive, in `multi_dataset/features/imaging_and_point_source/modeling.py:75`
and `cluster/start_here.py:153`. Both guard a one-off `urllib` download of real HST
data (RXJ1131, Abell 2744), not a simulator invocation, so `should_simulate`'s
capped-rebuild semantics would be actively wrong there — it would delete a
downloaded file to re-download it. Converting these would be a regression.

## Note on detection

This is the one finding across three sweeps that `pyauto-brain intake reconcile`
ranked `high` for the right reason: [[auto-simulate-guard-targets]] names the
prompt's path directly in its body. That is signal 3 in
`draft/feature/pyautomind/draft_staleness_detection_signals.md` working as
intended — though it still arrived among 51 other `high`s.

## Original prompt
# Normalise the two auto-simulate guard idioms

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft

Surfaced while fixing #455 (missing-auto-simulate-guards). Not folded into that
fix because it is a behaviour change to scripts that currently PASS.

Two auto-simulate guard idioms coexist in `autolens_workspace/scripts/`, and
they are **not equivalent**:

**A — the standard idiom** (now the large majority):

```python
if al.util.dataset.should_simulate(str(dataset_path)):
    subprocess.run([sys.executable, "scripts/.../simulator.py"], check=True)
```

**B — hand-rolled**, in four scripts:

- `scripts/cluster/likelihood_function.py:104` — checks `data.fits` AND `mass.csv`
- `scripts/interferometer/features/pixelization/many_visibilities_preparation.py:82`
- `scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_parametric.py:868`
- `scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_pixelized.py:995`

```python
if not (dataset_path / "data.fits").exists():
    subprocess.run([sys.executable, "scripts/.../simulator.py"], check=True)
```

## The difference that matters

`autoarray/util/dataset_util.py:should_simulate` does two things:

```python
if os.environ.get("PYAUTO_SMALL_DATASETS") == "1":
    if Path(dataset_path).exists():
        shutil.rmtree(dataset_path)
return not Path(dataset_path).exists()
```

Under `PYAUTO_SMALL_DATASETS=1` (set by `config/build/profile_smoke.yaml`
defaults) idiom A **deletes and rebuilds** the dataset at reduced resolution;
idiom B does not. So the four B scripts will happily read a
**full-resolution** dataset left on disk by an earlier uncapped run, in a run
that is supposed to be capped. That is the exact shape of the
`PYAUTO_SMALL_DATASETS` shape-mismatch problem `should_simulate` was written to
prevent.

They also differ in what they test: A tests the **directory**, B tests
`data.fits` specifically. B is stricter against a half-written directory; A is
correct about the cap. `cluster/likelihood_function.py` is the strictest of all
(two files) and would lose that if naively converted.

## Proposed work

1. Convert the four B sites to `al.util.dataset.should_simulate`.
2. For `cluster/likelihood_function.py`, preserve the `mass.csv` check —
   either keep an additional `or not (dataset_path / "mass.csv").exists()`
   clause alongside `should_simulate`, or establish that the simulator always
   writes both so the directory check subsumes it. Do not silently drop it.
3. Re-run each of the four under the capped smoke profile
   (`PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1`) from a genuinely empty
   dataset dir AND from a stale full-resolution one — the second case is the
   one that currently misbehaves and the whole point of the change.
4. Consider whether `should_simulate` should grow an optional
   `required_files=[...]` argument so the stricter checks have a home in the
   library rather than in workspace scripts (PyAutoArray change — would make
   this a library+workspace task rather than workspace-only).

## Caution

All four scripts currently PASS smoke. This change can only make them slower
(rebuilding datasets that were previously reused) or newly-failing (if a
simulator misbehaves under the cap). Measure before and after; do not assume
the conversion is free.
