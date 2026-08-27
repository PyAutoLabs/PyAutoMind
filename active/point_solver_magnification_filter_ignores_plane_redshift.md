# PointSolver magnification filter ignores plane_redshift

Type: bug
Target: pyautolens
Repos:
- @PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-27
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/480

GitHub issue **PyAutoLens#480** already exists (filed 2026-04-28 by Jammy2211,
untouched since). This prompt is the Mind-side record for fixing it; no new issue
should be opened.

## Why now

#480 is the gate on two other pieces of work, which is what surfaced it:

- `point_source/features/multiple_sources/{simulator,modeling}` are excluded from
  harness execution in @autolens_workspace `config/build/no_run.yaml:41-42`,
  named as blocked by #480.
- `draft/bug/pyautolens/point_source_json_datasets_record_no_regime.md` is parked
  behind exactly that exclusion — its re-check log names #480 closing as the
  single trigger for doing the work.

So this is one fix that clears a workspace exclusion, two skipped scripts and a
parked Mind task.

## The bug

`PointSolver.solve(..., plane_redshift=z)` returns 0 positions whenever `z` is an
**intermediate** plane of a multi-plane tracer. The triangle search is fine —
`magnification_threshold=0.0` recovers the candidates — only the magnification
post-filter rejects them, because it measures magnification at the wrong plane.

Two methods on the same class disagree about which plane is being solved for:

- `autolens/point/solver/shape_solver.py:224` — `_plane_grid` **honours**
  `plane_redshift`: `plane_index_via_redshift_from(redshift=...)`, then
  `tracer.deflections_between_planes_from(grid=..., plane_i=0, plane_j=plane_index)`.
- `autolens/point/solver/shape_solver.py:322` — `_filter_low_magnification` takes
  no `plane_redshift` at all. It builds `ag.LensCalc.from_mass_obj(tracer)`, whose
  deflection callable is the whole tracer, i.e. the **last** plane.

The search therefore solves to plane *j* and the filter judges those candidates
as if they were at plane *-1*. In the issue's repro (z = 0.5 / 1.0 / 2.0, solving
for z=1.0) the candidates come back at magnification ~1e-3–1e-5 — correct for a
z=2.0 source, meaningless for the z=1.0 one — and the 0.1 threshold discards
every one of them.

`point_solver.py:242` is the call site that drops the argument on the floor: it
has `plane_redshift` in scope (it passed it to `solve_triangles` seven lines
earlier) and does not forward it.

## The fix already exists as API — do not write new physics

@PyAutoGalaxy `autogalaxy/operate/lens_calc.py:165` already provides:

```python
LensCalc.from_tracer(tracer, use_multi_plane=True, plane_i=0, plane_j=-1)
```

which binds `tracer.deflections_between_planes_from` with those plane indices via
`functools.partial` — precisely the callable `_filter_low_magnification` should
be measuring against. The solver is simply calling the wrong constructor.

**It is a provable no-op for the default case**, which is what #480 asks for.
`autolens/lens/tracer.py:879-881`:

```python
if self.total_planes > 1:
    return self.deflections_between_planes_from(grid=grid, xp=xp)
return self.deflections_of_planes_summed_from(grid=grid, xp=xp)
```

`deflections_between_planes_from` defaults to `plane_i=0, plane_j=-1`, so for any
multi-plane tracer `from_mass_obj(tracer)` and `from_tracer(tracer, plane_j=-1)`
wrap the *same* callable. Single-plane tracers have one plane, so the summed and
between-planes forms agree there too. Passing `plane_j=-1` when `plane_redshift is
None` changes nothing — this is not an argument that needs a tolerance, it is the
same function.

## The fit side already does this — the solver is the half that was never wired

Worth stating because it changes what this task is: not "choose how to measure magnification at a
plane", but "finish a feature the rest of the point-source code already has".

@PyAutoLens `autolens/point/fit/abstract.py:125-134`, `magnifications_at_positions`:

```python
use_multi_plane = len(self.tracer.planes) > 2
plane_j = (
    self.tracer.extract_plane_index_of_profile(profile_name=self.name)
    if use_multi_plane else -1
)
od = ag.LensCalc.from_tracer(
    tracer=self.tracer, use_multi_plane=use_multi_plane, plane_j=plane_j
)
```

`_lens_calc_for` in `autolens/point/fit/solved.py:65-82` mirrors it for the Jacobian weighting. So
`LensCalc.from_tracer(..., plane_j=...)` is the established pattern for exactly this measurement,
and `from_tracer` exists in @PyAutoGalaxy to serve it. The solver is the single place it never
reached. The two resolve `plane_j` by different keys, each correct for its own API: the fit knows
the profile *name* (`extract_plane_index_of_profile`), the solver is handed a *redshift*
(`plane_index_via_redshift_from`).

**The two halves of one likelihood evaluation therefore disagreed.**
`autolens/point/fit/positions/image/abstract.py:124-130` already passes the redshift down:

```python
return self.solver.solve(
    tracer=self.tracer,
    source_plane_coordinate=self.source_plane_coordinate,
    xp=self._xp,
    plane_redshift=self.plane_redshift,
    remove_infinities=False,
)
```

and `plane_redshift`'s own docstring (`abstract.py:187-199`) says it exists "to ensure that if
multi-plane tracing is used when solving the model image-plane positions, the correct source-plane
is used". So for an intermediate-plane source, `model_data` measured magnification at the last
plane and returned nothing, while `magnifications_at_positions` measured at the source's own plane
and was right. That is the mechanism behind #480's "AnalysisPoint log-likelihood evaluation fails"
impact line.

`autolens/analysis/result.py:115` and `:184` pass `plane_redshift` too. The argument was plumbed
end-to-end through the callers; only the last consumer ignored it.

## Scope

1. Give `_filter_low_magnification` a `plane_redshift: Optional[float] = None`
   parameter and switch its constructor to `ag.LensCalc.from_tracer(...)` with the
   resolved `plane_j`.
2. Forward `plane_redshift` from `point_solver.py:242`.
3. Extract the `plane_redshift -> plane_index` resolution (currently inline in
   `_plane_grid`) into one helper both methods call. The bug was two methods
   disagreeing about the plane; leaving two copies of the resolution invites the
   same drift back.
4. Handle the unmatched-redshift case while in there. `plane_index_via_redshift_from`
   returns `None` when no plane is within its 1e-8 tolerance, and `_plane_grid`
   then evaluates `traced_grids_list[None]` and raises a bare `TypeError`. A
   mistyped redshift should say which redshifts the tracer actually has. This is a
   latent bug on the same lines, not scope creep.

## Testing

**The reason this shipped is that nothing tests it.** No test under
`test_autolens/point/triangles/` passes `plane_redshift` to the solver at all —
the multi-plane solve path has zero coverage. Adding that coverage is the larger
half of this task.

- The #480 repro becomes the regression test: a z=0.5/1.0/2.0 tracer, solve for
  the z=1.0 source, assert 4 positions rather than 0.
- Assert the no-op directly: for a multi-plane tracer, `plane_redshift=None` and
  `plane_redshift=<last plane's z>` return identical positions to the current
  implementation.
- Cover the unmatched-redshift error from scope item 4.
- The JAX path shares `_filter_low_magnification`, so check the padded/static-shape
  path is unaffected (`test_use_jax.py`, `test_implicit_diff.py`).

## Downstream, out of scope here

#480's own text notes that @autolens_workspace simplified its multi-source example
to work around this (dropping the intermediate source's mass profile), and wants
that reverted once fixed. That is a separate workspace task — this prompt is the
library fix. Removing the `no_run.yaml` entries should follow the fix, not ride
along with it.

<!-- Sizing: small. The fix is ~15 lines against an API that already exists; the
     missing multi-plane test coverage is the real work. -->
