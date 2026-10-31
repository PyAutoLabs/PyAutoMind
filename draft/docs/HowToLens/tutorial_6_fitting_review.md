# Resume HowToLens Chapter 1: Tutorial 6 Fitting

Type: docs
Target: @HowToLens
Consequence: judge
Status: checkpoint — future work, not started
Checkpoint date: 2026-10-31

## Original request
checkpoint for us to work on fitting in the futre

## Where to resume
Review `lens/HowToLens/scripts/chapter_1_introduction/tutorial_6_fitting.py` next. Read the current full source and relevant Brain tutorial-writing guidance before proposing changes. Begin by showing the first five coherent narrative/code blocks for human review. Do not bulk-rewrite or apply unapproved prose. No Tutorial 6 changes, issue or worktree exist for this checkpoint.

## Completed work
- HowToLens PR #106 merged: Tutorials 3 and 5 consolidated into Tutorial 3, with optional mathematics. Units and multi-galaxy ray tracing moved into Tutorial 2. Data, Fitting and Summary renumbered to 5, 6 and 7.
- PR #108 merged: Tutorial 4 point-source rewrite, reviewed in fifteen blocks. Triangle tracing explanation kept brief with a workspace guide link; clarified image multiplicity, fluxes, time delays and image-property output.
- PR #110 merged: Tutorial 5 now includes a brief PointDataset example with positions, fluxes, time delays and uncertainties, plus workspace guidance. Values are illustrative rounded Tutorial 4 predictions, not observed measurements.
- All eight GitHub jobs passed before each latest merge, including Python 3.12/3.13 smoke. Local full suite: 49 scripts passed. Generated notebooks, executed Markdown, catalogue and navigation validated.
- Latest merged HowToLens main: e2fc282eba2c608139996e4c0395ce7d1c3f1798. Canonical local main was fast-forwarded to it.
- Issues #105, #107 and #109 closed; completed tasks archived and dashboards refreshed. All three task worktrees and merged local branches removed with human approval of generated-data deletion.

## Review preferences
- Present five coherent prose/code blocks at a time; apply only after approval.
- Keep explanations short, clear, intuitive and scientifically precise. Mathematics in Tutorial 3 is optional; useful lensing science does not require following every derivation.
- Avoid a separate “Concise Code” section: place illustrative code beneath its explanation.
- Numerical method detail belongs in workspace guides; give a short explanation and a direct link in HowToLens.
- Distinguish model predictions from observations and from actual parameter inference.
- Preserve agreed examples and values unless a change is discussed or required for correctness.
- Use Brain `skills/TUTORIAL_WRITING_STYLE.md`; canonical Python scripts generate notebooks via PyAutoHands.
- Work through the normal development workflow once resumed; report repo/branch before edits, regenerate outputs, run required checks, open a PR. Merge requires a current human /prm instruction and green checks.

## Initial review question for Tutorial 6
The opening says it will recover model parameters. Verify what the code actually does: evaluating a specified model and its likelihood is different from searching for parameters. Explain that distinction accurately without repeating the earlier ray-tracing lessons. This is a review lead, not an approved rewrite or a confirmed finding.

## Permissions and state
This checkpoint authorizes saving the handoff only, not starting Tutorial 6 now. Earlier Heart RED development approvals and explicit merge commands are recorded in their completed tasks; do not invent a release grant or future merge authority. Read current Heart and branch/claim state when resuming. No monitor or automation is armed.

## Review artifacts retained
Windows root: C:\Users\Jammy\Workspace\Science\scratch\
- howtolens_ray_tracing_merge_2026-10-31/
- howtolens_point_sources_2026-10-31/
- howtolens_point_data_2026-10-31/

## Suggested resume message
Resume the HowToLens Tutorial 6 fitting checkpoint and show me the first five blocks for review.
