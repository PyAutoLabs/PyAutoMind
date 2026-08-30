# Multi-plane time delays

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- point-source
- cluster
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready

Filed: 2026-08-27

Multi-plane time delays: the time-delay equivalent of the PyAutoLens#480 magnification fix.

#480 fixed magnification being measured at the tracer's last plane rather than the plane being
solved for. Time delays have the same shape of gap one level up, and it is now the blocking one:
with #480 fixed, multi-plane point-source modeling works, so a PointDataset can carry
`time_delays` for a system whose time delays cannot be computed.

Two distinct pieces.

1. `Tracer.time_delays_from` refuses more than two planes. `tracer_util.time_delays_from` raises
   `RayTracingException` when `len(plane_redshifts) != 2`, and its docstring says so plainly: "It
   requires a two-plane system (lens and source), and does not currently support multi-plane time
   delay calculations involving more than two planes, but it could be extended to do so in the
   future." This is an honest, enforced limitation rather than a silent wrong answer, which is why
   it is a feature and not a bug. Extending it needs the multi-plane time-delay formalism: the
   time-delay distance `D_dt = (1+z_l) D_d D_s / D_ds` is a two-plane construction, and the
   multi-plane generalisation is a sum of per-plane terms, not a substitution into the same
   expression.

2. `LensCalc.fermat_potential_from` silently mixes planes, and this one IS a latent bug of exactly
   the #480 kind. `LensCalc.from_tracer(tracer, use_multi_plane=True, plane_j=j)` binds the
   deflection callable to plane j via `functools.partial`, but takes
   `potential_2d_from = getattr(tracer, "potential_2d_from", None)` unchanged and passes it in both
   branches. `Tracer.potential_2d_from` is the sum over ALL galaxies with no plane awareness
   ("the summed 2D potential of all galaxies in the tracer"). So a plane-bound LensCalc computes
   `fermat_potential_from` as a plane-j geometric term minus an all-planes potential -- including
   the potential of deflectors at and beyond plane j, which should not contribute to a source at
   plane j. `from_tracer` binds half of what the plane affects.

   Not currently reached by `Tracer.time_delays_from`, which builds via `from_mass_obj(galaxies)`
   on a guarded two-plane system, so this is latent rather than live. It becomes live the moment
   anything constructs a plane-bound LensCalc and asks for a Fermat potential -- which is what
   extending time delays to multi-plane will do. Fix it as part of this, or guard it: a plane-bound
   LensCalc whose potential is not plane-bound should refuse `fermat_potential_from` rather than
   answer wrongly.

Also worth checking while in here: `time_delay_geometry_term_from` computes
`src = grid - deflections` then `0.5 * ((grid - src)**2)`, which reduces algebraically to
`0.5 * |alpha|^2`. Correct for two planes; confirm what it should be for multi-plane before reusing
it there.

Prior art to read first: PyAutoLens#480 and the branch that fixed it, which established the
`from_tracer(..., plane_j=...)` pattern and the ray-traced-Jacobian cross-check used to validate
plane-dependent quantities. Use the same cross-check here -- an independent oracle matters more for
time delays, where there is no equivalent of "the solver returns 0 images" to make an error obvious.

<!-- formalised by the Intake (Conception) Agent on 2026-08-27 from file:/tmp/claude-0/-home-user/73120990-acb3-5546-bddd-2d75b5a0c771/scratchpad/intake2.md -->
