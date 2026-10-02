# Epics

Long-running multi-phase programmes — work that is bigger than any one task
and outlives any single issue. Each entry names the epic's canonical
**ledger**: the file that holds its phase/gate state, wherever it lives. The
dashboard renders these under In flight with a one-tap resume prompt that
works out where the epic stands from its ledger and continues it from the
next logical point — nobody should have to hunt for the issue that pairs
with an epic's current phase.

Schema per entry: `## <slug>` then `- title:` / `- ledger:` / `- notes:`
(and optionally `- status:` for a coarse, durable state — never per-phase
detail, which belongs in the ledger).

An entry whose `status:` **begins** SHIPPED or COMPLETE is retired by
`lifecycle.py epics --retire` (run by `dashboard_refresh.yml` on main): its
ledger moves to `complete/archive/epics/` if it was under `draft/` or
`active/`, the entry's text is appended there, and the entry is deleted from
this file.

A member prompt declares its membership in its own header: `Epic: <slug>`
(this file's slug) plus an optional `Phase: <n>`. The dashboard then keeps
members out of the pick lists and work-type sections and shows them only
grouped, phase-ordered, under their epic — worked in order through the
epic, never picked standalone.

## profiling-organ-birth
- title: Profiling organ — the cross-project dashboard layer above the `<lib>_profiling` project repos (name tbd): instance registry, `profiling-summary` read contract, organ board, cockpit transition
- ledger: draft/feature/pyautomind/profiling_organ_p0_name_row_and_boundaries.md
- status: filed 2026-10-02; phase 0 awaits the human's name choice and `gh repo create`; phase 1 (project-side contract in autolens_profiling) can start now
- notes: human request 2026-10-02 to begin the organ filed from the 2026-10-01 intake; design authority is `PyAutoBrain/docs/research/profiling_inference_organs.md` (Brain #444, read contracts and acceptance cases) on `ecosystem_levels.md` (Brain #440, roles not hierarchy) — do not re-derive either. Same layering as PyAutoEyes over `<lib>_visualization` (precedent `complete/2026/09/pyautoeyes-organ-decision.md`): project repos own producers, results, drift policy and their own Pages page; the organ owns the registry, the versioned read contract, ingest receipts and the cross-project board; the Brain's profiling conductor is the only judge. Phases under `draft/feature/`: 0 name + organ row + boundaries (`pyautomind/profiling_organ_p0_name_row_and_boundaries.md`, human-gated: name, fresh `gh repo create`, org-profile row; name candidates PyAutoPulse / PyAutoMuscle / PyAutoReflex / PyAutoMetabolism, human picks), 1 `profiling-summary` v1 exporter in autolens_profiling (`autolens_profiling/profiling_summary_v1_exporter.md`, not gated on the name), 2 organ skeleton — registry, reader, receipts, board, workflows (`profiling_organ/profiling_organ_p2_skeleton_registry_reader_board.md`; placeholder target folder renamed at phase 0), 3 Brain board strip + cockpit identity transition (`profiling_organ/profiling_organ_p3_brain_board_cockpit_transition.md`; supersedes `pyautobrain/register_profiling_dashboard_on_brain_board.md` unless that ships first), 4 second real `<lib>_profiling` adopter — no prompt until a real producer exists (spec: never manufacture empty siblings; a fixture is phase 2). Repoint the ledger to `<Name>/dashboard.md` once phase 2 lands. Issue ONE phase at a time. The inference organ is a separate epic, not started.

## point-source-cpu-speed
- title: Point-source (single-source) PointSolver CPU speed-up
- ledger: autolens_profiling/wiki/campaigns/point_source_image_plane_cpu.md (full record: results/notes/point_source_cpu_campaign.md)
- status: phases 1-3 shipped (p2 + p3 released in 2026.9.26.1: PyAutoArray `7fa8d271`, PyAutoLens `86054bbc`); phase 4a (re-baseline + solver-config sweep, workspace-only) shipped 2026-09-27 (autolens_profiling#321, merge `3e4a068`; record `complete/2026/09/point-source-cpu-p4.md`; step 0 = 66 % of the call, default solver complete, no library extent default change); phase 4b (step-0 containment without the (N,3,2) gather) shipped 2026-09-27 (PyAutoArray#580, merge `4383ea8`, pending release; autolens_profiling#330, merge `81af10f`; record `complete/2026/09/pointsolver-step0-gather.md`; `structured` default, 1.44x single / 2.27x vmap-16 on RAL 8490H job 357321); phase 4c (`MAX_CONTAINING_SIZE` 15 → 20, human-chosen at +6.2 % scalar for 3 triangles of headroom over the observed max 17) shipped 2026-09-27 (PyAutoArray#584 `9428eca`, PyAutoLens#753 `e92bde0`, pending release; autolens_profiling#335 `c1523ef`; record `complete/2026/09/pointsolver-mcs-headroom.md`); folder split shipped 2026-09-26 (autolens_profiling#318, merge `a5e3cdd`: `scripts/point_source/` → `scripts/point_source_image/` + `scripts/point_source_source/`; record `complete/2026/09/point-source-folder-split.md`); source-plane phase 1 (breakdown instrument) shipped 2026-09-26 (autolens_profiling#317, merge `f79ebf2`; record `complete/2026/09/point-source-source-plane-breakdown.md`) — source-plane phase 2a (RAL CPU/A100 rows + pytree-input A/B) shipped 2026-09-27 (autolens_profiling#323, merge `9c0203e`; record `complete/2026/09/point-source-source-plane-p2a.md`; human NO-GO on the PyAutoFit flatten lever, 0.0385 ms < 0.05 ms bar) ; source-plane phase 2b (backward-pass A/B) shipped 2026-09-27 (autolens_profiling#327, merge `4dc05a4`; record `complete/2026/09/point-source-source-plane-p2b.md`; forward-mode gradient GO, −38–46 %) ; source-plane phase 2c (fwd/rev crossover) shipped 2026-09-27 (autolens_profiling#331, merge `4c267b7`; record `complete/2026/09/point-source-source-plane-p2c.md`; no crossover through n=24) ; source-plane phase 2d (analysis-declared `gradient_mode`) shipped 2026-09-27 (PyAutoFit#1649 `867af1c`, PyAutoLens#752 `b3c9b68`, pending release; record `complete/2026/09/point-source-gradient-mode.md`) ; source-plane phase 2e (real MultiStartAdam confirmation) shipped 2026-09-27 (autolens_profiling#336, merge `17e2596`; record `complete/2026/09/point-source-source-plane-p2e.md`) — source-plane campaign core COMPLETE; parked candidates: blackjax forward mode, A100 vmap throughput row
- notes: human decision 2026-09-26 — SINGLE-SOURCE only, the `scripts/point_source_image/` + `scripts/point_source_source/` use case (formerly `scripts/point_source/`); the cluster use case moved to epic `cluster-pointsolver-speed`. Phase-4 campaign prompt recorded at `complete/2026/09/point-source-cpu-p4.md` (phase 4a, autolens_profiling#321, merge `3e4a068`; its `## Original prompt` holds the campaign contract); phase 4b shipped (record `complete/2026/09/pointsolver-step0-gather.md`); phase 4c shipped (record `complete/2026/09/pointsolver-mcs-headroom.md`); open members: `draft/feature/autolens/pointsolver_extent_sanity_check.md`, `draft/feature/autolens_workspace/pointsolver_grid_extent_per_package.md`, carried leftovers `draft/research/autolens_profiling/pointsolver_cpu_speed_campaign_remainder.md`; source-plane member prompt `draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md` (phases 2+, re-filed at close-out; ledger `results/notes/point_source_source_plane_campaign.md`) (re-tagged from `cluster-strong-lensing`, which is the unrelated Source & Cluster arc). Records `complete/2026/09/point-source-cpu-p{1,2,3,4}.md`. Issue ONE bounded phase at a time; any library default change (PyAutoLens `shape_solver.py` / PyAutoArray `MAX_CONTAINING_SIZE`) is a human decision at the phase-4a checkpoint.

## cluster-pointsolver-speed
- title: Cluster PointSolver — robustness and performance
- ledger: draft/research/autolens_profiling/cluster_pointsolver_speed.md
- status: Expanded by human agreement 2026-10-01 to own robust analysis settings, numerical correctness and performance. Carries Source & Cluster phase-1 remainder, phase-2 profiling coverage and forward ShapeSolver work; completed 1a–1d retained as linked evidence. No new task issued. Next production candidate: observable overflow with invalid-result policy and CI witnesses; representative-data/baseline profiling can be scoped concurrently with unresolved accuracy research, subject to repo claims.
- notes: Stable epic identifier retained. autolens_profiling owns campaign evidence and robust-settings/cost guidance; autolens_workspace_test owns bounded numerical regressions in required PR smoke or scheduled/release CI. Failing cases may be timed diagnostically but cannot underpin accepted speed/settings claims. Reconcile old profiling coverage with completed single-source campaigns; no duplication. Previous repo wiki/campaigns/cluster_pointsolver.md is the speed-only survey; reconcile it at first implementation, with this Mind contract authoritative for the expanded plan. Issue ONE bounded task at a time, no bulk queue.

## graphical-ep
- title: Expectation propagation (EP) campaign
- ledger: draft/research/graphical_ep/ep_campaign.md
- notes: umbrella phase map — each phase's real content lives in its own prompt under draft/research/graphical_ep/; the campaign file itself is never issued. Science half: PyAutoCortex `projects/{analytic_gaussian,ep_toy_gaussian,slope_hierarchy_scale,ic50_workspace}.md` (campaign phases 1b, 3 and 4).

## euclid-dr1-prep
- title: Euclid DR1 preparation — 15k-lens modelling prep
- ledger: draft/feature/euclid/euclid_dr1_prep_epic.md
- status: science half → Cortex 2026-09-01 (old phases 4, 5, 6a, 6b are now PyAutoCortex
  `phases/euclid/` 4, 5, 6, 7); the Mind keeps the software phases, renumbered 3a→3, 3b→4,
  6c→8, 7→9 — the renumbering table is in the ledger
- notes: 7 Mind phases (0, 1, 2, 3, 4, 8, 9) — issue ONE at a time as predecessors near
  shipping, no bulk issue queues. The four science phases moved to PyAutoCortex on
  2026-09-01 as `phases/euclid/` 4, 5, 6, 7 (were Mind 4, 5, 6a, 6b): RAL runs, human-driven
  and supervised, whose deliverable is a result and a written verdict, not a merged PR;
  never route them to an autonomous ship gate. Mind phase 8 (was 6c) is a PyAutoArray source
  audit that may spawn a separate bug prompt and can run alongside Cortex phase 7. Mind
  phase 9's (was 7) retroactive-update leg is explicitly allowed to conclude "no elegant
  solution — don't build it". The full renumbering table is in the ledger. Source of truth for
  all drift is /mnt/c/Users/Jammy/Science/euclid. Science half: PyAutoCortex
  `projects/euclid_dr1_prelim.md` (the former Cortex phases 4-7).
  Phase 0 shipped 2026-08-28; phase 1 shipped 2026-08-29 (euclid#43 closed, PR #44
  merged); phase 2 shipped 2026-08-29 (euclid#45 closed, PR #46 merged) — which also
  satisfies phase 4's "2 strongly preferred" gate. Phase 3a was INSERTED 2026-08-31
  (docs: restore the in-script narrative prose lost at 355b309; start_here.py back to a
  full end-to-end guide) and the old phase 3 renumbered to 3b; on 2026-09-01 the letters
  died in the Cortex split and 3a/3b became plain 3/4. Phase 3 shipped 2026-09-01
  (euclid#47 closed, PR #48 merged; record
  complete/2026/09/restore-pipeline-narrative-prose.md). Phase 4 shipped 2026-09-03
  (euclid#49 closed, PR #50 merged; record complete/2026/09/euclid-cpu-two-stage-route.md) —
  all Mind software phases 0-4 are now shipped, and both gates of the Cortex 10-lens science
  run (euclid#48, euclid#49) are closed. Phase 8 (Delaunay area audit) shipped 2026-09-04
  (PyAutoArray#522 closed, PR #523 merged, audit on the issue; record
  complete/2026/09/delaunay-area-magnification-audit.md): two defects proven and filed as follow-up
  bug prompts (autoarray Voronoi-vs-dual-area denominator; autolens magnification latent 0/0
  for pixelized sources — which also taints the vis_pix catalogue column Cortex phase 4
  witnesses). The autoarray fix shipped 2026-09-05 (PyAutoArray#524 closed, PR #525 merged,
  pending-release; record complete/2026/09/delaunay-dual-area-magnification.md); the autolens
  fix is next. Mind phase 9 remains, gated on Cortex phase 4.

## model-figures
- title: PyAutoFit model figures — structure-first model visualisation (caskade-style, scales to MGE/graphical/EP)
- ledger: draft/feature/autofit/model_figures_epic.md
- notes: phase 1 SHIPPED 2026-09-11 (complete/2026/09/model-figures-graph-spec.md, PyAutoFit#1606); phase 2 SHIPPED 2026-09-11 (complete/2026/09/model-figures-renderer.md — PyAutoFit#1614 + autofit_workspace#152 merged, pending-release PyAutoFit); phase 3 SHIPPED 2026-09-11 (complete/2026/09/model-figures-lens.md — PyAutoFit#1615 + PyAutoArray#550 + PyAutoGalaxy#616 + PyAutoLens#737 + autolens_workspace#541 + autogalaxy_workspace#240 merged, pending-release ×4; `__solved_parameters__` protocol); phase 4 SHIPPED 2026-09-12 (complete/2026/09/model-figures-graphical.md — PyAutoFit#1617 + autofit_workspace#153 + HowToFit#51 merged, pending-release PyAutoFit; plate notation, hoisted shared priors, hierarchical draws are not sharing); phase 5 SHIPPED 2026-09-13 (complete/2026/09/model-figures-ep-view.md — PyAutoFit#1619 merged, pending-release PyAutoFit; EP factor-graph view, af.EPPlotter, graph_model.png/graph_state.png); phase 6a SHIPPED 2026-09-13 (complete/2026/09/model-figures-rollout-autofit.md — PyAutoFit#1621 + autofit_workspace#154 + HowToFit#52 merged, pending-release PyAutoFit; figures beside every model.info in autofit_workspace + HowToFit, EP state figure); phase 6b SHIPPED 2026-09-14 in two waves (complete/2026/09/model-figures-rollout-lens.md — HowToLens#81 + autolens_workspace#543 wave 1, autolens_workspace#546 + HowToLens#83 wave 2; 102 scripts and 12 tutorials with their notebook twins). The per-figure reading commentary was RETIRED on the human's ruling the same day: every opener block is now two fixed paragraphs and the figure-rendering vocabulary is stripped from later-site notes, which supersedes 6b's "Pattern" section and retires its render-to-verify-vocabulary requirement. The same standard was swept across the six unclaimed repos as model-figure-prose-simplify (complete/2026/09/model-figure-prose-simplify.md — autofit_workspace#156, six PRs). Remaining cuts of phase 6: (b2) SLaM stages, (c) PyAutoGalaxy surfaces. 6 phased prompts; 1 → 2 → 3 in order, 4 after 2, 5 after 4, 6 (rollout across every workspace, HowTo chapter and sibling project) after 3 and 4; per-search figure output stays opt-in until phase-3 acceptance renders pass; sibling bug prompts under draft/bug/autofit/ are standalone.

## autolens-inference
- title: autolens_inference — inference benchmarking repo, birth to first base run
- ledger: autolens_inference/wiki/project/state.md
- notes: phase 1 SHIPPED 2026-09-10 (complete/2026/09/autolens-inference-birth.md); phase 2 SHIPPED 2026-09-11 (complete/2026/09/scrap-inference-programme.md — autolens_profiling#246 / PyAutoBrain#376 / PyAutoMind#401; archive ref `archive/condemned/autolens-profiling/inference-programme` @ `c8b60580`); 4 phases — 1 birth + registration (PyAutoMind#399), 2 Gut-archive and delete autolens_profiling's searches tier / baselines / inference notes (nothing inherited), 3 backend-parameterised SLaM driver + per-stage results + submit scripts (SHIPPED 2026-09-11, autolens_inference#3, complete/2026/09/slam-base-driver.md), 4 the first run on PyAutoCortex `projects/autolens_inference.md` (5-stage HST SLaM × {numba_cpu, jax_cpu, jax_gpu} × {dense, sparse}). Science half: that ledger. Ledger moved to autolens_inference/wiki/project/state.md when phase 3 landed 2026-09-11.

## linear-solver-programme
- title: Linear-solver accuracy/tolerance programme — a standing autolens_profiling package for positive-only solver studies
- ledger: autolens_profiling/wiki/campaigns/linear_solver_accuracy.md (contract: complete/2026/09/linear-solver-accuracy-study.md)
- status: phase 2 SHIPPED 2026-09-30 — PyAutoArray#595 merged (7a89e19a0, forward polish; pending release) + autolens_profiling#357 merged (4652580b2, ledger Phase 2 rows), issue PyAutoArray#594 closed, record `complete/2026/09/raw-pdip-forward-polish.md`; phase 1 shipped 2026-09-30 — autolens_profiling#355 merged (3ad68afad), record `complete/2026/09/linear-solver-accuracy-study.md`; next = phase 3 `draft/research/autoarray/mge_nnls_fix_pyautoarray_571_slam_60.md` (GPU/A100 timing + parity rows; blocked on a release shipping PyAutoArray#595)
- notes: human intent 2026-09-30 — solver tolerance/accuracy keeps recurring (#571/#572/#573, certified solver, 07-09 NNLS ledger, warm-start memo), so it gets one home that accumulates runs and data across releases. Phase 1 = `scripts/lens/solver/` package + corpus + CPU fp64 accuracy/early-stopping study + pre-registered rule + wiki page. Phase 2 = PyAutoArray fix per the verdict (shipped: `complete/2026/09/raw-pdip-forward-polish.md`; library-first, then re-verify the euclid latent test on library main). Phase 3 = GPU/vmap/A100 timing + parity rows (absorbs `draft/research/autoarray/mge_nnls_fix_pyautoarray_571_slam_60.md`). Standing: re-run the accuracy cell per release.
