# One construction path for plane-bound lensing quantities

Type: refactor
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- point-source
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

Filed: 2026-08-27

Give plane-bound lensing quantities one construction path instead of three hand-rolled ones.

Motivated by PyAutoLens#480, where the solver measured magnification at the wrong plane for four
months. The fix was small, but the reason the bug existed is structural: every caller that needs a
lensing quantity "at plane j" builds its own LensCalc, resolves the plane index by its own key, and
nothing checks the answers agree.

The three sites today:

- `AbstractFitPoint.magnifications_at_positions` (autolens/point/fit/abstract.py) --
  `use_multi_plane = len(self.tracer.planes) > 2`, then
  `plane_j = tracer.extract_plane_index_of_profile(profile_name=self.name)`, then
  `ag.LensCalc.from_tracer(...)`.
- `_lens_calc_for` (autolens/point/fit/solved.py) -- the same six lines again, duplicated
  deliberately with a comment saying it "Mirrors AbstractFitPoint.magnifications_at_positions".
- `ShapeSolver._filter_low_magnification` / `_plane_grid` (autolens/point/solver/shape_solver.py) --
  resolves by redshift instead, via `plane_index_via_redshift_from`. This is the one that was
  wrong; it now shares a `_plane_index` helper between the search and the filter, which is a local
  fix of the same duplication one level down.

So the plane is resolved by profile name in two places and by redshift in a third, and the fit
carries its answer to the solver as `plane_redshift = planes[plane_index].redshift` -- a
name -> index -> redshift -> index round trip across two modules. It happens to be consistent (there
is now a test pinning it), but nothing structural makes it so.

Two further smells worth folding in:

- `use_multi_plane = len(planes) > 2` is a no-op distinction. `Tracer.deflections_yx_2d_from`
  dispatches to `deflections_between_planes_from(0, -1)` whenever `total_planes > 1`, so the
  `use_multi_plane=False` branch of `from_tracer` wraps the same callable as the True branch with
  `plane_j=-1`. Two code paths, one behaviour. Verified numerically during #480: magnifications
  compare bit-identical, max|diff| = 0.0, for multi-plane and single-plane tracers alike.
- `from_tracer` binds the deflection callable to the plane but leaves `potential_2d_from` as the
  tracer's all-planes sum, so a plane-bound LensCalc is only half plane-bound. Filed separately as
  the multi-plane time-delay task; a refactor here should make that shape impossible to express
  rather than leave it to be remembered.

Likely direction, to be decided in the task: a single accessor on Tracer -- something like
`tracer.lens_calc_at(plane_index=... | redshift=... | profile_name=...)` -- that resolves the plane
once, binds every plane-dependent callable consistently, and is the only way the point-source code
obtains one. Behaviour-preserving: the #480 tests, the fit/solver agreement test and the
ray-traced-Jacobian cross-check already pin the numbers this must not change.

<!-- formalised by the Intake (Conception) Agent on 2026-08-27 from file:/tmp/claude-0/-home-user/73120990-acb3-5546-bddd-2d75b5a0c771/scratchpad/intake3.md -->
