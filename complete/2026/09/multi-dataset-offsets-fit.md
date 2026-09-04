## multi-dataset-offsets-fit
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/524 (CLOSED)
- completed: 2026-09-04
- user-facing: true (reporter @samlange04; receipt, plan, PR-open and Shipped comments posted)
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/532 (merged bbd36819)
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/235 (merged a19ce0ba)
- repos: autolens_workspace, autogalaxy_workspace
- summary: Community bug report verified true on all three counts and fixed. Every multi-dataset example that freed `DatasetModel.grid_offset` on a `model_analysis` copy then wrapped the uncustomised `model` in `AnalysisFactor`, so no inter-band offset was ever fitted; the SLaM simultaneous pipeline shared one `DatasetModel` with no free priors across every band and stage while its docstring said the offsets were fully modeled. Fix: examples wrap `model_analysis` (per-band +2 params, lens/source shared because `model.copy()` preserves prior `.id`); simultaneous.py builds a per-band `dataset_model_list` (band 0 fixed, later bands UniformPrior ±1" in every stage) threaded through 7 stages with lens/source composed once; prose states the fixed-zero config default. `Constant` default unchanged. Notebooks regenerated.
- verification: reporter's 5-number repro reproduced exactly (0/2/0/38/40); corrected loop runs under the vmapped JAX Nautilus fitness and the offset moves the likelihood; 5 scripts pass the smoke profile incl. the full 7-stage SLaM pipeline; PR file lists exactly scripts + notebook twins.
- notes: The user's prior ("the dataset_offsets feature example covers this, so the report is wrong") was itself wrong — that example carried the identical slip, and the autogalaxy port even had a comment preserving it. Shipped under Heart RED "release validation FAILED (stage integrate)" with explicit human authorization; the "PyAutoLens: 4 commits behind origin" RED reason was local staleness cleared by discarding a parked README re-wrap and ff-pulling. The Mind draft `draft/bug/autofit/dataset_model_free_grid_offset_pytree_roundtrip.md` was rewritten at this close-out: the real failure is a `ValueError` in `Model.tree_flatten` for any zero-direct-prior Model, never on the search path. Follow-up filed: `draft/bug/autolens_workspace/slam_simultaneous_subhalo_grid_search_fits_last.md` (subhalo_grid_search fits the last band only, no dataset_model).
- pending-release: none (workspace-only; no library change)

## Original prompt

No PyAutoMind prompt file — this task entered through `/community triage` → `/start_dev_for_user` on the user-filed issue. Issue title: "Multi-dataset examples never fit the inter-band grid_offset, while documenting that they do" (samlange04, 2026-09-03). Three causes reported: (1) `start_here.py` wraps `model` not `model_analysis`; (2) `config/priors/dataset_model.yaml` declares the offsets `Constant`; (3) `features/slam/simultaneous.py` shares one `DatasetModel` across all bands. Suggested fix: (1) one-line swap, (2) design question left as-is, (3) one `DatasetModel` per band with band 0 fixed as the reference.
