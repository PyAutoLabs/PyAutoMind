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

## cluster-strong-lensing
- title: Cluster strong lensing — Source & Cluster arc
- ledger: draft/feature/autolens/source_cluster_arc.md
- notes: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: PyAutoCortex tasks carrying `Epic: cluster-strong-lensing` (arc phase 11).

## graphical-ep
- title: Expectation propagation (EP) campaign
- ledger: draft/research/graphical_ep/ep_campaign.md
- notes: umbrella phase map — each phase's real content lives in its own prompt under draft/research/graphical_ep/; the campaign file itself is never issued. Science half: PyAutoCortex tasks carrying `Epic: graphical-ep` (campaign phases 3 and 4).

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
  all drift is /mnt/c/Users/Jammy/Science/euclid. Science half: PyAutoCortex tasks
  carrying `Epic: euclid-dr1-prep` (Cortex phases 4-7).
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

## image-source-mappings
- title: Image ↔ source plane mappings — regions, clumps, subplot_mappings, ShapeSolver validation, guide
- ledger: draft/feature/autoarray/image_source_mappings_epic.md
- status: phase 1 SHIPPED 2026-09-02 — PyAutoArray#517 merged, issue #515 closed, record `complete/2026/09/image-source-mappings-p1.md`; phase 2 (+2a) **SHIPPED** 2026-09-02 — PyAutoArray#518 (`c9f67e78`) → PyAutoLens#720 (`091fbdff`) merged, issue #719 closed, record `complete/2026/09/image-source-mappings-p2.md`; **both PyAutoArray and PyAutoLens releases are outstanding** (`pending-release`); phase 3 **SHIPPED** 2026-09-03 — autolens_workspace#526, HowToLens#76, HowToGalaxy#72, autogalaxy_workspace#232 merged, issue #525 closed, record `complete/2026/09/image-source-mappings-p3.md`; all three phases shipped, epic complete pending the PyAutoArray + PyAutoLens releases; library follow-ups in `draft/bug/autoarray/mapping_overlay_follow_ups_forward_regions_throu.md`
- notes: three phase prompts — Phase 1 PyAutoArray (`Mapping`/`ImageRegion` objects, `Inversion.source_clumps_from`, `regions=` overlay on `plot_array`/`plot_inversion_reconstruction`, restored `subplot_mappings`), Phase 2 PyAutoLens (ShapeSolver as the parametric engine + validation suite, `autolens/lens/mappings.py`, fit-level `subplot_mappings`, brightest multiple-image positions for spectroscopic follow-up), Phase 3 workspace (`guides/mappings.py`, tutorial_2_mappers rewrite with polygons, dead index-section fixes). Library-first; issue ONE phase at a time. Proceeds alongside ci-timing-fast-tests by user decision (2026-09-02).

## model-figures
- title: PyAutoFit model figures — structure-first model visualisation (caskade-style, scales to MGE/graphical/EP)
- ledger: draft/feature/autofit/model_figures_epic.md
- notes: phase 1 SHIPPED 2026-09-11 (complete/2026/09/model-figures-graph-spec.md, PyAutoFit#1606); phase 2 SHIPPED 2026-09-11 (complete/2026/09/model-figures-renderer.md — PyAutoFit#1614 + autofit_workspace#152 merged, pending-release PyAutoFit); phases 3 and 4 unblocked. 6 phased prompts; 1 → 2 → 3 in order, 4 after 2, 5 after 4, 6 (rollout across every workspace, HowTo chapter and sibling project) after 3 and 4; per-search figure output stays opt-in until phase-3 acceptance renders pass; sibling bug prompts under draft/bug/autofit/ are standalone.

## autolens-inference
- title: autolens_inference — inference benchmarking repo, birth to first base run
- ledger: active/slam_base_driver.md
- notes: phase 1 SHIPPED 2026-09-10 (complete/2026/09/autolens-inference-birth.md); phase 2 SHIPPED 2026-09-11 (complete/2026/09/scrap-inference-programme.md — autolens_profiling#246 / PyAutoBrain#376 / PyAutoMind#401; archive ref `archive/condemned/autolens-profiling/inference-programme` @ `c8b60580`); 4 phases — 1 birth + registration (PyAutoMind#399), 2 Gut-archive and delete autolens_profiling's searches tier / baselines / inference notes (nothing inherited), 3 backend-parameterised SLaM driver + per-stage results + submit scripts (ISSUED 2026-09-11, autolens_inference#2, branch `feature/slam-base-driver`), 4 PyAutoCortex task `slam_hst_base` (5-stage HST SLaM × {numba_cpu, jax_cpu, jax_gpu} × {dense, sparse}). Science half: PyAutoCortex tasks carrying `Epic: autolens-inference`. Ledger moves to autolens_inference/wiki/project/state.md once phase 3 lands.
