# Move committed job logs and JSON sidecars out of results/notes/

- Work type: refactor
- Target: @autolens_profiling
- Epic: profiling-research-wiki
- Autonomy: human-required
- Filed: 2026-09-27
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/341
Issued: 2026-09-27

## Original prompt

From the 2026-09-27 profiling review: `results/notes/` holds 74 files / 28,474 lines, of which
16 `.out` job logs (5,311 lines) and 10 `.json` sidecars (5,406 lines) are 38 % of the "notes"
tree; recent measurement PRs are 16k–26k lines each, mostly result JSON (e.g. #327 = 24,100 lines
of JSON, #335 = 15.5k). The maintainer agreed this is a problem.

## Scope

1. Decide and document the artefact policy in `results/README.md`: `.out` logs go to
   `results/logs/<campaign>/` (or stay on RAL and are cited by job id); JSON sidecars go beside the
   result JSONs they describe, not under `notes/`; committed result JSON is summarised (per-row
   medians + CI + provenance block), not per-repeat dumps.
2. `git mv` the existing 26 files with the ledger links rewritten (and `check_wiki.py`, lychee
   green). History is preserved by the move; nothing is deleted.
3. Add a lint-gate check that `results/notes/` contains only `.md`.
4. Mandatory provenance block for every result JSON: host, loadavg at start/end, SLURM job id,
   library revisions, dependency floors (nufftax etc.) — the fields the wiki index and the future
   dashboard read.

## Out of scope

Re-running anything; changing what any script measures.
