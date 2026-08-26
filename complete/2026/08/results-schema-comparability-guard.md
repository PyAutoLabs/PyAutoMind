Result rows are no longer compared across incompatible eval counters.

`performance.likelihood_evals` changed MEANING between results-schema v1 and v2
for `MultiStart*` searches: v1 recorded `samples.total_samples` (a
posterior-storage count), v2 records the reject-inclusive
`total_steps * n_starts`. One cell directory,
`results/searches/multi_start_prodigy_autoconv/imaging/mge/hst`, held both arms
of the same Prodigy n256 configuration with differing `config_name`, so nothing
deduped them: positions-OFF read 257 evals / 874.58 ms-per-eval, positions-ON
read 247,808 / 2.23 ms. `aggregate.py`'s comparison.json + shared log-scale
chart and `build_readme.py`'s searches table rendered them side by side,
implying a ~390x per-eval speedup that was pure counter semantics. Found while
interpreting the 2026-08-25 A100 harvest for #160.

**Shipped as a BASIS-keyed guard, not the literal one the prompt asked for.**
The prompt specified refusing rows whose `schema_version` differs. The break is
MultiStart-ONLY — a nested sampler's `total_samples` was already
reject-inclusive in v1, so `nautilus/imaging/pixelization/hst` holds a
legitimate v1 row at 58,464 evals beside a v2 row at 55,984. The literal guard
would have rejected that valid pair, and a guard that cries wolf gets switched
off. `eval_counter_basis` derives the basis from `(schema_version, sampler
family)` with a missing key read as v1. The control — Nautilus v1+v2 must NOT
trip — is a pinned test, as is the MultiStart pair that must.

**The bridge that made honest rendering possible:** v1's `likelihood_evals` IS
v2's `stored_samples` (both 257). A v1 MultiStart row therefore has an honest
stored count and NO recoverable evaluation count — `total_steps` was never
written — so its per-eval figure is withheld rather than approximated.

Landed in autolens_profiling PR #180 (merge `87493eb`, feature `bdab231`):
- `searches/_metrics.py` — `eval_counter_basis` / `basis_conflicts` /
  `eval_basis_label`. Also wires up `load_summary`, which had ZERO callers
  since W4/#161 — it was written for exactly this job and never connected.
- `searches/aggregate.py` — loads via `load_summary`; records the basis per
  config in comparison.json; a mixed cell has per-eval withheld outright,
  charts wall only, names every offending file, exits 3.
- `tooling/build_readme.py` — searches table gains a `Basis` column; a
  `stored` row renders em-dash for Evals and Time / eval. Its docstring claimed
  v1 and v2 "render identically" — false for MultiStart rows.
- `test/test_searches_schema_guard.py` — new, 19 tests.

**Prerequisite defect fixed in the same PR (not in the approved plan).**
`_discover_cells` recognised a cell only if it held one of six exact
`_CONFIG_ORDER` filenames. Real sweep arms are named
`hpc_hpc_a100_fp64_n256_seed0.json`, so EVERY MultiStart cell — including the
one this guard exists for — was invisible to an auto-discovered `aggregate.py`
run and reachable only via an explicit `--cell`. Aggregation already read those
files; only discovery disagreed. Discovery now uses the same `sampler`-key
predicate `build_readme._scan_search_artifacts` applies. Locally: 3 cells -> 21.

VERIFIED: 187 tests pass (19 new); ruff check + format clean; build_readme
`--check` idempotent; CI green on bdab231 (one `lint [pull_request]` run, one
job, 25/25 steps — `lint.yml` push trigger is main-only and the job has no
matrix, so that IS the complete run set for the sha). Control on real harvest
data: fires on the prodigy_autoconv cell (exit 3), does not fire on the
nautilus pixelization cell (exit 0).

SHIP CONDITIONS: merged on explicit human authorization over a Heart **RED**
board (`prm merge on red`). The five RED reasons were pre-existing and none
touched autolens_profiling; quoted verbatim in the PR body. `/prm` did not
re-judge the gate — it cannot — the human authorized the ship past it and
`/ship_workspace` executed.

PARALLEL CLAIM: ran in its own worktree while #175/#176 held autolens_profiling,
human-approved on disjoint files. Separate checkout = separate git index, so
none of the shared-index commit discipline applied.

OPEN: the guard fires on PR #174's harvest data by design. #174 is still
unmerged and now needs its comparison.json files regenerated against the guard
before it lands.

## Original prompt

# Phase 4 Stage 2 compares result rows across two incompatible schema versions

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: issued
Issued: 2026-08-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/177

The Prodigy n256 positions-off and positions-on arms are not measured on the
same eval counter, so their wall and throughput numbers cannot be compared.

The positions-OFF arms are schema v1: no `schema_version` key, and
`likelihood_evals=257`. The positions-ON arms are schema v2 (reject-inclusive
evals), reporting 32,000-247,808. `max_log_likelihood` remains comparable
between them; `performance.likelihood_evals`, `time_per_eval_ms` and anything
derived from them do not.

Found while interpreting the 2026-08-25 A100 harvest for
autolens_profiling#160 — the positions-off baseline comes from the earlier
CP-3 wave, the positions-on arms from the Phase 4 Stage 2 wave, and nothing in
either artifact flags the mismatch.

FIX: either re-run the positions-off baseline under schema v2, or add a guard
to the scoring/aggregation that refuses to compare rows whose
`schema_version` differs (and treats a missing key as v1). Prefer the guard —
it protects every future cross-wave comparison, not just this one.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p4.md -->
