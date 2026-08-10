# Compile-axis phase 2 — warm compile made identifiable, pinned, dashboarded

- shipped: 2026-08-10
- issues: https://github.com/PyAutoLabs/autolens_profiling/issues/103
- prs: autolens_profiling#104 (squash 355d555) · PyAutoBrain#220 (squash 74d7b1b)
- repos: autolens_profiling, PyAutoBrain
- arc: phase 2 of 3

## Summary

Tracking **warm** compile is the point of the arc — the persistent cache turned
117.0s into 2.3s (CPU MGE `vag`) and 5517.8s into 937.1s (A100 end-to-end), and
nothing watched for that reverting. Both wins are *settings*.

`cache_state` is now derived from what the compile DID (cache entries counted
either side of `lowered.compile()`), 25 warm pins are committed, the dashboard
renders through the existing sentinel-block mechanism, and
`ingest --axis compile` reports drift.

## Traps and findings

- **`cache_dir` is non-empty on COLD rows too** — the cold run is the one that
  populates the cache. Any truthiness check on it, or substring match on the tag,
  gets warmness exactly backwards. The corpus carries ~40 ad-hoc tag spellings.
- **`hardware` alone pools different machines.** It is only ever `local_cpu` /
  `local_gpu_<dev>`, so one `local_cpu` label spanned a laptop (66 records) and a
  32-core RAL node (12). The first rendered dashboard put pins from both side by
  side under one heading — the 7x host-load hazard, live. `hostname` joined the
  comparability key.
- **Pins must be STICKY.** "Most recent warm row wins" meant re-deriving pins after
  a cache regression would move the pin *onto* the regressed value and report
  all-clear forever — exactly inverted from the purpose. `--repin` is now required.
- **Rows predating a pin are not drift.** The first `ingest` run flagged four, all
  measurements the pin had been *chosen over*.
- Backfill used **end-anchored** tag matching: `mb_homo_cold_laxmap_gpu` contains
  "cold" mid-tag and is left `unknown` rather than mislabelled.
- `scripts/misc/test/` **ran in no workflow at all**; a pytest step was added to
  `lint.yml` (47 tests, ~2s). Its apparent failure outside CI was a missing
  `matplotlib` (imported at module scope by `aggregate.py`), not a defect.

## Original prompt

# Profiling Agent phase 2 — make warm compile machine-identifiable, pinnable, and dashboarded

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

> Depends on phase 1, `draft/feature/profiling/compile_axis_campaign_coverage.md`
> (its cell-resolution logic). Not declared as `Blocked-by:` yet because that key
> grades **issue** refs and phase 1 has no issue — add the real ref at
> `/start_dev` time, once phase 1 is issued.

Phase 2 of `profiling_agent_jax_compile_time_scope.md`. **Absorbs**
`draft/feature/autolens_profiling/jax_compile_time_profiling.md`, whose surviving
scope (2026-07-28 re-scope: "the recurring cell-grid compile **dashboard** — track
warm compile per cell so cache regressions are caught") is this prompt's workspace
leg.

## The blocker this prompt exists to remove

The whole arc's purpose is to catch the persistent-compilation-cache win
(117.0 s → 2.3 s CPU; 5517.8 s → 937.1 s A100 end-to-end) silently reverting.
That requires tracking **warm** compile per cell.

**Warm rows are not machine-identifiable today.** Warmness is encoded only in a
free-text `tag`. Across the 93 committed records there are ~40 distinct ad-hoc
values: `census-warm`, `census-warm2`, `cache-warm`, `a100-census-warm`,
`prodigy-census-warm`, `prodigy-census-warm-retry`, `prodigy-census-ral32-warm`,
`mb_homo_warm`, `mb_hetero_warm`, against colds spelled a dozen other ways, plus
`idle-check`, `smoke`, `matrix`, `pix-first`, `a100-at0`, `flag-parallel-codegen`.
No parser should be asked to guess at that, and a substring match on `"warm"`
would be a trap: `cache_dir` is non-empty on rows tagged `*-cold` too (the cache is
*configured*, and the cold row is the one that populates it).

`cache_dir` is recorded but as a machine-specific path
(`/tmp/jax_cache` vs the RAL path), so it answers "a cache was configured", never
"this row hit it".

## Workspace leg — `autolens_profiling`

1. **Add an explicit `cache_state` field to `probe.py`'s record**: `cold` | `warm` |
   `none` (no cache configured). Derive it from what the probe actually did, not
   from the tag. `--cache-dir` with a pre-existing populated entry for the shape is
   `warm`; a fresh/empty cache dir is `cold`; no `--cache-dir` is `none`.
2. **Add `host_state`** (or equivalent) capturing the idle/loaded provenance the
   README currently carries in prose. This is load-bearing, not bookkeeping: the
   first measurements were wrong by **7×** (851 s vs 117 s for the same compile)
   purely from host load, and `prodigy-census-ral32-*` rows sit in the same tree at
   a different core count. Record at least core count and load average; leave `tag`
   as the free-text human note it already is.
3. **Backfill** the existing 93 records where the mapping is unambiguous from tag +
   README provenance, and leave the rest `unknown` rather than guessing. Fix or
   delete the **4 malformed records** (`hardware`/`dataset_class`/`instrument` all
   `null`) as a deliberate call.
4. **Pin warm compile per cell** — the compile-axis equivalent of the runtime
   results' `pinned_expected`, which is the hook `ingest`/`triage` are already
   built around. A pin is only meaningful within one comparability key
   `(hardware, jax_version, mixed_precision, cache_state)`, so the pin store must be
   keyed on it.
5. **Dashboard rows** through the existing `build_baseline.py` / `build_readme.py`
   pattern, so warm compile per cell appears alongside the runtime tables.

## Brain leg — `PyAutoBrain`

6. **`ingest --axis compile`**: report compile records that are unpinned, and
   records whose warm compile has moved away from its pin — *only ever within one
   comparability key*. Cross-key pairs are not a regression and must not be
   reported as one. Mirror the runtime `ingest`'s freshness discipline (it skips
   probes older than the table file for a documented reason).
7. Emit the same shape as the runtime axis: rows to apply, plus `steps` and
   `next_action`.

## The trap

Do **not** let the dashboard compare a `cold` row against a `warm` pin, or an
A100 row against a CPU pin, or rows across a `jax_version` bump. Cache keys include
jax version and shapes, so a version bump recompiles once **by design** — that is
expected behaviour, not drift, and phase 3 classifies it as such. A tool that flags
it is a tool people learn to ignore.

## Acceptance

- `probe.py` records carry `cache_state` derived from probe behaviour; a fresh
  cold/warm pair on one cell produces exactly one `cold` and one `warm` record with
  no tag parsing anywhere in the pipeline.
- Warm compile per cell is pinned and rendered in the workspace dashboard.
- `pyauto-brain profiling ingest --axis compile` reports unpinned and drifted rows,
  and **never** pairs rows across `(hardware, jax_version, mixed_precision,
  cache_state)`.
- A synthetic warm row at cold-scale timing is reported as drift; the same row
  under a bumped `jax_version` is not.
- The 4 malformed records are resolved.
- Runtime-axis behaviour unchanged.

<!-- filed 2026-08-10 as phase 2 of the compile-axis arc; absorbs the workspace-side
     jax_compile_time_profiling.md. Tag/cache_state findings measured against the 93
     committed probe records on autolens_profiling main. -->
