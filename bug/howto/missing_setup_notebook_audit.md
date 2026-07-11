# Audit HowTo tutorials for missing setup_notebook() line

Type: bug
Target: HowToFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Discovered during the batch-2b markdown rollout ([[markdown-example-renderings]]).
Several HowTo tutorials are missing the standard
`# from autoconf import setup_notebook; setup_notebook()` line that every other
workspace/tutorial script carries (it chdir's to the workspace root + enables
inline plotting). Without it, a tutorial that loads data via a relative path
(or runs a simulator subprocess) FAILS when executed by nbconvert (which runs
with CWD = the notebook's own directory), and only works interactively if the
user happens to launch jupyter from the repo root.

Confirmed missing in chapter_1_introduction alone: HowToFit start_here.py +
tutorial_1_models.py; HowToGalaxy tutorial_4_methods.py; (HowToGalaxy
tutorial_3_fitting.py + HowToLens tutorial_7_fitting.py were fixed in batch 2b's
PRs since they blocked rendering). The 3 still-missing pass today only because
they don't load data by relative path.

Fix: audit ALL chapters of all three HowTo repos (and re-check the workspaces)
for scripts lacking the setup_notebook line; add it right after the opening
docstring, matching the sibling convention; regenerate the affected notebooks.
Low-risk boilerplate consistency fix.
