# jax_compile/probe.py lost its cell builder with the searches tier — give profiling its own

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax
- compile
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: `python scripts/misc/jax_compile/probe.py --cell <one pinned cell>` runs end to end and reproduces that cell's pinned warm-compile record within its tolerance
Review-minutes: 20
Unattended: ready
Filed: 2026-09-10

`scripts/misc/jax_compile/probe.py` built its cells through `searches._setup.build_for_cell`
(a 2,159-line module of the retired inference programme). autolens_profiling#245 removed
that tier (archived as PyAutoGut ref `archive/condemned/autolens-profiling/inference-programme`
@ `c8b60580`); `build_objective` now raises `NotImplementedError` naming the ref, so the
probe cannot run. Its pinned warm-compile records and the compile dashboard are intact.

Give the probe a builder this repo owns: the runtime/breakdown scripts already construct
every pinned cell (`_production_config.preset_for` + the per-cell model code in
`scripts/imaging/likelihood_runtime/*.py`), so factor the cell construction they share
into a small `scripts/misc/cells.py` (or reuse an existing helper if one exists — survey
first) and point `build_objective` at it. Do not restore anything from the archive ref.
Re-run the probe on every pinned cell and confirm the records still match.

Filed at the close of #245 (scrap-inference-programme); see
`complete/2026/09/autolens-inference-birth.md` for the epic.
