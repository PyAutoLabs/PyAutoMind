Likelihood lifecycle phase 3: the 39 day-zero designations recorded in PyAutoPulse.

- Merged: https://github.com/PyAutoLabs/PyAutoPulse/pull/84 (`bcaf6b86`, 2026-10-31, human merge command). Issue https://github.com/PyAutoLabs/PyAutoPulse/issues/83 closed. Heart RED development override invoked by the human 2026-10-31.
- Human decision 2026-10-31 (AskUserQuestion): "Approve all 39 (Recommended)", and for `datacube/delaunay` gpu_a100 "Hold, keep provisional (Recommended)" (1.03× at sma, within the 9 % tolerance).
- Derivation: re-derived on autolens_profiling `c218a428` (the #496 head) on the pre-registered axis (Q1/Q3 per-node throughput; Q2/Q11 GPU-only on gpu_a100; Q5 interferometer by `standard`; Q10 untested branches named in the rule). Changes from the 2026-10-29 draft: the interferometer/delaunay jvla CPU hold now separates (numba 2.17×), and point_source_source gpu_a100 is `jax_gpu_na_fp64` (Q2). The JAX CPU slowdown flips no group.
- Records: `decisions/<id>.md` ×39 (evidence pinned to c218a428; `basis: projected`) and 39 `kind: designation` rows. The placeholder test `test_the_live_index_holds_no_designation_yet` is replaced by `test_the_live_index_holds_the_day_zero_designations`. `pyauto-pulse check` OK, 370 tests.
- Next (day-zero write, not started): the autolens_profiling producer side (`class: optimal` + `decision_id` on the cited rows, retire `catalogue/provisional_designations.json`), the `day_zero` stamp and Pulse snapshot, the `day_zero.md` rule pages, the `setup-baseline` close, and the `runtime_estimates` export.

## Original prompt

# Likelihood lifecycle phase 3: record the 39 day-zero designations in PyAutoPulse

Type: research
Target: PyAutoPulse
Repos:
- PyAutoPulse
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: 39 decisions/<id>.md records and 39 `kind: designation` decisions.yaml rows, each matching Appendix B of likelihood_lifecycle_p3_designation_proposals.md as approved; pulse.decisions.load() passes; pyauto-pulse check and the Pulse test suite pass
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 3
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-31
Issued: 2026-10-31
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/83

## Request (human, 2026-10-31, verbatim)

"contonue do those steps" — then, via AskUserQuestion: "Approve all 39 (Recommended)" (record the 39 designatable groups as drafted) and "Hold, keep provisional (Recommended)" (datacube/delaunay gpu_a100 does not separate); "Override + create issue" (Heart RED).

## What

Record Appendix B (re-derived 2026-10-31 on autolens_profiling #496 head c218a428) as 39 Pulse designation decisions, date 2026-10-31, decision maker James Nightingale. Each canonical record states the per-instrument evidence (setups, projected calls/s/node, per call, separation vs tolerance, parity), `basis: projected` in prose (Q4 a; η = 1.0 declared, unmeasured until phase 4), the rule, secondaries, untested branches and caveats. The datacube/delaunay gpu_a100 hold is named, not recorded. Records are generated from the catalogue by the reviewed generator, never hand-typed.

Next (separate task, after autolens_profiling #496 merges): the producer side — build_catalogue reads the designations, sets class: optimal + decision_id on the cited rows, retires catalogue/provisional_designations.json.
