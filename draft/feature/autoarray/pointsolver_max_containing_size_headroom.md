# Point-source CPU speed-up phase 4c — raise `MAX_CONTAINING_SIZE` headroom (15 → ~20, measured)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- PyAutoLens
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Epic: point-source-cpu-speed
Filed: 2026-09-26
Parent: active/pointsolver_cpu_speed_phase_4.md (issue autolens_profiling#314)

## Goal

Raise PyAutoArray's `MAX_CONTAINING_SIZE` from **15 to about 20**. Measure 18, 20 and 24 and pick
the smallest that clears the observed maximum with margin. The cap is the static per-step capacity
of containing triangles in the JAX `PointSolver`, and it silently truncates when exceeded. Human
decision (2026-09-26): accepted as a phase-4a follow-up.

## Evidence (phase 4a sweep, RAL job 356367, Xeon 8490H, fp64)

Source: `lens/autolens_profiling/results/breakdown/point_source_image/solver_config_sweep_hpc_ral_cpu_fp64.json`,
key `uncapped_containing_counts`, counted in NumPy with no cap on 200 prior draws. Ledger: campaign
note, "Phase 4a".

- **Default geometry** (±9.9″ / 0.2 / 1e-3): step 0 has median 9, p99 15 and **max 17, on prior draw
  12**.
  - 23 draws exceed 12, and **1 exceeds 15**.
  - Steps 1–7 peak at 13 / 11 / 9 / 7 / 5 / 5 / 5.
  - Draw 12 still passed completeness, because the truncated entries were the spurious fold-line
    candidates. That is luck, not a guarantee.
- Under ±2.5/0.4, step 1 reaches exactly 15 (p99 15). The headroom is zero there too, and a smaller
  workspace grid (see `draft/feature/autolens_workspace/pointsolver_grid_extent_per_package.md`)
  pushes counts up.
- The cap is load-bearing. MCS 8 and MCS 10 lose images (prior multiplicity 62 % and 86.5 %), at
  1.11× and 1.06× speed.

## Method

- Harness: `lens/autolens_profiling/scripts/point_source_image/likelihood_breakdown/solver_config_sweep.py`.
  Add MCS 18 / 20 / 24 routes (the `max_containing_size` block already exists).
- Report the cost of each as its own interleaved row: median, CI, compile, FLOPs and temp memory. The
  cap sets the refinement grid size (720 rows per step at MCS 15: 240 kept triangles × 3) and the `f64[60]` neighbourhood
  sorts, so expect a modest cost, and measure it.
- **Prove no image-set change** on the 200 prior + 200 stress draws against both the default and the
  reference, **except** where the old cap was truncating (draw 12 and any others the uncapped count
  flags). Those draws must be explained one by one.
- Fiducial log L `7.743201200876812` must stay bit-identical, or, if the padded shape changes it,
  explain why and re-pin deliberately. Check autolens_workspace_test `point_source/jax_likelihood/*`
  and `jax_grad/gradient.py` pins, and positions shape `(MCS, 2)`.
- Consider a **debug-mode overflow counter or warning**: a non-JAX or `jax.debug`-gated count of how
  often the uncapped containing set exceeds the cap, so truncation is never silent again. It must not
  cost anything on the default JAX path.
- A100 no-regression row if the default changes.

## Traps

- **The `__defaults__` binding trap.** `MAX_CONTAINING_SIZE` is a module constant, but
  `ArrayTriangles.__init__` and `for_limits_and_scale` bind it as a **default argument at import**.
  Patching the module constant alone does nothing. The 4a cell had to patch those functions'
  `__defaults__` too, and restore them by value. In the library change, make sure every default
  reads the new value (or switch to a `None` sentinel resolved at call time), and grep PyAutoLens for
  any copy of the constant.
- PyAutoArray is currently claimed by `interferometer-transform-real-scatter`. Check at `start_dev`.
  Coordinate with phase 4b (`pointsolver_step0_gather_containment.md`), which also touches the
  triangles code, and prefer landing 4b first.
