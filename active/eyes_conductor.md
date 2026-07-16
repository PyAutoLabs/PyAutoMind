# Eyes conductor — the perceptive function (epic #117 Phase 2)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of the Eyes agent epic (PyAutoBrain#117; Phase 1 — render harness +
gallery + manifest in autolens_workspace_test — MERGED #170). Build the
domain-agnostic Eyes conductor in PyAutoBrain: the judge-and-iterate loop
(render → present → critique → delegate) over a project's visualization
surface, consuming the Phase-1 `viz_manifest.yaml` + gallery.

Design constraints settled at intake/Phase 1:

- Conductor, not faculty: it drives a human review loop and delegates edits —
  side-effecting. Like the hygiene conductor it reasons and delegates; it
  NEVER edits plot source itself. Edit surfaces it routes to: the functional
  plot API (`aplt.subplot_*`) and `config/visualize` yaml.
- Tenant firewall: no non-organ repo names in `eyes` .py/.sh — the conductor
  core takes a workspace/manifest path argument; instance pointers
  (autolens_workspace_test) live in the skill prose / AGENTS.md only. Do not
  grow FIREWALL_ALLOWLIST.
- Deterministic core (stdlib-only): `survey` (inventory + staleness +
  manifest↔disk drift over an images tree) and `review` (emit the
  EyesReviewSurface the agentic critique loop consumes). Rendering stays in
  the workspace (`scripts/gallery/gallery_run.sh`), driven by the skill.
- Phase 3 (paper-informed critique) is out of scope here.
