## wiki-backfill-drift
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/343
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/344 (merge `3ea93024`, head `fc622de`, 11 files, +20/−2)
- epic: profiling-research-wiki (follow-on)
- merge: by the human's typed `/prm` on green (lint.yml one run, one job, success; `mergeable_state: clean`)
- heart: GREY at the door (Pages host not on the container allowlist); docs and ledger only

### Summary
- Nine `results/notes/` ledgers gained one dated `> **Correction — 2026-09-27:**` line beside the
  text the wiki backfill (#339 / #340) found false or stale: the #566 issue vs PR #567,
  the harness-injection scope (phases 1–3 only), the Delaunay warm-compile exception to
  "≤ 2 s warm", the alma_high outcome, the unverified date of A100 jobs 323017–323022, the
  un-ingested NNLS A100 job 330046, the 2026-09-25 C1 human decisions, the levers release
  (2026.9.19.1), and the retired scalar config flip. No measurement or original wording was
  rewritten; no wiki page changed. The artefact-policy date was fixed to 2026-09-27.
- Mind (ledger-only commits on the session branch, landed by the ledger merge): two stale
  `Blocked-by:` lines resolved on `post_certified_solver_likelihood_breakdown.md` and
  `certified_solver_batched_guard_c2.md`; four records repointed from the renamed
  `certified_solver_cond_free_batched_fallback.md` to `certified_solver_batched_guard_c2.md`
  with a `pointer-correction:` line; `image_source_mappings_epic.md` release tags and
  `numpy_deflections_cpu_speedup.md` phase-3 row and goal-shortfall note corrected;
  `mass-field-profiling-live.md` pointer to the shipped resume draft; the
  `curvature_reg_matrix_rebuilt_every_access.md` draft retired with
  `complete/2026/09/curvature-reg-matrix-rebuilt-every-access.md` (PyAutoArray#555 settled it);
  `complete/archive/epics/certified_positive_solver_epic.md` written from the four records.

### Traps / notes
- A correction line goes after the paragraph it corrects; a marker that wraps across lines
  ("harness\n  injection") needs a marker from one line. Bare filename mentions in prose stay
  valid as names; only paths and links change.
- `lifecycle.py close --prompt draft/...` resolves a draft (unlike `record --prompt`), so a
  folded draft is retired with one verb.

## Original prompt

# Ledger and Mind drift surfaced by the profiling wiki backfill

- Work type: maintenance
- Target: @autolens_profiling (results/notes/ status lines), @PyAutoMind (records, drafts, epics)
- Epic: profiling-research-wiki (follow-up; the epic itself is complete)
- Autonomy: safe
- Filed: 2026-09-27
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/343
Issued: 2026-09-27
- Status: split out of `profiling-research-wiki-p2` at close-out — the wiki backfill shipped in
  `complete/2026/09/profiling-research-wiki-p2.md` (autolens_profiling#340); these are the
  stale lines it found in sources it was told not to edit.

## Original prompt

Phase 2 of the profiling research wiki (autolens_profiling#339 / #340) backfilled 18 campaign
pages from the ledgers, the Mind records and the issue bodies. Cross-reading those sources
turned up lines that are now false or stale. The wiki pages already state the corrected facts
(each page's Caveats section names the source and the fix); this task brings the sources into
line. Every item is a one-line edit; none changes a measurement or rewrites history — add a
dated correction line where the file is a ledger, fix the pointer where it is a record.

### autolens_profiling `results/notes/` (dated correction lines, never rewrites)

1. `hst_gpu_residue_phase4_logdet_2026_09.md` cites "PyAutoArray #566" as the library solver;
   #566 is the issue, the PR is PyAutoArray#567 (released 2026.9.26.1).
2. `profiling_campaign_status_2026_09.md`, GPU section: "the certified solver is still a
   harness injection" holds for residue phases 1–3 only; phase 4 (#306, job 350651) ran the
   library certified solver.
3. `multistart_prodigy_compile_census.md` TL;DR says every RAL cell warms to "≤ 2 s"; its own
   finding 2 has `delaunay_matern` warm = cold (16.3 s / 21.2 s, job 331379).
4. `preopt_breakdown_baseline.md` status line still says the alma_high A100 cells are "in
   flight"; issue #59 records the datacube rows landed and the interferometer Delaunay cell
   OOM'd (`gpu_unusable_breakdown`; follow-up shelved 2026-08-11).
5. `sparse_vs_dense_inversion_path.md` dates A100 jobs 323017–323022 to 2026-07-11, but those
   ids predate the 2026-07-10 PreOptimizationTimes jobs (330062+); verify the date.
6. `nnls_solver_ledger.md` lists A100 job 330046 as "Pending"; a #59 comment (2026-07-10)
   says its output exists on RAL and was never ingested.
7. `certified_solver_phase_c1_lane_rate_2026_09.md`, Decisions: the 2026-09-25 human
   decisions (Δ = 100 nats near-peak gate, 0.1 nat pin, rectangular pix1 stays on library
   PDIP) post-date the section; add a dated addendum.
8. `fixed_lens_light_levers_2026_09.md` top status line still says PyAutoArray#553–#555 are
   "pending release" (released 2026.9.19.1; the status page already carries the correction).
9. `certified_solver_policy_phase_b_2026_09.md`, policy item 1, still describes the scalar
   config-flip PR as pending; it was retired unbuilt on 2026-09-24
   (`complete/2026/09/certified-solver-scalar-default-flip.md`).

### PyAutoMind

10. `draft/research/autolens_profiling/post_certified_solver_likelihood_breakdown.md` and
    `draft/feature/autofit/certified_solver_batched_guard_c2.md`: `Blocked-by:` says
    PyAutoArray#567 is unreleased; it shipped in 2026.9.26.1. The first also names the retired
    `draft/feature/autoarray/certified_solver_scalar_default_flip.md`.
11. `complete/2026/09/hst-gpu-residue-p4.md`, `hst-gpu-non-solver-residue.md`,
    `certified-solver-phase-b.md`, `certified-solver-scalar-default-flip.md` cite
    `draft/feature/autofit/certified_solver_cond_free_batched_fallback.md`; the live draft is
    `draft/feature/autofit/certified_solver_batched_guard_c2.md`.
12. `complete/archive/epics/image_source_mappings_epic.md` retirement line names releases
    v2026.9.11.1 / v2026.9.14.1; tag containment puts PyAutoArray#517/#518 and PyAutoLens#720
    in 2026.9.4.1.
13. `complete/archive/epics/numpy_deflections_cpu_speedup.md`: phase 3 row still reads
    "PR-OPEN 2026-09-03" (merged; released 2026.9.4.1); "only NFW missed its 2x line" is too
    narrow (gNFW and elliptical Gaussian also fell short of the epic goal, re-scoped in phase 2).
14. `draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md` is still in `draft/`
    though it is marked folded into autolens_profiling#267 and PyAutoArray#555 settled it:
    retire it with a record.
15. `complete/2026/09/mass-field-profiling-live.md` says the staged pipeline "remains tracked
    in" `draft/maintenance/autolens_profiling/mass_field_pipeline_resume.md`, which shipped the
    same day as autolens_profiling#290.
16. Epic `certified-positive-solver` is named by four records but has no entry in `epics.md`
    or `complete/archive/epics/`; the certified-solver wiki page says "(not in epics.md)".
    Either add the archived ledger or leave the page's wording as the record.

## Out of scope

Any measurement, any wiki page (they already carry the corrected facts), any script.
