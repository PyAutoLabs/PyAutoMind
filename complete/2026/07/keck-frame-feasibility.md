## keck-frame-feasibility
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/31 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/32 (merged 34866b7, squash; docs-only)
- summary: Keck per-frame feasibility answered — GO in principle (strongest science case: frame-to-frame AO PSF variability, SHARP III's dominant systematic; epoch-matched per-frame PSFs extend tier-A evidence selection) via the prepared-frames-in-work-dir seam; registration INVERTS (measured offsets are truth, currently not serialized to provenance — delta 1 regardless); per-frame noise constructed from the MCDS detector model; per-frame CRs = frame-vs-stack outlier pass (same job as the stack CR open item). GATED sequence: #13 acceptance + plate-scale fix -> outlier pass -> frames branch. User accepted guidance
- followups: implementation prompts filed as predecessors clear (not upfront); offsets-to-provenance is a useful standalone delta
