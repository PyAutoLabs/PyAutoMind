# Collect Euclid inspection images before vis_pix

Status: withdrawn

> **Superseded 2026-10-07 (human decision; never shipped).** Issue closed as superseded. The vis_lp inspection deliverable was produced by RAL job 350581 on 2026-09-23, and the final DR1 catalogue requires both vis_lp and vis_pix. Successor: `draft/feature/euclid/upstream_dr1_final_catalogue_tooling.md` (Mind 4fdd1111). No branch or worktree was ever created.

@euclid_strong_lens_modeling_pipeline

Issued: 2026-09-19

## Original request

hmmm is it feasible to make it so we can do this before vis_pix exists? Feels like useful flexiblity

## Context

`scripts/tools/build_inspect.py` currently skips a lens unless both `vis_lp` and `vis_pix` outputs exist. A completed `vis_lp` result already contains `image/rgb.png` and `image/fit.png`, so the inspection folder could be populated before `vis_pix` finishes. Preserve the later incremental collection of `vis_pix` products once they become available.
