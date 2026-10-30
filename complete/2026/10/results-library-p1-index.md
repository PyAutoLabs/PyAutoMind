- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1739
- completed: 2026-10-30
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1743
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1744
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1743
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1744
- epic: results-library (phase 1; ledger draft/feature/autofit/results_library_epic.md)
- summary: **1a (#1743):** `ResultState` in the shared status vocabulary; `autofit/results/` — ResultsIndex (per-result
  JSON records as truth, incremental on a stat fingerprint, `--index-dir` for read-only trees, superseded siblings
  by (path_prefix, unique_tag, name)), classify() (status record → zip/folder `.completed` + CRC → checkpoint probe;
  I/O errors are unreadable, never corrupt), ResultsCache (local SQLite), CLI `python -m autofit.results
  {index,status,count}`; `dataset_identity.json` at fit start via `Analysis.dataset_identity()` (object id, inputs
  + SHA256, centre, library versions; config switches); `Aggregator.latest_per`; `SearchOutput.completed_at`.
  **1b (#1744):** ZipMember (pathlib-like, holds no open file), `SearchOutput.from_zip`, `open_member`,
  `value(name, kind=)`, `Aggregator.from_index` — zero extraction.
- witness: W1 — laptop DR1 mirror (partial): 338 results, 325 completed, 13 superseded, 0 corrupt, 0 location
  mismatches; Workspace/Science/scratch/results_library_p1_w1/. W1 caught the ENOMEM-as-corrupt bug.
- tests: 15k synthetic index 37 s / re-index 6.7 s; full suites 4,010 / 4,015 (conformance file set + 600-line
  guard fixed); smoke 6 workspaces 167/0; CI all green. #1744 retargeted to main after #1743.
- decisions flagged: latest_per key (path_prefix, unique_tag, name); never_started covers no-checkpoint folders;
  versions recorded in dataset_identity.json.
- follow-up: PyAutoArray/PyAutoLens `dataset_identity()` hook (real input paths + cutout centre).

## Original prompt

Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1739
Epic: results-library
Phase: 1
Blocked-by: phase 0 (COMPLETE 2026-10-29)
Concurrent-with: hpc-campaign phase 2 (ruling F11 — two PyAutoFit worktrees; this task owns `autofit/results/`, `aggregator/`, `non_linear/status/identity.py`, the `ResultState` enum in `states.py`, the identity hook in `abstract_search.py`/`analysis.py`, `config/general.yaml` identity keys)
Consequence: judge
Autonomy: human-required
Witness: W1 — `python -m autofit.results index` + `status` over the laptop DR1 mirror (`Workspace/Science/active/euclid_dr1/output*`, partial: say so), index written OUTSIDE the tree, state-class table in `Workspace/Science/scratch/results_library_p1_w1/`. Read-only; DR1 tree never modified.

# Results library phase 1 — results index, state classes, identity, lazy reads, CLI

Original request (human, 2026-10-30): "Ctoninue the PyAutoLEns II HPC runs and Results"

Ledger: `draft/feature/autofit/results_library_epic.md` §Phase 1 (rulings F2 index store, F10 identity).
Lane prompt: `Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_results_library.md` §Phase 1.
Evidence: `results_library_epic_report.md` (P3, P4, P5, P6, P13, P15, P16, P22, P25; gaps 1–5, 17).

@PyAutoFit scope:
- `ResultState` (completed, running, interrupted_valid_ckpt, corrupt_ckpt, corrupt_zip, failed,
  superseded, never_started) added to the shared vocabulary `autofit/non_linear/status/states.py`.
- `autofit/results/`: per-result JSON records (truth) under `<root>/.autofit_index/` or `--index-dir`,
  local SQLite cache rebuilt on demand (never truth, never on NFS), incremental on (zip path, size, mtime);
  reads `status.json` first, classifies from disk otherwise; layout-agnostic, many roots.
- `dataset_identity.json` at fit start (`files/`), `Analysis.dataset_identity()` hook, sha256 default on
  with a config off switch (F10).
- `Aggregator.latest_per(key=("unique_tag","name"), by="completed_at")`.
- Lazy zip reads: `SearchOutput.open_member`, `value(name, kind=...)`, `Aggregator.from_index(root)`.
- CLI `python -m autofit.results {index,status,count}`.

Done: 15k synthetic fixture indexes in minutes, re-index after 10 new results in seconds; aggregate over
the index with zero bytes extracted; W1 witness.
