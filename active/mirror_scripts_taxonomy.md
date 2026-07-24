# autolens_profiling: scripts/<dataset>/<task>/ taxonomy mirroring the workspaces

Type: refactor
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Blocked-by: group4-mge-search-benchmark (live claim on autolens_profiling; unmerged searches/+simulators/ branch with GPU runs pending)

User request 2026-07-24: apply the test-workspace restructuring recipe —
everything under scripts/, dataset folders first (scripts/imaging/...),
task subfolders second (scripts/imaging/vram/, .../jax_compile/, ...),
mirroring the workspaces. Current layout is task-first at the repo root
(vram/ jax_compile/ latent/ likelihood_breakdown/ likelihood_runtime/
pipeline_resume/ quick_update/ instruments/ searches/ simulators/ test/ +
an existing scripts/).

EXTRA COUPLING vs the _test repos (survey must map before any move):
- hpc/ sync CLI + RAL mirror (/mnt/ral/jnightin/...) — sbatch scripts and
  the cluster mirror carry paths; a restructure must update sbatch path
  refs and the sync must be re-run/verified on RAL afterwards.
- skills/profile_likelihood — path references.
- PyAutoBrain profiling conductor + samplers faculty read this repo.
- results/ trees and any aggregation scripts keyed to the current layout
  (results stay put or move with their producers — survey decides).
- No smoke/no_run/profile machinery here (not a validated workspace) —
  the resolved-env gates don't apply; gates are import/reference integrity
  + a smoke run of one script per moved family + RAL sync plan.

Two-step: read-only design survey first (mapping table old->new, dataset
classification of every task dir's scripts, full reference map); execution
as a follow-up once group4-mge-search-benchmark ships (its branch touches
searches/ simulators/ sweep.py — coordinate the rebase or fold its merge
first).
