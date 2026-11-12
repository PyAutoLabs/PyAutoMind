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
