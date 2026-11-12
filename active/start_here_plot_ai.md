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
