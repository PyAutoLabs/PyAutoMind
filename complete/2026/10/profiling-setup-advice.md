# Shipped — profiling-setup-advice

Completed: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/150
PR: https://github.com/PyAutoLabs/autolens_assistant/pull/151
Merge commit: 910db578af5fb5a30aeb67dbeeaf0f98646f0d59
Exact reviewed CI head: d1621f230dd426810a0bda15d7de3685f94058ba

Adds a standard-library lookup and assistant skill for profiling setup questions. It reports exact matches, approximate analogues or no applicable evidence, retaining validation status, unknowns, configuration differences and immutable record citations.

The reader verifies one committed index/shard/source snapshot, record values and JSON pointers. Historical recommendations remain qualified context; numeric analogues are not extrapolated. Fit-time arithmetic requires explicit assumptions and known single-call latency metadata. No scientific code is run or baseline accepted.

## Scripts Changed
- `autoassistant/profiling.py`: qualified catalogue lookup and explicit conditional fit-time arithmetic.
- `scripts/profiling_lookup.py` and `docs/profiling/alma_delaunay.json`: runnable offline lookup example.
- `skills/al_profiling_setup.md`, routing/source registry and generated Claude/Codex discovery adapters.
- Existing wiki-currency CI clones the cited profiling catalogue; focused consumer contracts added.

## Validation
- Applicable assistant suite: 189 passed, 1 skipped; final focused suite after review fixes: 43 passed.
- Full suite also encountered 9 errors in the pre-existing forward-model fixture, which requires autolens==2026.9.27.2 instead of installed 9999.0.0.dev0. The same failure reproduces on unchanged main; no fixture or gate weakened.
- Committed project producer integration (`aa84d7363ec008d658199067cedd3e9edd51deaa`): SDP.81 MGE/Delaunay/rectangular lookups resolve all five historical recommendations and preserve unreviewed status.
- Live committed ALMA example: 14 runtime candidates, all approximate/unreviewed; no prediction.
- Ruff/format, citation resolution, provenance check, generated discovery check, recipe API gate and workflow YAML parse passed. Provenance reports 91 existing moving-ref warnings.
- Independent review checked identity, malformed inputs, exact pointers and batching assumptions.

Closes #150.



## Merge evidence

CI runs37456421944/wiki-currency and37456421689/clone-boundary passed every job/step. Final boundary fix moved the unchanged query to domain-classified docs/profiling/.
Human /prm authorized this merge. Both repositories are full clones; fetched origin/main
contains the task head with zero unmerged commits. Project merged before assistant.
Independent CLEAN reviews preceded shipping; assistant's final four-file placement repair
passed43 focused tests, actual clone-boundary, live query and final GitHub CI.

Ship Heart YELLOW reasons explicitly acknowledged by the human:
- autogalaxy_workspace: open PR 7d old
- autolens_workspace: open PR 7d old
- euclid_strong_lens_modeling_pipeline: open PR 7d old
Stale: release validation stale: source moved since rehearsal (PyAutoNerves).
No RED override, release, profiling jobs, baseline acceptance or temporal charts.
Phase6 remains unstarted; retain the parent draft for that scope.

Local evidence archived under .worktree-archives/profiling-phase5-20261006/profiling-setup-advice/;
copied files hash-verified, synthetic review/integration fixtures retained there.

## Original prompt

# Add evidence-qualified profiling setup lookup

Type: feature
Target: autolens_assistant
Repos: autolens_assistant
Difficulty: medium
Consequence: judge
Autonomy: human-required
Filed: 2026-10-06
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/150

Primary repo: @autolens_assistant. Workspace-only; no scientific library API changes.
Parent: draft/feature/pyautopulse/profiling_setup_browser.md, approved Phase 5.
Branch: feature/profiling-setup-advice
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-advice

## Approved plan

1. Add a stdlib catalogue lookup in autoassistant/ with explicit dataset/model, size, masked pixels, source resolution, PSF, precision, hardware and revision matching; read versioned index and hash-verified shards without scientific imports.
2. Return exact match / approximate analogue / no applicable evidence with known mismatches, unknown metadata, validation status, source revision, concrete record citations and bounded recommendations. Never combine incompatible timing axes or promote archived records.
3. Add skills/al_profiling_setup.md and relevant discovery/routing links; regenerate existing skill adapters. Distinguish per-likelihood timings from conditional fit-time arithmetic with explicit evaluations, concurrency, setup/compile and overhead assumptions.
4. Add contract/lookup tests covering applicable, incompatible, absent, malformed and unknown evidence, plus examples checked against the project catalogue. Use the project Phase5 producer in an isolated checkout. No jobs, acceptance, baseline campaign or temporal charts.

Tier: judge — merge mode: human /prm.

## Survey and authorization

Parent design and suggested Phase5 branches already approved. User now says start phase 5.
Both canonical target repos are main at origin/main; preserve existing untracked datasets
and assistant scripts. No active Mind claims conflict. Older unregistered worktrees remain
untouched under the previously approved isolation; no new shared-checkout coordination.
Phase4 project PR381 and Brain PR478 confirmed MERGED. Entry Heart STALE permits planning;
read fresh shipping gates, no RED override or merge authority carried forward.

## Original request (verbatim)

start phase 5

The complete approved Phase5 requirements and original redesign request remain in the parent.

## Implementation and review checkpoint — 2026-10-06

Stdlib committed-snapshot reader, skill/recipe, query fixture and generated discovery.43focused tests pass; applicable full189pass1skip. Full suite9 fixture errors require autolens2026.9.27.2; same failure on unchanged main. Citation/provenance/discovery/Ruff checks pass. Live ALMA14runtime analogues; staged producer integration verifies all5 rules for SDP81 MGE/Delaunay/rectangular. Independent Sol CLEAN at staged treead267485e953feddbd125fbf9248c8b3329b7962.

Implementation is staged in the registered branch/worktree, not committed or pushed;
no PR yet. PR body and review evidence: `.worktrees/profiling-setup-advice/pr-body.md`,
`review.txt` and test logs alongside it. User asked to start Phase5; scope remains approved.
Fresh ship gate Heart YELLOW (2026-10-06T11:10:42Z):
- autogalaxy_workspace: open PR 7d old
- autolens_workspace: open PR 7d old
- euclid_strong_lens_modeling_pipeline: open PR 7d old
Stale: release validation stale: source moved since rehearsal (PyAutoNerves).
Current explicit acknowledgement requested; awaiting answer. No prior override carried
forward. Next: on acknowledgement, commit/push/open separate PR; merge stays human /prm.
No jobs, baseline acceptance or temporal charts. Phase6 unstarted.

## PR handoff — 2026-10-06

https://github.com/PyAutoLabs/autolens_assistant/pull/151 OPEN at `874ab3afa54d0ff9206f90cd9231f4539fb49221`; branch/worktree unchanged.
Human answered "yeah do it" to the explicit YELLOW acknowledgement request for
both Phase5 branches/PRs. The three exact yellow reasons above remain unchanged.
No RED override, release or merge authorized. Independent reviewed tree committed
unchanged; pending-release label verified. Exact-head CI in progress at inspection.
Both source worktrees clean. Project export committed at aa84d736 passes assistant
SDP81 MGE/Delaunay/rectangular integration with all5 rules remaining unreviewed.
PR body contains test evidence and baseline fixture/browser limitations. Next: human
/prm after every required run/job is green; project first, then assistant.
Phase6 remains unstarted; no profiling jobs or baseline acceptance.

## CI boundary fix — 2026-10-06

Human requested the fix after /prm correctly stopped on red clone-boundary CI.
Existing task/branch reused; commit d1621f2 pushed to PR151. The unclassified
examples/profiling/alma_delaunay.json moved byte-identically to docs/profiling/,
covered by the existing domain docs/* rule. Updated skill links, query test and
maintainer boundary explanation. No Brain change or weakened CI gate.
Actual boundary reproduced before fix and passes after; 43 lookup tests pass,
live query still14runtime analogues; Ruff/format/discovery/diff checks pass.
Fresh Heart YELLOW reasons identical to the already acknowledged three open-PR
reasons; PyAutoNerves rehearsal remains stale. No new override/merge grant.
Logs: .worktrees/profiling-setup-advice/boundary-{before,fix-tests,fix-vitals}.log.
Next: exact-head CI on d1621f2, then human /prm.
