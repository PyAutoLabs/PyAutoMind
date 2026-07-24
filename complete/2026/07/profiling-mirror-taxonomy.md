## Outcome — SHIPPED + MERGED 2026-07-24 (profiling#85 + Brain#161)

Issue #84 closed. autolens_profiling inverted to dataset-first:
scripts/{imaging,interferometer,point_source,multi,cluster,misc}/<task>/,
group-scale under cluster/ (human decision), datacube under interferometer,
agnostic drivers/framework/tooling under scripts/misc/<task>/. Shared libs
(_profile_cli, _adapt_image_util, instruments/) STAY at root; every leaf's
parents[N] math replaced by a sentinel-walk bootstrap (ruff.toml sentinel;
root + scripts/misc on sys.path) — ZERO import statements changed. results/
config/dataset/hpc stay at root, results section names stable. 28 sbatch +
both CI workflows rewritten. Brain profiling conductor lockstep (9 path
edits; results/hpc globs unchanged, verified by dry-run: 7 CELLS rows).

## Gates caught real regressions (the point of gates)
auto_simulate_if_missing's hardcoded simulators/ path; jax_compile probes'
output paths; a stale dashboard row from #83. Plus a PRE-EXISTING bug:
cluster/group simulators still call al.mp.dPIEMassSph(ra=,rs=,b0=) — broken
on main since the #506 Lenstool swap; filed
draft/bug/autolens_profiling/cluster_simulators_dpie_api_drift.md (may also
block the parked group4 GPU runs — check group4_mge.py).

## Agent-ops lesson
The implementation agent STALLED twice (600s watchdog; long smoke-runs /
backgrounded gates). SendMessage-resume with explicit timeout guidance +
"UNVERIFIED-with-reason beats blocking" recovered it both times with context
intact — resume, don't relaunch.

## PENDING POST-MERGE (needs cluster access)
Re-sync the RAL mirror (HPCPullPyAuto) and smoke ONE leaf per family there
before the next A100 campaign — all submit paths changed. Group4's parked
runs resume from scripts/cluster/searches/<sampler>/mge.py via
scripts/misc/searches/sweep.py (parked.md updated).

## Follow-ups (drafted)
dataset_auto_simulate.md (uncommit the 49 committed datasets — byte-identity
REQUIRED, baselines calibrated against committed bytes); the dPIE bug;
optional README cross-link tidy (lychee pass).

## Original prompt

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
