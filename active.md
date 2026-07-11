# Active Tasks

## starred-epsf-backend
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/35
- status: library-dev — optional STARRED super-sampled ePSF back-end for PyAutoReduce PSF stage. Design settled (2026-07-11 deep research): STARRED PSF-recon = standalone field-star ePSF (Moffat+starlet), reduction-stage Tier-1b, NOT the mislabelled Tier-3 target-reconstruction; two-channel deconvolution stays modelling-stage/out-of-scope. First edits: doc correction (hst_acs_pipeline Tier-3 → Tier-1b) + psf/starred_epsf.py seam mirroring fallback.py.
- constraints: STARRED is GPL-3.0-or-later → optional extra `pyautoreduce[starred]`, lazy import, GPL-isolated, never core. Depends on jax → prototypes/integration only, unit tests numpy/astropy (pytest.importorskip). Crux = drizzle-consistency of the super-sampled PSF onto mosaic grid (rebin vs frame_combine drop-convolve + WCS-Jacobian).
- progress: worktree live; commits local (NOT pushed) c6f83c2 doc-correction + seam psf/starred_epsf.py (loud hard-stop, 18 psf tests pass) + 79fe71f prototypes/starred_epsf_spike.py. SPIKE DONE (feasibility POSITIVE, findings on #35 comment-4947664108): STARRED 1.6.0 in dedicated ~/venv/starred (deps CONFLICT w/ PyAuto stack → validates isolation); build_psf(cutouts,noisemap,subsampling)→{full_psf,narrow_psf} super-sampled; Downsample route-a holds centring on 21×21; STARRED PSF cleaner than noisy tier-1 on F115W. Dataset = reused reduced COSMOS-Web F115W (~28 clean stars, NO download); star/compact-source mix = mechanics-validation not science-grade.
- consistency: DONE (adversarial ground-truth test prototypes/starred_drizzle_consistency.py, commit 635aeb0, findings #35 comment-4947816896). Route-a Downsample IS drizzle-consistent for well-sampled PSFs WITH centroid-preserving delivery (baseline centroid 0.002px, flux exact, size≤3%); route-b frame_combine NOT needed for centring. FOUND+FIXED half-pixel trap: naive even→odd crop=0.63px offset, centroid-crop+subpixel-recentre=0.009px (geometry_only check). Limits: undersampled FWHM≲1.3px→~24% broadening; N=4 low-SNR→0.13px wander+~40% broaden. no_dither harmless when well-sampled.
- wiring: DONE (commit 8a941ae, #35 comment-4947955572). build_starred_epsf implemented (extraction→build_psf→Downsample+centroid-preserving delivery+guards+provenance); dispatch via TargetSpec.psf_backend="starred" (noise plumbed into _psf); optional extra pyautoreduce[starred] (starred-astro>=1.6, autoreduce has NO astropy/scipy caps so coexists). Validated end-to-end F115W: 25 stars, psf/psf_full unit-sum, centroid_residual 0.008px, well-sampled. 206 tests pass. End-to-end caught 2 bugs unit-tests missed: (1) fixed 32px stamp can't deliver 61px psf_full→derive stamp from psf_full_shape; (2) global-COM recenter biased by asymmetric wings 0.69px→center on peak-windowed CORE 0.008px (COM-centering an asymmetric PSF is WRONG).
- comparison: ATTEMPTED on F115W (commit 1d0931f, #35 comment-4948021751) — INCONCLUSIVE by design: empirical sub-pixel-registered star-stack central-3x3 conc=0.04 → the "point sources" are EXTENDED GALAXIES not stars (real undersampled F115W star ~0.5-0.8), so no valid absolute PSF comparison possible on ANY reduced field (all extragalactic lens targets). STARRED conc=0.82 (matches F115W's ~1.3px PSF) resists the galaxy contamination photutils averages in (conc 0.11≈empirical 0.04) — suggestive STARRED more robust but UNVERIFIABLE without real stars. Naive per-source χ² is registration-dominated (rewards flat PSFs) — INVALID, don't use.
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/36 (release-labeled; branch pushed; --psf-backend example added to reduce_cosmos_web_ring.py; black-clean, 206 tests). User chose SHIP 2026-07-11.
- shipped: SHIP done — PR#36 open awaiting human merge; follow-up #37 filed (definitive stellar-field science comparison, HEAVY MAST+drizzlepac+CRDS, deferred). Back-end functionally COMPLETE. On merge: retire entry, worktree cleanup. Traps: reduction.json "96 stars"=JWST-config not strict point-src; worktree lacks gitignored outputs→reads canonical checkout; build_starred_epsf runs only in starred venv w/ autoreduce on PYTHONPATH; PyAutoReduce release label = "release" not "pending-release", add via gh api --input JSON array (`-f labels[]=` 422s).
- worktree: ~/Code/PyAutoLabs-wt/starred-epsf-backend (off origin/main; NOT the dirty feature/pj011646-wfc3-parity checkout)
- repos:
  - PyAutoReduce: feature/starred-epsf-backend

## lenstool-scaling-reference-magnitude
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/265
- status: workspace-dev — LensTool reference-magnitude (mag0) scaling-relation convention; explicit fixed reference luminosity (not max-of-sample), fixed exponent 0.5, full dPIE r_core/r_cut/b0 scaling (add ra_ref). 3 sequential PRs: [PR1 cluster = OPEN #267, unmerged] → PR2 group+imaging feature examples → PR3 SLaM pipelines
- pr1: https://github.com/PyAutoLabs/autolens_workspace/pull/267 (cluster; pending-release; Heart YELLOW ambient-acked at ship; b0/rs preserved <1%, ra now scales; dataset regenerated; cluster/simple gitignore-allowlisted)
- gotcha: notebook regen (generate.py autolens) surfaces PRE-EXISTING drift — 5 multi/features notebooks + llms-full.txt/workspace_index.json catalogue restated on main; MUST revert those and stage cluster-only (did so for PR1). cluster simulator preview-plot step crashes on matplotlib._api.check_getitem (pre-existing venv bug, post-write, cosmetic)
- note: CONCURRENT with markdown-renderings-workspaces batch 2a (#264) by user override 2026-07-10 — file sets disjoint (2a edits config/*.yaml, cluster EXCLUDED; ours edits scripts/). Watch for notebook-regen collisions on group/imaging at merge time
- worktree: ~/Code/PyAutoLabs-wt/lenstool-scaling-reference-magnitude
- repos:
  - autolens_workspace: feature/lenstool-scaling-reference-magnitude

## benchmark-calibration
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/59
- status: workspace-dev — first calibration campaign: teacher × {sonnet, haiku} + easy × {sonnet} via claude-code-subagent harness, serial (memory); records → benchmarks/runs/, RESULTS.md regen, rubric verdict on issue; PR at end
- autonomy: supervised effective (human-directed launch 2026-07-10 in-conversation, continuing #57 --auto chain; heart-ack: same set as #58 ship, in-session)
- note: judge = claude-fable-5 (this session) for judged rows; operator replies honest/minimal via SendMessage; failures recorded
- worktree: none (in-place: autolens_assistant on feature/benchmark-calibration)
- repos:
  - autolens_assistant: feature/benchmark-calibration

## pj011646-wfc3-parity
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/25
- session: claude --resume cc79d958-a1aa-45cb-b088-bd6cae94aa86
- status: awaiting-input — parked at ship sign-off (gate: tests 202 pass / smoke n-a / review CLEAN / Heart YELLOW 6-reason set UNACKED); branch feature/pj011646-wfc3-parity committed locally bd9806b, NOT pushed; phases 0-2 verdicts on #25; model-parity fits parked (2 OOMs at n_live=100, laptop contended)
- autonomy: safe effective (--auto launched 2026-07-10; plan human-approved in-session pre-launch; no heart-ack given)
- note: keck-ao/slacs1430 pattern — analysis on PyAutoReduce main, NO worktree claim (jwst-frame-feasibility holds it); ship gated on claim release or human direction; autolens_assistant driver-only (in-place branch belongs to assistant-ref-mechanics — scratch writes only); model-parity fits SERIAL on quiet machine (~5.5GB)
- question: https://github.com/PyAutoLabs/PyAutoReduce/issues/25#issuecomment-4936211921
- worktree: none (analysis on PyAutoReduce main; branch feature/pj011646-wfc3-parity only at ship)
- repos:

## rect-adapt
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/372
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: MERGED 2026-07-10 (human-directed via kernel-cdf session, coordinated order #375→#374; issue #372 closed with verification upthread) — entry ready to retire to complete.md by its owning session
- pr: https://github.com/PyAutoLabs/PyAutoArray/pull/375
- autonomy: supervised effective (--auto chain 2026-07-09; bug cap binds over safe header; ship sign-off will park with question per contract)
- heart-ack: same 6-reason set as the assistant-ref-mechanics entry (in-session 2026-07-09); binds to exactly that set, any new reason parks
- note: consumers of edges_transformed = plot/inversion.py pcolormesh + mesh_geometry/rectangular_rotated.py — both inherit the fix; mcmc-corner-smoke (nightly blocker) queued in planned.md on autofit_workspace/PyAutoFit claims
- worktree: ~/Code/PyAutoLabs-wt/rect-adapt
- repos:
  - PyAutoArray: feature/rect-adapt

## slacs1430-acs-parity
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/17
- session: claude --resume cc79d958-a1aa-45cb-b088-bd6cae94aa86
- status: MERGED 2026-07-10 (0face12, squash; human-authorized in-session) — branches deleted; #17 stays OPEN for the parked model-parity leg only; entry retires to complete.md once that leg's verdict lands
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/23
- resume(model-parity leg): `~/venv/PyAuto/bin/python prototypes/slacs1430_parity_fit.py autoreduce` then `... legacy` from PyAutoReduce root; compare fit_summary_*.json; verdict on #17
- note: acquire-dupe bug prompt RETIRED (fixed on main by #18's is_direct_product; my run disclosed on PR#23 as HAP-family); PJ011646 WFC3 follow-up prompt queued (methodology notes on #17)
- autonomy: safe effective (--auto launched 2026-07-09; plan human-approved in-session pre-launch; no heart-ack given)
- note: keck-ao pattern — analysis on PyAutoReduce main, NO worktree claim (frame-products holds it); outputs gitignored scripts/output/; script commit + PR gated until claim releases; autolens_assistant is driver-only (public template, no commits, scratch only)
- worktree: none (analysis on PyAutoReduce main; branch feature/slacs1430-acs-parity only at ship)
- repos:

## keck-ao-acceptance-checks
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/13
- status: parked-resumable (laptop reset) — check 3 done: plate-scale finding (adapter 9.942 wrong; 9.952 pre-2015/9.971 post; fix gated); check 4 fit CHECKPOINTED ~1h in (94MB checkpoint.hdf5); resume command on the issue's interim comment
- resume: re-run prototypes/b1938_lens_fit.py (Nautilus auto-resumes from output/b1938_keck_acceptance identity path); then report θ_E vs 0.45" on #13; then propose keck_ao.md parity appendix + epoch-aware native_scale adapter fix (present-and-wait)
- autonomy: default present-and-wait (no --auto); analysis read-only in prototypes/, doc/adapter edits gated on user review
- worktree: none (analysis on PyAutoReduce main; branch only if an edit is approved)
- repos:

## refactor-post-phase3
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/8
- session: claude --resume be7cb926-7874-4cc2-8c05-64c9644a64d9
- status: MERGED 2026-07-09 (371721f, squash) — human-directed merge in the keck-ao session (user authorized in-conversation); main checkout returned to main; PyAutoReduce claim released. Entry ready to retire to complete.md by its owning session (branch deletion via repo_cleanup)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/10
- notes: witnesses byte-identical both paths; 2 disclosed fix riders (CPDIS fobj, ePSF window +20) caught by baseline capture
- autonomy: default present-and-wait (refactor cap safe; no --auto given)
- worktree: released (was in-place)
- repos:

## ep-analytic-updates-scope
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1337
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: complete-pending-pickup — phase 6 done; implementation plan for all 4 WPs on #1338 (plan-only, human-directed no-implement); backlog anchor feature/autofit/ep_analytic_updates.md
- plan: https://github.com/PyAutoLabs/PyAutoFit/issues/1338
- autonomy: supervised (--auto, launched 2026-07-08)
- worktree: none (read-only)
- repos:

## ep-deterministic-reconcile
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1336
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — phase 5 complete; recommendation A (keep both, document trade-off, resurrect #1153 test) on #1336 pending decision
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1336#issuecomment-4917522033
- autonomy: supervised (--auto, launched 2026-07-08)
- worktree: none (read-only)
- repos:

## ep-priors-fable-reassess
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1330
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — phase 0 complete; decision hub PyAutoFit#1331 open for maintainer/contributor guidance (fix-batch + 5 decisions)
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1331
- worktree: none (read-only reassessment on PyAutoFit main @ 0f26ff2d8; verdicts land in PyAutoMind bug/priors)
- repos:

## morning-status-release-rehearsal
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/39
- session: claude --resume ff9a8b2f-fda0-4bab-8962-1814843aa374
- status: RESOLVED 2026-07-09 (by session 5d58ef6a) — user re-set BOTH May-17 secrets (webhook + CLAUDE_CODE_OAUTH_TOKEN); morning_health dispatched → Slack POST success; digest needed 3 more CI fixes on Mind main (checkout, show_full_output, allowedTools Write; 51e869e/d042289/0b78d5f) → fully green, delivered. Details: issues/39#issuecomment-4924031684. Entry ready to retire to complete.md by its owning session
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 (independent; merge Mind last is tidiest — its morning_health reads the others)
- post-merge: dispatch morning_health.yml on Mind main (Slack POST leg); flip vars.RELEASE_MODE=live on PyAutoBuild when satisfied (human)
- autonomy: human-required effective (release cap; --auto launched 2026-07-08, plan approved in-session; ship sign-off + merge human)
- cleanup 2026-07-09: worktree removed + feature branches (local+remote) deleted via /repo_cleanup — all PRs were merged; remaining leg (webhook secret + morning_health.yml dispatch) is human-only and needs no repo claim


