# Likelihood lifecycle phase 0A: `profiling-summary@3` (class/status), `walltime-validation@1`, `designation` decisions and Class-first Pulse board

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoPulse
Themes:
- profiling
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `pyauto-pulse check` accepts a fixture `profiling-summary@3` catalogue in which every record carries `class` and `status`, refuses a second `current` record on one (likelihood, instrument, setup_id, host_class, model_variant, measurement) key, refuses `class: optimal` without a resolvable `decision_id`, accepts a `walltime-validation@1` document, and the rendered board's first `<select>` is Class with Optimal selected and superseded rows hidden until the History toggle
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 0
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-21
Note: Pulse PR #68 (docs/receipts) is open and unmerged on 2026-10-21; branch from main and rebase after it merges — not a gate.

Phase 0 of the `likelihood-lifecycle` epic (ledger: `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`; bodies and architecture: `likelihood_lifecycle_epic_report.md` §3.1, §3.2, §3.6, §3.8, §4 phase 0; evidence: `likelihood_lifecycle_epic_surveys/02_pulse_insight_contracts.md`). Phase 0 is the spine and has five sub-issues, one per repo, issued in order: **0A PyAutoPulse (this prompt)** → 0B autolens_profiling → 0C autolens_inference → 0D PyAutoInsight → 0E PyAutoBrain. Each later sub-issue is filed as its own prompt (`likelihood_lifecycle_p0_<target>.md`, `Phase: 0`) once 0A is shipped, because 0B's catalogue builder and 0C's exporter emit the contract this issue defines. Library first: Pulse is the contract owner, so it goes first.

## Rulings assumed (report §5; the human confirms or amends at plan approval)

- R1 vocabulary and `setup_id` grammar as report §3.1 (`<backend>_<device>_<operator>_<precision>[_<transformer>]`; site/tier moves to `host_class`).
- R2 day-zero history cut is label-only; nothing is deleted or re-run in phase 0.
- R3 the provisional designations in report §3.3 are the phase-0 labels; phases 2–3 confirm.
- R7 `host_class` is provenance, never identity; `local_laptop` / `local_gpu` rows can never be `current`.
- R4/R5 enter as validator enumerations only (mixed precision allowed with `class: experimental`; `compile` is a measurement, not a class axis).

## What (sub-issue 0A, PyAutoPulse only)

1. **`profiling-summary@3` contract** (`pulse/summary.py` SUPPORTED, `pulse/catalogue.py` validate, `REFERENCE.md`): additive on v2 with a version bump. Record fields: `likelihood {dataset_type, variant}`, `instrument`, `regime`, `setup {backend, device, operator, precision, transformer, threads}` + `setup_id`, `host_class`, `model_variant`, `measurement`, `class` ∈ {optimal, secondary, experimental}, `status` ∈ {current, superseded, archived}, `superseded_by`, `day_zero`, `figures[] {kind, path, sha256}`, `decision_id`, `release_pin`, `measured_at`. Enumerations for the ten `dataset_type`s, `host_class`, `measurement` (adds `gradient`, `parity`, `walltime_validation`) and `class`/`status` live in REFERENCE.md and the validator. Rules: exactly one `current` per (likelihood, instrument, setup_id, host_class, model_variant, measurement); `class: optimal` ⇒ `decision_id` present and resolvable in `decisions.yaml`; `host_class` ∈ {local_laptop, local_gpu} ⇒ `status != current`; `archived` records are excluded from `records[]` and counted in `archive_record_count`; `planned_cells` carry `class` so coverage is reported per class. v2 instances keep validating unchanged (autofit_profiling stays @2).
2. **`walltime-validation@1` evidence axis** (new schema, producer autolens_inference): record keyed by (likelihood, instrument, setup_id, host_class, model_variant, sampler, seed) with `wall_s`, `likelihood_evals`, `implied_ms_per_eval`, `reference_runtime_record_id`, `predicted_ms_per_eval`, `ratio_measured_over_predicted`, `cores`, `parallel_efficiency`, `release_pin`, `slurm_job_id`, `max_log_likelihood`, `parity_status` ∈ {match, diverged, not_assessed}. All derived numbers producer-declared; Pulse validates and renders only. Registry accepts a second summary per instance (or a second instance kind) for this axis; REFERENCE.md states these are full-fit measurements.
3. **`designation` decision kind** (`decisions/README.md` template, `decisions.yaml`, `pulse/decisions.py`): fields `likelihood`, `regime`, `hardware_class` ∈ {cpu_many_core, gpu_a100, laptop}, `optimal: <setup_id>`, `secondary: [<setup_id>…]`, `evidence: [record ids]`, `rule` (one sentence in dataset-property terms), `supersedes`. The validator's optimal⇒decision_id rule resolves against these rows. No designation records are written in 0A (phase 3 writes them); the kind, template and test fixture are.
4. **Board** (`pulse/setup_browser.js`, `pulse/board.py`, `dashboard.md`): for @3 instances the selector order becomes Class (Optimal default | Secondary | Experimental | All) → Likelihood (dataset type → variant) → Instrument → Hardware class → Measurement; a History toggle reveals `superseded` rows; a Coverage panel lists Optimal cells that are `not_measured`; archived records are counted, never rendered. @2 instances keep today's browser. The check-in prose (`CHECKIN.md`) says research lookups read `class: optimal` + `status: current` unless asked otherwise.
5. **Doc drift**: REFERENCE.md :9, :36, :42, :99-101 still describe v1 as live; fix alongside the @3 section. README mirrors.
6. **Tests**: @3 fixture catalogue under `tests/fixtures/` exercising every rule above (accept, duplicate-current refusal, optimal-without-decision refusal, laptop-current refusal, archived exclusion); `walltime-validation@1` fixture; browser test asserting the first `<select>` is Class with Optimal default and that superseded rows are hidden until History.

## Out of scope for 0A

The autolens_profiling catalogue builder and move-only PRs (0B), the autolens_inference exporter (0C), Insight's additive fields (0D), the Brain lifecycle template and conductor grid (0E), any designation decision record (phase 3), any re-measurement (phase 3) and the `setup-baseline` campaign closure (phase 3).

## Boundaries (epic invariants)

Optimal is always a producer-declared class backed by a Pulse decision record; Pulse infers nothing, selects no fastest row and computes no ratio. Exactly one `current` per key, chosen by the producer under the day-zero rule, never by date. Sessions end at their deliverable; the human runs `/prm`.
