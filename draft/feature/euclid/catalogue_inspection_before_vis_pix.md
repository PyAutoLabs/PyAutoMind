# Collect Euclid inspection images before vis_pix

@euclid_strong_lens_modeling_pipeline

## Original request

hmmm is it feasible to make it so we can do this before vis_pix exists? Feels like useful flexiblity

## Context

`scripts/tools/build_inspect.py` currently skips a lens unless both `vis_lp` and `vis_pix` outputs exist. A completed `vis_lp` result already contains `image/rgb.png` and `image/fit.png`, so the inspection folder could be populated before `vis_pix` finishes. Preserve the later incremental collection of `vis_pix` products once they become available.
