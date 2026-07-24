# Phase 2: Detect and clean adjacent script docstrings through Hygiene

Type: feature
Target: PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Depends on: `draft/bug/pyautobuild/back_to_back_docstrings_notebook.md`

## Requested scope

Extend @PyAutoBrain's Hygiene Agent with a script-docstring surface that scans every
user-facing `*_workspace` and `HowTo*` repository for consecutive top-level triple-quoted
documentation blocks separated only by whitespace. The Hygiene Agent must preserve its
reasoning-only boundary: report exact findings and delegate safe, mechanical merges through
the development workflow rather than editing repositories during its read-only pre-scan.

Use the new capability to merge confirmed adjacent documentation blocks in the affected
workspace and HowTo scripts. Preserve prose and notebook section semantics, do not merge
ordinary string literals or docstrings separated by executable code, and validate that the
cleaned scripts still generate structurally correct notebooks.

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
