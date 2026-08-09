# Fix JIT quick-update visualization output regressions

Type: bug
Target: health_fixes
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## 2026-08-09 — EVERY SCRIPT PATH BELOW IS STALE (they moved, they were not deleted)

Checked by the draft/ sweep. All 4 scripts named in § Scripts return **404** at the
paths written below, and **all 4 still exist** under a renamed layout. Do not read the
404s as "the scripts were deleted" or "this was fixed by removal".

Two systematic renames landed in both test workspaces since this prompt was filed:

```
scripts/jax_likelihood_functions/<dataset>/X.py  ->  scripts/<dataset>/jax_likelihood/X.py
scripts/<dataset>/modeling_visualization_jit.py  ->  scripts/<dataset>/visualization/modeling_visualization_jit.py
scripts/multi/...                                ->  scripts/multi_dataset/...
```

Verified in `autolens_workspace_test` (`4cea3f8c`, cloned) and
`autogalaxy_workspace_test` (raw, every path resolves 200). This is the **same rename
family** that cost a previous session time on
`draft/bug/autolens/jax_point_source_point_smoke_sentinel.md` — treat a 404 in this
cluster as path drift until proven otherwise.

Corrected paths:

| named in § Scripts | actual path on main | repo |
|---|---|---|
| `…/scripts/ellipse/modeling_visualization_jit.py` | `scripts/ellipse/visualization/modeling_visualization_jit.py` | autogalaxy_workspace_test |
| `…/scripts/imaging/modeling_visualization_jit.py` | `scripts/imaging/visualization/modeling_visualization_jit.py` | autogalaxy_workspace_test |
| `…/scripts/interferometer/modeling_visualization_jit.py` | `scripts/interferometer/visualization/modeling_visualization_jit.py` | autogalaxy_workspace_test |
| `…/scripts/point_source/modeling_visualization_jit.py` | `scripts/point_source/visualization/modeling_visualization_jit.py` | autolens_workspace_test |

### Parking state — read before assuming CI still exercises these

**1 of the 4 is parked.** `autolens_workspace_test` `config/build/no_run.yaml:30`:
`point_source/visualization/modeling_visualization_jit # SLOW 2026-07-08 - JIT + Part-2
live Nautilus fit exceeds 300s cap`. The three `autogalaxy_workspace_test` scripts are
**not** parked and should still be running.

Adjacent and worth knowing: `autolens_workspace_test` also parks its *own*
`imaging/visualization/modeling_visualization_jit` (SLOW 2026-07-30, "re-measured: times
out at the 300s cap") and `interferometer/visualization/modeling_visualization_jit`
(SLOW 2026-07-30, "local re-measurement OOM-killed"). Those two are not named in this
prompt but are the same script family, so the timeout problem is broader than the four
listed here.

**This changes what the prompt's premise means.** A parked script cannot fail in
release validation, so the 2026-08-07 release drive's Stage 3 result (51/51 jobs green,
`657p/0f/101s/0t` — note the **101 skips**) is *not* evidence these were fixed. Nothing
here is graded shipped; the failures are simply no longer being provoked. Note too that
the parkings are for **timeouts**, a different failure from the defect this prompt
describes — so unparking is a precondition for reproducing it at all.

Not re-graded here: whether the underlying defect still reproduces. That needs real
runs, which a cloud session cannot do.

---
## Context

Four test-workspace scripts expect real release-profile searches to invoke the JIT-cached
quick-update visualization path and produce fit images. CI reported missing files. Local
`main` still fails the ellipse, interferometer, and point-source cases, while imaging
passes.

Owners: @PyAutoFit, @PyAutoGalaxy, @PyAutoLens, @autogalaxy_workspace_test, and
@autolens_workspace_test.

## Scripts

- `autogalaxy_workspace_test/scripts/ellipse/modeling_visualization_jit.py`
- `autogalaxy_workspace_test/scripts/imaging/modeling_visualization_jit.py`
- `autogalaxy_workspace_test/scripts/interferometer/modeling_visualization_jit.py`
- `autolens_workspace_test/scripts/point_source/modeling_visualization_jit.py`

## Required work

1. Reproduce from clean output directories with JAX enabled and real release-profile
   searches.
2. Trace search update cadence, visualization dispatch, cached fit creation, output-path
   routing, and exception handling for all four dataset types.
3. Fix the shared library path where possible; do not add sleeps, weaken assertions, or
   fabricate image files in scripts.
4. Add focused tests proving quick updates invoke visualization and write the expected
   artifact for ellipse, imaging, interferometer, and point-source analyses.
5. Run owning-library tests and all four scripts under the release profile.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
