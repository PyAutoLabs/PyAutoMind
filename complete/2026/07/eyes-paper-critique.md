# Eyes Phase 3 — paper-informed critique (epic #117 CLOSED)

## Outcome

Phase 3 (final) of the Eyes agent epic shipped and MERGED on 2026-07-16:
PyAutoBrain#129 (4b40f69, 5 files all Eyes-owned, zero shared files). This
closes PyAutoBrain#117 — the full epic, conceived and shipped in one day:

- Phase 1: render harness + gallery + viz_manifest (autolens_workspace_test#170)
- Phase 2: the Eyes conductor + /eyes skill (PyAutoBrain#127)
- Phase 3: paper-informed critique (PyAutoBrain#129)

Phase 3 adds `eyes review <workspace> --against <reference-dir>`: a paper's
extracted panels (png/jpg, recursive) ride the EyesReviewSurface as
`reference_figures`; the note schema gains optional `reference`; the /eyes
skill's paper-informed pass reads the references FIRST and writes an
explicit convention-list rubric (colormaps, panel composition,
critical-curve/caustic annotation, colorbar placement + units, fonts, scale
bars) shown to the human before critiquing. Core stays decision-only,
stdlib-only, firewall-clean — it never fetches; the session gathers papers.

## Key decisions

- "Does the core change at all?" — resolved as a minimal core addition
  (--against + schema field) with the substance in skill prose; references
  are review context, never batch items, so review targets are unchanged.
- Empty/figure-less reference dir → exit 4 (same code as
  not-a-visualization-workspace: bad input surface).
- First REAL paper run deliberately deferred to the /eyes maiden voyage with
  a human-chosen paper — acceptance here = hermetic tests + a stand-in
  mechanics demo (64 figures + 1 reference on the live tree).

## Gotchas

- Phase-2 fixture had a real mtime race: figures written BEFORE their
  producer script → sub-second mtime resolution nondeterministically
  flagged STALE. Fixture now writes the producer first (the normal rendered
  state). Lesson: strict `>` mtime comparisons + fixture write order matter.

## Future work

- Maiden voyage part 2: human review session over the fresh gallery
  (production run done 2026-07-16; human looks 2026-07-17), then the first
  paper-informed pass with a chosen lensing paper.
- draft/feature/workspaces/gallery_runner_missing_tiers.md: add
  visualization_upper to the runner defaults; decide the
  modeling_visualization_jit tier.
- Feature Agent draft/-path parsing drift (recorded in Phase-2 record too).

## Original prompt

# Eyes Phase 3 — paper-informed critique

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 (final) of the Eyes agent epic (PyAutoBrain#117; Phase 1 harness
MERGED autolens_workspace_test#170, Phase 2 conductor MERGED PyAutoBrain#127).

Extend the /eyes loop with the "restyle to match this paper" capability the
original intake asked for: given a paper (PDF/figures/arXiv link), the review
pass compares the workspace's figures against the paper's visual conventions
(colormaps, scale bars, panel layout, annotation of critical curves/caustics,
colorbar placement, font sizing) and emits critique notes in the Phase-2
note schema, routed to the same edit surfaces.

Design constraints:

- Consults the memory faculty (PyAutoMemory wikis / autolens_assistant
  literature) for style precedent; PyAutoMemory citations never reach public
  output (privacy seam).
- The conductor core stays firewall-clean and decision-only; paper figures
  are review *context* gathered by the session, not fetched by the core.
- Likely shape: an `eyes review --against <paper-figures-dir>` mode or a
  skill-level step — decide at plan time whether the deterministic core
  needs any change at all (it may be pure skill prose + note-schema usage).
- Exercise it on a real case as the acceptance test (e.g. restyle the fit
  subplots toward a chosen lensing paper's conventions) and ship the
  resulting critique as intake prompts, not edits.
