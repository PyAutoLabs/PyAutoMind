# autolens_profiling lint is red on main: XLA census PSF anchors point at stale PyAutoArray `convolver.py` line ranges

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: the `lint` workflow is green on autolens_profiling main against current PyAutoArray main, `test_census_anchors_verify_against_the_installed_pyautoarray` passes, and a re-run of autolens_profiling#532's lint goes green with no change to that PR
Review-minutes: 5
Unattended: ready
Lane: any
Filed: 2026-11-24

Original request (human, 2026-11-24, after `/prm` refused autolens_profiling#532 on red lint): "File the bug"

## The failure

The `lint` workflow has been red on autolens_profiling `main` since
2026-11-22 (last green 2026-11-16). It blocks every PR in the repo, and
autolens_profiling#532 (`stale_auto_simulated_cluster_dataset`, shift
2026-11-24-am) is waiting on it. One test fails, on `main` and on the PR alike:

```
FAILED scripts/misc/likelihood_breakdown/test/test_xla_attribution.py::test_census_anchors_verify_against_the_installed_pyautoarray
AssertionError: ['def convolved_mapping_matrix_from spans [(1153, 1330)], not enclosed by the census range 1086-1300',
                 'def _convolved_mapping_matrix_over_sampled_jax_from spans [(731, 750)], not enclosed by the census range 670-691',
                 'ok']
```

`main`'s only commits in that window are hook propagation, so nothing in
autolens_profiling changed. PyAutoArray `main` moved: functions in
`autoarray/operators/convolver.py` shifted down by about 60 lines, and the
census's hard-coded line ranges no longer enclose them.

## Where

`scripts/misc/likelihood_breakdown/xla_attribution.py`, the
`psf_convolution_mapping_matrix` `StageRule`s and their `requires=` (around
lines 781-800 on main): the ranges `(1086, 1300)`, `(632, 642)` and
`(670, 691)`. The comment above them names the ranges too (`1086-1300`,
`520-700`, `1000-1085`). `CENSUS_ANCHORS` and `census_anchor_status()` are in
the same module.

## Fix

1. Re-derive each `convolver.py` range from current PyAutoArray main. The
   census already reports the live spans (`1153-1330`, `731-750`); check the
   other ranges, `632-642` and the image-helper ranges, the same way. Update
   the rules, `requires=` and the comment together.
2. Check that attribution still assigns the PSF rows
   (`fft_convolver_total`, `fft_mapping_matrix`, `fft_image`,
   `conv_mapping_matrix`) to `psf_convolution_mapping_matrix`. That means the
   full `scripts/misc/*/test/` suite passes, not just the one test.
3. Out of scope, but say in the PR if it looks cheap: ranges tied to line
   numbers break every time PyAutoArray moves code. Deriving them from function
   spans at census time would stop this recurring. That would be a follow-up
   prompt, not part of this fix.

## Notes

- PyAutoArray is claimed by `likelihood-lifecycle-p5b-array`. This fix only
  edits autolens_profiling, so the claim does not block it. If p5b moves
  `convolver.py` again before this merges, the ranges need re-deriving.
- After this merges, re-run autolens_profiling#532's lint and `/prm` it.
