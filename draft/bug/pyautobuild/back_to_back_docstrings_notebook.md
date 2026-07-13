# Notebook generation mis-renders back-to-back docstring blocks as a code cell

Type: bug
Target: PyAutoBuild
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

`autobuild/add_notebook_quotes.py` + `ipynb-py-convert` (via `build_util.py::py_to_notebook`)
mis-render a docstring block that immediately follows another docstring block (only a blank
line between the closing `"""` and the next opening `"""`): the second block lands in the
generated notebook as a **code cell containing literal `# %%` and `'''` markers** instead of
a markdown cell.

Reproduce: `autolens_workspace/start_here.py` lines ~296–300 (`__Units__` follows the
previous section's close with no code between). The published
`autolens_workspace/start_here.ipynb` carries this artifact today — the `__Units__` prose is
a code cell. Any generated notebook whose source script has adjacent docstring sections is
affected; a repo-wide sweep of generated notebooks for cells starting with `# %%\n'''` will
find the blast radius.

Root cause sketch: on close, `add_notebook_quotes` emits `["'''", "\n\n", "# %%\n"]` and on
open `["# %%", "\n", "'''\n"]`; with no code line between them `ipynb-py-convert` merges the
marker runs so the second `# %%\n'''` sequence survives as cell *content*.

Fix options: make `add_notebook_quotes` collapse adjacent close→open pairs into a single
markdown-cell boundary, or normalize the marker emission so an empty code segment between
docstrings is dropped. A correct reference implementation for the split semantics now exists
in `autolens_assistant/autoassistant/to_notebook.py` (adjacent docstrings → two markdown
cells), with a unit test pinning the case.

Found 2026-07-10 while validating autolens_assistant#51 (script→notebook converter)
against the pipeline on identical input: 25/26 cells byte-identical, this artifact was the
26th.
