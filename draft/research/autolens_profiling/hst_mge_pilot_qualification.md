# HST/MGE pilot: independent correctness qualification design

Filed: 2026-10-13
Type: research
Consequence: judge
Target: @autolens_profiling
Status: draft; awaiting approval of the bounded plan

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
