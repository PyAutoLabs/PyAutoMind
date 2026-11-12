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
