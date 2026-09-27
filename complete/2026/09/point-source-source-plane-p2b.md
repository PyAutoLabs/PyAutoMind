## point-source-source-plane-p2b

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/325
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/327 (merge `4dc05a4`)
- epic: point-source-cpu-speed
- parent-record: complete/2026/09/point-source-source-plane-p2a.md
- campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Phase 2b of the source-plane point-source chi-squared campaign (single-source only): a backward-pass A/B that prototypes the gradient levers inside a profiling cell (no library edits), merged in autolens_profiling#327.

**Shipped**
- `scripts/point_source_source/likelihood_breakdown/backward_pass_ab.py` — routes `rev` (production `value_and_grad`), `fwd` (jacfwd over the flat parameter vector), `rev_jacrev`, `rev_analytic` (closed-form SIE Hessian), `fwd_analytic`; scoped monkeypatch of `LensCalc._hessian_via_jax`; correctness gate before timing; interleaved 20×20 timing with bootstrap CIs; pre-registered verdict block.
- Results `results/breakdown/point_source_source/backward_pass_ab_{local_cpu_fp64,hpc_ral_gpunode_cpu_fp64,hpc_a100_fp64}.{json,png}`; RAL submits; job log 357381; campaign note "Phase 2b" section; README bullet.

**Correctness:** green on every route/host/lane — Hessians ≤ 9.8e-16 vs jacfwd (incl. near-critical points); log L ≤ 1.7e-12; gradients ≤ 3e-11 over PRNGKey 0..15; eager ≡ JIT. `shear_yx_2d_from` returns `[:,0]=γ₂, [:,1]=γ₁`.

**Verdict (human re-based the rule onto the quiet RAL gpu-node EPYC 7702 row, job 357381; 8490H job 357380 cancelled — node 10-2 busy with DR1 arrays):**
- `fwd` GO: −46 % solved (0.636 → 0.341 ms), −38 % plain; A100 −24–34 %, compile 4.1 → 1.8 s; laptop −28–37 %. Flops unchanged — the saving is reverse-tape/dispatch structure.
- `rev_analytic` passes on CPU only and adds nothing over `fwd` — not pursued. `rev_jacrev` NO-GO (≤ 3 %).

**Next (human decision 2026-09-27):** phase 2c = workspace-only crossover study of fwd vs rev as `n_params` grows (5 → ~20: shear, multipoles, second lens) on RAL CPU + A100, then design the PyAutoFit gradient-entry-point switch from the measured crossover.

**Carried**
- Library bug: `Isothermal.convergence_2d_from` / `shear_yx_2d_from` not jit-traceable with traced `ell_comps` (`PowerLawCore.convergence_2d_from` calls `convergence_func` without `xp`; `autogalaxy/convert.py:80`) → intake as a PyAutoGalaxy bug.
- RAL cleanup: `/mnt/ral/jnightin/autolens_profiling_wt/point-source-source-plane-p2a`, `.../point-source-source-plane-p2b`, `p2b.bundle`, `p2b_worktree_add.log`, local branch in `/mnt/ral/jnightin/autolens_profiling`.
- Heart YELLOW at ship (manifest drift ×3, release validation incomplete), acknowledged by the human.

## Original prompt

# Point-source source-plane chi-squared campaign — phase 2b: backward-pass A/B

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Epic: point-source-cpu-speed
Lane: any
Filed: 2026-09-27
Issued: 2026-09-27
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/325
Parent-record: complete/2026/09/point-source-source-plane-p2a.md
Campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Phase 2b of the campaign prompt above (retained in `draft/` as the campaign intent; the campaign
contract there governs). Plan approved by the human 2026-09-27; full plan on issue #325.

## Context

Phase 2a (autolens_profiling#323, merged 2026-09-27) established the RAL CPU reference for the
single-source source-plane likelihood: fused solved forward 0.1465 ms, `jit(value_and_grad)` 0.331 ms
= **2.26× forward, +0.185 ms**, 4× compile. The pytree-flatten lever was kept NO-GO (0.0385 ms < 0.05 ms
bar), so the campaign promoted the **backward pass** as the largest absolute residue and the only one
that scales with the math.

Why the backward pass is expensive: the solved likelihood builds the precision tensor
`Wᵢ = Aᵢ⁻ᵀΘAᵢ⁻¹` from `LensCalc.jacobian_from` → `hessian_from` → `_hessian_via_jax`
(`PyAutoGalaxy/autogalaxy/operate/lens_calc.py:574`), a per-position `jax.jacfwd` of
`deflections_yx_scalar` under `jnp.vectorize`. `jax.value_and_grad` then runs **reverse mode over that
forward-mode Hessian** (reverse-over-forward on the deflection stack) for only **5 model parameters**
(SIE centre ×2, θ_E, ell_comps ×2) on 4 positions.

Phase 2b is a **bounded measurement phase**: prototype the candidate levers *inside the profiling cell*
(no library edits), gate them on correctness, A/B them interleaved on RAL CPU, and decide which (if
any) earns a library-first phase 2c. Same shape as phase 2a's `pytree_input_ab.py`.

## Levers under test (one route each, same harness)

| Route | What changes | Why it might win |
|---|---|---|
| `rev` (control) | `jax.value_and_grad(ll)` — production today | baseline |
| `fwd` | forward-mode gradient: `jax.jacfwd(ll, has_aux)` over the flat 5-vector, value returned as aux | 5 params ≪ size of the reverse tape; forward-over-forward avoids storing the Hessian's residuals |
| `rev_jacrev` | as `rev`, but the in-cell Hessian uses `jax.jacrev` instead of `jax.jacfwd` over `deflections_yx_scalar` | ordering study: 2 outputs × 2 inputs is square, so which ordering XLA fuses better is empirical |
| `rev_analytic` | as `rev`, but the SIE Hessian comes from the closed form `H_xx = κ+γ₁`, `H_yy = κ−γ₁`, `H_xy = γ₂` using `Isothermal.convergence_2d_from` / `shear_yx_2d_from` (`PyAutoGalaxy/autogalaxy/profiles/mass/total/isothermal.py:132`) | removes the inner derivative entirely, so the backward pass differentiates plain elementwise arithmetic |
| `fwd_analytic` | `fwd` + analytic Hessian | combined upper bound |

The Hessian swaps are injected by a scoped monkeypatch of `LensCalc._hessian_via_jax` **inside the cell
only** (context manager, restored after each route; asserted restored). Both lanes (solved,
plain) get each route; the plain lane's magnification path reads the same Hessian.

## Deliverables (autolens_profiling only)

1. `scripts/point_source_source/likelihood_breakdown/backward_pass_ab.py` — reuses the phase-2a harness
   pieces from `pytree_input_ab.py` (`_model`, `_analysis`, `register_model_pytrees`, `_vector_stream`,
   `_stats_ms`, `_median_ratio` bootstrap CI, `_compile_route`, `_timed_call`, provenance/JSON
   contract, `--config-name`, `AUTOLENS_PROFILING_SMOKE=1`). Import or copy per the repo's existing
   convention between sibling cells (check how `pytree_input_ab.py` relates to `source_plane.py`
   first; do not refactor the shipped cell).
   Rows per lane × route: lower / compile seconds, first call, warmed median ms (20 rounds × 20 calls,
   **interleaved** round-robin across routes, `block_until_ready`, parameters varied per call
   through the production likelihood), ratio vs `rev` with bootstrap 90 % CI, XLA flops where
   available.
2. **Correctness gate before any timing** (a route that fails is reported, never timed):
   - analytic vs jacfwd Hessian components: rtol 1e-10 at the dataset positions **and** at a
     near-critical set (positions stepped toward the tangential critical curve) and perturbed models;
   - every route's log L equals `rev` to rtol 1e-10; gradient vs `rev` to rtol 1e-8, finite and
     non-zero; sweep `PRNGKey` 0..15 for the parameter draws (single-key gradient checks are coin
     flips — memory gradKeys);
   - eager ≡ JIT parity for each route.
3. Results `results/breakdown/point_source_source/backward_pass_ab_{local_cpu_fp64,hpc_ral_cpu_fp64,hpc_a100_fp64}.{json,png}`,
   RAL submits `hpc/batch_cpu/submit_backward_pass_ab_point_source_source_ral_cpu_fp64` and
   `hpc/batch_gpu/submit_backward_pass_ab_point_source_source_a100_fp64` (mirror the phase-2a submit
   files; CPU on the quiet 8490H node, `--nodelist` pinned, record CPU model).
4. Campaign note: new `## Phase 2b — backward-pass A/B` section in
   `results/notes/point_source_source_plane_campaign.md` with the table, the go/no-go verdict and the
   corrected residue; README hand-bullets + `build_readme.py` regeneration if the README lists
   breakdown rows.

## Go / no-go rule (pre-registered, same shape as 2a)

A route is **GO for phase 2c (library-first)** if on RAL CPU its `value_and_grad`-equivalent call saves
**≥ 0.05 ms AND ≥ 15 %** vs `rev` (90 % CI excluding the bar), with the correctness gate green.
- `rev_analytic` / `rev_jacrev` GO → phase 2c = PyAutoGalaxy analytic/ordered `hessian_from` for
  `Isothermal` (and the general dispatch), GPU regression check, then refreshed rows.
- `fwd` GO → phase 2c = the PyAutoFit gradient entry point (forward-mode `jacfwd` when
  `n_params` is small), which is a sampler-facing change — flagged for your decision, not assumed.
- Nothing GO → record the negative result; the source-plane single-call campaign is at its floor on
  CPU and the next candidate is the A100 `vmap` throughput row (residue item 5).

Compile time is reported alongside but is not part of the rule.

## Execution

- Worktree `~/Code/PyAutoLabs-wt/point-source-source-plane-p2b`, branch
  `feature/point-source-source-plane-p2b`, repo `autolens_profiling` only.
- **Parallel claim:** `autolens_profiling` is also claimed by `point-source-cpu-p4` (#321),
  `pointsolver-step0-gather` (p4b) and `interferometer-mesh-breakdown-a100`. This phase touches only
  the new cell, `results/breakdown/point_source_source/backward_pass_ab_*`, the two new submit files,
  the source-plane campaign note and README rows — disjoint from all three, as in phase 2a. Needs
  your approval for its own worktree.
- Delegation: implementation, laptop lead run and the RAL submit/pull delegated to an Opus subagent
  with a progress file + Monitor; planning, the verdict and the note's decision paragraph stay here.
- Ship via `/ship_workspace` (no library PR in this phase).

## Verification

- `AUTOLENS_PROFILING_SMOKE=1 python scripts/point_source_source/likelihood_breakdown/backward_pass_ab.py`
  exits 0 in the worktree; full laptop run produces the JSON/PNG and the correctness gate block.
- RAL CPU + A100 rows via `hpc/sync push-submit`, logs pulled (scp batch_cpu logs by hand).
- `python build_readme.py --check` clean; repo lint (the PR's `lint` job) green.
- Assert `PYTHONPATH` points at the library mains and the JSON `source_revisions` match them
  (memory activatePP) before any timing.
