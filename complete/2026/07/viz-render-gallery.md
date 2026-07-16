# Visualization render harness + gallery + manifest (Eyes agent Phase 1)

## Outcome

Phase 1 of the Eyes agent epic (PyAutoBrain#117, stays OPEN for Phases 2–3)
shipped and MERGED on 2026-07-16: autolens_workspace_test#170 (commit
b82b356), adding `scripts/gallery/`:

- `gallery_build.py` — walks `scripts/<domain>/images/**` (imaging,
  interferometer, point_source, multi, cluster) and emits a contact-sheet
  `gallery.html`, a machine-readable `viz_manifest.yaml` (the "every figure
  the project outputs" inventory the future Eyes conductor consumes — 41 png
  + 8 fits at ship time) and, with `--embed`, a single self-contained
  `gallery_embedded.html`. `--check` verifies gallery ↔ manifest ↔ disk in
  both directions. Outputs land under gitignored `output/gallery/`.
- `gallery_run.sh` — per-domain runner from the workspace root; default =
  fast tier (imaging 153s, interferometer 132s, point_source 23s, multi
  96s/139s); cluster (803s) demoted to a slow tier; `--all` adds slow + JAX
  variants.

The critique loop was proven both ways in-session: the agent read the PNGs
directly (dataset + delaunay fit spot-checks), and the 20 MB embedded gallery
was delivered to the human via FromWSL.

## Key decisions

- Epic phased at start_dev: Phase 1 harness/gallery (this task, workspace
  only) → Phase 2 Eyes conductor in PyAutoBrain (was blocked by the
  workspace-agent claim; PR #118) → Phase 3 paper-informed critique. The
  Feature Agent's "re-home as research" was rejected — intake had already
  settled the design.
- The Eyes conductor (Phase 2) reasons and delegates like the hygiene
  conductor; it will never edit plot source. Its edit surface is the
  functional plot API (`aplt.subplot_*`) + `config/visualize` yaml — the old
  `MatPlot2D`/`Output` plotter classes no longer exist.
- Manifest is generated from produced outputs, not a committed
  expected-list (the visualization scripts already own expected-output
  derivation from the Visualizer source; a committed manifest would drift).
- Shipped through Heart RED on explicit human ack (6 organism-level reasons
  unrelated to the change, recorded verbatim in the active.md heart-ack line);
  merge was a separate human act.

## Gotchas

- The workspace_test visualization scripts must run from the workspace ROOT
  (they resolve `scripts/...` simulator paths relative to cwd) — running from
  `scripts/<domain>/` breaks the dataset self-bootstrap.
- Tooling drift found en route: the Feature Agent cannot parse `draft/`-
  prefixed prompt paths (mis-reads work-type/target, resolves no repos) —
  same lifecycle-split family as the intake root-write bug.

## Future work

- Phase 2: Eyes conductor (`agents/conductors/eyes/`?) consuming
  `viz_manifest.yaml` + the gallery; Phase 3: paper-informed restyling.
- Possible later: per-project viz-manifest contract for other projects
  (PyAutoFit/PyAutoGalaxy workspaces) once the conductor exists.

## Original prompt

# Visualization eyes agent — render, judge, update PyAuto visuals

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoLens
- PyAutoArray
- autolens_workspace_test
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

I am now at the point where PyAutoLens and other projects produce lots of
visualizations, but I dont have an easy way to look at them, judge them and
then get them updated based on my requirements. We have places which outputs
them for tests (e.g. autolens_workspace_test/scripts/imaging/visualizaiotn.py),
but I think we need a more formal mechanism for me to look at images, judge
them and then update them.

In particular, I wonder if PyAutoBrain would benefit from a visualization
agent for this task, which handles both a streamlined way to make .png files
from PyAutoLens (and other projects), shows me them and then has the context
to change them based on my input as well as make suggestions for how they
could be improved. I can imagine me giving it papers and asking it to make
updates based on how those papers work.

What do you think? Full on brain conductor or something simpler? Obviously
the agent should not be project specific (PyAutoScientist is code-base and
domain agnostic), but it needs to interface with PyAutoLens to understand
"These are all the images it could output, there are lots (imaging /
interferometer / point source", it probably needs to output them via a
Visualizer so its representation of modeling runs. So maybe we need a domain
agnostic visualization (eyes) conductor but also something which more
direclty links to how it runs on a given project.

## Design decision (from intake discussion, 2026-07-16)

Two layers, phased — conductor-shaped but mechanics first:

1. **Render harness + gallery (no new agent).** A cheap PNG-generation path —
   the existing `workspace_test` visualization scripts are already ~the
   harness, run under TEST_MODE / small datasets — plus a contact-sheet
   gallery the user can actually look at. Claude reads PNGs natively, so the
   critique loop works in-session once this exists.
2. **Eyes conductor (PyAutoBrain).** Domain-agnostic judge-and-iterate loop:
   render → present → take critique → translate into mat_plot config /
   plotter edits routed through the normal dev workflow (start_dev), plus its
   own improvement suggestions. Like the hygiene conductor, it reasons and
   delegates — it never edits plot source itself.
3. **Paper-informed critique.** "Here's a paper, restyle to match" — leans on
   the per-project manifest and PyAutoMemory wikis; valuable but must not
   gate phases 1–2.

Cross-cutting contract: a **per-project viz manifest** each project publishes
("these are all the figures I can output" — imaging / interferometer /
point_source…) and how to render them cheaply. The conductor stays
codebase-agnostic; PyAutoLens ships the richest manifest. No new organ repo —
Eyes is a conductor inside PyAutoBrain, same as hygiene/profiling.

PyAutoArray is in the repos list because the plotter/mat_plot machinery lives
there; most "change how this looks" edits land in mat_plot config yaml and
the plot modules there and in Galaxy/Lens.

## Risks / notes

- Architectural / API surface is broad — split into phased PRs at start_dev
  time (each phase above is at least one).
- Visual judgment is inherently human-in-the-loop: autonomy stays supervised.
