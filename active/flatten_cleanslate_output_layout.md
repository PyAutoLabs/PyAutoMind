# Flatten the clean-slate output layout: drop the dated `cleanslate_2026_10_17` level

Type: refactor
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoInsight
Themes:
- inference
- hpc
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-10-19
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/35
Filed: 2026-10-18
Blocked-until: RAL arrays 412539, 412541 and 412565 (jax_cpu dense, jax_cpu sparse, numba_cpu sparse) have finished; they write into the dated tree.

# Flatten the clean-slate output layout

User request (verbatim, inference chat 2026-10-18): "can we make it so locally the folder
is not cleanslate / experiments / experimental sources etc but just the new structure
which doesnt need a cleanslate folder?" and, on the proposed tree, "yes that is what i
mean albeit I think it should go output/autolens/imaging..   i guess 1 is fine so we
would wait", then "Augolens does not replace slam." "It should be autolens/imaging/slam not the other way" and "I think hst before slam makes sense too the search type and setup is the inner component".

## Context

The clean-slate campaign (Insight `hst-imaging-mass-samplers`, pin 2026.10.17.1) is now
the starting point of autolens_inference: on 2026-10-18 the pre-clean-slate RAL trees
`output/slam` and `output/archive` were moved to
`/mnt/ral/jnightin/inference/aside/autolens_inference_pre_cleanslate/`, and the laptop
mirror is `/mnt/c/Users/Jammy/Science/inference/autolens_inference/output` (the checkout's
`output/` is a symlink to it; `LOCAL_PULL_ROOT` stays the checkout). With the old trees
gone, the dated `cleanslate_2026_10_17` level that kept the campaign apart from them no
longer earns its place.

Today the dated name appears in: the four `submit_hst_cleanslate_*` and the two
`submit_hst_cleanslate_mass_samplers_*` scripts (`--output-dir output/cleanslate_2026_10_17`,
`--results-tag cleanslate_2026_10_17`, `--export-prepared output/prepared/cleanslate_2026_10_17`),
`wave.py` / `prepared.py` (prepared-problem paths and the `cs1017_` run-id prefix), the
`__cleanslate_2026_10_17` config-name suffix of every clean-slate results directory, the
`output_path` recorded in every stage row, the `.cortex/pull.json` checkpoint manifest,
and `hpc/README.md` / `scripts/imaging/slam/README.md`.

## Scope

1. New layout, RAL and laptop alike (the pull mirrors 1:1, so flatten the source, not the
   mirror):
   ```
   output/
     autolens/
       imaging/hst/slam/<variant>/<config>/seed_<n>/<stage>/   # was cleanslate_2026_10_17/slam/imaging/hst/...
       prepared/<variant>/...                                    # was prepared/cleanslate_2026_10_17/...
       experiments/<arm>/
       experiment_sources/<arm>/
   ```
   Human clarification 2026-10-18 (verbatim): "Augolens does not replace slam." Then
   (verbatim): "It should be autolens/imaging/slam not the other way". Then
   (verbatim): "I think hst before slam makes sense too the search type and setup is the
   inner component". So `autolens` is a new level directly under `output/`; beneath it
   the order is dataset class, instrument, then pipeline: `imaging/hst/slam/...`. The
   search type and its setup (`slam/<variant>/<config>`) are the innermost component,
   replacing today's `slam/imaging/hst/...` order. Assumption to confirm in the plan: `prepared`, `experiments` and
   `experiment_sources` also move under `output/autolens/`; `results/slam/...` and the
   README `slam` table are unchanged.
2. Drop `--output-dir`/`--results-tag`/`--export-prepared` dated values from the
   clean-slate submits and the runner defaults; the clean-slate rows become the plain
   `<config_name>` rows (there are no competing plain rows left: the superseded 2026-09-24
   rows live only in git history and PR #23).
3. Move the RAL tree once the three arrays are COMPLETED (never mid-job); rewrite
   `output_path` in the committed rows and the `prepared` paths `wave.py` reads; keep the
   `cs1017_` prefix only if the wave accounting needs it (say so in the plan).
4. Update `hpc/README.md`, the SLaM README, Insight `campaigns.yaml` next/evidence, and
   the Cortex `projects/autolens_inference.md` output roots.
5. Guard: the pull must not re-create the dated folder on the laptop afterwards; delete
   it on RAL only after a verified pull.

## Out of scope

Wave 1 attempt 2 submission, the sparse fixed-light divergence bug, and any sampler change.
