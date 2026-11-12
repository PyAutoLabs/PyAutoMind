# Feature housekeeping completed

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/659

Merged all four PRs on 2026-11-12 after all 24 exact-head CI jobs passed, every PR was CLEAN/MERGEABLE, and Heart reported not frozen. Live human merge authorization; no release.

- PyAutoLens #853: 92498a4b111eec6152e6138080a2b70c267a217a
- PyAutoGalaxy #712: d6f304a51926ed0f0e7f5ca1f02039d4f15df5bc
- autolens_workspace #660: 3272361554bf905f6bae472203eac4901c245f99
- autogalaxy_workspace #278: f714fa48bab8518856d946949144baf75d6eced0

Scientific-use-case-first prose for fluxes, time delays and manual S/N simulations; corrected H0 and peak-pixel S/N explanations. Added AutoLens advanced imaging ellipse introduction routing to maintained PyAutoGalaxy fit/modeling/multipoles examples. Compact AutoLens overview links, fuller Galaxy ellipse overview, corrected README routes, notebooks and navigator exports. Existing images and executable behavior preserved.

Validation: six Python AST/code-cell sets unchanged, new ellipse prose-only, notebook schemas and 14 links pass; Sphinx feature pages pass with warnings as errors; navigator/search-memory/size/whitespace checks pass. #658 edit paths disjoint. Executed Markdown renderer lacked dill, so only prose synchronized while preserving existing outputs; CI subsequently all green.

Heart RED development-only override recorded at ship; merge used separate live human authorization and clear freeze. Review artifacts: C:\Users\Jammy\Workspace\Science\scratch\feature_housekeeping_review_20261112\applied\.

## Original prompt

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/659
Issued: 2026-11-12

# Final feature housekeeping

Consequence: judge
Targets: @autolens_workspace @autogalaxy_workspace @PyAutoLens @PyAutoGalaxy

## Original request
Yes, do that. Apply the housekeeping changes with ellipse as a small imaging feature in autolens, linking to the PyAutoGalaxy examples. Open the PRs for review, don't merge yet. Make it an advanced feature

## Approved plan
- Apply reviewed scientific-use-case-first prose to fluxes, time delays and both manual S/N examples. Preserve all executable code.
- Add AutoLens imaging/features/advanced/ellipse/start_here.py as a small scientific introduction routing to maintained PyAutoGalaxy ellipse examples. Link through imaging and advanced READMEs.
- Replace stale ellipse routes in both main start_here.py files and both RTD feature overviews. AutoLens uses a compact inline entry; PyAutoGalaxy retains the fuller overview.
- Repair ellipse folder README routes; regenerate notebook/Markdown and navigator/search outputs. Preserve images and #658's README/image edits.
- Validate executable AST/code-cell preservation, notebook schema, links, generated outputs, Sphinx, whitespace and compatibility with #658. Open four PRs; do not merge.

Tier: judge — merge mode: human /prm

Coordination: live user approved separate documentation worktree alongside workspace-readme-images (#658), preserving their edits and checking compatibility.
Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/feature_housekeeping_review_20261112/
Branch: feature/feature-housekeeping

## Applied checkpoint
PASS: 6 Python ASTs and notebook code-cell sets unchanged; new ellipse is prose-only; schemas valid; 14 notebook links resolve; generated Markdown prose synchronized with outputs preserved; #658 edit paths disjoint; whitespace clean.

Both Sphinx feature-page builds pass with warnings as errors. Navigator, search-memory and size checks pass. Numeric fits were not rerun: executable behavior is unchanged. Full executed-Markdown regeneration failed because the Jupyter kernel lacks dill; only changed prose was synchronized into existing rendered pages, preserving all outputs and figures. No images modified.

Review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/feature_housekeeping_review_20261112/applied/index.html
Heart RED: awaiting live task-specific override for #659 before source commit/push/PR.

## PR-open checkpoint
Live user approved development-only Heart RED override for #659. Four commits pushed, four PRs open; no merge or release.
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/853
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/712
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/660
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/278
