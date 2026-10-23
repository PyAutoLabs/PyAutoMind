## likelihood-lifecycle-p0-brain
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/535
- completed: 2026-10-23
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/536
- epic: likelihood-lifecycle (phase 0, sub-issue 0E of 0A–0E)

- Summary: PyAutoBrain#536 (185a370, merged a64b7990) — (a) `skills/profiling/lifecycle.md`: the report §3.9 L0–L7 sequence as eight Mind prompt blocks with full headers (`Epic: lifecycle-<dataset_type>-<variant>`, integer phases 0–7, placeholders `<dataset_type>`, `<variant>`, `<instrument>`, `<regime>`, `<trigger>`), linked from the profiling skill and conductor AGENTS.md; `tests/test_profiling_lifecycle_template.py` renders imaging/delaunay and checks every header through intake's own `census()`. (b) Profiling conductor: on a published `profiling-summary@3` catalogue, `campaign` reports a per-likelihood × class × measurement coverage grid (current / stale / superseded / missing), parses `setup_id` by the R1 grammar (`SetupIdError` on violation, in the catalogue or results-tree folder names), never counts `local_*` host classes as current (R7), reports class as declared (R3), routes CPU cells to `--partition=ral` and A100 cells to `gpu --gres`; v2/absent catalogue byte-identical (live dry-run sha256 be73b898… before = after; 22 cells / 23 done / 4 unusable / 17 missing; tier a100, compile axis and text outputs identical). (c) Samplers faculty mature tier reads `autolens_inference/scripts/<dataset_type>/<variant>/samplers/` (3 point_source + 8 imaging cells live), `validation/` leaves in their own tier, autofit_inference unchanged. (d) Pulse/Insight read prose: current+optimal default, `walltime-validation@1` is Pulse's (`lens-walltime`), Insight sampler records `setup_mode: auto`, optimal is always a Pulse designation. pytest 1268 → 1282; ruff unchanged.
- Human rulings: claim-guard override 2026-10-23 ("I authorize you to go") — shipped on PyAutoBrain alongside `github-token-p2b-writers-app` (#534) on a separate branch, no `.github/` or token files touched. Heart STALE at the door, YELLOW at ship (workspace manifest drift; PyAutoLens release validation stale), unrelated.
- Deviations / follow-ups: the @3 contract has no catalogue-level `release_pin`, so "stale" is judged against the envelope pin if present else the newest record pin (candidate Pulse follow-up); on v3 `--tier` is echoed but cells route by `host_class`; template `Blocked-by:` names the prior phase and is swapped for `Repo#N` at filing. Live witness on autolens_profiling lands when 0B mirrors `results/` and re-pins `lens` to @3 — until then the grid is proven on the tmp_path fixture and Pulse's v3 fixture.
- Next: phase 0 has only 0B left (`planned.md likelihood-lifecycle-p0-profiling`, queued behind the cluster-pointsolver starting-grid claim on autolens_profiling); phase 1 (figures) is independent of 0 and may be filed next; phase 8 renders `lifecycle.md` as the `pyauto-brain profiling lifecycle` verb.

## Original prompt

# Likelihood lifecycle phase 0E: PyAutoBrain lifecycle prompt template (`skills/profiling/lifecycle.md`), profiling conductor grid on the mirrored tree and `setup_id`/`host_class`/class/status grammar, samplers faculty paths, Pulse/Insight read prose

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Themes:
- profiling
- samplers
- dashboard
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `skills/profiling/lifecycle.md` exists and renders the §3.9 L0–L7 sequence as a filled phase-prompt template (a Brain test renders it for `imaging/delaunay` from a fixture and the output passes `intake census` header hygiene); `pyauto-brain profiling campaign --workspace <fixture>` dry-run on a fixture laid out per report §3.7 (`results/<dataset_type>/<variant>/<instrument>/<setup_id>/<host_class>/runtime.json` + a `profiling-summary@3` catalogue) reports coverage per likelihood × class × measurement with current / superseded / missing cells, while the same command on the live autolens_profiling checkout still returns today's legacy result unchanged; `pyauto-brain samplers` reports the autolens_inference mature tier from `scripts/<dataset_type>/<variant>/samplers/` and its AGENTS.md no longer names `scripts/<dataset>/searches/<sampler>/`
Review-minutes: 25
Unattended: never
Epic: likelihood-lifecycle
Phase: 0
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-23
Issued: 2026-10-23
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/535

Phase 0 sub-issue 0E of the `likelihood-lifecycle` epic (ledger `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`; report §3.1 vocabulary, §3.7 layouts, §3.8 dashboards, §3.9 lifecycle sequence, §4 phase 0 "0E PyAutoBrain", phase 8 "lifecycle verb"; survey `likelihood_lifecycle_epic_surveys/05_brain_conductors_epic_format.md` §4). Depends on 0A (PyAutoPulse#70: `profiling-summary@3` shape — per-record `likelihood`, `instrument`, `regime`, `setup` + `setup_id`, `host_class`, `model_variant`, `measurement`, `class`, `status`, `planned_cells` with `class`) and 0C/0D (autolens_inference mirrored tree; Insight lifecycle fields). **Does not depend on 0B**: autolens_profiling's `results/` is not yet mirrored (0B is queued behind the cluster-pointsolver starting-grid claim), so the conductor's new-tree reader is proven on a fixture here and on the live tree when 0B lands. Nothing in this issue edits autolens_profiling, autolens_inference, Pulse or Insight.

## State found 2026-10-23 (do not re-survey)

- `agents/conductors/profiling/_profiling.py`: `campaign` already reads `catalogue/script_routes.json` (model-first `scripts/<dataset>/<model>/<measurement>.py`, `runtime_cells`, `compile_probe`; "Source routes require profiling-summary v2" in `_catalogue.py`) with the legacy `sweep.py CELLS` AST fallback. Coverage is counted from `results/runtime/` buckets by sweep **config** name (`local_cpu_fp64`, `a100_…`) — the pre-R1 grammar — and knows nothing of `class`/`status`/`host_class`. Live dry-run today: 22 grid cells, 23 done, 4 unusable, 17 missing (legacy result; must stay unchanged).
- `agents/faculties/samplers/_samplers.py` `tier_mature` walks every `scripts/**/*.py` leaf and reads the `run_search(...)` declaration, so the 0C move did not break it (live: 3 mature autolens_inference cells). Its docstring and `agents/faculties/samplers/AGENTS.md` §"maturation lane" still name `autolens_inference/scripts/<dataset>/searches/<sampler>/`, say "Empty until autolens-inference phase 3", and the no-declaration fallback parses the `searches/<sampler>/<model_type>.py` path shape. The 0C tree is `scripts/<dataset_type>/<variant>/samplers/…` and `…/validation/…`; the old `scripts/<dataset>/{searches,slam}/` paths are README pointers only.
- No lifecycle template exists: `skills/profiling/` holds `SKILL.md` + `profiling.md` only. `skills/profiling/profiling.md` and `skills/sampler_pipeline/{SKILL,reference}.md` are the only Brain prose on how Pulse/Insight are read; neither says "read `class: optimal` + `status: current` unless asked" (report §3.8), that full-fit wall-time validation is a Pulse axis (`walltime-validation@1`, instance `lens-walltime`), or that Insight sampler records assume `setup_mode: auto` (R8).
- Brain tests: `tests/test_profiling_conductor.py` (48 tests), `tests/test_samplers_surface.py` (17).

## Rulings applied

R1 (`setup_id` = `<backend>_<device>_<operator>_<precision>[_<transformer>]`, `host_class` separate), R2 (label-only; the conductor never deletes or re-runs), R3 (provisional designations are labels the producer declares — the conductor **reports** class coverage, it never assigns a class), R7 (`local_*` host classes never count as current; the conductor flags them), R8 (Insight `…/<sampler>/{auto|explicit/<setup_id>}/seed_<n>`). Boundary: the Brain's profiling conductor is the only judge of timing; Pulse/Insight validate and render; the conductor emits plans only and never runs sweeps.

## What (one PyAutoBrain PR; sub-steps lettered)

(a) **`skills/profiling/lifecycle.md`** — the §3.9 sequence as a prompt template: L0 register (taxonomy row, regime, Pulse `planned_cells` with class) → L1 figures (viz plotter `fit.png`, Eyes loop when new) → L2 profile (runtime + breakdown under Optimal/Secondary candidates on reference hosts, parity, → `current`, prior → `superseded`) → L3 designate (Pulse `designation` decision, wiki decision-rule note, library rule-table PR, `runtime_estimates` refresh, workspace/assistant text) → L4 validate (autolens_inference → Pulse `walltime-validation`) → L5 gradient (value_and_grad + FD check → Pulse `gradient`) → L6 samplers (Insight campaign under `auto`, only when the change could alter sampler choice) → L7 close (Pulse task complete, Mind record, Cortex note). Each L-step carries: owning repo(s), the Brain door (`/profiling`, `/eyes`, `/sampler_pipeline`, `/cortex`), the human gate, the witness, and the Mind prompt header it produces (`Epic: <slug>`, integer `Phase:`, `Witness:`, `Blocked-by:`). Re-optimisation enters at L2; a new likelihood at L0. Written so phase 8's `pyauto-brain profiling lifecycle` verb can render it from the taxonomy mechanically — one placeholder set (`<dataset_type>`, `<variant>`, `<instrument>`, `<regime>`, `<trigger>`), no free prose a renderer would have to invent. Linked from `skills/profiling/SKILL.md`, `skills/profiling/profiling.md` and `agents/conductors/profiling/AGENTS.md`. A test renders the template for `imaging/delaunay` (string substitution) and asserts every produced prompt header passes the same header check `pyauto-brain intake census` applies.

(b) **Profiling conductor grid on the mirrored tree + grammar** (`agents/conductors/profiling/_profiling.py`, `_catalogue.py`): feature-detect a `profiling-summary@3` catalogue (`class`/`status` on records, `planned_cells` with `class`); when present, `campaign` reports coverage per likelihood (`<dataset_type>/<variant>`) × class (optimal / secondary / experimental) × measurement with cells `current` / `superseded` / `missing` / `stale` (stale = current record's `release_pin` behind the catalogue's pin), reads `results/<dataset_type>/<variant>/<instrument>/<setup_id>/<host_class>/` when the directory exists, parses `setup_id` by the R1 grammar and flags `local_*` host classes as never-current (R7). When the catalogue is v2 or absent, behaviour is byte-identical to today (legacy `results/runtime/` config buckets). Dispatch plans unchanged in policy (CPU caps, `ral` partition). Fixture under `tests/fixtures/profiling_v3_tree/` laid out per report §3.7 with a minimal @3 catalogue (two likelihoods, optimal + secondary, one superseded, one missing, one `local_laptop` row); tests: new-tree coverage, legacy unchanged on the existing fixture, bad grammar refused with a named error.

(c) **Samplers faculty paths** (`agents/faculties/samplers/_samplers.py`, `AGENTS.md`): the mature tier names `autolens_inference/scripts/<dataset_type>/<variant>/samplers/<sampler>/…` (0C layout; `validation/` leaves are wall-time validation, listed separately, not sampler cells); the path-shape fallback accepts the new shape (keep the old shape for `autofit_inference` and pointer READMEs); "Empty until phase 3" prose replaced by the live reading; tests in `tests/test_samplers_surface.py` on a two-leaf fixture.

(d) **Pulse/Insight read prose** (`skills/profiling/profiling.md`, `agents/conductors/profiling/AGENTS.md`, `skills/sampler_pipeline/{SKILL,reference}.md`, `agents/faculties/samplers/AGENTS.md`): research and check-in lookups read `class: optimal` + `status: current` unless asked otherwise (report §3.8); full-fit wall-time validation is a **Pulse** evidence axis (`walltime-validation@1`, instance `lens-walltime`, producer autolens_inference), never an Insight artefact; Insight sampler campaigns record `setup_mode: auto` with `setup_resolved` as provenance (R8); `optimal` is always a Pulse designation decision, never inferred by a conductor. Where the board or memory faculty prose quotes the Pulse selector order, state the 0A order (Class → Likelihood → Instrument → Hardware class → Measurement).

Checks before PR (Brain AGENTS.md): ruff, `python -m pytest tests -q`, `bin/pyauto-brain profiling campaign` live dry-run unchanged, `bin/pyauto-brain samplers` live.

## Out of scope

The phase-8 `pyauto-brain profiling lifecycle` verb itself (renders this template; separate phase); any autolens_profiling/autolens_inference/Pulse/Insight edit; the conductor's `ingest`/`triage` modes beyond reading the grammar; coverage-matrix *tool* inside autolens_profiling (0B iv — the conductor consumes its catalogue, it does not replace it); designation decisions (phase 3).

## Blocked-by (operational, not a header gate)

PyAutoBrain is claimed by `github-token-p2b-writers-app` (PyAutoBrain#534, worktree `~/Code/PyAutoLabs-wt/github-token-p2b-writers-app`, library-dev, no PR yet as of 2026-10-23) — hard conflict per `worktree_check_conflict`; queued in `planned.md` until that task ships. Also present: unregistered Brain worktrees `board-one-click-update` (#504) and `pyautodna-stack-management`; different files, rebase if they land first.
