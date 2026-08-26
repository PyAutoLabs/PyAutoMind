# Phase 4 Stage 2 compares result rows across two incompatible schema versions

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

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
