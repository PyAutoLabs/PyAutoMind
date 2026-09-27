## profiling-notes-sidecars-out
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/341
- completed: 2026-09-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/342 (merge `282076cf`, head `ab1e4fd`, 45 files, +1150/−25)
- epic: profiling-research-wiki (follow-on; the epic itself closed with phase 2)
- merge: by the human's typed `/prm 342` on green (lint.yml one run, one job, success; `mergeable_state: clean`)
- heart: GREY at the door (Pages host not on the container allowlist); no ship-time vitals read — tooling, docs and file moves only, no library change

### Summary
- `results/notes/` is the ledger tree again: the 16 SLURM `.out` logs moved to
  `results/logs/point_source_image/` (12) and `results/logs/point_source_source/` (4), the 10
  JSON sidecars moved to `results/breakdown/imaging/` beside the fixed-light trace and numba
  results they describe. All `git mv`, history kept; 19 same-directory ledger links, 3 wiki
  links and 3 prose paths rewritten; `check_wiki.py --check` green.
- The artefact policy is written into `results/README.md`: notes markdown-only, logs under
  `logs/<campaign>/` or cited by job id, sidecars beside their result JSON, new measurements
  commit summarised JSON (medians + CI + provenance) not per-repeat dumps, the provenance
  contract. New `results/logs/README.md`. The two evidence-pack folders under `notes/`
  (`clipper_campaign/`, `point_source_cpu_2026_09_17_reported/`) stay, allowlisted by name.
- `_profile_cli.provenance_dict()` → `device.provenance`, attached inside `device_info_dict()`
  so the 60 cells that already record their device carry it with no per-script edit: schema,
  UTC timestamp, host, SLURM job/array/task ids, load average at import and at write,
  profiling revision, library revisions (via `likelihood_breakdown/provenance.py`), library
  versions, dependency versions (jax, jaxlib, numpy, scipy, numba, nufftax). Never raises.
- `scripts/misc/tooling/check_results_layout.py --check` (stdlib) in `lint.yml`: notes-only
  rule, provenance required on any device-recording result JSON not in the grandfather
  manifest `results/provenance_grandfathered.txt` (530 pre-policy files; a ratchet, lines only
  ever removed), dead manifest lines fail.
- Tests: `test_check_results_layout.py` (10) and `test_provenance_dict.py` (4); with the
  wiki and cell-contract tests 52 passed locally; ruff, README dashboard and both gates green;
  smoke and lychee ran green in CI.

### Traps / notes
- `git mv` + link rewrite as one script: ledgers link a sidecar by bare filename (same dir),
  the wiki by `../../results/notes/<file>`; three prose mentions in the source-plane ledger
  carried the `results/notes/` path in backticks and were rewritten too. Bare filename mentions
  in prose stay valid as names.
- Retrofitting the block onto the 530 existing JSONs is impossible (the fields were never
  captured), so enforcement is a manifest ratchet, not a retro-edit. `--write-grandfather` is
  meant to run once; the header says so.
- ruff UP017 wants `datetime.UTC` (py311 target); the load-average helper must swallow every
  exception, not just OSError, for the never-raise contract to hold (a test caught it).
- Session branch reuse: after #340 merged, the designated branch was restarted from `main`
  (`git checkout -B … origin/main`) per the harness rule for a merged designated branch.

### Remainder (re-filed)
- none. The epic's remaining follow-ons are unchanged:
  `draft/feature/autolens_profiling/runtime_dashboard_and_profiling_organ_vision.md` and
  `draft/maintenance/autolens_profiling/wiki_backfill_ledger_and_mind_drift.md`.

## Original prompt

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
