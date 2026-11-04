# Align ecosystem documentation with the current HowToLens and HowToGalaxy courses

Type: docs
Difficulty: large
Autonomy: supervised
Consequence: judge
Issued: 2026-11-04
Issue: https://github.com/PyAutoLabs/HowToLens/issues/127
Target: @PyAutoLens @PyAutoGalaxy @autolens_assistant @autogalaxy_assistant @HowToLens @HowToGalaxy @autolens_workspace @autogalaxy_workspace

## Original request
can we now do a sweep of all docs and make sure the way they link to HowToLens and HowToGalaxy reflects these updates, really check this for the whole ecosystem.

## Approved audit and plan
Audited current default-branch tracked references across all 51 registered repositories plus the organization profile (52 checkouts). Refreshed refs, using HTTPS without changing origin configuration for two SSH-auth failures. Full inventory and raw results: /mnt/c/Users/Jammy/Workspace/Science/scratch/tutorial_link_sweep_2026-11-04/.

Initial URL validation finds 348 distinct file/URL pairs targeting missing main-branch tutorial paths across six repositories. Most are assistant-generated notebook guidance: fix the source skills and routing first, then regenerate consumers. This count excludes version-pinned pages: library docs still describe the previous 12-lesson Lens chapter and 6-lesson Galaxy chapter. Check prose-only chapter/tutorial references and pinned destinations as well as URLs.

1. Finish a contextual mapping of old topics to current lessons across all chapters, using current HowToLens and HowToGalaxy scripts/contents as authority. Distinguish renamed, merged and removed topics; link to production guides when no current lesson teaches the promised content.
2. Update the two libraries' docs/howto* chapter indexes and relevant overview descriptions. Make current-course links follow the current course; retain intentionally historical/version-specific records. Review release URL-bumping policy before changing pins.
3. Repair the two assistant skill sets' tutorial links, labels and explanations, plus colab/contexts.yaml number-sensitive routing. Update relevant chapter summaries/routing in the courses. No unrelated science/API rewrite.
4. Regenerate affected notebooks and navigation in both courses and both workspaces using the repaired assistant sources; never hand-edit generated notebook instruction cells.
5. Repeat the whole-ecosystem audit (52 coverage receipts), validate local/remote tutorial targets and promised topics, verify routing and generated-source parity, build affected docs, run appropriate repository checks and independent review. Produce a before/after report and open linked PRs for affected repositories.

Tier: judge — merge mode: human /prm. Approved for autonomous implementation and PR creation on 2026-11-04. Existing historical records remain historical. Branch/claim conflicts must be checked before worktrees are created.

## Branch/claim survey
All eight affected canonical checkouts are on main and clean at audit time. Existing active claims cover PyAutoLens/PyAutoGalaxy (`magnification-maps-wiring`) and autolens_assistant (`results-library-p5a-assistant`, open PR177). Do not overlap or remove those claims. Phase implementation around available owners; queue the claimed-repository phases through start_dev unless their owners release them. No API dependency is introduced by these documentation changes, despite the generic FeatureDecision's library/API warnings.

Suggested phases: (1) canonical teaching links, topic descriptions and Colab routing in available assistant/docs owners, with claimed owners queued; (2) regenerate the four consuming notebook repositories after the relevant canonical source changes are ready; (3) repeat ecosystem-wide verification and ship documentation-only PRs with coverage/limitations recorded. One approval covers these phases; each merge remains human /prm.

## Approved steering
User explicitly approved autonomous source fixes, regeneration and ecosystem checks, stressing that correct .py sources can coexist with stale notebooks. Compare source, generated notebook and injected assistant guidance separately.

## 2026-11-04 implementation and PR handoff

Five PRs are open:
- https://github.com/PyAutoLabs/autogalaxy_assistant/pull/43
- https://github.com/PyAutoLabs/HowToGalaxy/pull/103
- https://github.com/PyAutoLabs/autogalaxy_workspace/pull/271
- https://github.com/PyAutoLabs/HowToLens/pull/128
- https://github.com/PyAutoLabs/autolens_workspace/pull/617

Galaxy assistant 43 is the canonical dependency for Galaxy course 103 / workspace 271. Both Lens consumer PRs are drafts until the queued assistant source patch is applied through its own claim-safe PR. PyAutoLens/PyAutoGalaxy documentation patches remain queued behind magnification-maps-wiring; autolens_assistant behind results-library-p5a-assistant/PR177. Coordination comments posted; claims and their checkouts remain untouched. Do not close umbrella issue 127 or remove this worktree on partial merges.

Validation: regenerated 570 notebooks (Lens 42, Galaxy 31, Lens workspace 361, Galaxy workspace 136). Schema, exact source narrative/executable parity, inventory, assistant-context assembly, navigator and deterministic catalogue checks pass. Regen restored existing Python source changes absent from 13 Lens notebooks; executable source scripts unchanged. Lens canonical smoke: 42 scripts + 2 notebooks passes. Galaxy assistant full suite: 84 passed; API audit: 221 symbols / 0 missing. Lens assistant proposal focused tests: 5 passed; full suite: 107 passed / 1 skipped then unchanged fixture requiring 2026.9.27.2 wheel rather than local source 9999.0.0.dev0; supplementary suite excluding that fixture: 294 passed / 2 skipped / 1 xfailed. This is not a full-suite pass. Independent review CLEAN. Both six-page library proposals build under isolated Sphinx/MyST -W (not complete library autodoc builds).

52-repository audit: 1,192 unique course URLs, 0 missing active destinations in the combined five-worktree/three-proposal view. This does not mean queued patches are applied/published. Current-course navigation uses main; 3 publication/test pins remain deliberate. Fresh Heart YELLOW reason unchanged from acknowledgment: `workspace validation not passing (0 failed, 1 timeout, cloud#41432188469: autofit_test scripts/searches/MultiStartResumeNaNCounters.py)`; stale `release validation incomplete: no rehearsal for current source`.

Review and reproducibility artifacts: /home/jammy/Code/PyAutoLabs/.worktrees/tutorial-link-sweep/review/. Human review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/tutorial_link_sweep_2026-11-04/. Three patches are in review/proposals and copied to the human bundle. Lens assistant patch includes canonical COSMOS notebook metadata regeneration (17 files). Runtime environments/data remain in the task bundle; no cleanup until all queued work is resolved. Notebook generation uses canonical Hands conversion/injection with its unrelated autofit-project rewrite disabled in a task-local wrapper. No generator source changed.

Merge remains human `/prm`; CI snapshots retained in review/ci-snapshot.json. Final snapshot: assistant43, HowToGalaxy103, Galaxy workspace271 and HowToLens128 green; Lens workspace617 has six passing checks and two smoke jobs running. Both Lens PRs remain draft. No scheduled polling or automatic merge armed.

## Explicit documentation-only claim exception, 2026-11-04

User: "Yes, go ahead with separate documentation-only worktrees for all three, preserve the existing claims and changes, run the checks and get the PRs up."

Created real worktrees for PyAutoLens, PyAutoGalaxy and autolens_assistant inside the existing task bundle on feature/tutorial-link-sweep. Applied the reviewed six-page library patches and 17-file assistant patch including generated metadata. Original task claims and worktrees remain intact. This is a narrow human exception to the repository-wide conflict guard, not release or merge authorization. Full checks and independent review are running on these actual worktrees. All five existing PRs are green.
