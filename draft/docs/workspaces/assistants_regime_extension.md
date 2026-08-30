# Assistants: regime-aware routing for multi_galaxy / group / cluster (follow-up)

Type: docs
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- assistants
- cluster
Difficulty: medium
Autonomy: safe
Priority: low
Status: in progress — autolens_assistant leg shipped 2026-07-25 (autolens_assistant#91); autogalaxy leg deferred until the autogalaxy packages exist
Consequence: judge
Review-minutes: 20
Unattended: ready
Parent: draft/docs/autolens/split_lensing_regimes.md
Filed: 2026-07-25 (backfilled from git)

Once the three-regime reorganization (parent plan) has landed in
autolens_workspace, autogalaxy_workspace and the RTD docs, extend the
assistants so a user describing their system is routed to the right regime
workflow.

## Scope

- @autolens_assistant: add/extend skills so "I have a lens with two lens
  galaxies / a group / a cluster" routes to the multi_galaxy, group or
  cluster workflow respectively; teach the regime decision rules (co-dominant
  deflectors vs host halo vs many-source point workflow; all groups/clusters
  are multi-galaxy systems but not vice versa); refresh `wiki/core/` regime
  pages via `al_update_wiki`; add the parent plan's flagship literature
  systems to `wiki/literature/` following its schema.
- Galaxy-side assistant: the autogalaxy assistant does not exist yet as a
  repo; when it is seeded (via the Clone/Mitosis machinery), its seed should
  inherit the multi_galaxy + cluster (light) workflows. Record the
  requirement here; do not create the repo as part of this task.

## Landed (2026-07-25, autolens_assistant#91)

All the stale surfaces below were updated: group_and_cluster_lensing.md
rewritten around the three-rung ladder (+ native dPIEMass, group_halo,
Bergamini+19 tie), mass_profiles.md row split, al_build_imaging_model
triage bands, skill_citation_map multi_galaxy row, external
index/workspace enumerations. Remaining for this prompt: regime-routing
skill work beyond the wiki surfaces (a dedicated multi_galaxy skill if
demand appears), wiki/literature entries for the flagship systems, and
the autogalaxy-assistant leg.

## Specific stale surfaces (post-merge Opus sweep, 2026-07-25) — now fixed

The autolens_assistant is systematically one rung behind the shipped split;
highest-value targets when this task starts:

- `wiki/core/concepts/group_and_cluster_lensing.md` — the canonical
  above-galaxy page presents a two-rung (group/cluster) set: title, the
  "galaxy to group to cluster" ladder sentence, and the Einstein-radius
  enumeration all need the multi_galaxy rung.
- `wiki/core/concepts/mass_profiles.md` model-picking table — the
  "Group / cluster lens | multi-galaxy Isothermal ± scaling relations" row
  uses "multi-galaxy" to MEAN group/cluster; now doubly wrong (the
  multi_galaxy rung is free per-deflector models with no scaling tier).
- `skills/al_build_imaging_model.md` triage question pins group at "(2-4)"
  galaxies — now the multi_galaxy band; merged group/README says 2-10.
- `wiki/core/external/skill_citation_map.md` — no multi_galaxy row, so a
  two-deflector request routes to group/start_here.py.
- `wiki/core/external/index.md` + `external/workspace.md` — stale top-level
  folder enumerations (mitigated: the regenerated llms-full.txt /
  workspace_index.json the assistant is told to read DO contain
  multi_galaxy).
- Nothing in the assistant references `group/features/group_halo/`.

## Ordering

Blocked on: multi_galaxy_package, group_halo_explicit_choice,
cluster_regime_narrative, autogalaxy packages. The workspace/docs core
shipped 2026-07-25 (autolens_workspace#346 + companions), so the
autolens_assistant leg is now unblocked; the autogalaxy-side leg still
waits on the autogalaxy packages.
