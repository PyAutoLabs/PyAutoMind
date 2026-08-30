# Restore lensing-of-lens in the multiple_sources workspace example

Type: feature
Target: workspaces
Themes:
- point-source
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised — UNBLOCKED 2026-08-27, ready to start
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-04-28 (backfilled from git)

Revisit `@autolens_workspace/scripts/point_source/features/multiple_sources/` now
that PyAutoLens#480 is fixed.

## UNBLOCKED — #480 shipped 2026-08-27

PyAutoLens#480 (PointSolver magnification filter used the tracer's last plane
instead of `plane_redshift`) was fixed in PyAutoLabs/PyAutoLens#712, merged
`c1bba66`, and the issue is closed. Record:
`complete/2026/08/point-solver-magnification-plane-redshift.md`.

`Difficulty` drops `too-large` -> `large`: that rating carried the "first fix #480"
leg, which is now done. What remains is the workspace work in steps 1-7 below.

### The validation asked for below was done — and the doubt was well placed

The original text (kept verbatim at the end of this section) asked for explicit
tests removing the mass profile and varying `magnification_threshold`, saying
"I'm a bit unsure I totally buy it". Both were run. The cause is confirmed, and
the skepticism turned out to point at something real: **the bug is
configuration-dependent, and removing source_0's mass profile masks it.**

Measured on the #480 tracer (lens z=0.5 R_E=1.6; source_0 z=1.0; source_1 z=2.0),
solving for source_0 at `plane_redshift=1.0`:

| source_0 | mu at z=1.0 (correct) | mu at z=2.0 (what the old code measured) | old code's result |
|---|---|---|---|
| **with** mass (R_E=0.2) | `27.9  9.06  23.1  16.0` | `7e-3  2e-3  1e-3  2e-3` | all rejected -> **0 images** |
| **without** mass | `27.9  9.06  23.1  16.0` | `1.86  1.54  2.38  2.56` | survive -> **4 images** |

Three things follow, and they matter for this task:

1. **This is why the simplified example worked.** Dropping source_0's mass was not
   incidental to the workaround — it removes the very condition that triggers the
   bug. Only a *compact* deflector at the intermediate plane de-magnifies hard
   enough (by ~3-4 orders of magnitude) for the 0.1 threshold to reject every
   candidate. Restoring that mass in step 1 is exactly what would have re-broken
   the example before #712.
2. **`magnification_threshold=0.0` recovers the candidates in both rows**, which is
   what isolates the fault to the post-filter rather than the triangle search.
3. **mu at z=1.0 is identical in both rows.** Correct physics — a deflector sitting
   *at* plane j does not affect the mapping *to* plane j — and a useful sanity
   check that the fixed path is measuring what it claims.

Beyond this, the fix was cross-checked three ways at the solved plane (NumPy
Richardson FD, exact JAX autodiff in float64, and a ray-traced Jacobian sharing no
code with the Hessian path), agreeing to 1.7e-08. See the completion record.

> Original request, kept for provenance: *"First, let's fix
> https://github.com/PyAutoLabs/PyAutoLens/issues/480. I want you to first validate
> that the cause of the issue described there is actually right. I'm a bit unsure I
> totally buy it, so do some explicit tests which more directly remove the mass
> profile but also edit the `magnification_threshold` setting. I'm happy to be
> convinced, but need a bit more confirmation."*

When that workspace example was first written (autolens_workspace issue #97),
the upstream PointSolver bug made it impossible to simulate or fit a configuration
where the intermediate source itself acts as a deflector for the further source.
To unblock the multi/factor-graph tutorial, the example was simplified so the
only deflector is the foreground lens — both source galaxies are point-only at
different redshifts, no source-plane mass profile.

This task restores the original "double Einstein cross" intent now that the
PointSolver bug is fixed:

1. Update `simulator.py` so source_0 (z=1.0) regains its `Isothermal` mass profile
   at (0.02, 0.03) with `einstein_radius=0.2` and a small ellipticity. Source_0
   should now genuinely lens source_1 in addition to the foreground lens.
2. Verify the simulator still runs end-to-end with a single tracer
   `[lens, source_0_with_mass, source_1]` and that `solver.solve(plane_redshift=1.0)`
   returns >=4 image-plane positions for source_0.
3. Update `modeling.py` so the model includes source_0's mass:
     - `source_0 = af.Model(al.Galaxy, redshift=1.0, mass=al.mp.Isothermal, point_0=al.ps.Point)`
   The lens model dimensionality goes from N=9 to N=14.
4. Decide whether the `AnalysisFactor` for source_0's dataset should fit using
   the full multi-plane model or a sub-model excluding source_1. With #480 fixed,
   the full multi-plane model should fit cleanly and is preferred — both factors
   share `lens` and `source_0.mass` priors, the factor graph sums log-likelihoods.
5. Re-run end-to-end with `PYAUTO_TEST_MODE=2` (no `PYAUTO_SMALL_DATASETS`) to
   confirm the simulator and modeling both work, then regenerate notebooks.
6. Update the script docstrings and the folder/feature README to mention the
   lensing-of-lens richness again, and remove any "simplified to work around
   PyAutoLens #480" comments.
7. **Remove the two `no_run.yaml` exclusions** (not in the original text, and the
   step that actually re-enables the example). In @autolens_workspace
   `config/build/no_run.yaml`:

   ```
   - point_source/features/multiple_sources/simulator # Blocked by PyAutoLens #480: ...
   - point_source/features/multiple_sources/modeling # Blocked by PyAutoLens #480: ...
   ```

   Match on the entry text, not line numbers — those have drifted twice already.
   Note it is **two** scripts, simulator *and* modeling. Until these go, the
   scripts stay out of harness execution however good the code is.

## Downstream: this unblocks a second prompt

`draft/bug/pyautolens/point_source_json_datasets_record_no_regime.md` is parked
behind exactly the `no_run.yaml` exclusion in step 7 — that exclusion is the sole
reason its exposure is not live. Its re-check log now names those entries
disappearing as its trigger. Doing step 7 fires it, so re-read that prompt when
this task lands rather than leaving it parked another cycle.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
