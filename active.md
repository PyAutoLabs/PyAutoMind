# Active Tasks

## gaussian-precompute-p2
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/604
- prompt: active/gaussian_precompute_p2_jax_trace_time_constant.md
- issued: 2026-09-03
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/gaussian-precompute-p2
- repos:
  - PyAutoArray: feature/gaussian-precompute-p2
  - PyAutoGalaxy: feature/gaussian-precompute-p2
  - autolens_profiling: feature/gaussian-precompute-p2
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge) — exact reasons from `pyauto-heart readiness --json`:
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
- heart-note: acknowledgement covers only these two reasons; a new reason at ship time re-blocks
- epic: gaussian-deflections-precompute (phase 2; ledger draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)

## mind-post-cortex-p4-batch-fidelity
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/345
- prompt: active/mind_post_cortex_p4_batch_plan_fidelity.md
- issued: 2026-09-03
- session: local CLI (Fable architect, Opus execution)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/346
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/394
- status: library-shipped, awaiting-merge (two PRs open 2026-09-03; PyAutoMind#394 was STACKED on
  PyAutoMind#393 — **#393 merged 2026-09-03 (`7d3ed60f`) and GitHub retargeted #394 onto `main`
  itself**, where it now reads CONFLICTING on the generated `dashboard.md`/`.html` only: take
  upstream, then re-render with `intake --mind . --apply dashboard` from a cwd inside the Mind
  checkout against a pulled PyAutoBrain main. Then merge PyAutoBrain#346 in either order, the two
  diffs are independent; close-out via /prm)
- ci: both PRs green 2026-09-03 — PyAutoBrain#346 pytest 3.12 + 3.13 pass (after a tenant-firewall fix:
  the new comments and fixtures named real repos); PyAutoMind#394 drift + refresh + privacy pass (after
  a shallow-clone fix: `lifecycle check` runs at depth 1 in CI, where "has this path ever existed" is
  unanswerable, so the leg degrades to one warning and lifecycle_drift.yml now checks out fetch-depth 0).
  PyAutoMind#394 carries a regenerated dashboard.md/.html — expect the usual dashboard conflict against
  a moved main, and take upstream then re-run `intake --mind . --apply dashboard` on the branch.
- worktree: ~/Code/PyAutoLabs-wt/mind-post-cortex-p4-batch-fidelity
- repos:
  - PyAutoBrain: feature/mind-post-cortex-p4-batch-fidelity
  - PyAutoMind: feature/mind-post-cortex-p4-batch-fidelity
- parallel-claim: PyAutoBrain and PyAutoMind are claimed by three sibling phases of the same epic, so
  `worktree_check_conflict` exits 1 on both. Known and accepted — the file sets are disjoint. This
  task owns, in Brain, `agents/conductors/batch/_batch.py` + `agents/conductors/batch/AGENTS.md` +
  the batch tests (p2 edits `_sizing.py`/`_intake.py`/`_feature.py`, p3 edits `_intake.py` and the
  ship/prm skills — neither touches `_batch.py`); and in Mind, `scripts/lifecycle.py`'s batch-record
  legs, `tests/test_lifecycle_check.py`, `queue.md`, `batches/AGENTS.md` and `batches/2026-08-31-pm.md`.
  The Mind branch is BRANCHED FROM and stacked on `feature/mind-post-cortex-p3-pr-ledger`, because
  phase 3 adds the `cmd_check` tail and the `registry_multi`/`_as_root` helpers this phase extends.
  Resolved 2026-09-03: phase 3 shipped (`complete/2026/09/mind-post-cortex-p3-pr-ledger.md`) and
  #394 now targets `main`.
- heart-note: `pyauto-heart readiness --json` was RED when the PRs were opened (checked 2026-09-03,
  before PR-open). Verbatim reasons:
  - PyAutoLens: CI failure
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
  None touches this diff — one Brain conductor, one lifecycle script, three ledger/doc pages and their
  tests; no library source and no release surface. The acknowledgement the human gave earlier today was
  scoped to gaussian-precompute-p1 and jax-faddeeva-clamp-audit and is NOT carried here: the RED is
  unacked for this task and merge needs the human's own call. Opened for review only.
- merge-tree: scratch-merged origin/feature/mind-post-cortex-p2-science-residue and
  origin/feature/mind-post-cortex-p3-pr-ledger into both branches before ship. PyAutoBrain: CLEAN
  against both (neither sibling touches `_batch.py`). PyAutoMind: clean against p3 (it is the base),
  and against p2 the only conflicts are the generated dashboard.md/.html — a control merge of p2 into
  p3 alone produces the identical 13 hunks, so it is phase 2's own rebase debt, not an interaction
  with this task. queue.md, scripts/lifecycle.py, tests/ and batches/ are conflict-free.
- epic: mind-post-cortex (phase 4; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)

## mind-post-cortex-p5-heart-freeze
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/196
- prompt: active/mind_post_cortex_p5_heart_freeze_flag.md
- issued: 2026-09-03
- session: local CLI (Fable architect, Opus execution)
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/197
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/347
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/275
- status: library-shipped, awaiting-merge (three PRs open 2026-09-03; merge order PyAutoHeart#197
  first — it ships the `freeze` verb the other two document — then PyAutoBrain#347 and
  PyAutoHands#275 in either order, the two are independent; close-out via /prm)
- decision-taken: the prompt's one human-required question (may `/prm --thaw` override an active
  freeze?) was answered by the architect on the prompt's own recommendation — yes, with the override
  logged to `autonomy_log.md` under a `## Freeze overrides` heading created on first use. Flagged at
  the head of PyAutoBrain#347 and in the issue; reverse before merge if the human disagrees (it is
  confined to the `--thaw` bullets in `skills/prm/prm.md` + the `reference.md` mirror). The section
  is deliberately NOT pre-created in `autonomy_log.md`: a ledger push auto-merges to main, which
  would land the decision ahead of its review.
- worktree: ~/Code/PyAutoLabs-wt/mind-post-cortex-p5-heart-freeze
- repos:
  - PyAutoHeart: feature/mind-post-cortex-p5-heart-freeze
  - PyAutoBrain: feature/mind-post-cortex-p5-heart-freeze
  - PyAutoHands: feature/mind-post-cortex-p5-heart-freeze
- parallel-claim: PyAutoHeart and PyAutoBrain are also claimed by sibling phases of the same epic, so
  `worktree_check_conflict` exits 1 on both. Known and accepted — the file sets are disjoint. This task
  owns, in Heart, `heart/freeze.py` (new), the `freeze` verb in `bin/pyauto-heart`, the ingest-side
  clear in `heart/validate.py`, `tests/test_freeze.py` and one `REFERENCE.md` section (p3's Heart diff
  is `skills/review_release/review_release.md` only — this task appends a further step to that same
  file, so a `git merge-tree` against p3 is run before ship and the second to merge rebases); in Brain,
  `agents/faculties/vitals/*`, `skills/prm/prm.md`, `agents/conductors/batch/_status.py` and the
  collect legs of `_batch.py` (p2 edits `_sizing.py`/`_intake.py`/`_feature.py`; p3 edits `_intake.py`
  and the ship/prm skills — `prm.md` overlaps, merge-tree checked; p4 edits `_batch.py`'s outcomes and
  merge-order blocks, not `_status.py`); and PyAutoHands, which no sibling claims.
- heart-note: `pyauto-heart readiness --json` was RED when the PRs were opened (checked 2026-09-03,
  before PR-open). Verbatim reasons:
  - PyAutoLens: CI failure
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
  None touches this diff — one new Heart module and CLI verb, one ingest-side clear, three skill/doc
  files and their tests; no library source and no release surface. The acknowledgement the human gave
  earlier today was scoped to gaussian-precompute-p1 and jax-faddeeva-clamp-audit and is NOT carried
  here: the RED is unacked for this task and merge needs the human's own call. Opened for review only.
- merge-tree: scratch-merged origin/feature/mind-post-cortex-p3-pr-ledger and
  origin/feature/mind-post-cortex-p4-batch-fidelity into this branch before ship. PyAutoBrain: CLEAN
  against both (p3 edits `prm.md` §5, this task §4/§6/Usage; p4 edits `_batch.py`'s outcome and
  merge-order blocks, not `_status.py` or the head of `collect_report`). PyAutoHeart: CLEAN against p3
  — both append to `skills/review_release/review_release.md`, p3 at the end (step 6) and this task
  inside step 3, so the two hunks do not touch. PyAutoHands is claimed by nobody else.
- epic: mind-post-cortex (phase 5; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)

## euclid-cpu-two-stage-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/49
- prompt: active/cpu_vis_lp_jax_vis_pix_numba_submission.md
- issued: 2026-09-02
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01BhD2t684rJZi1tT34u2KgR
- status: pr-open — https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50 (opened 2026-09-03; workspace-only, no pending-release, merge is human via /prm). Ship gate: pytest 72 passed, smoke 9/9. Both RAL routes COMPLETED (GPU 1 h 14 min on an A100, two-stage CPU 3 h 17 min on 8 cores).
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50
- heart-ack:
  - "PyAutoLens: CI failure"
  - "release validation FAILED (stage integrate)"
  - "PyAutoArray: open PR 11d old"
- follow-ups filed: draft/bug/euclid/gpu_per_lens_time_vs_documented_10_min.md (measured 74 min/lens vs the documented ~10 min; carries the apply_sparse_operator else-branch verdict), draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md (control test found no hang; boundary kept as the conservative default)
- worktree: ~/Code/PyAutoLabs-wt/euclid-cpu-two-stage-route
- repos:
  - euclid_strong_lens_modeling_pipeline (feature/euclid-cpu-two-stage-route)
- epic: euclid-dr1-prep (Mind phase 4; gates PyAutoCortex phases/euclid/dr1_prelim_10_lens_science_run)

## image-source-mappings-p3
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/525
- prompt: active/mappings_guide_and_tutorial_rewrite.md
- issued: 2026-09-03
- session: claude --resume 7edd9743-c486-48ec-be0a-9f184a4898d4
- status: workspace-dev
- epic: image-source-mappings (phase 3 — ledger draft/feature/autoarray/image_source_mappings_epic.md; opened 2026-09-03 by user decision ahead of the PyAutoArray/PyAutoLens releases that gated it; every PR carries pending-release)
- heart-ack:
  - "release validation FAILED (stage integrate)"
  - "PyAutoArray: open PR 11d old"
- worktree: ~/Code/PyAutoLabs-wt/image-source-mappings-p3
- parallel-claim: autolens_workspace — over-sample-snr-double-division (#523) ran in its own worktree with disjoint files; MERGED 2026-09-03 (autolens_workspace#527), claim released — rebase onto main before shipping
- repos:
  - autolens_workspace: feature/image-source-mappings-p3
  - HowToLens: feature/image-source-mappings-p3
  - HowToGalaxy: feature/image-source-mappings-p3
  - autogalaxy_workspace: feature/image-source-mappings-p3
- summary: |
    Phase 3 of image-source-mappings (workspace). New guide autolens_workspace/scripts/guides/mappings.py
    (point → parametric region → pixelized region mappings with the 0.2/0.5/0.8 clump threshold demo,
    subplot_mappings, 4MOST brightest-position recipe with guide-level astropy WCS, magnification per image);
    HowToLens/HowToGalaxy tutorial_2_mappers rewritten to draw polygons via mapper.mappings_from + regions=,
    BUGGY line dropped; dead slim_indexes_for_pix_indexes sections in the pixelization delaunay.py /
    likelihood_function.py scripts fixed; prose + total_mappings_pixels config sweep. One issue, four PRs,
    one worktree. Fable session; execution delegated to Opus (subagent A guide, subagent B tutorials/dead sections).
