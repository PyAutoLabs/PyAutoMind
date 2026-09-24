# Point-source CPU speed-up campaign — phase 3: static step-0 lattice precompute

Precomputed the static step-0 triangle lattice of the JAX `PointSolver` as a cached geometric unique-vertex table, so step 0 deflects only the unique lattice vertices, and measured it with an interleaved in-process A/B on RAL CPU (host-pinned, constant folding off and on) and a RAL A100. Phase 3 of the phased CPU campaign only; phase 4 remains open and is re-filed as `draft/research/autolens_profiling/pointsolver_cpu_speed_phase_4.md`, pointing at this record. Issue PyAutoArray#568 is closed (phases 2 and 3 done); phase 4 gets its own issue at start_dev.

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/568
- completed: 2026-09-24
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/570
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/749
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/305
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/570
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/749

## Shipped

- Merged [PyAutoArray#570](https://github.com/PyAutoLabs/PyAutoArray/pull/570) at `7fa8d2714f7da43fec2b23c31bff580764831670` (branch head `d6c5e524`), then [PyAutoLens#749](https://github.com/PyAutoLabs/PyAutoLens/pull/749) at `86054bbc19baa2f710a12e04a94fa27ab37cc354` (branch head `c9ba49fb2`), then [autolens_profiling#305](https://github.com/PyAutoLabs/autolens_profiling/pull/305) at `9ad12abdaa44659c95b59ec024dfbbad378b415d` (branch head `629ce0c1`) — library first, human `/prm` 2026-09-24, every CI leg green, no freeze. Each feature head proven an ancestor of `origin/main` (0 commits ahead) per repo at close-out.
- PyAutoArray (`ad0bf97b`): `static_vertex_table(y_min, y_max, x_min, x_max, scale)` — an `lru_cache`d NumPy builder keyed on the integer lattice position, first-occurrence floats, read-only; `CoordinateArrayTriangles(vertex_table=None)` and `for_limits_and_scale(..., static_vertices=False)` (opt-in). 11 859 of 69 849 slots on the simple ±9.9″ / 0.2″ lattice (28 665 exact-float distinct), 46 516 of 276 507 on the cluster 200×200 @ 0.7″ lattice. Derived lattices and pytree round-trips drop the table.
- PyAutoLens (`b346b6a0`, tie test `972d454e`): `AbstractSolver._initial_triangles` passes `static_vertices=True` on the JAX path only — on by default for the JAX PointSolver, as decided by the human on 2026-09-24.
- CI fix after the first ship: `d6c5e524` (PyAutoArray) / `c9ba49fb2` (PyAutoLens) define the parametrize constants outside the jax guard — fixes test collection on the `unittest-nojax` leg.
- autolens_profiling: `scripts/point_source/likelihood_breakdown/static_lattice_ab.py` (control / exact / lattice / library routes, fresh closures + `jax.clear_caches()`, 20 rounds × 20 calls, FLOPs / `memory_analysis` / RSS / compile / table-build provenance, `--constant-folding` with an HLO `c @ c` probe), RAL CPU + A100 submits, results `results/breakdown/point_source/static_lattice_ab_{hpc_ral_cpu,constant_folding_hpc_ral_cpu,hpc_ral_a100,laptop_cpu,constant_folding_laptop_cpu}_fp64.{json,png}`, job logs, campaign ledger `results/notes/point_source_cpu_campaign.md` phase 3 (DONE, ACCEPTED).

## Evidence

- RAL CPU job 350636 (`ral`, pinned `--nodelist=euclid-ral-compute-10-2`, Intel Xeon Platinum 8490H — the phase-1 host; 8 CPUs, fp64, JAX 0.10.2). Folding off: simple solved 3.540 → 1.758 ms (**2.01×**, 90 % CI 1.63–2.09), simple plain 2.08×, vmap-4 1.43×, two-source cluster solved 47.36 → 9.085 ms (**5.21×**, CI 5.10–5.30), cluster plain 5.16×. Folding on: simple 2.1–2.4×, vmap-4 1.39×, cluster 3.9–4.5×.
- RAL A100 job 350637 (`euclid-ral-gpu-1`, fp64): **1.01–1.07×** — no GPU regression (the GPU call is launch/latency-bound, not FLOP-bound).
- FLOPs simple 7.05M → 3.38M (−52 %), cluster 139.4M → 39.5M (−72 %). XLA temp memory 4.82 → 1.69 MB (simple), 91.6 → 22.6 MB (cluster), A100 3.36 → 0.39 / 42.1 → 6.35 MB — 3–4× lower. Compile `compile_s` +3.3 % to +12.2 % folding off, +1.9 % to **+16.5 %** folding on, −1.6 % to +13.2 % A100: every row under the +20 % stop rule (single cold compile per route, not a median).
- Correctness: 31 / 31 gates bit-identical in all three RAL JSONs (log L every route/instance, fiducial simple solved `7.743201200876812`, solved positions and image counts, `jax.grad` finite and non-zero, vmap-4 vs scalar, step-0 `containing_indices`); `library_matches: lattice` on every row. PyAutoArray suite 1645 passed; PyAutoLens suite 756 passed, 1 xfailed; step-0 shape guard red on main (69 849) green on branch (11 859); autolens_workspace_test point-source `jax_likelihood` ×4 + `jax_grad` identical to main.
- **Tie case PASSED by human decision 2026-09-24:** a source placed bit-exactly on a traced step-0 vertex made the flat control return a duplicate third image (control 3 vs lattice 2 in 1 / 13 constructed ties); the lattice path returns exactly the 2 true images. Main's own flat path is not self-consistent at such ties (eager vs jit differ on 22 / 25). Pinned as PyAutoLens `test_autolens/point/triangles/test_static_lattice_jax.py::test__source_on_a_step_0_vertex_returns_the_two_true_images`.
- Post-fix budget (FLOP estimate): simple — step 0 ≈ 22 %, seven refinement steps ≈ 60 %, rest ≈ 18 %; cluster — step 0 ≈ 51 %, deflections of the 13-component lens dominate both halves.

## Heart RED development override (history)

- heart-red-override:
  - authorization: "2026-09-24 live human, this session: asked 'When ingestion finishes, how should I ship? Heart is RED...' with options 'Ship with RED override (Recommended): Authorize the development-only Heart RED override for PyAutoArray#568 phase 3...' or hold; the human selected 'Ship with RED override (Recommended)'. Scope commit/push/pending-release PRs only (PyAutoArray#570, PyAutoLens#749, autolens_profiling#305); no merge, no release."
  - red-reasons: "release validation FAILED (stage integrate); workspace validation not passing (4 failed, cloud#35579888156: autolens notebooks/cluster/modeling.ipynb, autolens notebooks/weak/a2744.ipynb, autolens scripts/cluster/modeling.py, +1 more); manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml"
  - passed: "pytest test_autoarray 1645 passed at ad0bf97b; pytest test_autolens 756 passed, 1 xfailed at 972d454e (both re-run at ship); step-0 shape guard red on main (69 849) green on branch (11 859); workspace_test point-source jax_likelihood x4 + jax_grad identical to main; A/B 31/31 gates bit-identical on RAL CPU 350636 (folding off+on) and A100 350637; tie case pinned as test__source_on_a_step_0_vertex_returns_the_two_true_images; build_readme and check_submits --check pass. Branch does not fix Heart; Heart stays RED for release."
- The merge itself was the human's `/prm` on 2026-09-24 (override recorded at ship in Mind `eccdb368`); Heart remains RED for release purposes.

## Handoff

- Remainder (phase 4) re-filed: `draft/research/autolens_profiling/pointsolver_cpu_speed_phase_4.md`; issue PyAutoArray#568 closed — phase 4 gets its own issue at start_dev.
- First step after the PyAutoArray + PyAutoLens release: `HPCPullPyAuto` on RAL, re-run the phase-1 `point_source` and `cluster` `likelihood_breakdown/image_plane.py` cells under a new label (record node CPU model) so the per-step wall-time split backs the phase-4 ranking.
- Phase-4 re-ranking (campaign note, phase-3 handoff): simple — initial scale vs refinement steps first (refinement ≈ 60 % of FLOPs); cluster — dPIE/NFW deflections first (separately scoped PyAutoGalaxy phase); then grid-extent guidance, then `MAX_CONTAINING_SIZE` / neighbourhood fan-out.
- Follow-ups found, not fixed: RAL cleanup after release of `/mnt/ral/jnightin/autolens_profiling_wt/{PyAutoArray,PyAutoLens}_point-source-cpu-p{2,3}` clones, the `point-source-cpu-p3` RAL worktree and `_p2_untracked_backup_20260924`; RAL compute-1..19 NOT_RESPONDING on 09-24; compile figures are single cold compiles; the PyAutoLens JAX unit test file (~85–100 s) departs from the no-JAX-in-unit-tests convention — consider moving to autolens_workspace_test; `jax.grad`/`register_model` zero-gradient library candidate; phase-1 leftovers (`check_submits.py` regex gap, `activate.sh` worktree-leak guard, CI smoke coverage for the breakdown cells).

## Original prompt

# Point-source CPU speed-up campaign — phases 3–4: static-lattice precompute and measured iteration

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoLens
- PyAutoArray
Themes:
- point-source
- profiling
- cluster
- jax
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: cluster-strong-lensing
Filed: 2026-09-17
Updated: 2026-09-24
Issued: 2026-09-24
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/568
Parent-record: complete/2026/09/point-source-cpu-p2.md

## Phase 2 shipped — remainder re-filed (2026-09-24)

Phase 2 ("Remove redundant vertex deduplication") is COMPLETE and ACCEPTED:
[PyAutoArray#569](https://github.com/PyAutoLabs/PyAutoArray/pull/569) merged at `681938ae`
(**pending release**) and [autolens_profiling#301](https://github.com/PyAutoLabs/autolens_profiling/pull/301)
at `93757902`, record `complete/2026/09/point-source-cpu-p2.md`, ledger
`autolens_profiling/results/notes/point_source_cpu_campaign.md` (phase 2 section).
RAL CPU job 350582: simple 24.00 → 5.38 ms (4.47×), two-source cluster 155 → 78 ms (1.98×);
RAL A100 job 350587: no GPU regression (1.71–2.05× faster); every gate bit-identical.
This prompt now carries **phases 3–4 only**. Issue
[PyAutoArray#568](https://github.com/PyAutoLabs/PyAutoArray/issues/568) was deliberately
left open to track them (its title is phase-2 scoped; re-title or file a fresh issue at
start-dev if preferred).

**Next steps, in order:**

1. Wait for the PyAutoArray release carrying #569 (`pending-release` in the record).
2. `HPCPullPyAuto` on RAL so the shared install carries the fix.
3. Re-run the phase-1 breakdown cells (`scripts/point_source/likelihood_breakdown/image_plane.py`
   and the `cluster` cell) on RAL under a **new label** so the README dashboard rows move;
   record the node's CPU model. Re-run `vertex_dedup_ab.py`: its `library` route must read
   `library_matches: nodedup` (sort count 7 / 12) — a `control` reading means a stale install.
4. **Phase 3 (next bounded task) — precompute the static initial lattice**, ranked first
   because deflections are **70 %** of the post-fix simple call's FLOPs (4.94M of 7.05M).
   Build the step-0 unique vertices + index map in NumPy at construction and pass them as
   immutable JAX inputs: step-0 trace 69 849 → 28 665 points on `simple` (≈ 1.56M FLOP,
   ≈ 22 % of the call), scaling with the cluster's 276 507-point input. Report setup cost,
   memory and cache invalidation on geometry change; never cache model-dependent deflections.
   The `constant_folding` flag A/B belongs here (the step-0 lattice is a compile-time
   constant). Measure against a control refreshed on the **same node**.
5. Phase 4 ranking after phase 3: (a) grid-extent guidance, (b) initial scale vs steps
   (step 0 = 2.92M of 4.94M deflection FLOPs; each extra step ≈ 0.29M), (c)
   `MAX_CONTAINING_SIZE` / neighbourhood fan-out (smallest share, correctness knob),
   (d) cluster dPIE/NFW deflections (separately scoped PyAutoGalaxy phase).

**Phase-2 follow-ups carried here (not fixed):**

- CPU A/B ran **5 calls/round**, not the planned ≥ 20 (the A100 leg ran 20 × 20); the cell
  does not record the XLA intra-op thread count or per-route memory — add both before the
  phase-3 run.
- **Host pinning:** `ral` jobs land on different CPU models (Xeon Platinum 8490H in phase 1,
  EPYC 7763 in phase 2; cluster control +15–20 % from the host alone). Use `--nodelist` /
  `--constraint` on the submits or always take an in-job control.
- **RAL cleanup:** remove the `/mnt/ral/jnightin/autolens_profiling_wt/PyAutoArray_point-source-cpu-p2`
  clone and the `_p2_untracked_backup_20260924` dir once the release is synced.
- **Library follow-up candidate (PyAutoFit / PyAutoLens):** `jax.grad` of an `AnalysisPoint`
  likelihood silently returns all zeros without `autofit.jax.register_model(model)` (forward
  values stay right) — raise or warn on an unregistered model. File via intake, separately
  from this campaign.
- Still open from phase 1: `check_submits.py` `python3 -u` regex gap (also hits the phase-2
  submit), `activate.sh` worktree-leak guard (phase 2 swapped `PYTHONPATH` by hand again),
  CI smoke coverage for the breakdown cells (now incl. `vertex_dedup_ab.py`).
- Still-unmeasured controls: vmap batches 1/16, post-fix grid/`n_steps`/capacity sweeps,
  direct deflections on the 276 507-point cluster input.

## Phase 1 shipped — remainder re-filed (2026-09-23)

Phase 1 ("Reproduce and publish the CPU evidence") is COMPLETE: autolens_profiling#297 /
PR #298 merged at `9f5a3ba`, record `complete/2026/09/point-source-cpu-p1.md`, ledger
`autolens_profiling/results/notes/point_source_cpu_campaign.md`. This prompt now carries
phases 2–4 only. **Next bounded task = phase 2:** remove the JAX-only throwaway
`jnp.unique` at `CoordinateArrayTriangles._vertices_and_indices` as used by
`_plane_triangles` (PyAutoArray + PyAutoLens, library-first), red control = bit-identical
likelihood + cluster solved positions + gradient/vmap parity against the frozen baseline
(PyAutoArray `22e6d608`, PyAutoLens `2aaa1c1a8`; RAL `ral` partition rows
`hpc_ral_cpu_fp64`: point-source fused solved 24.69 ms, cluster fused plain 128.05 ms),
interleaved A/B on RAL with distinct function objects + `jax.clear_caches()`, medians and
dispersion, fused control, `len(os.sched_getaffinity(0))` and XLA intra-op threads recorded.
The GPU campaign takes its A100 baseline on the frozen revisions before phase 2 merges, or
from those SHAs afterwards.

## Campaign contract (2026-09-19)

This execution plan supersedes the earlier deliverable/gate wording retained below.
This is one of two optimization campaigns in a three-task plan. The independent
shared breakdown task is their common prerequisite.
It is a phased campaign: at start-dev, issue only the next bounded phase (one task /
one PR per member), retaining this prompt as the campaign intent until all phases
are resolved. Do not attempt a cross-library, multi-PR campaign as a single task.
Use start-dev and the applicable library/workspace worktree and ship procedures;
obtain implementation-plan approval before source edits. No profiling or library
implementation was performed during this consolidation.

### Measurement and acceptance contract

- Use @autolens_profiling for timing and versioned JSON + PNG evidence, with
  README/dashboard regeneration. Correctness evidence belongs in library tests
  and @autolens_workspace_test, not a timing-only assertion of scientific validity.
- Record exact library/profiling commits, JAX/jaxlib versions, device, precision,
  XLA flags, thread settings, model/data seed, source planes, solver grid/scale,
  precision, neighborhood degree, capacity, warm-up, repetitions and cache state.
  Historical numbers are leads, not comparable current baselines.
- Separate tracing/lowering, compilation, first execution and warmed runtime.
  Synchronize device outputs with block_until_ready; pass varying parameter
  inputs through the production likelihood so constant folding cannot fake work.
  Report repeated/interleaved A/B medians and dispersion on identical hardware,
  both ms/likelihood and batch throughput, plus memory where relevant.
- Retain a fused end-to-end production likelihood control. Prefix timing
  differences can change fusion and contain noise: report residuals/negative
  differences honestly and corroborate with a device trace rather than claiming
  independently timed steps sum to the fused runtime.
- Compare likelihood, image counts/positions, NaN padding/masks, magnification
  filtering and source-redshift handling. Cover perturbed models, doubles/quads,
  near-caustic/critical configurations and cluster multi-source/multiplane cases.
  Preserve custom_jvp, eager/JIT/vmap parity and gradient correctness; distinguish
  nondifferentiable image-topology transitions from failures in smooth regions.
- Each iteration: baseline -> one hypothesis -> bounded prototype -> correctness
  gate -> repeated full-likelihood A/B -> accept/reject -> reprofile and rank the
  remaining bottleneck. State minimum detectable improvement from observed noise;
  keep a change only for a repeatable material gain without correctness or
  unacceptable compile/memory regressions. Record negative results too.
- Stop when remaining cost is explained and no worthwhile measured lever remains,
  or a concrete external blocker prevents the next experiment. Do not promise the
  historical speedup, optimize indefinitely, or weaken correctness to hit a target.

### Split request (verbatim)

break into 3, with the first build the shared likelihood breakdown first, which I guess is CPU or GPU agnostic but maybe not, then PR them into main

### Original consolidation request (verbatim)

We did two reviews or assessments of the point source likelihood function recently one for CPU which was JAX and numba sparse (it concluded numba spaerse not worth it) and one for GPU. We may of made some prompts but I want you to assess all that the review put forward and ultimately end with two mind task or prompts, which could be epics, which will profile them with autolens_profiling and iteratively work on the speed up. One was focused in particular on writing an autolens_profiling likelihood_breakdown script, which it may of wrote or just planned, this would likely be the task before we go into specific CPU or GPU speed up

## CPU campaign: dependencies and phase order

**Start condition:** task 1 shipped in
[autolens_profiling#293](https://github.com/PyAutoLabs/autolens_profiling/pull/293)
and is recorded in `complete/2026/09/point-source-shared-breakdown.md`; it owns
the shared `scripts/point_source/likelihood_breakdown/` instrument and CPU
reference results under `results/breakdown/point_source/`.
CPU source optimization waits for that merged instrument and CPU baseline, not
for the GPU campaign. Preserve the exact unoptimized library revisions and
configuration so task 3 can reproduce an A100 baseline even if CPU fixes land
first. Avoid two branches changing the same solver at once.

1. **Reproduce and publish the CPU evidence.** Re-run the simple solved likelihood
   and the 13-component, two-source cluster case with the shared harness. The
   September 17 scratch note/JSONs are not committed in the inspected profiling
   tree; recover them if available, otherwise reproduce and explicitly label the
   old measurements as reported evidence. Measure unsolved and solved paths
   separately; do not attribute a likelihood-variant difference to hardware.
2. **Remove redundant vertex deduplication, if reproduced.** The recorded
   `_vertices_and_indices` sort is still present in the inspected PyAutoArray
   checkout. Test the JAX-only throwaway conversion at `_plane_triangles`, not
   blanket removal of all `unique`/`remove_duplicates` operations. Reproduce the
   red control on the original path, confirm masks/index semantics and full
   likelihood/gradient parity, then ship the bounded library change before
   refreshing workspace results. The recorded 40.0 -> 8.1 ms simple and
   117 -> 48 ms/source cluster gains are hypotheses to reproduce on current code.
3. **Precompute static initial geometry.** If deflections dominate after phase 2,
   evaluate construction-time NumPy unique vertices plus an index map for the
   initial lattice, reused as immutable JAX inputs. Count actual traced vertices,
   report setup/memory/amortization, and verify cache invalidation when solver
   geometry changes. Never cache model-dependent deflections or warm-start from
   the preceding sampler call. This lever was proposed, not measured.
4. **Profile the residue and iterate.** Rank the following by new evidence:
   (a) safe grid-extent guidance; (b) initial scale versus refinement count;
   (c) MAX_CONTAINING_SIZE/neighborhood fan-out; (d) cluster dPIE/NFW deflections.
   Grid/capacity changes require image-completeness evidence and must be reported
   as separate configurations, not silently substituted into the speed comparison.
   Profile components through the existing `scripts/lens/deflections/` surface
   when needed; any resulting PyAutoGalaxy work is a separately scoped phase.

### Disposition of every CPU assessment recommendation

- **Numba/sparse rewrite:** do not pursue by default. The assessment found no
  reusable kernel and existing unpadded NumPy was 96 ms/solve, about 12x slower
  than the patched JAX path. Reopen only if new post-fix measurements demonstrate
  a substantial unsolved bottleneck and preserve JVP/vmap/GPU contracts.
- **Step count:** seven refinement steps reportedly cost ~3 ms in total; fewer
  than four degraded the likelihood. Low priority, never a blind accuracy trade.
- **Extent:** reported 30x30 / 100x100 / 140x140 timings were 6.4 / 39.8 / 72 ms;
  a fiducial bit-identical likelihood does not prove coverage across a prior.
- **Fit/chi-squared, beta-star and magnification filter:** reported 0.34% of the
  original call. Re-rank after the main fix; don't assume the old fraction holds.
- **Duplicate model_data solve:** reportedly eliminated by XLA CSE; verify in
  fused execution before proposing Python caching as a performance fix.
- **Unmeasured controls:** vmap batches 1/4/16; post-fix grid/n_steps and capacity
  sweeps; constant-folding-pass flag A/B; direct deflections on the actual
  276,507-point cluster input (the old lower bound was extrapolated).
  Recompile independent function objects / fresh processes for monkeypatch A/B;
  JAX function-identity caching must not reuse the old executable.
- **Warm starts:** reject cross-call mutable solver state; maintain a pure
  likelihood for arbitrary sampler order and transformations.

### Completion evidence

Commit a CPU campaign note in `results/notes/` with baseline/final comparisons,
all candidate dispositions, reproducible commands, linked artifacts and shipped
phase PRs. Include a GPU regression check for shared library changes and state
any unmeasured hardware limitation. A ranked list alone is not completion: run
and decide the warranted bounded iterations, including justified no-go results.

## Preserved September 17 assessment and provenance

The following is historical context; the campaign contract above governs new work.

# PointSolver image-plane chi-squared CPU speed-up: is the JAX CPU path sub-optimal enough for a sparse/numba lever?

User request (verbatim):

In autolens_profiling, we have done lots of work speeding up imaging and interferometer on CCD. Now, I want us to speed up the point_source image plane chi-squared, with this issue focusing on CPU. This will likely use the JAX implementation, for other LH functions we had existing numba code to build on and there was lots of sparsity to exploit. Im not sure doing a whole numba CPU implementation is worth it. However, its worth some research, and asking if the JAX CPU implementation is sufficiently sub optimal that there are obvious low hangign fruit improvements with a clever CPU sparse approach, noting that cluster modeling will rely heavily on the PointSolver.

We may not have a likelihood_breakdown of this likelihood function yet, in which case we should make one before trying any kind of CPU or JAX code. I have another claude chat looking into that so bare that in mind and we wont do any real dev work until that is made

## Gate

Gated on the point_source likelihood_breakdown cell (scripts/point_source/likelihood_breakdown/) being built by a concurrent session; no CPU or JAX implementation work starts until that breakdown exists. This session's deliverable is the research note + ranked candidate levers. Research phase COMPLETE 2026-09-17 (see Findings); the implementation phase (lever 1 first, library-first in PyAutoArray/PyAutoLens) still waits on the breakdown cell.

## Baseline

Committed CPU runtime for image_plane_solved (v2026.7.23.1): eager 274 ms/call, single-JIT full pipeline 38.6 ms/call, vmap(3) 28 ms/call — results/runtime/point_source/image_plane_solved/.

## Where the code lives

- `autolens_profiling` — profiling cells and committed runtime results.
- `PyAutoLens` — solver source, `autolens/point/solver/`.
- `PyAutoArray` — triangle machinery, `autoarray/structures/triangles/`.

## Related

Sibling (not parent): `draft/research/autolens_profiling/point_solver_profiling_cells.md` — the PointSolver profiling-cells research prompt in the same cluster-strong-lensing epic.

<!-- formalised by the Intake (Conception) Agent on 2026-09-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/a4c1ddc1-40ff-4f6b-9048-5c5e0b329332/scratchpad/intake_input.md; Target/Epic/title hand-restored after the conductor resolved Target: PyAutoArray and dropped Epic: -->

## Findings (2026-09-17 research run, CPU, read-only — no repo edited)

Full note + reproducible scratch scripts/JSONs: session scratchpad `pointsolver/pointsolver_cpu_research_note.md` (to be landed in `autolens_profiling/results/notes/` with the fix PR). Machine: WSL2 laptop, 8 cores, NPROC=8, fp64, jax 0.10.2, autolens 2026.8.17.1; speed-ups are within-run interleaved ratios.

**Answer:** the JAX CPU path is sub-optimal, but not from sparsity or padding — ~84% of the call is a `jnp.unique` sort that is a no-op under jit.

- **Mechanism.** `CoordinateArrayTriangles._vertices_and_indices` (PyAutoArray `autoarray/structures/triangles/coordinate_array.py`) calls `jnp.unique(flat_vertices, size=3*N, fill_value=nan)`. Under jit the static `size=3N` means the "deduplicated" table has exactly as many rows as the input (69 849 for the 100×100 `simple` grid, 59% NaN fill), so it saves zero deflection evaluations and costs one lexicographic sort of 69 849 fp64 rows. The `ArrayTriangles` it builds is used only for `containing_indices` and thrown away every step. JAX-path-only defect: the NumPy sibling's `np.unique` genuinely shrinks 69 849 → 28 665.
- **Proof (monkeypatched in scratch, library untouched).** Full `AnalysisPoint.log_likelihood_function` on the `image_plane_solved` config: 40.0 → 8.1 ms/call (4.9× median, 5.4× p10), log-likelihood bit-identical (7.743201200876812), HLO sorts 15 → 7, FLOPs 15.58M → 6.50M. Real cluster solver config (200×200 @ 0.7″, 92 169 triangles, 13 mass components, 3 planes, 2 sources): 117 → 48 ms per source (2.4×), solved positions identical; a 2-source cluster likelihood 237 → 98 ms.
- **Lower bound.** Bare deflections for one solve ≈ 6 ms (69 849 + 7×720 points) inside a 26–42 ms call → 77–86% bookkeeping. Post-fix the simple solve is ~1.4× its deflection bound; the cluster solve is at its (extrapolated) bound, so at cluster scale the remaining lever is the dPIE/NFW deflection code, not the solver.
- **Sensitivity.** n_steps: all 7 refinement steps cost ~3 ms total (~0.45 ms each) — not a lever, and LL degrades below 4 steps. Grid extent: 30×30 = 6.4 ms vs 100×100 = 39.8 ms vs 140×140 = 72 ms with bit-identical LL — the cell tiles ±9.9″ to find images at ~1.6″. Fit/χ² + β* centre + magnification filter = 0.34% of the call. The solve is invoked twice per likelihood (`model_data` property) but XLA CSEs it — no lever.
- **NumPy path (the existing unpadded sparse implementation).** 96 ms/solve doing 2.5× fewer deflection evaluations — 12× slower than the fixed JAX path.
- **Numba verdict: not worth it.** No existing kernel, no exploitable sparsity beyond what the NumPy path already has, headroom gone after a ~20-line fix, and a callback loop would forfeit the `custom_jvp` implicit gradient, `vmap` and the GPU path.

**Ranked levers:** (1) drop the throwaway `jnp.unique` on the JAX trace path (PyAutoArray + PyAutoLens `_plane_triangles`; red-control bit-identical LL + cluster positions) — 4.9× simple / 2.4× cluster; (2) precompute the initial lattice's unique vertices + index map once at solver construction in NumPy (the step-0 tiling is static), cutting step-0 deflection count ~2.4–6× with no runtime sort — matters most at cluster scale where deflections dominate post-fix (not measured); (3) solver grid extent guidance / defaults (6.2×, zero code); (4) coarser initial `scale` + more steps (~4× on step 0, completeness risk, not measured); (5) `MAX_CONTAINING_SIZE` / 240-triangle fan-out (≲1.5 ms, correctness knob); (6) mass-profile deflection code at cluster scale. Recommend against warm-starting across sampler calls (breaks the pure-function contract `vmap`/`custom_jvp` rely on).

**Not measured:** vmap batch 1/4/16 post-fix, `MAX_CONTAINING_SIZE` sweep, post-fix grid/n_steps sweep, `--xla_disable_hlo_passes=constant_folding` A/B, bare deflections at 276 507 points. Trap: jax caches jaxprs on function identity — a monkeypatch A/B needs a distinct function object and `jax.clear_caches()` before each compile.
