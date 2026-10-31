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
