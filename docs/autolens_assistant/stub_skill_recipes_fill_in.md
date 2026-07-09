# Fill in the 14 stub skill recipes (one at a time)

Type: docs
Target: autolens_assistant
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

The 14 `al_*` skills marked `(stub)` in `skills/README.md` ("Pending — stubbed") have
frontmatter + Orient/Ask/Branch/Combine scaffolds but TODO `Branch` recipes:
point_source, time_delay_cosmography, group_lensing, cluster_csv_api, multi_dataset,
weak_lensing, datacube_modeling, subhalo_detect, sensitivity_mapping,
hierarchical_inference, aggregator_bulk_analysis, adaptive_pixelization,
mge_decomposition, custom_analysis.

Decided at release (assistant-wiki-release, autolens_assistant#40, shipped 2026-07-09):
stubs ship honestly-labeled; their wiki/core companion pages are verified complete, so
the *what/why* layer is covered — only the procedural recipes are pending.

Fill them **one at a time** (do not bulk-issue — spawn a task per skill as its
predecessor nears shipping), pairing each recipe with a smoke run of the generated
script under `PYAUTO_TEST_MODE=1` and the `_style.md` conventions. Derive every recipe
from the matching autolens_workspace scripts + installed source, never memory. Suggested
first pick: `al_point_source` (largest user surface). The "Queue (catalogued, not yet
stubbed)" topics in skills/README.md are a separate later decision.
