# likelihood-menu-labels

Completed: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/19
PR: https://github.com/PyAutoLabs/PyAutoInsight/pull/20
PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/37

Removed Insight's routine Evidence details disclosure and capture/integrity prose while preserving actual warning states. Explicit JAX labels now match Pulse. Pulse uses parenthesized JAX/Numba labels and likelihood priority Delaunay, Rectangular, MGE, KNN, MGE Mass, Sersic, then other families. Unspecified variants are hidden without reclassifying evidence or breaking direct links. Per user clarification, one plain Sersic fallback preserves its unclassified latent tools; known implementations suppress that fallback.

Validation: Insight 170 and Pulse 193 tests; both real Chromium suites; actual captured menus; independent CLEAN including unknown evidence deep links and four Sersic fallback/duplicate cases; Ruff, format, offline feed and diff checks. Heart STALE solely `release validation incomplete: no rehearsal for current source`.

Exact-head CI: Insight6430a82 lint37758259743/job113248095304 and refresh37758259795/job113248095290; Pulse1ffaf8c lint37758273007/job113248137510 and refresh37758272961/job113248137703. All jobs passed; no skipped test jobs. Both PRs CLEAN/MERGEABLE before user-authorized merge. Merge commits09b2459ccc162b0aff6721f3acbc332d76681fe0 and0d3e15a747fb0aa0574e6ee08e092be301f9d936 proved by Git ancestry and GitHub MERGED state. Issue closed.

Revert commands in respective repositories: `git revert -m 1 09b2459ccc162b0aff6721f3acbc332d76681fe0` (Insight), `git revert -m 1 0d3e15a747fb0aa0574e6ee08e092be301f9d936` (Pulse).

Postmerge publication passed: Insight lint37758437138/refresh37758437205 and final Pages37758470406 at6cf5a422b6748364f5283b5cf7d16179ab4690b3; Pulse lint37758452153/refresh37758452477 and final Pages37758479751 at95e38fa10b25cc8b4d4f535d20cb08fe29990d28. Pulse initial Pages run37758452134 was superseded by the successful refreshed deployment. Live Chromium confirms no Evidence details, explicit labels and requested priority/plain Sersic. Mind dashboard regenerated and checked; active claim released; shadow row9/20 appended. Browser screenshots retained under Mind tmp/likelihood-menu-labels.

## Original prompt

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
