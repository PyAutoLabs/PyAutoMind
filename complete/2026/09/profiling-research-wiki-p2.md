## profiling-research-wiki-p2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/339
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/340 (merge `5deb704a`, head `6211028`, 20 files, +1270/−207)
- epic: profiling-research-wiki (phase 2 of 2 — epic COMPLETE)
- merge: by the human's typed `/prm 340` on green (lint.yml one run, one job, success; `mergeable_state: clean`)
- heart: GREY at the door (Pages host not on the container allowlist); no ship-time vitals read — docs-only change, no library or script touched

### Summary
- Every one of the 18 header-only stubs left by phase 1 is now a full campaign page under
  `autolens_profiling/wiki/campaigns/`: why (cited to issues and Mind records, never pasted),
  a phases table with each phase's pre-registered rule, RAL jobs and PRs, a "what shipped"
  table with merge SHA and first release tag, open/parked/drafts, caveats, and a dated journal.
- Release states verified for every cited library PR against the first library tag containing
  its merge commit (blobless clones of PyAutoArray, PyAutoGalaxy, PyAutoLens, PyAutoFit,
  PyAutoNerves). No "release not verified" remains anywhere in the wiki. Unreleased on
  2026-09-27: PyAutoArray#580/#582/#584, PyAutoLens#752/#753/#754, PyAutoFit#1649.
- The PyAutoArray#582 F/D evaluation-count discrepancy is settled on the interferometer page
  by reading the pre-fix source at `879b2be1`: F=2/D=4 per full `figure_of_merit` under the
  packaged positive-only + edge-zeroed solver (the profiling rows); F=2/D=2 is the unit-test
  config's positive-negative branch. Both right in context; both 1/1 after the fix.
- Seven library speed-ups with no profiling note recorded as journal entries on the nearest
  page and as a "Library speed-ups with no profiling note" table at the foot of
  `wiki/index.md` (PyAutoArray#517, #540, #541, #544, #545, #582; the retired scalar-default
  flip; gaussian-precompute phase 3 = autolens_workspace#530).
- Corrections applied on the pages: #226 is an issue (PR #228); PyAutoArray#543 shipped as
  PR #545 and #542 as #544; PyAutoFit#1430 is the issue, PR #1431; the fixed-light numba
  1.80x chain runs jobs 343345 → 343356 with 343355 the failed bridge control (still not in
  the tree); the HST residue headline is job 343350; PyAutoArray#557 and mass-field PR #290
  added; the DelaunayNN headline re-pointed from the superseded 2.18x to the #537
  same-session A/B (1.22x).
- `wiki/index.md`: the closed/parked/draft table rebuilt from the pages (22 rows), the
  interferometer row's library-PR cell, the "stub / backfill pending" wording gone.
- Gate: `check_wiki.py --check` OK (23 campaign files, 46 ledgers linked); wiki tests 5 passed;
  ruff clean; README dashboard unchanged; lychee ran green in CI.

### Traps / notes
- Remote container session: Mind was claimed by `eyes-organ-order`, so every Mind write was
  ledger-only on the session branch (`active.md`, `active/`, this record) and landed through
  `mind_ledger_merge.yml`; the profiling repo was cloned via `add_repo` and worked on the
  session branch `claude/profiling-wiki-phase-2-b8vtjm`.
- Squash/merge-commit grep for `(#N)` misses this org's merge commits: match
  `Merge pull request #N` on `origin/main`; a `(#N)` hit can be the *issue* closed by a
  different PR (PyAutoArray#568 → PR #569, PyAutoFit#1430 → PR #1431).
- Library issues (PyAutoArray etc.) are outside the session's GitHub scope; the Mind records'
  `## Original prompt` sections carried every pre-registered rule the pages needed.
- Eight page-writing agents in parallel (one per shared source set) with a common brief and
  a verified release sheet; each reported index-row cells and out-of-scope corrections,
  integrated centrally. The JAX-faddeeva clamp audit (#215, PyAutoGalaxy#603, released
  2026.9.4.1) is folded into the numpy-deflections page rather than given its own page.
- The harness's stop hook asked for commits while agents were mid-write; pages were
  committed one group at a time as each agent finished, never mid-edit.

### Remainder (re-filed)
- The ledger and Mind drift the backfill surfaced but could not touch (results/notes/ and
  Mind records were out of scope) is filed as
  `draft/maintenance/autolens_profiling/wiki_backfill_ledger_and_mind_drift.md`.
- Epic follow-ons unchanged: `draft/refactor/autolens_profiling/notes_logs_and_sidecars_out_of_results_notes.md`,
  `draft/feature/autolens_profiling/runtime_dashboard_and_profiling_organ_vision.md`.

## Original prompt

# Profiling research wiki — phase 2: backfill the closed campaigns

- Work type: docs
- Target: @autolens_profiling
- Epic: profiling-research-wiki
- Autonomy: human-required
- Filed: 2026-09-27
- Depends on: phase 1 (autolens_profiling#337) merged
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/339
Issued: 2026-09-27

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
