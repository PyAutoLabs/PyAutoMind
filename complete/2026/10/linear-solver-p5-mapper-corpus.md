Linear-solver programme phase 5 (research): a Mapper (pixelized) corpus — is the released raw PDIP + polish admissible, and is Jacobi (the Mapper default) stable, on the systems pixelized and mixed likelihoods actually produce? The human's "option 2" (2026-10-08): one bounded evidence step before any default decision.

**Shipped:** autolens_profiling#401 (merged 2026-10-08), issue autolens_profiling#399. #400 carried the same work and was closed unmerged because it committed three 50–56 MB corpus files; #401 re-landed it from a fresh branch with those files out of git (human decision, 2026-10-08) and the old branch was deleted on the human's instruction. New `capture.py` runners `delaunay_hst`, `rectangular_hst`, `slam_mixed_hst` (8 near-truth vectors each; n = 1500 / 1369 / 1540; captures assert positive-only, Mapper present, pdip solver, jacobi mode); lossless `sym_tri_xor` Q encoding and an external-storage contract in `_corpus.py` (manifest `storage`, `sha256`, `bytes`, `regenerate`; `ExternalCorpusMissing` / `CorpusHashMismatch`); copies at RAL `/mnt/ral/jnightin/autolens_profiling_corpus/` and the laptop canonical checkout; `hpc/batch_gpu/submit_lens_solver_mapper_corpus_a100_fp64`; artefacts for accuracy, timing and batched_divergence over the three groups, CPU (tag worktrees) and A100 (job 399225, euclid-ral-gpu-2, 6:20); ledger section "Phase 5 (2026-10-08) — Mapper corpus"; wiki research page "Mapper corpus (phase 5)" with the recommendation table; campaign page row and Next; README auto-tables.

**Result:** `pdip_jacobi` converged on 24/24 systems with 0/24 A100 batched-vs-unbatched sensitive lanes (max |Δ| 1.5e-12; the batched Cholesky still rounds differently at k=0, nothing amplifies it). `pdip_raw` admissible under the phase-1 rule, stated as extended to this corpus, on Delaunay and mixed; both PDIP modes fail criterion 2 on rectangular (significant-column error 0.956 / 1.05). `certified` fails on mixed (1/8 uncertified) and rectangular. Cost per evaluation at batch 8 on the A100, compile separate (~1 s): raw 1.05× (Delaunay), 1.62× (rectangular), 1.15× (mixed) the Jacobi cost; CPU 1.01× / 1.77× / 1.19× under heavy background load. Recommendation the evidence supports: option A — keep Jacobi for Mapper; D (move to raw+polish) adds no stability these systems need and costs more.

**Human decision 2026-10-08:** keep Jacobi as the Mapper default and raw+polish for MGE-only; no library, tolerance, cap or pin change. Canonical record PyAutoPulse `decisions/linear-solver-mapper-default-jacobi.md` (Pulse PR #38). This closes the programme's open question; the task returns to Pulse for the final status flip.

**Caveats / not established:** all vectors near-truth (wide-prior systems unmeasured); interferometer group skipped (no importable harness); laptop CPU batched vs unbatched Jacobi differ by ≤ 4.2e-13 at n ~ 1500 (bit-identical at n = 60) without changing iterations or flags, not localised; why mixed systems stay Jacobi-stable despite signal-free MGE columns is not established; accuracy.py ran with `--repeats 1` (its wall is context only); regenerating a group reproduces the systems but not necessarily the bytes (zip timestamps); a stray process overwrote `results/breakdown/imaging/mge_breakdown_hst_v2026.8.17.1.*` in the worktree at 10:59 and was reverted, nothing committed from it. RAL sibling worktrees `autolens_profiling_wt/linear-solver-p{3,3b,4a,5}` remain for the human to prune.

**Remainder:** none filed. Revisit conditions are in the decision record (wide-prior or production Mapper system found Jacobi-unstable; an interferometer corpus; PDIP/Jacobi/polish or cuSOLVER changes; a rectangular accuracy study). Pulse task: mge_nnls_fix_pyautoarray_571_slam_60.

## Original prompt

# Linear-solver programme phase 5: a Mapper (pixelized) corpus — is raw+polish admissible and is Jacobi stable on the systems pixelized likelihoods actually produce?

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- linear-solver
- gpu
- pixelization
Difficulty: moderate
Autonomy: supervised
Priority: medium
Consequence: judge
Status: active
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/399
Depends-on: complete/2026/10/linear-solver-p3b-gpu-timing.md; autolens_profiling#398 (phase 4a: the A100 Jacobi batched/unbatched divergence is batch-shape-dependent Cholesky rounding amplified on Jacobi-unstable systems)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md

## Original request (chat 2026-10-08)

"I want a fast solution but it also needs to be stable for all likelihood functions." Options were
laid out (wrap up / one bounded evidence step / switch the Mapper default now / keep probing
Jacobi); the human chose the bounded evidence step: "Lets do option 2".

## Why

Every phase so far ran on SLaM MGE systems (n = 60). The programme's open decision is the Mapper
(pixelized) GPU default, which is Jacobi today, and no pixelized system has been through the cells.
Jacobi's known trigger is the scaling of signal-free MGE columns, which pure Mapper systems do not
have — but the production SLaM pixelized stages are *mixed* (lens light MGE + source pixelization),
where both the trigger and the Mapper default apply. Raw+polish is fast and bit-stable on MGE but
its admissibility on pixelized systems is untested.

## Scope

1. **Capture new corpus groups** with new `--source` runners in `scripts/lens/solver/capture.py`
   (same `_recording_solver` wrap of `reconstruction_positive_only_from`, post-regularisation,
   pre-Jacobi; `_corpus.add_group` computes the fnnls reference; existing groups untouched):
   - `delaunay_hst`: imaging, parametric lens mass + Delaunay source (the profiling repo's HST
     Delaunay preset), ~8 parameter vectors (near-truth + spread);
   - `rectangular_hst`: same with the default rectangular mesh, ~8 vectors;
   - `slam_mixed_hst`: lens light 2×20 MGE + Delaunay source (the SLaM source_pix configuration),
     ~8 vectors — the production case;
   - optional `interferometer_delaunay`: ~4 vectors if the interferometer harness captures cleanly.
   Record `no_regularization_index_list`, `source_column_index_list`, model, n, and confirm the
   positive-only solver setting the captured path used.
2. **Run the existing cells over the new groups**, CPU and one A100 job: `accuracy.py` (all
   candidates), `timing.py` (batch sizes scaled to n; compile separate), `batched_divergence.py`.
3. **Judge** against the phase-1 pre-registered rule, stated as *extended* to this corpus (it was
   pre-registered for MGE): is raw+polish admissible on Mapper and mixed systems; does Jacobi
   diverge or show the A100 batched/unbatched sensitivity on any of them; what does each cost.
4. **Write-up**: extend `wiki/research/jacobi_a100_batched_divergence.md` (or a sibling page) with
   the Mapper evidence and a recommendation table for the default decision; ledger rows; README
   auto-tables; campaign page Next line. No default, pin or tolerance changes here.

## Witness

New corpus groups in `results/lens/solver/corpus/`, CPU + A100 artefacts for the three cells over
them, the wiki recommendation table; `ruff`, `build_readme.py --check`, lint smoke.

## Compute

One A100 job (minutes to tens of minutes; n up to ~1600 batched fp64) from the private base
`/mnt/ral/jnightin/PyAuto_wt/linear-solver-p3` via the RAL `autolens_profiling_wt/linear-solver-p4a`
worktree. CPU on the laptop from tag worktrees. Needs separate compute authorization.
