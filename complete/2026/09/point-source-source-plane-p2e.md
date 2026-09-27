## point-source-source-plane-p2e

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/334
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/336 (merge `17e2596`)
- epic: point-source-cpu-speed
- parent-record: complete/2026/09/point-source-gradient-mode.md
- campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Phase 2e of the source-plane point-source chi-squared campaign (single-source only): confirmation that the phase-2b/2c forward-mode gradient speed-up arrives through the real library path shipped in phase 2d (PyAutoFit#1649, PyAutoLens#752, pending release). Merged in autolens_profiling#336. Workspace-only.

**Shipped**
- `scripts/point_source_source/likelihood_breakdown/gradient_mode_library_ab.py` — runs `af.MultiStartAdam().fit(model, AnalysisPoint)` under a `jax.jit` recorder that captures the search's own `jax.jit(jax.vmap(_value_and_grad_finite))` step (built from `value_and_grad_from(fitness.call, mode)`) and aborts before compile; forward = declared default, reverse = `gradient_mode="reverse"`; B = 8, phase-2c L5 / L24 rungs, both lanes; gates, interleaved timing vs phase 2c, end-to-end fit walls.
- Results `results/breakdown/point_source_source/gradient_mode_library_ab_{local_cpu_fp64,hpc_ral_gpunode_cpu_fp64,hpc_a100_fp64}.{json,png}`; RAL submits (scratch clones at the merge commits — the shared RAL stack lacked them and was not touched); job log 359192; campaign note "Phase 2e" + verdict; README bullet.

**Result:** gates green on every host (mode resolution + log lines; fwd ≡ rev objective ≤ 6.2e-12, gradient ≤ 2.1e-9 over PRNGKey 0..15; end-to-end L5 same best vector ≤ 1.4e-12). Quiet RAL EPYC (job 359192) forward/reverse 0.455 / 0.580 / 0.364 / 0.562 (L5 solved / plain, L24 solved / plain) ≈ phase-2c batched ratios; library overhead ~0.03 ms/step at L5; L24 solved compile 95.9 → 11.2 s. A100 (job 359193) agrees (its L24 solved cell ran beside another host job; no claim rests on it).

**Campaign status:** phases 1–2e complete. Remaining candidates, not started: blackjax NUTS/SMC forward-mode `value_and_grad`; A100 `vmap` throughput row.

**Carried / done alongside**
- Bugs filed via intake: `draft/bug/autoarray/galaxy_duplicate_pytree_registration_after_jax_fitness.md`, `draft/bug/autogalaxy/power_law_multipole_m1_singular_at_isothermal_slope.md`.
- RAL cleaned: p2a–p2e worktrees, branches, bundles, `/mnt/ral/jnightin/p2d_check`.
- Root `activate.sh` rewritten to canonical mains (it pointed at the removed phase-2d bundle; worktree.sh bug prompt still open).
- Heart YELLOW at ship, acknowledged by the human.

## Original prompt

# Point-source source-plane chi-squared campaign — phase 2e: real MultiStartAdam forward vs reverse

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Epic: point-source-cpu-speed
Lane: any
Filed: 2026-09-27
Issued: 2026-09-27
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/334
Parent-record: complete/2026/09/point-source-gradient-mode.md
Campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Phase 2e of the campaign prompt above — the workspace follow-up approved in the phase-2d plan
(2026-09-27). Full plan on autolens_profiling#334.
