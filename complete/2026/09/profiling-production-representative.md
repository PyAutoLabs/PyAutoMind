## profiling-production-representative
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/235
- completed: 2026-09-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/236
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/56
- merged: autolens_profiling 68008df (PR #236), euclid_strong_lens_modeling_pipeline 5f2b472 (PR #56)
- also: subhalo_validation main 122079f (lp radial bins, committed directly)
- heart-ack: 2026-09-08 YELLOW — "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and "release validation incomplete: no rehearsal for current source"; neither in the shipped repos

**Summary.** The CPU numba imaging cells of `autolens_profiling` now default to the production configuration per instrument — Euclid ↔ the Euclid pipeline `vis_pix` stage (530-vertex Delaunay with 30 zeroed edge, Hilbert 3.5/0.01, free `AdaptSplit` on the production priors, positions penalty 3.0/0.2, MGE 20×2), HST ↔ subhalo_validation `source_pix[2]` (1280 vertices, S/N-capped adapt image, MGE 30×2) — with pixelization over-sampling 4/2 by the source S/N>3 rule, thread env pinned to 1, an iid prior stream in place of one repeated instance, the NNLS warm-start memo explicitly off and recorded, and a post-compile cold eval plus warm iid median reported beside the production `search.summary` reference (jobs 342301 / 342311: pooled wall/sample 0.15–0.33 s, cold eval 0.45–1.13 s, speed-up 3.0–4.3). Presets and provenance live in `_production_config.py`; `--variant legacy` reproduces `main` to 0.15 %. The NNLS warm-start memo experiment moved to `scripts/misc/nnls_warm_start/` + `results/nnls_warm_start/`. The lp over-sampling outer radial bin retired sub-size 1 (`[4,2,1]` → `[4,2,2]`, `[16,4,1]` → `[16,4,2]`) across autolens_profiling (including the deflection-accuracy axis), the Euclid pipeline and subhalo_validation, every shifted pin re-measured and dated.

**Witness.** 4 of 8 production runs within 1.5× of the logged production cold eval (all four rectangular cells). Delaunay misses in opposite directions — Euclid 2.9× faster than the real-tile log, HST 1.8× slower on a laptop core — with every preset field matched: the residual is dataset realism (simulated 3.5" mask vs real VIS cut-out) and host, not configuration. Numbers and retired pins: `autolens_profiling/results/notes/production_representative_cells.md`.

**Traps / notes.**
- Production is two configurations, not one; the two presets differ in S/N cap, positions, MGE and mesh size. A single-process cell compares to the cold eval (= wall/sample × speed-up), never to pooled wall/sample.
- The Euclid pipeline's latent replay test (`tests/test_compute_latent_variable.py`) pins `truth.json` latents computed through the same over-sampling helper, and its magnification cross-check exposed a real bias: with sub-size 1 retired, the lensed arcs integrate correctly (0.03 % of converged) but the unlensed compact source at 0.18" sits in the 0.1–0.3" sub-size 2 annulus and under-integrates by ~0.6 %; the old [4,2,1] agreement was two under-integrations cancelling. Production lp bins are therefore `[4,4,2]` and the unlensed source-flux latent integrates on its own uniform over-sample-4 grid (only [4,4,4] passed by binning alone; [4,4,2] left +0.21 % from the source wings in the outer bin) — human decisions 2026-09-08; truth.json re-recorded (`simulator.py --from-params --seed 1`, FITS byte-identical). The autolens_profiling Euclid preset still says [4,2,2] — follow-up filed.
- `scripts/misc/searches/_targets.py` mirrors `_setup.py`'s over-sample recipe into `target_id` hashing — search target ids changed.
- Subagent sandboxes cannot commit under `/mnt/c/Users/Jammy/Science`; the architect session commits science-project edits.
- Deflection pins are insensitive to the lp bin (largest move 3e-11): they sit on grids the recipe does not touch.

**Follow-ups filed.** `draft/refactor/workspaces/retire_lp_sub_size_1_radial_bins.md` (autolens_workspace_test + developer sites, markdown regen); `draft/bug/autolens_profiling/breakdown_pixelization_stale_module_import.md` (JAX rectangular breakdown cell broken on main by a PyAutoArray module split). Not filed: a real cut-out profiling dataset to close the Delaunay witness gap; GPU production-representativeness for the JAX cells.

## Original prompt

# Profiling run times representative of production; NNLS warm-start to misc

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: the profiling harness's default Euclid and HST imaging cells reproduce the production vis_pix / source_pix configuration (AdaptSplit regularization, over_sample_size_pixelization 4/2 by the S/N 3.0 rule, an iid model sequence, warm-start memo per the production default) and their reported per-evaluation medians land within 1.5x of the wall-time-per-sample measured in the euclid_dr1_prelim job 342301 and subhalo_validation job 342311 logs; the NNLS warm-start scripts, results and notes live under a misc/ directory and no default profiling cell depends on them.
Review-minutes: 3
Unattended: ready
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/235


Original request (verbatim): update the autolens_profiling which the run time comes from to be representative of production runs, for Euclid but also just in general. I want autolens_profiling to match production, I think we already changed something to AdaptSplit. Also move the warm-start NNLS stuff to misc, it is not currently used in production and profiling run times should not be based on it (but maybe it will come back once we change sampler)

Context from the 2026-09-08 vis_pix timing diagnostic (euclid_dr1_prelim jobs 342301/342314 vs subhalo_validation jobs 342299/342311, both on the RAL stack at array-library commit e36a5af4 which contains the whole 2026-08-27/28 numba campaign):

- The campaign's Euclid Delaunay cells (results/breakdown/imaging/delaunay_numba_nnls_iterations_euclid_*_v2026.8.17.1.json, results/notes/nnls_warm_start_memo_matrix.md) were measured with ConstantSplit regularization, over_sample_size_pixelization=1 (hard-coded in delaunay_numba_nnls_iterations.py around line 204), a random-walk parameter sequence, and the NNLS warm-start memo on. Production vis_pix uses AdaptSplit, over-sampling 4 where source S/N>3 else 2, and a Nautilus pool whose workers see an effectively iid stream. Only the adapt_reg cell uses AdaptSplit, and it is not the default cell.
- Locally, matching production over-sampling alone moved the 530-pixel Euclid AdaptSplit cell from 0.30 s to 0.55 s (iid); the memo's 4-10x iteration saving under random walk drops to 0.88-1.05x under iid.
- The headline "<0.4 s Euclid" figure is the mesh_600 ConstantSplit random-walk memo-on row (0.426 s); the production-like row did not exist in the matrix.
- VERIFY before moving anything: neither production project sets nnls_warm_start_memo, and the array library's Settings module (settings.py, around lines 232-273) defaults it to true with tolerance 1.5, so the memo IS in effect in production today unless that default is changed. The human's intent is that profiling run times should not depend on it; decide with the human whether the production default should also be turned off, or whether profiling should measure memo-off as the production baseline and memo-on as a misc sampler-dependent experiment.

Scope:
1. Audit every default imaging profiling cell (Euclid and HST, Delaunay and rectangular) against the production pipelines (the Euclid pipeline repo's scripts/initial_lens_model.py vis_pix stage; the subhalo_validation science project's scripts/imaging.py source_pix stage): mesh type and pixel count, regularization class (AdaptSplit), over-sampling (lp and pixelization, S/N rule), sparse operator, positions penalty, MGE size, thread pinning, and the model-sequence regime (iid vs random walk). Make the defaults match production and keep the old variants as explicitly named non-default cells.
2. Report the same quantity production reports: document that the fitting library's logged likelihood evaluation time is one cold main-process evaluation (non_linear/search/updater.py in the fitting library, ~311-317) and have the harness print both a warm median and a cold first-eval so the two are comparable; add wall-time-per-sample from the .out logs as the production reference in the results notes.
3. Move the NNLS warm-start memo scripts, result JSONs and notes under misc/ (or the repo's existing equivalent bucket), leave a pointer note saying why (not used as the production baseline; may return with a sampler change), and make sure no default cell or README table cites a memo-on number as the headline.
4. Re-run the Euclid and HST default cells once and update the results tables and README with the production-representative numbers, noting the date and library commit.

Related (not a duplicate): draft/feature/autolens_profiling/numba_breakdown_harness_memo_blind.md covers the breakdown harness being blind to the cross-evaluation memo; this prompt is about the default cells and the headline numbers matching production.

<!-- formalised by the Intake (Conception) Agent on 2026-09-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/57e6c543-0042-4147-9573-df3686a157da/scratchpad/intake-profiling-production.md -->
