# Cluster PointSolver speed-up — work out the data and likelihood_breakdown, then rank levers

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
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

## Status

**Filed, not started.** Split out of the point-source CPU campaign (epic `point-source-cpu-speed`,
prompt `active/pointsolver_cpu_speed_phase_4.md`) by human decision on
2026-09-26. That campaign is now single-source only; everything cluster-scale lives here. Issue one
bounded phase at a time; this prompt stays the campaign intent until its phases are resolved.

## User request (verbatim)

Lets push through all work on single source, working in autolens_profiling/scritps/point_source, we will do cluster use case as as eparate epic so maybe move this as part of an intake that will do that whole thing starting from working out the data and likelihood_breakdown.

## Phase 1 — work out the cluster data and a released-code likelihood_breakdown baseline

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

## Later phases (sketch, re-rank after phase 1)

2. Deflection-cost lever (JAX dPIE/NFW deflection cell first; PyAutoGalaxy change separately scoped).
3. Cluster grid-extent guidance with completeness evidence.
4. Whatever the phase-1 split exposes (per-source batching, multiplane bookkeeping, capacity).
