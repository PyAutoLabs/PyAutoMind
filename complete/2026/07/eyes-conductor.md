# Eyes conductor — the perceptive function (epic #117 Phase 2)

## Outcome

Phase 2 of the Eyes agent epic (PyAutoBrain#117, stays OPEN for Phase 3)
shipped and MERGED on 2026-07-16: PyAutoBrain#127 (commit 231a3de, 9 files,
+465). The organism gained its thirteenth conductor:

- `bin/pyauto-brain eyes survey <workspace-root>` — EyesSurvey: per-script
  figure inventory, stale renders (producer mtime vs newest figure),
  never-rendered gaps, orphan image trees, gallery currency.
- `bin/pyauto-brain eyes review <workspace-root> [--batch N]` —
  EyesReviewSurface: ordered figure batches for the agentic PNG-read loop +
  the critique-note schema routing each accepted note to its edit surface
  (workspace `config/visualize` yaml | library plot functions | producing
  script | data).
- `/eyes` skill: survey → render (workspace `gallery_run.sh`) → review
  (in-session PNG reads + human critique) → delegate via intake →
  start_dev. The conductor never renders and never edits plot source.

Validated: full Brain suite 98 passed; hermetic contract tests (5, incl.
never-writes); live survey against autolens_workspace_test correct and
immediately productive (see Future work).

## Key decisions

- Conductor (side-effecting loop-driver), not faculty; placed after
  `workspace` in CONDUCTOR_ORDER — the Voice speaks, the Eyes see.
- Tenant firewall as architecture: the core takes the workspace root as an
  argument and names no repositories, so FIREWALL_ALLOWLIST did not grow and
  an adopting fork points it at its own workspace. Instance pointer
  (autolens_workspace_test) lives only in skill prose/AGENTS.md.
- Gallery contract = the interface: any repo with
  `scripts/<domain>/images/<script>/**` + `output/gallery/` is surveyable —
  the per-project manifest idea from intake became "implement the contract",
  not per-project code.
- AGENTS.md command-surface block regenerated via
  `install.sh --write-agents-surface` (never hand-edit it).
- Shipped as a parallel PR alongside community-ears-v2-prs' PyAutoBrain
  claim (user-approved; additive-only shared-file edits; merged first with
  no conflict).

## Gotchas

- Producer↔images join is by script stem (`*visualization*` token); scripts
  sharing a stem prefix would collide — acceptable for the current tree.
- `test_command_surface_block_is_current` fails on any bin/pyauto-brain edit
  until the surface is regenerated — regenerate, don't hand-sync.

## Future work

- Phase 3 (epic #117): paper-informed critique via the memory faculty.
- Live-survey findings to fix in autolens_workspace_test:
  `visualization_upper` (imaging + interferometer) missing from
  gallery_run.sh defaults; decide whether the never-rendered
  `modeling_visualization_jit*` tier belongs in the gallery run.
- Maiden voyage: first real /eyes review pass over the 41-figure gallery.
- Tooling drift (separate): Feature Agent cannot parse `draft/`-prefixed
  prompt paths.

## Original prompt

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
