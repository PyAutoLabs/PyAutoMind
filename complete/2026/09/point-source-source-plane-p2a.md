## point-source-source-plane-p2a

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/322
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/323 (merge `9c0203e`)
- epic: point-source-cpu-speed
- parent-record: complete/2026/09/point-source-source-plane-breakdown.md

Phase 2a of the source-plane point-source chi-squared campaign (single-source only): the RAL CPU and A100 reference rows for the `point_source_source/source_plane` breakdown, plus a pytree-input A/B that sizes the fixed per-call `ModelInstance` flatten cost, merged in autolens_profiling#323.

**Shipped**
- `scripts/point_source_source/likelihood_breakdown/pytree_input_ab.py` — pytree vs flat_leaves vs flat_vector input A/B on the fused solved likelihood.
- `results/breakdown/point_source_source/source_plane_hpc_{ral_cpu,a100}_fp64.{json,png}` and `pytree_input_ab_hpc_{ral_cpu,a100}_fp64.{json,png}`; README rows.
- Submit scripts `hpc/batch_cpu/submit_breakdown_point_source_source_source_plane_ral_cpu_fp64`, `hpc/batch_gpu/submit_breakdown_point_source_source_source_plane_a100_fp64`; RAL job log `results/notes/point_source_source_plane_2026_09_26_ral_job_356368.out`.
- Campaign note `results/notes/point_source_source_plane_campaign.md` updated with the phase 2a section.

**Measured (RAL CPU 8490H, quiet — the reference; A100 fp64)**
- fused solved 0.1465 ms / plain 0.1450 ms; `value_and_grad` 2.26× forward (+0.185 ms), 4× compile.
- pytree / flat_vector = 1.361 [1.343, 1.385] → 0.0385 ms saved (plain 0.0452 ms); flat_leaves ≈ flat_vector, so the cost is the Python flatten of `ModelInstance`.
- A100 launch-bound: 0.222 / 0.265 ms.

**Decision (human, 2026-09-26):** NO-GO on the PyAutoFit flatten fast path — the relative bar (26–31 %) passes, the absolute 0.05 ms bar fails. Phase 2b = the backward-pass lever (jacfwd/jacrev ordering + analytic SIE Hessian study; library-first only if a lever appears). Remainder re-filed at `draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md`.

**Not done / carried**
- Laptop rows never refreshed (host busy; RAL is the reference).
- `scripts/misc/wall/check_submits.py` misses `python3 -u`; `hpc/sync pull` skips batch_cpu logs (scp'd by hand).
- RAL worktree `/mnt/ral/jnightin/autolens_profiling_wt/point-source-source-plane-p2a` to remove.
- Heart YELLOW at ship, acknowledged by the human 2026-09-26.

## Original prompt

# Point-source source-plane chi-squared speed-up campaign — phases 2+ (phase 1 shipped)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoLens
- PyAutoFit
Themes:
- point-source
- profiling
- jax
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: point-source-cpu-speed
Lane: any
Filed: 2026-09-26
Updated: 2026-09-26
Parent-record: complete/2026/09/point-source-source-plane-breakdown.md

## Phase 1 shipped — remainder re-filed (2026-09-26)

- **Merged:** autolens_profiling#317 at `f79ebf2` (after the folder split #318, `a5e3cdd`, which
  moved `scripts/point_source/` → `scripts/point_source_image/` + `scripts/point_source_source/`;
  paths below that still say `scripts/point_source/` now live under `scripts/point_source_source/`).
  Record `complete/2026/09/point-source-source-plane-breakdown.md`; campaign note
  `results/notes/point_source_source_plane_campaign.md` (ranked residue + "carried to cluster epic").
- **Measured headline** (laptop CPU fp64, 8 threads, median of 500): fused solved 0.438 ms /
  plain 0.457 ms; `value_and_grad` 2.43× forward (4× compile); dispatch floor 0.07–0.09 ms with
  the pytree argument (0.019 ms scalar); XLA merges the repeated Hessian/precision evaluations
  (hypothesis #1 answered: CSE does merge them — tidiness only). The plain-path
  `TracerArrayConversionError` guard was retired (plain fit JITs end-to-end). **Laptop host load
  was ~16 on 8 cores — re-take on an idle host or RAL before ranking.**
- **This prompt now carries phases 2+ only.** Next steps, in order:
  1. **(a)** idle-host or RAL re-run of the `point_source_source/source_plane` breakdown row under a
     new label (plus the unrun `hpc_ral_cpu_fp64` / `hpc_a100_fp64` rows; commands in the note).
  2. **(b) Phase 2 = the top residue lever — fixed per-call cost / `ModelInstance` pytree
     flattening** (~0.1 ms of a ~0.3–0.4 ms call; flat-leaf or single-vector input cut the floor to
     0.15–0.20 ms in a scratch probe). Likely PyAutoFit-scoped (`register_model` pytree
     flattening) — library-first.
  3. **(c)** backward-pass cost (2.43× forward, 4× compile) as the phase 3 candidate.
  4. **(d)** A100 launch-bound / vmap-throughput row — unmeasured.

## User request (verbatim, 2026-09-26)

Continue on going work to speed up the JAX source plane chi squared point solver, which we have been working on recently. should be an epic laid out for it I think? We have work on the image plane one, but maybe not the source plane chi squarded, so have a look at what is available. first task will be to write a likelihood_breakdown and then speed up from there, autolens_profiling gives a clear overview of the whole process and task and steps and design which you can use from other examples like imaging and the image plane point source.

## Scope steer (human, 2026-09-26): single-source only

This campaign is **single-source only** — the `scripts/point_source/` use case. No two-source /
cluster setups, rows, submits or levers; `scripts/cluster/` is never touched. The cluster use
case is epic `cluster-pointsolver-speed` (its own data and `scripts/cluster/likelihood_breakdown/`
baseline). Cluster-specific evidence found on the way is written into a short "carried to
cluster epic" note in the hand-off, never acted on. Epic tag is `point-source-cpu-speed`
(`cluster-strong-lensing` is the unrelated Source & Cluster arc).

## Survey (2026-09-26): what exists

- The **image-plane** PointSolver campaign is fully laid out and three phases in:
  shared breakdown instrument `scripts/point_source/likelihood_breakdown/image_plane.py`
  (record `complete/2026/09/point-source-shared-breakdown.md`, note
  `results/notes/point_source_shared_likelihood_breakdown.md`), phases 1-3 shipped
  (`complete/2026/09/point-source-cpu-p{1,2,3}.md`, ledger
  `results/notes/point_source_cpu_campaign.md`), phase 4 drafted at
  `active/pointsolver_cpu_speed_phase_4.md`.
- The **source-plane** chi-squared (`al.FitPositionsSource` / `al.FitPositionsSourceSolved`,
  Lenstool's default likelihood, no lens-equation solve) has **no campaign, no epic entry and
  no breakdown instrument**. What exists:
  - runtime cells `scripts/point_source/likelihood_runtime/source_plane.py` (plain; its
    end-to-end JIT is guarded by a `try/except TracerArrayConversionError` fallback to a
    ray-trace-only prefix) and `source_plane_solved.py` (full pipeline JITs;
    `results/runtime/point_source/source_plane_solved/…v2026.7.23.1.json`: eager 10.9 ms,
    single-JIT 0.34 ms/call, vmap(3) 0.12 ms/call, LL 0.5986504555530896);
  - `scripts/cluster/likelihood_breakdown/source_plane.py` (593 lines, v2026.7.23.1): a
    closure-based per-step decomposition of the 13-component (2 dPIE + 10 scaling-tier dPIE +
    1 NFW), two-source (z=1,2) multi-plane cluster case — steps: multi-plane ray trace of the
    observed positions, Hessian magnification at every observed position
    (`magnification_2d_via_hessian_from`, re-evaluates the full deflection stack several
    more times per position), magnification-weighted chi-squared, log-likelihood assembly;
    plus a plain-vs-solved eager per-system comparison (steps 5-6). README row
    `cluster/source_plane` local_cpu_fp64 step-sum 4.5 ms. It closes over a fixed tracer
    (params are compile-time constants, so constant folding can fake work), is CPU-only in
    practice, and its docstring records the plain end-to-end fit as JIT-blocked.
- Issue #657 series (`project` memory: point-source solved likelihoods): `PointSolved` +
  `FitPositionsSourceSolved` regression literal SourceSolved −94.70750993 (cluster,
  vmap==eager exact); the paper is Lombardi 2024 arXiv:2406.15280 §5.1.
- The point-source defaults campaign (`results/notes/point_source_defaults_campaign.md`,
  PyAutoLens#678) adopted tensor source-plane weighting + solved centres as defaults, and
  found gradient searches not yet competitive at cluster scale on the source-plane objective —
  so per-call cost AND gradient cost both matter here.

## Campaign contract

This is a phased campaign, the source-plane sibling of the image-plane CPU campaign. At
start-dev issue ONLY the next bounded phase (one task / one PR per member), retaining this
prompt as the campaign intent until every phase is resolved. The image-plane campaign's
**measurement and acceptance contract** (in
`active/pointsolver_cpu_speed_phase_4.md`, "Campaign contract")
governs verbatim: record commits / JAX versions / device / precision / threads / seeds;
separate lowering, compile, first call and warmed runtime; block_until_ready; vary
parameters through the production likelihood so constant folding cannot fake work; retain a
fused end-to-end production-likelihood control; report interleaved A/B medians + dispersion
on identical hardware; cover perturbed models, doubles/quads and near-caustic cases; preserve custom_jvp / eager-JIT-vmap parity / gradient
correctness; each iteration = baseline → one hypothesis → bounded prototype → correctness
gate → repeated A/B → accept/reject → reprofile; record negative results; stop when the
residue is explained.

### Phase 1 — SHIPPED (see above)

_Original phase-1 heading: shared CPU/GPU likelihood breakdown instrument._

Build `scripts/point_source/likelihood_breakdown/source_plane.py` (single-source `simple` instrument only), structurally mirroring
`image_plane.py` (same result-JSON contract, `--config-name` hardware rows, provenance
block, JIT-phase split, numerical controls, PNG, README dashboard regeneration via
`build_readme.py`), for the production `AnalysisPoint.log_likelihood_function` with:

1. **Primary path** `al.ps.PointSolved` + `al.FitPositionsSourceSolved` (the adopted
   default); **separately labelled control** free-centre `al.ps.PointFlux`/`al.ps.Point` +
   `al.FitPositionsSource`. Never conflate the two variants.
2. **One instrument:** the seeded four-image `simple` dataset (as `image_plane.py`). At this scale
   the call is ~0.3 ms so fusion/launch overhead may dominate — report it honestly.
3. **Cumulative prefix boundaries through the fused production likelihood** (not a fixed
   closure): (a) multi-plane ray trace of the observed positions to each source plane;
   (b) Hessian magnification at each observed position; (c) β* solve (solved path) / model
   centre lookup (plain path); (d) magnification-weighted chi-squared + noise normalisation;
   final row = fused likelihood minus last prefix. Parameters enter as a registered
   `af.ModelInstance` pytree and are varied per call. Retain the telescoping-sum caveat
   from the image-plane note (prefix rows are not independently additive).
4. **Controls:** eager ≡ JIT ≡ vmap(2) log-likelihood parity, hard-coded regression
   literals (refresh procedure documented), full-model `jax.grad` finite AND non-zero
   (`autofit.jax.register_model` — an unregistered model silently yields all-zero grads),
   and a **gradient-cost row** (ms per `value_and_grad` call vs forward) because the
   defaults campaign found gradient searches uncompetitive at cluster scale.
5. **Plain-path JIT status:** ground on the live stack whether `FitPositionsSource`
   end-to-end still raises `TracerArrayConversionError` (the runtime cell's guard and the
   cluster breakdown's docstring both say blocked; PyAutoArray#414 claimed the `xp` fix).
   If it JITs, drop the fallback from the runtime cell in the same PR; if not, record the
   exact failing frame as the first ranked lever for phase 2.
6. **Results:** `results/breakdown/point_source/source_plane_{local_cpu_fp64,…}.json/.png`
   for both cells on this laptop (record `NPROC`, XLA threads) and, if RAL is reachable,
   `hpc_ral_cpu_fp64` + `hpc_ral_a100_fp64` rows under `--nodelist`-pinned submits with the
   CPU model recorded; a campaign note
   `results/notes/point_source_source_plane_campaign.md` with the ranked residue for phase 2.
   Smoke: honour `AUTOLENS_PROFILING_SMOKE=1`; regenerate READMEs (`build_readme.py --check`).
7. **Out of scope for phase 1:** any library edit beyond the plain-path fallback removal;
   no speed-up levers.

### Phases 2+ (to be ranked by the phase-1 breakdown, issued one at a time)

Candidate levers, unmeasured — the phase-1 residue ranks them:
- **Hessian magnification / precision-tensor re-evaluation** — the plain path evaluates
  `magnifications_at_positions` twice per likelihood and the solved path rebuilds the jacfwd
  precision tensor three times (plus `_beta_hat` twice); whether XLA CSE merges them is hypothesis #1; a `jax.jacfwd` of the single ray trace, or
  reusing the ray-trace deflections, may remove those evaluations (bit-identical-or-tolerance
  gate against the finite-difference Hessian, near-critical positions included).
- **Plain-path JIT block** (`Grid2DIrregular` `xp` propagation) if still present.
- **Gradient cost** — if `value_and_grad` ≫ forward, profile the backward pass
  (jacfwd-of-deflections Hessian-of-Hessian).
- **vmap batch throughput** on A100 (launch-bound at 0.3 ms/call).
Each phase: library-first (PyAutoLens/PyAutoArray) then refresh the profiling rows under a
new label; GPU regression check on every shared library change.

## Where the code lives

- `autolens_profiling/scripts/point_source/` — cells (`scripts/cluster/` is out of scope: epic `cluster-pointsolver-speed`).
- `PyAutoLens/autolens/point/fit/` — `FitPositionsSource`, `solved.py` (`SolvedCentre`), `autolens/lens/` — multi-plane tracer, `LensCalc.magnification_2d_via_hessian_from`.
- `PyAutoGalaxy/autogalaxy/operate/lens_calc.py` — `hessian_from` / `magnification_2d_via_hessian_from` (jacfwd path).

## Related

- `active/pointsolver_cpu_speed_phase_4.md` — image-plane sibling campaign (contract source), same epic.
- `draft/research/autolens_profiling/cluster_pointsolver_speed.md` — the cluster epic that receives any carried cluster evidence.
- `draft/research/autolens_profiling/point_solver_profiling_cells.md`, `point_source_image_plane_gpu_breakdown.md` — related point-source prompts.

