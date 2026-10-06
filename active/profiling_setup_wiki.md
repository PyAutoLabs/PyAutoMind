# Build catalogue-backed profiling setup wiki

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: medium
Consequence: judge
Autonomy: human-required
Filed: 2026-10-06
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/382

Primary repo: @autolens_profiling. Workspace-only; no scientific library API changes.
Parent: draft/feature/pyautopulse/profiling_setup_browser.md, approved Phase 5.
Branch: feature/profiling-setup-wiki
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-wiki

## Approved plan

1. Generate deterministic per-setup wiki navigation from dashboard/catalogue.json and verified evidence shards, linking exact configuration, selected records, hazards, recommendations, canonical scripts and explicitly bound campaign journals.
2. Add structured, narrowly scoped historical interferometer decision-matrix recommendations to catalogue/registry.json with supporting record IDs, measured revisions, applicability bounds and acceptance caveats; keep all imported support unreviewed.
3. Extend scripts/misc/tooling/check_wiki.py and add a setup wiki builder/contract tests; document regeneration, wire the existing validation path, and verify generated output is current.
4. Preserve results, campaign journals, measurement semantics and v1 feeds. Validate applicable/incompatible/absent evidence, all links, deterministic output and existing tests without running profiling jobs.

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

571 generated wiki pages for540 exact setups; five unreviewed historical rules with exact support and constraints. Full1077pass6skip; final65focused pass, Ruff, Pulse contract, wiki/dashboard/link checks pass. Browser local check unavailable (playwright missing); JS/CSS unchanged. Results/journals/v1 unchanged. Independent Sol CLEAN at staged tree1de7a47bacf20a05cb3e1e3f18079cd094c38805.

Implementation is staged in the registered branch/worktree, not committed or pushed;
no PR yet. PR body and review evidence: `.worktrees/profiling-setup-wiki/pr-body.md`,
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

https://github.com/PyAutoLabs/autolens_profiling/pull/383 OPEN at `aa84d7363ec008d658199067cedd3e9edd51deaa`; branch/worktree unchanged.
Human answered "yeah do it" to the explicit YELLOW acknowledgement request for
both Phase5 branches/PRs. The three exact yellow reasons above remain unchanged.
No RED override, release or merge authorized. Independent reviewed tree committed
unchanged; pending-release label verified. Exact-head CI in progress at inspection.
Both source worktrees clean. Project export committed at aa84d736 passes assistant
SDP81 MGE/Delaunay/rectangular integration with all5 rules remaining unreviewed.
PR body contains test evidence and baseline fixture/browser limitations. Next: human
/prm after every required run/job is green; project first, then assistant.
Phase6 remains unstarted; no profiling jobs or baseline acceptance.
