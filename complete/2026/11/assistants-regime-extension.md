Shipped in two legs: autolens_assistant#91 (2026-07-25) and autogalaxy_assistant#45 (merged 2026-11-08, merge commit cc8b601); issue autogalaxy_assistant#44 closed.

- autogalaxy leg: `wiki/core/external/skill_citation_map.md` splits `ag_multi_galaxy_and_cluster` into a multi_galaxy row (`multi_galaxy/start_here.py`, HowToGalaxy tutorial_2) and a cluster row; `external/index.md` gains "Route by regime first" (no `group/` package in autogalaxy_workspace — a compact group routes to multi_galaxy or cluster); `external/workspace.md` repinned to autogalaxy_workspace@81e3c63; `ag_build_imaging_model` triage now banded. wiki/core edits via the ag_update_wiki procedure (repinned + provenance restamped); all audit checks and `make test` green.
- Not done (pre-existing): citation map lacks an `ag_refresh_colab_contexts` row (says 27 skills vs 28).
- Remaining items from the autolens leg's note (dedicated multi_galaxy skill "if demand appears", flagship-system literature pages) were not re-filed: the 2026-11-05 re-scope dropped them from live scope.

## Original prompt

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
Status: in progress — autolens_assistant leg shipped 2026-07-25 (autolens_assistant#91); autogalaxy leg UNBLOCKED and still undone (2026-09-14: `autogalaxy_assistant/` now exists, but carries no regime routing)
Consequence: notify
Witness: `wiki/core/external/skill_citation_map.md` carries a multi_galaxy row, so a two-deflector request routes to the multi_galaxy workflow instead of `group/start_here.py`; and each flagship system named in the parent plan's literature section has a `wiki/literature/` page following that schema. The autogalaxy-assistant leg stays out of scope until those packages exist.
Review-minutes: 0
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

Blocked on: multi_galaxy_package (COMPLETE 2026-09-17,
`complete/2026/09/multi-galaxy-j1011-real-data.md`), group_halo_explicit_choice,
cluster_regime_narrative, autogalaxy packages. The workspace/docs core
shipped 2026-07-25 (autolens_workspace#346 + companions), so the
autolens_assistant leg is now unblocked; the autogalaxy-side leg still
waits on the autogalaxy packages.

## Re-scoped 2026-11-05 — what is left (draft-queue sweep)

- **Done:** autolens leg: autolens_assistant#91.
- **Remaining:** The autogalaxy_assistant leg (no multi_galaxy in its wiki/).

_Evidence from the 2026-11-05 read-only sweep (Mind ledger + GitHub search); remaining items are the live scope of this prompt._
