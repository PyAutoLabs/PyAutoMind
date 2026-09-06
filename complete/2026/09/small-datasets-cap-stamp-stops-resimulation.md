# Capped interferometer / multi_dataset datasets stop re-simulating on every run — the SMALLSHP cap card

PyAutoNerves#160 → `efe7c04` (closing PyAutoNerves#159) and PyAutoArray#529 → `bcd15cd9`
(closing PyAutoArray#528), merged 2026-09-06 in that order on branch
`claude/ci-test-timing-epic-ke2lul`. Phase 8c (library leg) of the `ci-timing-fast-tests`
epic. Fable-planned on the issues; implemented by Opus subagents (the second resumed after
a container restart interrupted the first mid-PyAutoArray).

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/528
- issue-2: https://github.com/PyAutoLabs/PyAutoNerves/issues/159
- completed: 2026-09-06
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/160
- library-pr-2: https://github.com/PyAutoLabs/PyAutoArray/pull/529

## What shipped
- PyAutoNerves: `stamp_small_datasets_regime` writes a `SMALLSHP` card (`"<rows>x<cols>"`)
  under the cap beside `SMALLDAT`; `SMALL_DATASETS_SHAPE_NATIVE` gets its canonical home in
  `autonerves.test_mode` (autoarray keeps a literal that a test pins to agree, so a
  pre-stamp autonerves degrades safely rather than ImportError-ing).
- PyAutoArray: `SMALLSHP` readers, `_capped_data_paths` resolving `data.fits` →
  `{waveband}_data.fits` → `channel_*/data.fits`, and `_is_capped_at_the_current_cap`
  rewritten around them — read *with* the both-axes contradiction guard (the card records
  the writing process, not the array: the issue's literal diff would have kept a 180×180
  image written in a capped shell and two existing tests caught it). Path resolution is
  widened for the capped (delete → keep) branch only.
- Measured: `should_simulate` True → False on the second run of
  `autolens_workspace interferometer/modeling.py` (12.40 → 6.69 s), `multi_dataset/modeling.py`
  (10.48 → 6.32 s), `autogalaxy_workspace interferometer/start_here.py` (10.93 → 6.52 s);
  ~26 s per autolens_workspace CI run and ~28 s per autogalaxy_workspace run once the
  dataset cache carries a stamped set. Both `_test` gates green with the branches installed.

## Key traps / findings
- A card that records "the env var was set at write time" is not "capped at today's cap";
  the reader has to compare the recorded cap, and still guard against a shape that
  contradicts it.
- The re-simulation subprocess costs ~5 s of which ~4.5 s is a fresh interpreter importing
  the stack.

## Follow-ups
- `draft/maintenance/autoarray/small_datasets_followups_after_8c.md`: bump the autonerves
  floor and delete the defensive `try/except` once the PyAutoNerves release exists.
- Releases: PyAutoNerves and PyAutoArray outstanding (`pending-release`).

## Original prompt

# Capped interferometer / multi_dataset datasets are re-simulated on every run (stamp the cap, not just the flag)

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoNerves
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-06
Epic: ci-timing-fast-tests
Phase: 8c
Issued: 2026-09-06

Library leg of phase 8 (autolens_workspace#536): a shared-machinery finding from the
user-workspace slow-script diagnosis, traced to the unguarded call in the library and written
up as a diff there rather than patched per script. The measurement and the diff below are the
phase-8 executor's; nothing was applied to the library. Library-first gate: this lands before
any workspace script relies on it. Validation: the library unit tests plus a before/after of
the named workspace scripts under the smoke profile.

## (a2) PyAutoArray — capped interferometer / multi_dataset datasets are re-simulated on every run

**File** `autoarray/util/dataset_util.py`
**Functions** `_is_capped_at_the_current_cap`, plus a writer-side card in
`autonerves/fitsable.py` (`stamp_small_datasets_regime`)

`_is_capped_at_the_current_cap` requires **both** `SMALLDAT = T` **and** a measured
`data.fits` shape equal to `SMALL_DATASETS_SHAPE_NATIVE`. Its docstring explains why the second
half exists: the stamp records *"the env var was set at write time"*, not *"capped at today's
cap"*. Interferometer `data.fits` is `(n_visibilities, 2)` and multi_dataset prefixes its FITS
(`{waveband}_data.fits`), so neither family can ever corroborate the stamp by shape and both are
deleted and re-simulated on **every** run.

**Measured**: 5.2–6.5 s per script, of which ~4.5 s is the simulator subprocess's own import
floor. It is paid by 4 of the 37 `autolens_workspace` smoke entries and 5 of the 16
`autogalaxy_workspace` ones — roughly **26 s and 28 s per CI run respectively**, plus the same
cost on every local run of those scripts.

The fix removes the need for shape corroboration by recording the cap itself, which is the
proposition `_is_capped_at_the_current_cap` actually wants to test:

```diff
--- a/autonerves/fitsable.py
+++ b/autonerves/fitsable.py
@@
 SMALL_DATASETS_HEADER_KEY = "SMALLDAT"
+# The cap in force in the writing process, as "<rows>x<cols>". Absent on every
+# file written before this card existed, which readers must treat as "unknown".
+SMALL_DATASETS_SHAPE_HEADER_KEY = "SMALLSHP"
@@ def stamp_small_datasets_regime(header):
     header[SMALL_DATASETS_HEADER_KEY] = (small_datasets(), SMALL_DATASETS_HEADER_COMMENT)
+    if small_datasets():
+        from autoarray.util.dataset_util import SMALL_DATASETS_SHAPE_NATIVE
+        header[SMALL_DATASETS_SHAPE_HEADER_KEY] = "%dx%d" % SMALL_DATASETS_SHAPE_NATIVE
```

```diff
--- a/autoarray/util/dataset_util.py
+++ b/autoarray/util/dataset_util.py
 def _is_capped_at_the_current_cap(dataset_path):
-    return (
-        _small_datasets_stamp_on_disk(dataset_path) is True
-        and _is_small_datasets_on_disk(dataset_path)
-    )
+    if _small_datasets_stamp_on_disk(dataset_path) is not True:
+        return False
+    # Preferred: the writer recorded the cap it used, so no shape corroboration
+    # is needed and the families whose shape cannot corroborate (interferometer,
+    # multi_dataset, datacube) are covered for the first time.
+    recorded = _small_datasets_shape_on_disk(dataset_path)
+    if recorded is not None:
+        return recorded == SMALL_DATASETS_SHAPE_NATIVE
+    # Absent card -> pre-SMALLSHP file -> today's behaviour, unchanged.
+    return _is_small_datasets_on_disk(dataset_path)
```

plus a `_small_datasets_shape_on_disk` reader alongside `_small_datasets_stamp_on_disk`, and the
`{waveband}_data.fits` / `channel_XXX/` path resolution the existing "Known gap" section names
(without which multi_dataset and datacube still get no verdict and keep re-simulating).

Safety: the change only ever moves a dataset from *delete* to *keep*, and only when the writing
process recorded **exactly today's cap**. A stale dataset written at a different cap still has a
mismatching card and is still deleted, which is the property PyAutoArray#471 / PyAutoNerves#153
established.

**Alternative, if the header change is unwanted** (category (c)): cache `dataset/` between smoke
runs in PyAutoHeart's reusable `smoke-tests.yml`, keyed on the cap constant plus the simulator
scripts' hashes. That fixes CI only — the library patch also fixes every local run — and it
re-introduces the stale-dataset class the stamp exists to prevent unless the key is exactly right.
