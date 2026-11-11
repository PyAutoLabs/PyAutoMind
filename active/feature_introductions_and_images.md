# Feature introductions and scientific illustrations

## Current scope — supersedes the short-form/image pilot

Human: "Yes this is much better, apply this approach across the features in both workspaces. Keep the teaching detail and only remove repetition. Leave the images for now."

Text-only rollout approved. Keep the fuller MGE teaching model, preserve example-specific explanations, and consolidate only repeated material. Images and root-tour/RTD integration are deferred. Earlier pilot details below are history, not current scope.


Repos: @autolens_workspace @autogalaxy_workspace @PyAutoLens @PyAutoGalaxy
Type: docs
Consequence: judge
Status: planning

## Original request (verbatim)

In autolens_workspace and autogalaxy_workspace, each features/ folder does not have a start_here.py file. but, the features next to it often have repetition, for example the advantages and disadvantages sections. I want each to have a start_here.py file added, which removes this rpeetition. I also want each feature to have a brilliant image which illustrates the crux of it, which will also be the images used in the main start_here.py file of each workspace and on the RTD, we have images for this but some a bit a bit meh. So, go over each feature, work out the rewrite to reduce text, have me approve and review the changes and also improve the image which illustrates each feature.

## Authorization and boundary

2026-11-10: Heart RED reported. Asked permission to proceed with read-only feature/image audit and bring proposed rewrites and image improvements for approval. Human replied: "go I approve". Audit and planning authorized; implementation plan still awaits review. No release or merge authorization.

## Audit result and proposed implementation plan

- Coverage: 11 topic-level features/ hubs, 285 non-initializer Python scripts, 32 feature/standalone-example briefs. Read all module introductions and extracted prose headings; no execution validation claimed.
- Add topic-level feature choosers and missing per-feature introductions. Preserve existing runnable start_here.py examples. Move shared motivation/trade-offs; retain technical assumptions and code-adjacent explanations.
- Pilot both imaging workspaces: linear_light_profiles, multi_gaussian_expansion, pixelization; human reviews exact prose diffs and old/new scientific figures before wider rollout.
- Continue remaining light features, multi-dataset features, advanced lensing and point/weak-lensing features with domain-specific variants.
- Reuse canonical scientific assets across workspace root tours, feature introductions and library RTD overview pages. Proposed asset location: each library docs/overview/images/features/; preserve reproducible producers/provenance. No library algorithm changes proposed.
- Validate unchanged executable ASTs for prose-only edits; validate figure producers; regenerate notebooks/catalogues; run applicable smoke, navigation, link, docs-build and size checks.
- Suggested branch: feature/feature-guides-images; worktree setup and current claims check follow approval. Both workspaces currently main; AutoLens has pre-existing untracked dataset.fits, AutoGalaxy clean.
- Tier: judge — merge mode: human /prm.
- Review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/feature_guides_review_20261110/review.html (all briefs and exact file coverage), existing_images.jpg, inventory.json.
- Next action: human reviews proposal; implementation has not begun. No issue, branch, commit or PR created for implementation.

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/626
Issued: 2026-11-10

2026-11-10: Human approved continuing the pilot and required preserving recent README/docs PRs. Workspace heads: 5827331a and 93ffa50. Library docs integration deferred while library claims are active; pilot assets live with workspace producers.

## Pilot handoff — 2026-11-10

- Implemented local review pilot: 6 feature introductions + 2 imaging choosers; 12 fit/modeling introductions shortened; 6 numerical figures with PNG/SVG, producers and provenance.
- Examples’ introductory words: 9,593 → 3,108; shared introductions add 1,701 (50% combined reduction, excluding choosers).
- Existing executable ASTs and notebook code cells unchanged (12 each); 8 narrative scripts execute; 20 notebooks and both catalogues regenerated with PyAutoHands.
- Both navigator checks, size guards, whitespace checks and 45 new-introduction local link checks pass. SVG XML and producer syntax pass. Full fitting smoke/RTD builds not run at review phase.
- Figure solvers completed: intensity recovery absolute error <0.02; pixel residual RMS 0.988 lens / 1.001 galaxy. Fixed-geometry NumPy/SciPy demonstrations, not PyAuto inference outputs.
- Current source branches: feature/feature-guides-images, baselines 5827331a (AutoLens workspace) / 93ffa50 (AutoGalaxy workspace). Source changes remain uncommitted for human review. Assets force-added because workspace image paths are ignored.
- Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/feature_guides_review_20261110/pilot/index.html; includes exact text diffs, all figures, old-image comparisons, provenance and checks.
- Audit/validation logs: canonical organs/PyAutoMind/tmp/feature_guides_review/ (notebooks.log, navigator_lens.log, navigator_galaxy.log, ast_checks.json, validation.json).
- Latest README/docs front-door PRs are preserved; no README or library source edits. RTD/library claims still require coordination.
- Next: human reviews pilot text/figures; then remaining feature families and main-tour/RTD integration. No release, source PR or merge performed.

## Text rollout handoff — 2026-11-10

- Applied across both feature trees: 90 new introductions/choosers (65 AutoLens, 25 AutoGalaxy), including all 11 topic features/ hubs; 9 existing start-here tutorials retain their workflows. Review contains all 99 guides.
- Consolidated 20 complete repeated conceptual sections / 40 occurrences across 16 examples. Example-specific parameter counts and assumptions remain local; materially different teaching was retained. Added introduction navigation to other examples.
- Reverted the aggressive pilot trimming. No image, README, root start_here.py or library edits in the current patch; old ignored image experiments remain outside the patch.
- 278 existing scripts: executable AST and all text outside module introductions unchanged; substantive original introductory paragraphs remain local or are accounted for in the explicit relocation record. Approved MGE teaching supplies its revised general explanation.
- 90 new narrative scripts execute. Regenerated 368 notebooks and both catalogues through PyAutoHands; existing notebook code cells unchanged. Both navigator/size/whitespace checks pass; all 376 guide links resolve locally.
- Smoke: AutoLens 42 scripts + 2 notebooks passed; AutoGalaxy 14 scripts + 2 notebooks passed. Initial missing nbformat was resolved in task-local notebook_deps; final notebooks passed without writing back.
- Evidence: canonical organs/PyAutoMind/tmp/feature_text_rollout/validation.json, moves.json, smoke_summary.json, *_passed.json and execution logs.
- Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/feature_guides_review_20261110/text_only/index.html (rendered guides, source copies and exact diffs).
- Workspace branches feature/feature-guides-images at baselines 5827331a / 93ffa50. Text-only patch staged, uncommitted. No source PR opened.
- Ship gate RED: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "autocti_workspace: Smoke Tests failure on main" (Heart readiness 2026-11-10T20:43:16.413100+00:00).
- Next: human development-only Heart RED override to commit/push/open the two workspace PRs; merge remains separate human /prm. No source release or merge authorization.

## Human-requested pause — 2026-11-10

Human: "finishing tomorrow so wrap up with memory to resume". Stop at the completed local text patch; no shipping override or merge approval granted. Resume 2026-11-11 if requested. Worktree indexes verified: 582 AutoLens / 158 AutoGalaxy staged files, no unstaged tracked changes and no staged images. Resume note and recovery patches: /mnt/c/Users/Jammy/Workspace/Science/scratch/feature_guides_review_20261110/text_only/RESUME.md and resume_backups/. Task record remains on Mind feature/feature-guides-images, not main. On resume, verify state and current Heart; reuse passing evidence unless changes warrant rerunning. No work scheduled beyond this session.

## Development-only Heart RED override — 2026-11-11

Human: "Yes I approve the development-only Heart RED override for #626. Commit, push and open both workspace PRs, leave merging for later. Can you have them in a place I can skim read beforer we merge"

Exact RED reason (2026-11-11T08:44:25.021680+00:00): "autocti_workspace: Smoke Tests failure on main".

56 script and 4 notebook smoke checks passed; 278 existing executable ASTs unchanged; teaching preservation audit, 90 narrative executions, 368 notebook regeneration/code parity, 376 links, navigator, size and whitespace checks passed. Human-approved teaching approach; in-session diff review. Saved patches match and bases unchanged.

Commit/push/open both workspace PRs authorized. No merge, release or failed-check bypass.

## PRs open — 2026-11-11

AutoLens #627 (1472d662); AutoGalaxy #273 (061fad8). Both committed and pushed. No merge. Human skim review at text_only/skim.html; full review at index.html. Validation unchanged from saved exact patches. GitHub checks must be evaluated before a separately authorized merge.

## Human refinement — 2026-11-11

Human: "The start here in dataset level stuff like imaging/features is covered by README.md so dont have a start_here.py. I think the extraction is good and we will want to review each start_here.py individually in a follow up including images"

Removed all 11 topic-level feature hub scripts and corresponding notebooks; regenerated both catalogues. 79 new per-feature introductions + 9 existing guides remain (88 review entries). Remaining scripts unchanged; navigation/link checks pass. Follow-up explicitly requested: review each feature introduction individually, including images. No image work or merge now.
