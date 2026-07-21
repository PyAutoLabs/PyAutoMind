# Adaptive pixel-signals IndexError (off-by-one) in double-Einstein-ring SLaM (real lib bug)

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Surfaced by the 2026-07-21 census AFTER a parallel chat un-parked the double_einstein_ring SLaM
scripts (the old opaque FitException is gone — this is the sharp underlying bug). Genuine PyAutoArray
library off-by-one in adaptive regularization:

```
autolens_workspace/scripts/imaging/features/advanced/double_einstein_ring/slam.py  (also group/ variant)
  PyAutoArray/autoarray/inversion/regularization/adapt.py:210 regularization_weights_from
  -> mappers/abstract.py:469 pixel_signals_from
  -> mappers/mapper_util.py:62 adaptive_pixel_signals_from
     flat_data_vals = xp.take(adapt_data[slim_index_for_sub_slim_index], I_sub, axis=0)
  IndexError: index 177 is out of bounds for axis 0 with size 177
```

index == size ⇒ classic off-by-one. Likely the multi-plane (double-Einstein-ring) adapt-data indexing
in `adaptive_pixel_signals_from` builds `slim_index_for_sub_slim_index` / `I_sub` off the wrong
plane's pixel count. Reproduce autolens_workspace/imaging/features/advanced/double_einstein_ring/slam
on clean main (real data, unset SMALL_DATASETS), fix the indexing in mapper_util, add a numpy unit
test, remove the NEEDS_FIX marker if the chat re-added one (currently un-parked and FAILING).
