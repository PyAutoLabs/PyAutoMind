## start-here-plot-ai
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/647
- completed: 2026-11-12
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/651
- merge: d20312235967cb825ddecd7199533bbc7425b788
- authorization: human /prm after separately recorded Heart RED development-shipping authorization; no release.
- summary: Introductory grid uses 30x30 points without x/y labels; subsequent light-profile and lensing calculations retain the 150x150 grid over the same field. Added three Gemini experiments and dedicated PyAutoLens assistant guidance. Incorporated merged new-user guide #649 and regenerated notebook, Markdown and figures.
- validation: six executed CI jobs passed, all three workflows successful. CI smoke matrix intentionally skipped by change filter, not counted as a pass. Local 42 script smokes, 2 notebook smokes and all 13 start-here cells passed. Notebook schema/metadata, blank labels, dimensions, rendered figures and diff checks passed.
- evidence: /home/jammy/Code/PyAutoLabs/.task-logs/start-here-plot-ai/
- preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/start_here_plot_ai_2026-11-12/start_here.html
- cleanup: human authorized removal of the worktree and generated test datasets/outputs. Preview and external validation logs retained.
- reconciliation: five unrelated suspects in draft/bug/autolens retained (point_solver_error_bisect_health, runtime_single_jit_median_reach_and_a100_witness, jit_cache_not_hit_modeling_visualization, positions_threshold_fixture_off_axis, point_source_plot_script_residual_shape_mismatch); none covered by this plotting/docs change. Follow-up door: intake reconcile draft/bug/autolens.

## Original prompt

# Start-here plots and AI experiments

Target: @autolens_workspace
Consequence: judge
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/647

## Original request
\- for start_here.ipynb (and prob other examples)? It has x(") and y(") labels being plotted when they shouldnt, so fix,\
I also think the grid is too high resolution it has aliasing no my screen.\
\- I think putting a few AI nudges in the start here colab notebook is a good shout, both to encourage users\
to mess around withGemimi but emphasise that their is bespokje dediciated support integrated with the PyAutoLens assistant.

## Approved plan
Human approved 2026-11-12. Suppress unwanted introductory grid labels; survey other examples. Use a coarse display grid while retaining fine calculation sampling. Add three Gemini nudges and explain the dedicated assistant integration. Regenerate notebook and validate execution/rendering. Tier: judge; human /prm merge.

## Implementation
Source: start_here.py; generated: start_here.ipynb. 30x30 display grid at 0.25 arcsec/pixel and 150x150 calculation grid at 0.05, both 7.5 arcsec wide. Use supported ax interface and clear labels through Matplotlib. Existing Gemini metadata unchanged.

Issued: 2026-11-12

## Validation and handoff
- Full regenerated notebook executed successfully with Python 3.12; notebook schema valid.
- Asserted blank grid axis labels, 30x30 display and 150x150 calculation grid.
- Rendered grid visually inspected; individual points resolve clearly. Existing Gemini metadata unchanged.
- Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/start-here-plot-ai/autolens_workspace
- Branch: feature/start-here-plot-ai
- Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/start_here_plot_ai_2026-11-12/grid.png
- Evidence: /home/jammy/Code/PyAutoLabs/.task-logs/start-here-plot-ai/
- Ship-time Heart RED: PR publication awaits explicit development-only override; no merge authority.

## Latest integration
Merged origin/main through 4ee301ec (new-user guide PR #649). Changes reapplied cleanly and notebook regenerated, all 13 cells passed again. Human authorized shipping after RED reasons were surfaced: "new user guide updates merged so work those in and then get this stuff in". Latest RED: PyAutoNerves: 2 commit(s) behind origin; PyAutoArray: 2 commit(s) behind origin; PyAutoGalaxy: 4 commit(s) behind origin; PyAutoLens: on branch feature/extra-galaxies-review (not main); PyAutoLens: 2 uncommitted source change(s); PyAutoCTI: 2 commit(s) behind origin; install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate).

## PR handoff
PR: https://github.com/PyAutoLabs/autolens_workspace/pull/651
Commit: 8087a94e174ae9dbc82bd45ef630e60be2b535ed
Validation: 42 script smokes, 2 notebook smokes, all 13 introductory notebook cells passed. Generated Markdown refreshed from current source, 11 figures verified, image links corrected. Preview updated with merged guide illustrations. No runtime failures; generator emits an existing markdown-cell outputs schema warning on its intermediate notebook, final regenerated notebook validates cleanly. Next: judge PR checks, human /prm; no merge or release performed.
