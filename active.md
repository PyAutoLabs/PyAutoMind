# Active Tasks

## mind-post-cortex-p1
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/389
- prompt: active/mind_post_cortex_p1_retire_batch_epic.md
- issued: 2026-09-03
- session: local CLI (Fable architect, Opus execution)
- status: ledger-dev — PyAutoMind ledger only; branch `claude/mind-post-cortex-p1` lands via `mind_ledger_merge.yml` (no worktree, no PR)
- repos:
  - PyAutoMind: claude/mind-post-cortex-p1
- epic: mind-post-cortex (phase 1; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)

## mind-post-cortex-p2
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/390
- prompt: active/mind_post_cortex_p2_science_residue.md
- issued: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/391
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/343
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/8
- session: local CLI (Fable architect, Opus execution)
- status: library-shipped, awaiting-merge (three PRs open 2026-09-03; no merge order forced — the
  three diffs are disjoint, though PyAutoMind#391 and PyAutoCortex#8 are two halves of one move and
  should land together; close-out via /prm)
- worktree: ~/Code/PyAutoLabs-wt/mind-post-cortex-p2-science-residue
- repos:
  - PyAutoMind: feature/mind-post-cortex-p2-science-residue
  - PyAutoBrain: feature/mind-post-cortex-p2-science-residue
  - PyAutoCortex: feature/mind-post-cortex-p2-science-residue
- heart-note: `pyauto-heart readiness` was RED at ship (checked 2026-09-03 after PR-open, which is
  the process slip to know about). The two reasons are byte-identical to the pair the human
  acknowledged earlier today for gaussian-precompute-p1 and jax-faddeeva-clamp-audit, and neither
  touches this diff (no library source, no release surface — organ docs and registries only):
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
  That acknowledgement was scoped to those tasks, so it is NOT carried here: the RED is unacked for
  this task and merge needs the human's own call.
- epic: mind-post-cortex (phase 2; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)

## mind-post-cortex-p3-pr-ledger
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/392
- prompt: active/mind_post_cortex_p3_pr_ledger_pending_release.md
- issued: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/393
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/344
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/195
- session: local CLI (Fable architect, Opus execution)
- status: library-shipped, awaiting-merge (three PRs open 2026-09-03; merge order PyAutoMind#393 first
  — it carries the REFERENCE.md schema the other two point at — then PyAutoBrain#344, then
  PyAutoHeart#195; close-out via /prm)
- worktree: ~/Code/PyAutoLabs-wt/mind-post-cortex-p3-pr-ledger
- repos:
  - PyAutoMind: feature/mind-post-cortex-p3-pr-ledger
  - PyAutoBrain: feature/mind-post-cortex-p3-pr-ledger
  - PyAutoHeart: feature/mind-post-cortex-p3-pr-ledger
- parallel-claim: PyAutoMind + PyAutoBrain are also claimed by two sibling phases of the same epic,
  and `worktree_check_conflict` exits 1 on both. Known and accepted: mind-post-cortex-p1 (#389) is
  ledger-only, already landed on main, carries `worktree: -` and holds no checkout — it is awaiting a
  /prm close-out, not editing anything. mind-post-cortex-p2 (#390) has its own worktree and its diff is
  disjoint from this one: p2 removes REFERENCE.md's `Lane:` / queue-kind sections and edits the
  ROUTING/AGENTS/README work-type lists, scripts/status.sh and spawn; this task edits REFERENCE.md's
  `active.md` schema block, scripts/lifecycle.py and tests, and (in Brain) _intake.py's registry parse
  and dashboard renderers against p2's _sizing.py work-types and board/_theme.py. Verified by
  `git merge-tree` against origin/feature/mind-post-cortex-p2-science-residue before ship; second to
  merge rebases.
- heart-note: `pyauto-heart readiness --json` was RED when the PRs were opened (checked 2026-09-03,
  before PR-open). Verbatim reasons:
  - PyAutoLens: CI failure
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
  None touches this diff — no library source and no release surface; organ docs, one lifecycle script,
  one skill markdown and their tests. The acknowledgement the human gave earlier today was scoped to
  gaussian-precompute-p1 and jax-faddeeva-clamp-audit and is NOT carried here: the RED is unacked for
  this task and merge needs the human's own call. Opened for review only.
- merge-tree: scratch-merged origin/feature/mind-post-cortex-p2-science-residue into both branches
  before ship. PyAutoBrain: CLEAN. PyAutoMind: conflicts only in the generated dashboard.md/.html,
  and a control merge of that same p2 branch into plain origin/main produces the identical conflict —
  phase 2's own rebase debt against a moved main, not an interaction with this task. This task's three
  Mind files (REFERENCE.md, scripts/lifecycle.py, tests/test_lifecycle_check.py) are conflict-free.
- epic: mind-post-cortex (phase 3; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)

## mind-post-cortex-p4-batch-fidelity
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/345
- prompt: active/mind_post_cortex_p4_batch_plan_fidelity.md
- issued: 2026-09-03
- session: local CLI (Fable architect, Opus execution)
- status: library-dev
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
  phase 3 adds the `cmd_check` tail and the `registry_multi`/`_as_root` helpers this phase extends;
  its PR targets that branch and is retargeted to main once #393 merges.
- epic: mind-post-cortex (phase 4; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)

## gaussian-precompute-p1
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/601
- prompt: active/gaussian_precompute_p1_numpy_memo.md
- issued: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/602
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/214
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: library-shipped, awaiting-merge (PRs open 2026-09-03; merge order PyAutoGalaxy → autolens_profiling; close-out via /prm)
- worktree: ~/Code/PyAutoLabs-wt/gaussian-precompute-p1
- repos:
  - PyAutoGalaxy: feature/gaussian-precompute-p1
  - autolens_profiling: feature/gaussian-precompute-p1
- parallel-claim: PyAutoGalaxy + autolens_profiling also claimed by jax-faddeeva-clamp-audit (#600); file sets disjoint (audit: mge.py _wofz_rational / spherical branch, scripts/misc/hazards/; this: deflections_memo.py, MassProfile entry hook, scripts/lens/deflections/basis.py) — human-approved 2026-09-03 under the #176/#177 precedent; second to merge rebases
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge) — exact reasons from `pyauto-heart readiness --json`:
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
- heart-note: RED at start (pre-existing release-validation integrate:fail + unrelated worktree drift); ship gate to re-read
- epic: gaussian-deflections-precompute (phase 1; ledger draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)

## jax-faddeeva-clamp-audit
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/600
- prompt: active/jax_faddeeva_seams_and_spherical_clamp_audit.md
- issued: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/603
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/215
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: library-shipped, awaiting-merge (PRs open 2026-09-03; merge order PyAutoGalaxy → autolens_profiling; close-out via /prm)
- worktree: ~/Code/PyAutoLabs-wt/jax-faddeeva-clamp-audit
- repos:
  - PyAutoGalaxy: feature/jax-faddeeva-clamp-audit
  - autolens_profiling: feature/jax-faddeeva-clamp-audit
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge) — exact reasons from `pyauto-heart readiness --json`:
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
- heart-note: RED at start (pre-existing release-validation integrate:fail + worktree drift on unrelated worktrees); ship gate to re-read
- parent: complete/archive/epics/numpy_deflections_cpu_speedup.md (follow-up of the numpy-deflections-cpu epic)

## euclid-cpu-two-stage-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/49
- prompt: active/cpu_vis_lp_jax_vis_pix_numba_submission.md
- issued: 2026-09-02
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01BhD2t684rJZi1tT34u2KgR
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/euclid-cpu-two-stage-route
- repos:
  - euclid_strong_lens_modeling_pipeline (feature/euclid-cpu-two-stage-route)
- epic: euclid-dr1-prep (Mind phase 4; gates PyAutoCortex phases/euclid/dr1_prelim_10_lens_science_run)

## over-sample-snr-double-division
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/523
- prompt: active/over_sample_snr_double_division.md
- issued: 2026-09-02
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/527
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/290
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/119
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01UpLMvgejg1kNXbG3P789wy, resumed session_01TPaqrFZCUtvsknEx66Yneq
- status: workspace-shipped, awaiting-merge (3 PRs open 2026-09-03, all pending-release, no library PR; close-out via /prm)
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge) — exact reasons from `pyauto-heart readiness --json`, quoted to the human who replied "ok drop it then prm":
  - PyAutoLens: CI failure
  - release validation FAILED (stage integrate)
  - PyAutoArray: open PR 11d old
- heart-note: "PyAutoLens: CI failure" = Tests failed on main 6fbab3b 2026-09-03 18:43Z (unittest 3.12/3.13/nojax), unrelated to these workspace scripts; smoke 31/32 PASS, the FAIL (imaging/features/advanced/subhalo/sensitivity/slam_source_pixelized.py, AttributeError al.MapperValued) reproduces on main
- worktree: ~/Code/PyAutoLabs-wt/over-sample-snr-double-division
- repos:
  - autolens_workspace (feature/over-sample-snr-double-division)
  - autolens_workspace_test (feature/over-sample-snr-double-division)
  - autolens_assistant (feature/over-sample-snr-double-division)

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
- parallel-claim: autolens_workspace — over-sample-snr-double-division (#523) in its own worktree; touches SLaM scripts, guides/advanced/over_sampling.py and guides/modeling/slam_start_here.py only; file sets disjoint
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
