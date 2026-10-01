# Cluster PointSolver — robustness, analysis settings and performance

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- autolens_workspace_test
- PyAutoLens
- PyAutoArray
- PyAutoGalaxy
Themes:
- cluster
- point-source
- profiling
- jax
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: cluster-pointsolver-speed
Filed: 2026-09-26
Parent-record: complete/2026/09/point-source-cpu-p3.md

## Status and ownership — approved 2026-10-01

Canonical planning ledger for epic `cluster-pointsolver-speed` (identifier
retained; display title broadened). `autolens_profiling` is the execution/evidence
home for both “make autolens fast” and “which settings make the analysis robust”.
This expands the unstarted cluster speed campaign; it does not restart completed
single-source work. The profiling repo's `wiki/campaigns/cluster_pointsolver.md`
is the earlier speed-only survey, to be reconciled when the first campaign task
starts; this Mind contract governs the newly approved scope in the meantime.

Transferred from Source & Cluster arc:
- `draft/bug/autolens/point_solver_error_bisect_health.md`: remaining phase-1
  overflow, accuracy/identity and regression obligations, historical-bisect
  limitation disposition. Completed 1a–1d records remain in their original arc.
- `draft/research/autolens_profiling/point_solver_profiling_cells.md`: old phase-2
  coverage gaps, reconciled with current profiling taxonomy and the already
  completed single-source campaign before any issue is filed.
- Forward ShapeSolver rehabilitation/retirement and its finite-source convergence
  tests from arc phase 6. Primary pixel-based area magnification stays in the arc.

No task in this programme is issued by this transfer. Issue ONE bounded task at
a time as its predecessor nears shipping; not the umbrella and not a bulk queue.

## Working contract

1. **Robustness/settings evidence belongs in autolens_profiling.** Measure initial
   grid scale, extent, target precision, capacity, backend/dtype and applicable
   source/redshift regimes against independent numerical references. Publish the
   supported settings and their tested domain, unresolved outcomes, cost and
   provenance together. Shared library repairs remain general, not cluster-only.
2. **Numerical integration guarantees belong in autolens_workspace_test.** Distil
   every accepted repair/settings claim into bounded reproducible regressions:
   positions, per-image coverage, overflow, unresolved multiplicity, eager/JIT/vmap
   and registered-tracer/gradient behavior where affected. Name and wire a CI lane:
   cheap deterministic witnesses in required PR smoke; expensive coverage in the
   scheduled/release suite. A standalone opt-in diagnostic with no CI consumer is
   not completion of this regression obligation. Existing 1c/1d cells remain
   historical evidence in workspace_test; do not move or duplicate them wholesale.
3. **Performance measurement can begin before all repairs finish.** Label failing
   cases diagnostic/invalid and retain their timings, but exclude them from
   accepted speed-up and robust-settings claims. Matching the old likelihood is
   insufficient: require independent accuracy/coverage, no silent truncation and
   relevant derivative/batch checks before accepting an optimisation. Record
   compile, first-call and warmed costs separately on pinned hardware.
4. **Finite acceptance target.** Specify supported workloads/tolerances first;
   detect overflow, establish per-image accuracy/coverage, expose unresolved cases,
   and verify backend behavior. Do not use “trusted everywhere” as an unbounded
   exit condition or silently change scientific tolerances to win speed.
5. **Handoffs.** Profiling evidence → bounded library repair → CI regression →
   settings recommendation. Downstream Source & Cluster tasks depend on the
   concrete capability they use, not completion of this whole programme.

## Next task selection and workstreams

Next production candidate: observable containment-overflow contract under eager,
JIT and vmap, including caller invalid-result behavior and CI witnesses. Recheck
claims and approve the API design through start_dev before issuing it. The earlier
streaming #600 Array claim has closed; that is not a standing conflict waiver.
Representative cluster data and baseline profiling below can be scoped without
waiting for every accuracy question; failing configurations remain labelled.

Accuracy/identity work uses 1c/1d's counterexamples: three non-converged false
accepts from the local correction screen; adding convergence loses closest-cusp
coverage. Investigate safeguarded refinement/nonlinear error control, not another
unqualified distance/residual rule. Forward ShapeSolver work requires its own
bounded current-code audit, backend dispatch, per-image area/convergence evidence
and CI tests, or an explicit retirement decision. Preserve the old phase-6
requirement to compare any promoted forward implementation with independent
simulated area truth/pixel-based results; it no longer blocks the primary API.

Completed evidence: `complete/2026/09/point-solver-error-audit.md`,
`complete/2026/09/point-solver-padding-backend.md`,
`complete/2026/10/point-solver-duplicate-policy.md`,
`complete/2026/10/point-solver-image-accuracy.md`.

## User-approved expansion (verbatim)

Ok  I agreem autolens_profiling is evolving into "make autolens fast" but also "these are the settings I need to ensure the analysis is robust" so this work is also more and more belonging there, albeit we need numerical integration tests in autolens_workspace_test which ensure this all makes it way into CI. Update accordingly and then wrap up

## User request (verbatim)

Lets push through all work on single source, working in autolens_profiling/scritps/point_source, we will do cluster use case as as eparate epic so maybe move this as part of an intake that will do that whole thing starting from working out the data and likelihood_breakdown.

## Profiling workstream — cluster data and a released-code baseline

No lever is ranked until this exists. Deliverables:

1. **Work out the cluster data.** Pick one or more representative cluster datasets and justify them
   against real cluster modelling in `@autolens_workspace` (`scripts/cluster/`). For each, record:
   - the number of sources and source planes / redshifts;
   - the number of multiple images per source;
   - the lens model components (BCG, cluster-scale halo(s), member galaxies — profile types and
     counts, e.g. dPIE / NFW);
   - the solver grid (extent, `pixel_scale_precision`) production cluster fits actually use.

   The current profiling case (`dataset/cluster/simple`, gitignored and auto-simulated: 13 mass
   components, 3 planes, 2 sources) is a starting point, not a verdict.
2. **Audit and refresh `@autolens_profiling` `scripts/cluster/likelihood_breakdown/`.**
   `image_plane.py` and `source_plane.py` both exist; check them against the point-source
   instrument (`scripts/point_source/likelihood_breakdown/` plus the shared
   `scripts/misc/likelihood_breakdown/{timing,provenance,_profile_cli}.py`). Then bring them to the
   campaign measurement contract:
   - fused production likelihood control;
   - separated compile vs first vs warmed timings;
   - interleaved medians + CI;
   - `source_revisions`, thread environment, XLA memory and FLOPs recorded;
   - a per-step / per-component split (step 0 vs refinement, deflections vs bookkeeping, per
     source).
   - **Precision caveat:** the current cell runs `pixel_scale_precision=0.01` (to keep compile at
     minutes), not production `0.001`. Measure both, or justify the choice explicitly.
3. **Baseline on released code** (2026.9.26.1 or later, which carries point-source p2 + p3) on a
   pinned RAL CPU node (Xeon 8490H, `--nodelist`; check `sinfo` first), with an A100 row. Update
   the README dashboards. Record the per-step wall-time split, which then ranks phase 2+.

## Carried evidence (from point-source p1–p3; records `complete/2026/09/point-source-cpu-p{1,2,3}.md`, ledger `autolens_profiling/results/notes/point_source_cpu_campaign.md`)

- **Two-source cluster solved likelihood, per phase:**
  - p1 RAL baseline (Xeon 8490H): fused plain 128.05 ms, fused solved 134.52 ms, per-source solves
    110 / 115 ms. Per-source solves exceed the fused call, a fusion-boundary effect.
  - p2 vertex-dedup removal (RAL job 350582, EPYC 7763): 155.22 → 78.32 ms (1.98×). The control is
    +15–20 % from the host alone, so pin the node.
  - p3 static step-0 lattice (RAL job 350636, Xeon 8490H pinned): 47.36 → 9.085 ms (5.21×); 3.9–4.5×
    with constant folding on.
  - FLOPs: 184.2M → 139.4M → 39.5M.
  - XLA temp memory: 91.6 → 22.6 MB (A100 42.1 → 6.35 MB).
- **Lattice:** the 200×200 @ 0.7″ cluster step-0 lattice now deflects **46 516 of 276 507** unique
  vertices.
- **Where the cost is now (FLOP estimate, not measured):** deflections of the 13-component lens
  dominate every cluster step. Step 0 is ≈ 51 % of cluster FLOPs.
- **Lever: dPIE/NFW deflection cost.** This is likely a PyAutoGalaxy phase, separately scoped.
  `@autolens_profiling` `scripts/lens/deflections/` is **NumPy-only** and has **no dPIE spec**, so a
  JAX deflection cell with dPIE/NFW specs is a prerequisite for measuring it.
- **Lever: grid-extent guidance.** Stronger at cluster scale, where it acts on the ≈ 51 % step-0
  share plus containment. It needs image-completeness evidence across a prior, with each extent
  reported as its own configuration and never substituted into a speed row.
- **Unmeasured control:** direct deflections on the full 276 507-point cluster input. The old
  "cluster solve is at its deflection bound" claim was extrapolated, not measured.
- **Single-source phase 4a** (solver-config sweep: initial scale × precision,
  `MAX_CONTAINING_SIZE`, extent) may produce methods or findings reusable here. Read its ledger
  section before planning phase 2.

## Measurement contract

This inherits the point-source campaign contract (phase-4 prompt, "Campaign contract (2026-09-19)"):
- exact revisions recorded;
- interleaved A/B on identical hardware with distinct function objects + `jax.clear_caches()`;
- a fused production control;
- a correctness gate before any speed claim: bit-identical likelihood, solved positions,
  multi-source / multiplane coverage, JVP / vmap parity;
- negative results recorded;
- one bounded phase per issue and PR.

## Later performance candidates (re-rank after the baseline)

2. Deflection-cost lever (JAX dPIE/NFW deflection cell first; PyAutoGalaxy change separately scoped).
3. Cluster grid-extent guidance with completeness evidence.
4. Whatever the phase-1 split exposes (per-source batching, multiplane bookkeeping, capacity).
