# Phase 1: Notebook generation must handle back-to-back docstrings

Type: bug
Target: PyAutoHands
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

## Requested scope

@PyAutoHands must make notebook generation robust to consecutive top-level docstring
blocks, so this formatting cannot break generation even before source hygiene is applied.

The Hygiene scanner and source cleanup requested at the same time are tracked as dependent
phases in `draft/feature/pyautobrain/adjacent_docstring_hygiene.md` and
`draft/maintenance/workspaces/merge_adjacent_docstrings.md`, following the Bug Agent's
required multi-repo split.

## Original user request (verbatim)

Double docstring formatting like this currently breaks ntoebook generate:   GPU; not wrong, but slower than `jnp.sqrt(...)` if you're inside a hot
  loop. For one-off analysis code, don't worry about it.
- The `.array` property of `aa.Array2D` etc. is the raw backing array — a
  `numpy.ndarray` on the NumPy path, a `jax.Array` on the JAX path.

The `data_structures.py` guide (`scripts/guides/data_structures.py`) covers
the wrapper-vs-raw-array distinction in detail.
"""

"""
__Units__
 in the corresponding start_here.ipynb it looks like this: 
# %%
'''
__Units__

The units used throughout the strong lensing literature vary, therefore lets quickly describe the units used in
**PyAutoLens**.

The `Tracer` object and all mass profiles describe their quantities in terms of angles, which are defined in units
of arc-seconds. To convert these to physical units (e.g. kiloparsecs), we use the redshift of the lens and source
galaxies and an input cosmology. A run through of all normal unit conversions is given in guides in the workspace
outlined below.

The use of angles in arc-seconds has an important property, it means that for a two-plane strong lens system 
(e.g. a lens galaxy at one redshift and source galaxy at another redshift) lensing calculations are independent of
the galaxies' redshifts and the input cosmology. This has a number of benefits, for example it makes it straight
forward to compare the lensing properties of different strong lens systems even when the redshifts of the galaxies
are unknown.

Multi-plane lensing is when there are more than two planes. The tracer fully supports this, if you input 3+ galaxies
with different redshifts into the tracer it will use their redshifts and its cosmology to perform multi-plane lensing
calculations that depend on them.

__Extensibility__
, can you make it so that the generate function that builds notebooks in autohands does not let these things break notebook generation and can you make it so the hygeine agent looks for and merges these in the scripts of all worskpaces, HowTos
