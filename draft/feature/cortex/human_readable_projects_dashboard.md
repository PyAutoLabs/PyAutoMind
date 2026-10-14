# Human-readable Cortex Projects dashboard

Targets: @PyAutoBrain @PyAutoCortex
Type: feature

## Original request (verbatim)

The contents of the Cortex dashboard under Projects is hard to follow, theres tons of text, too much information and it is not structured in a readable away. I think it probably contains the right information, and mostly of the stuff I need, but maybe it just needs text like this: 342299_1 — open — ral — 2026-09-07 — delaunay_adapt_split_pl_eff_0: job B, numba chain at the standard 1250-pixel Delaunay mesh (8c / 96gb / 48 h); reloads job A 342231_1; the 09-07 ruling: run al…
342299_2 — open — ral — 2026-09-07 — delaunay_adapt_split_pl_eff_1_outer: job B, numba chain at the standard 1250-pixel Delaunay mesh (8c / 96gb / 48 h); reloads job A 342231_2; the 09-07 ruling:…
342311_1 — open — ral — 2026-09-07 — rectangular_adapt_pl_eff_0: job B, numba chain (8c / 96gb / 48 h) at the standard 1250-pixel mesh under PIPELINE=rectangular_adapt; reloads job A 342237_1; the…
342311_2 — open — ral — 2026-09-07 — rectangular_adapt_pl_eff_1_outer: job B, numba chain (8c / 96gb / 48 h) at the standard 1250-pixel mesh under PIPELINE=rectangular_adapt; reloads job A 342237_…
342311_0 — open — ral — 2026-09-07 — rectangular_adapt_pl_sersic_0: job B, numba chain (8c / 96gb / 48 h) at the standard 1250-pixel mesh under PIPELINE=rectangular_adapt; reloads job A 342237_0;… to be in a structured table with clearly aligned readable columns?  However, maybe there is better approaches we can take to presenting the information? It all feels very AI readable and thus via the Cortex / Scientist prompt would probably allow me to successfully check in for the project, but dashboards are meant to be human readable and in its current state it is not.   I think having each project as its own drop down with "Projects" would also help reduce information overload. I think thatt for each project having a high level summary of the output folder may help, e.g. how many lenses or datasets have been modeled, estimate of total CPU or GPU time spent on project.

## Proposed design (awaiting approval)

- Collapsed project disclosures with name, short purpose, recorded run counts and evidence freshness.
- Expanded view: current position, output summary, structured run table, collapsed history and technical locations, existing resume action.
- Runs: job ID, recorded state, partition, date, description with full details available. Preserve source meaning and do not invent fields from ambiguous prose.
- Output summary: unique datasets with completed outputs separately from fit/search counts, CPU core-hours and GPU device-hours separately, evidence timestamp and coverage. Unknown is not zero; requested walltime is not consumed compute.
- Keep source ledgers authoritative and preserve check-in/resume behavior.

## Implementation outline

1. In PyAutoBrain agents/conductors/cortex/_cortex.py, update _card_html and _card_md and introduce scoped presentation helpers. Follow shared board sizing/navigation/orchestration contracts and concise-copy policy. Avoid changing shared components unless required.
2. Add optional structured output-summary receipts owned by Cortex, with schema/provenance/coverage validation in scripts/cortex.py and documentation in REFERENCE.md. First inspect available output metadata; collection must be explicit and read-only against configured project roots. Rendering consumes saved receipts and never crawls outputs or contacts RAL. Missing/unavailable sources remain visible; no scientific acceptance is inferred.
3. Add tests to Brain tests/test_cortex_conductor.py and applicable Cortex tests for disclosure/table rendering, full-detail access, escaping, unknown/partial/stale receipts and deduplication/accounting semantics. Validate keyboard/mobile behavior with rendered examples.
4. Regenerate Cortex dashboard.md/dashboard.html using the conductor; check ledger validity and renderer drift. Preserve existing local edits and coordinate the active Cortex claim before setup.

Tier: undeclared — merge mode: human /prm

## Phasing decision

Feature Agent recommends separate phases. Phase 1 is the presentation change (steps 1, 3 and 4 as applicable); Phase 2 is output accounting (step 2 plus receipt/collector validation), after identifying reliable metadata. Phase 1 must not depend on collecting metrics. Both remain awaiting human plan approval. Proposed branches: feature/cortex-project-readability and feature/cortex-output-summary.

## Current coordination

PyAutoBrain main is clean. PyAutoCortex main is behind origin/main and has existing local edits. Mind active.md claims Cortex for search-ext-b5a-wave2. Resolve that claim before implementation; no source edits have been made for this proposal.

## Approval

The user approved the two-phase direction in this session: "I approve". No repeat plan approval is required for this scope. Phase 1 is queued behind active Brain and Cortex claims; merge remains human /prm.
