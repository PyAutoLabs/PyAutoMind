SLaM `scripts/multi_dataset/features/slam/simultaneous.py` timed out at 1805 s
against the 1800 s per-script cap in PyAutoHeart's Release Integrate run
(https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194, profile
`release`), having passed in 355.7 s on 09-02 and 366.9 s on 09-03. The script
is back inside its baseline.

## Cause

autolens_workspace #523 (`17568188`) gave the `source_pix_2`, `light_lp` and
`mass_total` analyses — and by inheritance the SUBHALO stages — an adaptive
`over_sample_size_pixelization` map, `np.where(source_image_raw > 3.0, 4, 2)`,
in place of the dataset's uniform sub-size of 4.

The map has strictly *fewer* sub-pixels, and the script still got slower,
because the cost is JAX **compile**, not evaluation. A uniform sub-size bins the
over-sampled grid with one fixed-shape reshape and average
(`OverSampler.binned_array_2d_from`, the `sub_is_uniform` branch); a non-uniform
one bins ragged sub-pixel blocks with `jax.ops.segment_sum`, a general scatter,
and that branch is traced on every light-profile evaluation inside the
likelihood. No script in the workspace pays that compilation more often than
this one: once per SLaM stage, over every band jointly, and again for every cell
of the SUBHALO grid search — which is why the same #523 change left the
single-dataset scripts *faster* (`features/slam/independent.py` went 179.7 s →
166.4 s in the very same job), and why the per-PR smoke gate
(`PYAUTO_TEST_MODE=2`, `PYAUTO_DISABLE_JAX=1`) never saw it.

## What shipped

autolens_workspace #534 drops the three
`apply_over_sampling(over_sample_size_pixelization=...)` calls and the per-band
map they consumed; the analyses go back to
`result.max_log_likelihood_fit.dataset`. The `__Pixelization Over-Sampling__`
prose cell is rewritten to say what the single-dataset pipelines do and why they
are right to, why a simultaneous fit does not follow them, and — for anyone
adapting the script to their own multi-wavelength data — to raise the *uniform*
sub-size rather than make it adaptive. The notebook was regenerated.

Measured locally under the `release` profile environment:
**706.6 s → 366.3 s** (`EXIT=0`), against the 366.9 s baseline. Read the
within-run contrast rather than the absolute totals (the two runs were minutes
apart under different background load): with the map, `source_pix[1]` →
`source_pix[2]` goes 16.0 s → 38.3 s at exactly the stage the map is first
applied; without it the same pair is 11.2 s → 11.6 s, and the `source_pix[2]`
wall time goes 138 s → 42 s.

## Corrective-red note

The PR was opened while `pyauto-heart readiness` read **RED** with exactly one
reason — `release validation FAILED (stage integrate)` — and that reason *is*
this timeout. It shipped under the reason-scoped corrective-PR exception in
`PyAutoBrain/AUTONOMY.md`, stopping at PR-open
(https://github.com/PyAutoLabs/autolens_workspace/issues/533#issuecomment-5543678192);
merge was human, via `/prm`. Workspace repo, so no Heart freeze gate and no
`pending-release:` obligation.

## Follow-ups left open

Both are filed as drafts and neither is closed by this record:

- `draft/bug/autoarray/non_uniform_over_sample_jax_compile_cost.md` — the
  library-side compile cost of the non-uniform binning path, with this
  evidence. When it is gone, this script can go back to the adaptive map.
- `draft/bug/autolens_workspace/slam_simultaneous_subhalo_grid_search_fits_last.md`

## PRs

- workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/534 (MERGED,
  merge commit `ae7bd53b`; CI green on head `ecd78814` — Navigator Check 3 jobs,
  Smoke Tests 3.12 + 3.13, Script Size Guard)
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/533 (closed)

## Original prompt

# SLaM multi-dataset `simultaneous.py` times out (1805 s) after the #523 adaptive over-sampling change

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci
- hygiene
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Review-minutes: 5
Unattended: ready
Filed: 2026-09-04

## The finding

PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194
(profile `release`, per-script cap `BUILD_SCRIPT_TIMEOUT=1800`) hit
`TIMEOUT (1805s)` on `scripts/multi_dataset/features/slam/simultaneous.py`.

Timing history for the same script under the same profile:

| Date | Result |
|------|--------|
| 2026-09-02 | PASS 355.7 s |
| 2026-09-03 | PASS 366.9 s |
| 2026-09-04 | **TIMEOUT 1805 s** |

The runner is not the cause: every other `multi_dataset` script in the same job
ran at 0.74-1.03x its previous time (the sibling
`scripts/multi_dataset/features/slam/independent.py` went 179.7 s -> 166.4 s).

The only change to the script in that window is commit `17568188`
(autolens_workspace #523, "SLaM adaptive over-sampling thresholds the S/N map
once, from source_pix_2"), which added

```python
dataset.apply_over_sampling(
    over_sample_size_pixelization=al.Array2D(
        values=np.where(source_image_raw > 3.0, 4, 2), mask=...
    )
)
```

to the `source_pix_2`, `light_lp` and `mass_total` analyses, inherited by the
SUBHALO stages. #532 (`94665797`, per-band `DatasetModel`) does not touch those
calls.

The nominal sub-pixel count went **down** (the dataset default is a uniform
sub-size of 4, the new map is 4 on the bright source and 2 elsewhere), so the
suspect is the switch from a uniform `int` to a non-uniform `Array2D`
over-sample map on the `use_jax=True` pixelized + subhalo-grid-search path -
or a script-level misuse of the new API specific to this multi-dataset script.
`independent.py` makes the same change and got *faster*, so whatever is slow is
particular to the simultaneous (FactorGraph + subhalo) pipeline.

## What to do

1. Time the script per stage under the release-profile environment to find
   which search explodes.
2. Fix it minimally, keeping the script near its ~367 s baseline: prefer
   repairing a genuine misuse; otherwise drop the adaptive
   `over_sample_size_pixelization` from the affected stages of this script with
   a comment naming #523 and the follow-up.
3. If the cost is a library-side slow path for non-uniform over-sample maps,
   file that separately against PyAutoArray.
