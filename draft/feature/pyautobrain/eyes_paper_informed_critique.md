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
