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

## jax-inference-profiling
- title: JAX profiling — inference programme
- ledger: autolens_profiling/results/notes/inference/PROGRAMME.md
- cortex-half: PyAutoCortex/epics.md#jax-inference-profiling
- status: science half → Cortex 2026-09-01 (the whole programme's runs and rulings now live in
  PyAutoCortex `phases/inference_programme/`; the ledger stays at PROGRAMME.md and this entry
  stays the Mind's half — REWOUND to Phase 1, the InferenceRefs_v1 refs redo awaiting ruling)
- notes: DECISIONS.md (append-only gate log) and phase_<NN>_*/RESULTS.md sit beside the ledger; slices ship as autolens_profiling issues/PRs, not Mind prompts.
  REWOUND 2026-08-31 to Phase 1 (InferenceRefs_v1); mesh-pix runs quarantined to output/legacy_wrong, MGE to output/legacy (reusable pending batch review); redo runs step-by-step under batch-and-review; gates A/B1/B2 provisional; queue anchor autolens_profiling#200.

## cluster-strong-lensing
- title: Cluster strong lensing — Source & Cluster arc
- ledger: draft/feature/autolens/source_cluster_arc.md
- cortex-half: PyAutoCortex/epics.md#cluster-strong-lensing
- notes: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues.

## graphical-ep
- title: Expectation propagation (EP) campaign
- ledger: draft/research/graphical_ep/ep_campaign.md
- cortex-half: PyAutoCortex/epics.md#graphical-ep
- notes: umbrella phase map — each phase's real content lives in its own prompt under draft/research/graphical_ep/; the campaign file itself is never issued.

## euclid-dr1-prep
- title: Euclid DR1 preparation — 15k-lens modelling prep
- ledger: draft/feature/euclid/euclid_dr1_prep_epic.md
- cortex-half: PyAutoCortex/epics.md#euclid-dr1-prep
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
  solution — don't build it". The full renumbering table is in the ledger. Source of truth for all drift is /mnt/c/Users/Jammy/Science/euclid.
  Phase 0 shipped 2026-08-28; phase 1 shipped 2026-08-29 (euclid#43 closed, PR #44
  merged); phase 2 shipped 2026-08-29 (euclid#45 closed, PR #46 merged) — which also
  satisfies phase 4's "2 strongly preferred" gate. Phase 3a was INSERTED 2026-08-31
  (docs: restore the in-script narrative prose lost at 355b309; start_here.py back to a
  full end-to-end guide) and the old phase 3 renumbered to 3b; on 2026-09-01 the letters
  died in the Cortex split and 3a/3b became plain 3/4. Phase 3 shipped 2026-09-01
  (euclid#47 closed, PR #48 merged; record
  complete/2026/09/restore-pipeline-narrative-prose.md). Phase 4 is IN FLIGHT since
  2026-09-02 on euclid#49 (the pre-opened Cortex gate ref, reused — never open a second);
  prompt active/cpu_vis_lp_jax_vis_pix_numba_submission.md, branch
  feature/euclid-cpu-two-stage-route.

## ci-timing-fast-tests
- title: CI test timing — finish the board, fast physical tests
- ledger: draft/feature/pyautoheart/ci_timing_fast_tests_epic.md
- notes: 9 phased prompts (1-9) — finish the timing board (smoke-timings ingester, permanent history in PyAutoHeart, dead unit-test/import/testmode legs live), snapshot a LEGACY timing round, then the _test physical+fast rebuilds (autogalaxy rehearses, autolens follows; one pin-regeneration wave each), CI caches, user-workspace/HowTo pass, and a source hot-spot census. ALL other source/workspace development is paused while this epic runs (stable state of truth; pin changes validated by unit tests + developer/profiling workspaces). Issue ONE phase at a time — no bulk issue queues. Design doc: docs/pyautoheart/test_performance_board_assessment.md (Planes B/C are phases 1-2).

## image-source-mappings
- title: Image ↔ source plane mappings — regions, clumps, subplot_mappings, ShapeSolver validation, guide
- ledger: draft/feature/autoarray/image_source_mappings_epic.md
- status: phase 1 SHIPPED 2026-09-02 — PyAutoArray#517 merged, issue #515 closed, record `complete/2026/09/image-source-mappings-p1.md`; phase 2 (+2a) **SHIPPED** 2026-09-02 — PyAutoArray#518 (`c9f67e78`) → PyAutoLens#720 (`091fbdff`) merged, issue #719 closed, record `complete/2026/09/image-source-mappings-p2.md`; **both PyAutoArray and PyAutoLens releases are outstanding** (`pending-release`); phase 3 **ACTIVE** 2026-09-03 — autolens_workspace#525 opened by user decision ahead of the releases, worktree `image-source-mappings-p3`, four `pending-release` PRs to come
- notes: three phase prompts — Phase 1 PyAutoArray (`Mapping`/`ImageRegion` objects, `Inversion.source_clumps_from`, `regions=` overlay on `plot_array`/`plot_inversion_reconstruction`, restored `subplot_mappings`), Phase 2 PyAutoLens (ShapeSolver as the parametric engine + validation suite, `autolens/lens/mappings.py`, fit-level `subplot_mappings`, brightest multiple-image positions for spectroscopic follow-up), Phase 3 workspace (`guides/mappings.py`, tutorial_2_mappers rewrite with polygons, dead index-section fixes). Library-first; issue ONE phase at a time. Proceeds alongside ci-timing-fast-tests by user decision (2026-09-02).

## gaussian-deflections-precompute
- title: Fixed-geometry deflection memo — rescale Gaussians by the free mass-to-light ratio (numpy + JAX)
- ledger: draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md
- status: phase 1 SHIPPED 2026-09-03 (record complete/2026/09/gaussian-precompute-p1.md) — issue PyAutoGalaxy#601 closed, PyAutoGalaxy#602 (`a647aa32f`) + autolens_profiling#214 (`5f7a3ab1d`) merged; Basis-30 hst 135.6 → 6.3 ms (21.5x), SLaM-shaped likelihood 3.0x bit-identical; PyAutoGalaxy pending-release; phase 2 next (draft/feature/autogalaxy/gaussian_precompute_p2_jax_trace_time_constant.md); phase 2 in flight 2026-09-03 — PyAutoGalaxy#604 (active/gaussian_precompute_p2_jax_trace_time_constant.md)
- notes: three phase prompts — gaussian_precompute_p1_numpy_memo.md (SHIPPED, folded into
  complete/2026/09/gaussian-precompute-p1.md), draft/feature/autogalaxy/gaussian_precompute_p2_jax_trace_time_constant.md,
  draft/feature/autogalaxy/gaussian_precompute_p3_downstream_sweep.md (numpy memo + witness; JAX
  trace-time constant; downstream sweep). Successor to numpy-deflections-cpu (archived ledger
  complete/archive/epics/numpy_deflections_cpu_speedup.md). Profiling home
  autolens_profiling/scripts/lens/deflections/.

## mind-post-cortex
- title: Mind after the Cortex — shed the science-epic scaffolding, add the PR ledger
- ledger: draft/maintenance/pyautomind/mind_post_cortex_epic.md
- notes: five phased prompts from the 2026-09-03 assessment — (1) retire the two-slot-batching
  epic keeping witness campaign / tier-A shadow / slice as standalone prompts and reconcile the
  five stale 2026-08-31-pm active.md rows; (2) delete the science residue (cortex-half keys,
  jax-inference-profiling entry, Lane:/epic-slice/theme-sweep, phantom experiment/ work-type,
  five RAL prompts → Cortex phases, am batch record); (3) schematise library-pr/workspace-pr +
  PR column + pending-release view; (4) batch plan fidelity (derived backpressure, queue order,
  merge order, batch-record drift checks); (5) Heart freeze flag. Issue ONE at a time, in order.
