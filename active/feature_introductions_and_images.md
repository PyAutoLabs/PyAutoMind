# Feature introductions and scientific illustrations

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
