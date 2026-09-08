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
