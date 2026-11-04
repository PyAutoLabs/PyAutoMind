# Ecosystem tutorial links and generated guidance — merged

All eight PRs merged on 2026-11-04 under the human's `/prm` authorization. Checked every workflow run and matrix job at each exact feature head: 22 runs / 46 jobs passed, all PRs CLEAN, Heart library freeze clear. Git ancestry confirms every claimed feature branch is contained in origin/main.

| Repository / PR | Merge commit |
|---|---|
| [PyAutoGalaxy](https://github.com/PyAutoLabs/PyAutoGalaxy/pull/694) | `cccd8ea9a0a46caef7c1922b7ed5cd2a10dd3e91` |
| [PyAutoLens](https://github.com/PyAutoLabs/PyAutoLens/pull/819) | `1e925fb558ce63431bbc24815b0ee09a6c76899d` |
| [autogalaxy_assistant](https://github.com/PyAutoLabs/autogalaxy_assistant/pull/43) | `3db66df3fbcd8d8a85e27a5d2c044977195014a0` |
| [autolens_assistant](https://github.com/PyAutoLabs/autolens_assistant/pull/178) | `c693bbdb1c0f43ca03af4817c89f0d77da4b54a9` |
| [HowToGalaxy](https://github.com/PyAutoLabs/HowToGalaxy/pull/103) | `b0bec1dbf2b6d438e8bb5de1cd5b17b4d527320a` |
| [autogalaxy_workspace](https://github.com/PyAutoLabs/autogalaxy_workspace/pull/271) | `b999c66619866d58753089874fe2316fb2ded178` |
| [HowToLens](https://github.com/PyAutoLabs/HowToLens/pull/128) | `caea218293bd26e16aaec2f567bb2c07f4ee3dc6` |
| [autolens_workspace](https://github.com/PyAutoLabs/autolens_workspace/pull/617) | `a1184c808a442c675670c9acc82348502b5ee81d` |

## Delivered

Aligned library course indexes, assistant teaching citations and topic routing, course navigation and workspace references with the updated HowToLens / HowToGalaxy syllabus. Restored Fit Problems discovery and the combined adaptive reconstruction progression. Current-course navigation follows main; publication/test references retain their deliberate historical pins.

Regenerated 570 notebooks and verified narrative/executable-source parity, inventory, schema and assistant-context provenance. This restored existing Python-source changes absent from 13 Lens notebooks. The final source audit covers 52 ecosystem repositories, eight actual worktrees and 1,192 course URLs, with no unresolved active destinations. This is a source-target audit, not a live HTTP/anchor availability crawl.

## Validation

- PyAutoGalaxy full suite: 1,465 passed, 1 skipped.
- PyAutoLens full suite: 1,021 passed, 1 expected failure.
- Lens assistant full suite: 305 passed, 3 skipped, 1 expected failure, using the exact isolated 2026.9.27.2 wheel environment required by its existing fixture. No fixture/version-guard bypasses. Earlier source-stack fixture error resolved.
- Galaxy assistant full suite: 84 passed; API audit: 221 symbols, none missing.
- Lens canonical smoke: 42 scripts and 2 notebooks passed; includes regenerated interferometer simulator. Other prose/metadata-only changes have documented smoke n/a applicability.
- Both edited six-page library documentation sets build with Sphinx/MyST -W; focused context tests, reproducible regeneration, navigation/catalogue and whitespace checks pass.
- Independent review CLEAN. Final shipping Heart STALE solely for missing release rehearsal; no release performed. Both library PRs retain their pending-release labels.

## Coordination and close-out

The user explicitly authorized separate documentation-only worktrees overlapping repository claims. The magnification-maps-wiring and results-library-p5a-assistant claims, branches and worktrees remain untouched. Their committed file sets do not overlap these documentation patches. Libraries merged first, assistants before their consumers. No outstanding tutorial-sweep implementation remains.

The separate alw-optdeps-escapes task is now unblocked; its optional-dependency guard and raw-docstring fixes were not part of this sweep. The hygiene tidy live-branch bug remains independently filed; this merge does not fix it.

User explicitly approved removal of the task worktree, its test environments, generated datasets and fit outputs. Cleanup follows ledger completion. Preserve the separate review bundle at /mnt/c/Users/Jammy/Workspace/Science/scratch/tutorial_link_sweep_2026-11-04/ (Windows: C:\Users\Jammy\Workspace\Science\scratch\tutorial_link_sweep_2026-11-04). Merge receipts, validation logs and the review report are retained there. No scheduled waiter or automatic merge remains armed.

## Original prompt

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

## Documentation exception completed — eight PRs open

Additional PRs: PyAutoGalaxy#694, PyAutoLens#819, autolens_assistant#178. Both Lens consumers (#128/#617) are ready for review; merge assistant#178 first. Galaxy assistant#43 remains the dependency for Galaxy consumers (#103/#271). Library documentation PRs are independent and have the required pending-release labels. No library API or science-source changes. Existing magnification-maps-wiring/results-library-p5a-assistant claims and worktrees remain intact; both committed library branch diffs and assistant PR177 have no path overlap with these changes. Other worktrees' uncommitted data was not accessed or modified.

Full actual-worktree checks: PyAutoGalaxy 1,465 passed/1 skipped; PyAutoLens 1,021 passed/1 expected failure. Assistant full suite 305 passed/3 skipped/1 expected failure using an isolated exact 2026.9.27.2 wheel environment, resolving the earlier fixture blocker without source/test/version-guard changes. Focused contexts 5/5; regenerated metadata idempotent and all 403 Lens consumer contexts exactly match actual canonical source. Both six-page documentation builds pass; independent review CLEAN. Repeated 52-repo audit now uses all 8 real task worktrees: 1,192 course URLs, 0 unresolved active destinations. Historical publication/test pins preserved.

Final readiness STALE solely due to no release rehearsal for current source. Final CI snapshot: five original PRs green; new Galaxy library694 and Lens assistant178 green; new Lens library819 CI running. All task worktrees clean. Evidence: review/docs-ship-validation/ plus updated Science/scratch/tutorial_link_sweep_2026-11-04/index.html. No merge or scheduled wait armed. Task is now awaiting human /prm rather than blocked on claims; do not close umbrella #127 until all 8 PRs handled.
