# Profiling research wiki — phase 2: backfill the closed campaigns

- Work type: docs
- Target: @autolens_profiling
- Epic: profiling-research-wiki
- Autonomy: human-required
- Filed: 2026-09-27
- Depends on: phase 1 (autolens_profiling#337) merged

## Original prompt

"be sure we are building the research wiki of all this work so the profiling work we do is kept
and tracked" — phase 1 built `wiki/index.md`, the four live campaign pages and the drift check;
this phase fills the ~18 stub pages.

## Scope

For every `wiki/campaigns/*.md` stub left by phase 1 (fixed lens light, fixed-light numba CPU,
HST GPU residue p1–4, certified positive solver, post-certified breakdown, numba interferometer
revisit, Delaunay/DelaunayNN A100 series, A100 pixelized baseline, matrix-free pixelized,
numpy deflections CPU, gaussian deflections precompute, image-source mappings, compile time,
PreOptimizationTimes baseline, reference notes, imaging over-sampling, mass-field profiling,
point-source GPU breakdown):

1. Move the "why" (question + pre-registered go/no-go rule) out of the GitHub issue body and the
   Mind `complete/2026/09/*.md` `## Original prompt` / `complete/archive/epics/*` ledgers into the
   page. Cite the issue number; do not paste whole issue bodies.
2. Per-phase table (phase | dates | question | rule | result | RAL jobs | PRs) and the release
   table, verified with `git tag --contains <merge-sha>`.
3. Caveats section: provenance gaps (e.g. job 343355 control missing from the tree behind the
   fixed-light 1.80x), laptop-only rows, inconsistent numerical gates (1e-9 vs PDIP tolerance).
4. Record the ~7 library speed-ups that have no profiling note (PyAutoArray #515, #538, #539,
   #543, #581, the scalar-default flip autolens_profiling#302, gaussian-precompute p3) as rows or
   journal entries so the index is complete.
5. Update each index row's Status / Verdict / Last updated; `check_wiki.py --check` stays green.

## Out of scope

Rewriting or moving the `results/notes/` ledgers; the dashboard; any script change.
