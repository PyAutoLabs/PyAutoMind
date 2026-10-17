## Summary
Design-only phase (autolens_profiling#418, issue #417; Codex session, shipped 2026-10-13, merged 2026-10-17 under human `/prm` after an independent review with verdict FINDINGS, none blocking). Adds `scripts/misc/jax_compile/QUALIFICATION.md` and a pointer in `PILOT.md`: derives what the HST/MGE CPU pilot computes (no positions term, two unregularized 20-Gaussian bases → the normalized Gaussian data log-likelihood; the 1e-3 stabilizing diagonal changes coefficients, adds no likelihood term), records the PDIP raw-plus-polish controls, proposes an independent witness (independently built imaging operator + `scipy.optimize.nnls`, first as a synthetic harness in autolens_workspace_test with a project adapter), lists every identity to capture, gives candidate tolerances marked unaccepted, and closes with an open-decisions table. No contradiction with the #416 runner; nothing executed, no threshold accepted, no compute authorized.

Review findings carried as the next bounded step (not fixed here): background-load method missing; the 1e-8 relative image L2 budget is likely unattainable against the packaged solver's inactive-column flux allowance, so synthetic-harness calibration must be allowed to revise tolerances; the correctness-process feasibility Pulse requested before finalizing the 32-process / 16 CPU-hour budget is deferred. Pulse: campaign `setup-baseline`, tasks `hst_mge_cpu_pilot` / `hst_mge_cpu_pilot_choices` (status needs-decision until the human selects data/host/stack).

## Original prompt

# HST/MGE pilot: independent correctness qualification design

Filed: 2026-10-13
Type: research
Consequence: judge
Target: @autolens_profiling
Status: approved; research documentation in progress
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/417
Approval: human "I approve, go", 2026-10-13

## Original request

> ok continue

Context: continue after merging autolens_profiling#416 and PyAutoPulse#55 and
closing implementation issue #415. The raw measurement tooling is shipped;
independent scientific correctness and collection approval remain pending.
Canonical intent: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/hst_mge_cpu_pilot.md
Previous phase: complete/2026/10/hst-mge-pilot-observations.md.

## Proposed bounded phase

Audit the exact imaging-mge-runtime-v1 objective and design its independent
correctness witness before implementing or executing that witness. This phase
produces a source-grounded qualification design, not numerical acceptance.

1. Trace current.from_dataset/build_workload and cell_builders.imaging_mge through
   the actual AnalysisImaging/FitImaging objective and inversion settings. Pin
   inspected source revisions; distinguish configured defaults from values only
   knowable on the chosen execution host. Enumerate input, mask, PSF,
   oversampling, parameter, coefficient-ordering, solver and normalization identity.
2. Audit candidate references and existing regression fixtures. Preserve
   non-negativity, actual objective terms and reconstruction semantics. Explicitly
   assess shared-code weaknesses; same-code eager/JIT agreement is insufficient.
   Recommend an independent construction/solve route or record why unavailable.
3. Specify the witness artifact and comparisons: reference hashes/provenance,
   likelihood terms, coefficients and reconstructed image, absolute/relative
   errors, near-zero normalization, and conditioning/non-uniqueness handling.
   Propose justified tolerance choices for human review, never silently accept
   inherited constants or fabricate numerical evidence.
4. Document remaining collection choices (host, immutable stack, production
   dataset, resolved settings, load method and resource ceiling) as unresolved
   where no verified evidence exists. Define a separately bounded implementation
   and synthetic validation follow-up, routed to the correctness-owning regression
   workspace if required; do not expand this research phase into library fixes.

## Planned files and validation

Add scripts/misc/jax_compile/QUALIFICATION.md with source links and the decision
table; add a short link from PILOT.md. No producer, library, test, default or
timing-record changes. Review every source citation and objective term, check
relative links, and run the applicable project documentation/generated checks.
Do not regenerate measurement timestamps or claim accepted baseline evidence.

No inference, production profiling, scientific witness execution, HPC submission,
baseline freeze/promotion or release. Production inputs and scientific tolerance
approval remain a later human decision. Pulse retains campaign state; this phase
does not duplicate its campaign or interfere with a concurrent Pulse check-in.

Tier: judge — merge mode: human /prm.

## Shipped design handoff — 2026-10-13

- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/418, head `3d6f83f73b84d81ed708129b09a97b4c873e5d3c`; CI in progress at publication.
- Worktree: `.worktrees/hst-mge-pilot-qualification/autolens_profiling`, branch `feature/hst-mge-pilot-qualification`.
- Added `scripts/misc/jax_compile/QUALIFICATION.md` and linked it from `PILOT.md`; no executable, default, measurement or generated timing metadata changes.
- Audit established the non-negative, diagonally stabilized solve versus the reported unregularized Gaussian data likelihood; documented raw/polished PDIP semantics and independent operator/augmented NNLS design.
- Recorded `PYAUTO_SMALL_DATASETS` actual-count/provenance limitation as a future guard requirement; no runner fix included.
- Proposed explicit scalar/image error budgets for review; coefficient tolerances and reference KKT accuracy remain unresolved. No scientific thresholds were accepted and no numerical witness ran.
- Validation passed: ruff (288 files), README/catalogue with Pulse contract reader/wiki/dashboard checks, 23 pinned-source and local-link checks, and existing MGE import-only smoke. Link/smoke/readiness logs: `tmp/hst-mge-qualification-links.log`, `tmp/hst-mge-qualification-smoke.log`, `tmp/hst-mge-qualification-ship-readiness.json`.
- Heart readiness STALE only: `release validation incomplete: no rehearsal for current source`; development publication permitted. No release, inference or production profiling.
- Next: human `/prm`, then separately plan the correctness-owning regression harness and project adapter with explicit synthetic execution caps. Pulse retains production host/stack/data/load/resource/collection choices and scientific acceptance.
