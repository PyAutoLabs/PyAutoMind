# Point-source source-plane chi-squared campaign — phase 2c: fwd vs rev gradient crossover

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
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/329
Parent-record: complete/2026/09/point-source-source-plane-p2b.md
Campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Phase 2c of the campaign prompt above (retained in `draft/`; its campaign contract governs). Plan
approved by the human 2026-09-27; full plan on issue #329.

## Context

Phase 2b (autolens_profiling#327, merged 2026-09-27) found that computing the gradient of the
source-plane point-source likelihood in forward mode (`jax.jacfwd` over the flat parameter vector)
instead of reverse mode (`jax.value_and_grad`) cuts the call by 38–46 % on RAL CPU and 24–34 % on
the A100, at **5 free parameters** (one SIE). Forward mode costs one JVP per free parameter, while
reverse mode costs a roughly constant multiple of the forward call, so forward mode must lose above
some crossover `n*`. A production switch in PyAutoFit therefore has to be conditional on `n_params`.

You chose (2026-09-27) to **measure the crossover first**, workspace-only, and design the PyAutoFit
switch from the measured `n*` afterwards. This phase delivers that curve plus a short design memo
listing where the switch could live. No library edits.

## What gets measured

A model-complexity ladder on the same seeded single-source `simple` dataset (single-source only, per
the campaign scope). Extra components are added with priors centred on zero perturbation so the
likelihood stays well-defined on the SIE-simulated data:

| Rung | Solved-lane free params | Added component |
|---|---|---|
| L5 | 5 | `Isothermal` (phase 2b baseline) |
| L7 | 7 | + `ExternalShear` |
| L9 | 9 | + `PowerLawMultipole` m=4, free `multipole_comps` (centre/θ_E/slope tied to the SIE) |
| L11 | 11 | + m=3 multipole comps |
| L16 | 16 | + a second `Isothermal` (satellite) at the lens redshift |
| L~20 | 19–21 | Isothermal → `PowerLaw` (free slope) + satellite shear or m=1 comps (exact count recorded) |

The plain lane (`FitPositionsSource`, free source centre) runs the same ladder at +2 parameters.

Per rung × lane, routes `rev` (control) and `fwd`:
- **single call**: `value_and_grad`-equivalent, warmed median, 20 rounds × 20 calls interleaved,
  bootstrap 90 % CI on the ratio `fwd / rev`;
- **batched call**: `jit(vmap(...))` over B = 8 parameter vectors, because the multi-start gradient
  search evaluates its starts this way (`multi_start_gradient/search.py:1089`);
- lower + compile seconds, XLA flops when available.

Output per host: the ratio curve `fwd/rev` vs `n_params` and a crossover estimate `n*` (the
interpolated point where the ratio reaches 1, with a bootstrap interval), for single and batched
calls.

## Correctness gate (before timing, per rung)

- `fwd` value and gradient equal `rev` (log L rtol 1e-10, gradient rtol 1e-8), finite and non-zero,
  over PRNGKey 0..15 draws (`autofit.jax.register_model` registered; memory grad0 / gradKeys);
- eager ≡ JIT; no route reuses another's compiled executable (StableHLO hash check, as phase 2b).

## Deliverables (autolens_profiling only)

1. `scripts/point_source_source/likelihood_breakdown/gradient_mode_crossover.py`, built from the
   phase-2b harness `backward_pass_ab.py` (same self-contained flat-script convention, provenance
   and JSON contract, `--config-name`, `AUTOLENS_PROFILING_SMOKE=1`, PNG of the ratio curve with CI
   bands, single vs batched).
2. Results `results/breakdown/point_source_source/gradient_mode_crossover_{local_cpu_fp64,hpc_ral_gpunode_cpu_fp64,hpc_a100_fp64}.{json,png}`;
   RAL submits `hpc/batch_cpu/submit_gradient_mode_crossover_point_source_source_ral_cpu_fp64` and
   `hpc/batch_gpu/submit_gradient_mode_crossover_point_source_source_a100_fp64` with a measured
   WALL-BASIS (`check_submits.py --check`).
   **Reference CPU host = the quiet gpu-partition CPUs (EPYC 7702, no `--gres`)**, for continuity with
   the phase-2b verdict you re-based. The 8490H is not the reference this phase; it is run only if
   the `ral` partition is quiet at submit time, as an extra row.
3. Campaign note: `## Phase 2c — gradient-mode crossover` in
   `results/notes/point_source_source_plane_campaign.md`: the ladder, gate table, ratio tables,
   `n*` per host (single and batched), compile times. README hand-bullet; `build_readme.py --check`.
4. **Design memo** (a subsection of the same note, main session writes it). It lists the PyAutoFit
   gradient call sites a switch would touch, found in this survey:
   - `Fitness.grad` — `autofit/non_linear/fitness.py:933` (`jax.grad(self.call)`);
   - multi-start gradient — `autofit/non_linear/search/mle/multi_start_gradient/search.py:974`
     and `:1072` (`jax.value_and_grad`, vmapped at `:1089`);
   - blackjax NUTS / SMC — `autofit/non_linear/search/mcmc/blackjax/{nuts,smc}/search.py`.
   It also gives the measured `n*`, and the options: an opt-in flag, or an automatic switch on
   `n_params < threshold`. Picking one is your decision before any library phase is issued.

## Out of scope

- Library edits of any kind, including the carried `Isothermal` jit-traceability bug (that goes to
  intake separately).
- Analytic-Hessian routes (phase 2b showed they add nothing on top of `fwd`).
- Cluster / multi-source models (epic `cluster-pointsolver-speed`).

## Execution

- New Mind prompt `active/point_source_source_plane_phase_2c.md` for this phase (the campaign prompt
  stays in `draft/`); issue on autolens_profiling; worktree
  `~/Code/PyAutoLabs-wt/point-source-source-plane-p2c`, branch `feature/point-source-source-plane-p2c`.
- **Parallel claim:** `autolens_profiling` is also claimed by `pointsolver-step0-gather`,
  `point-source-cpu-p4` and `interferometer-mesh-numba-p1`. This phase touches only the new cell, its
  results/submits, the source-plane campaign note and README rows, which is disjoint as in 2a/2b.
  It needs its own worktree (approval requested with this plan).
- Delegation: build, laptop run and RAL runs go to an Opus subagent with a progress file + Monitor.
  The `n*` interpretation and the design memo stay in this session.
- Ship via `/ship_workspace`.

## Verification

- `AUTOLENS_PROFILING_SMOKE=1` run exits 0; full laptop run writes JSON/PNG with the gate block green
  at every rung.
- RAL gpu-node CPU + A100 jobs complete; logs pulled (batch_cpu logs by scp).
- `build_readme.py --check`, `ruff check` / `ruff format --check`, `check_submits.py --check`; PR
  `lint` green.
- JSON `source_revisions` equal the library mains; `PYTHONPATH` checked for stale worktrees.
