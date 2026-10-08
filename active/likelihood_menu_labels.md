# Explicit implementation labels and likelihood priority

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight, PyAutoPulse
Difficulty: easy
Consequence: glance
Autonomy: safe
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/19

## Plan

Remove the Insight Evidence details disclosure and routine capture/integrity prose entirely from the rendered dashboard, retaining actual failure/stale/local warnings and machine-readable provenance. Label Delaunay and Rectangular JAX explicitly. On Pulse label known JAX/Numba implementations explicitly for likelihoods including KNN/MGE; omit unspecified implementation navigation variants without reclassifying any records. Order likelihood menu Delaunay, Rectangular, MGE, KNN, MGE Mass, Sersic, with deterministic implementation ordering within each. Preserve existing URLs and evidence snapshots. Files: each organ's setup_browser and associated board render, targeted browser expectations, generated dashboards. Validate existing suites, actual-menu browser witness, independent review and CI. Continue same-session user-authorized dashboard refinements through merge and deployment on green. Tier: glance; witness exact requested labels/order and no provenance block.

## Original request

remove "Evidence details
Integrity: ok · Freshness: freshness policy unspecified · evidence time unknown · Scientific qualification: 0/56 accepted by producer; remaining assessments shown below

Captured source branch: main. Revision: de37acfe797465205128d45973af5e853c74a684. Capture time: 2026-10-08T08:44:26Z. Latest attempt: 2026-10-08T08:44:26Z."        For PyAutoPulse I like how clear the four options under Imaging are. Lets call Delaunay -> Delaunay (JAX) and Rectangular -> Rectangular (JAX). Lets do the same renames to PyAutoPulse, where we will also remove the "implementation unspecified" variants, put those brackets in for KNN, MGE and have Delaunay top, then Rectangular, then MGE, then KNN, then MGE Mass, then Sersic, so its in descending order of priority and typical use

Routing: presentation-only organ changes, no scientific or public API changes; override keyword-derived library/large route to one bounded workspace task with two reviewed PRs. Branch survey clean main both repos; no competing claims.

## Sersic clarification

User chose: Keep one plain “Sersic” entry last, without claiming JAX or Numba.
The fallback is suppressed when known Sersic implementations exist.
