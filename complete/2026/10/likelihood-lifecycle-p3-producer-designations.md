Likelihood lifecycle phase 3, day-zero write 1/4: autolens_profiling classes its records from the PyAutoPulse designations.

- Merged: https://github.com/PyAutoLabs/autolens_profiling/pull/498 (`8c40e7d`, 2026-10-31, human /prm; CI lint green on head `3b32642`). Issue https://github.com/PyAutoLabs/autolens_profiling/issues/497 closed. Heart RED development override invoked by the human 2026-10-31 ("Override + create issue").
- Human rulings 2026-10-31 (AskUserQuestion): setups measured on a designated key but not named by its designation → `experimental`; `local_*` hosts and `source_pixels_<n>` regimes inherit the role as `secondary` with an `undesignated_regime_or_host` limitation and no `decision_id`; a synced JSON mirror (`catalogue/pulse_designations.json`) rather than reading PyAutoPulse directly.
- Mirror: `build_catalogue.py --sync-designations ../PyAutoPulse` writes the 39 `kind: designation` rows; `--check --validate-with ../PyAutoPulse` fails on drift and resolves every `decision_id` via `pulse.ingest.unresolved_decisions`.
- Result (`dashboard/catalogue.json`, 1,548 records): 536 `class: optimal` (283 current) across all 39 decision_ids; 368 named secondary with a decision_id; 199 experimental; 445 secondary without one (inherited, or the held group). Every designation has a current optimal record; all 230 evidence ids present.
- Hold: datacube/delaunay `hpc_a100` stays provisional (24 records, `secondary` + `provisional_optimal: true`) via `catalogue/designation_holds.json`, which also keeps the planning metadata from the retired file (GPU hosts, regime-only routes, the R1(a) dense-NUFFT-at-sma rule).
- `catalogue/provisional_designations.json` deleted; planned cells derive from designations + hold: 272 → 232 (148 optimal, 84 secondary), all current. Frozen phase-2 campaign tests now assert each manifest ⊇ the designated cells, every extra being a setup its designation dropped.
- Next: day-zero write 2/4 — `day_zero` stamp on the frozen rows and the Pulse `day_zero` snapshot.

## Original prompt

# Likelihood lifecycle phase 3, day-zero write 1/4: autolens_profiling reads the Pulse designations

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/497
Consequence: judge
Witness: build_catalogue --check --validate-with ../PyAutoPulse passes, and every decision_id in dashboard/catalogue.json resolves in PyAutoPulse decisions.yaml (pyauto-pulse ingest/check); every record whose key and setup a designation names is class optimal or named secondary with that decision_id; catalogue/provisional_designations.json is gone; datacube/delaunay hpc_a100 stays provisional (secondary + provisional_optimal: true)
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 3
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-31

## Request (human, 2026-10-31, verbatim)

"autolens_profiling producer side: build_catalogue reads the Pulse designations, sets class: optimal + decision_id on every cited row (and secondary where named), and retires catalogue/provisional_designations.json in favour of the records. CI's build_catalogue --check --validate-with ../PyAutoPulse and pyauto-pulse check must resolve every decision_id. Keep the datacube A100 cell provisional."

## Human rulings (AskUserQuestion, 2026-10-31)

- Heart RED: "Override + create issue" (development only; merge via /prm).
- Setups measured on a designated key but not named by its designation: `experimental` (no decision_id).
- Records no designation covers (local_gpu, local_laptop, source_pixels_* regimes): inherit the role of the reference-host / standard designation as `secondary` with an `undesignated_regime_or_host` limitation and no decision_id.
- Source: a synced JSON mirror `catalogue/pulse_designations.json` generated from PyAutoPulse decisions.yaml; `--validate-with ../PyAutoPulse` fails on drift.

## Plan

1. `build_catalogue.py --sync-designations <PyAutoPulse>` writes `catalogue/pulse_designations.json` (the `kind: designation` rows, sorted); `--check --validate-with` compares it with Pulse.
2. `catalogue_lifecycle.py`: the class rule reads the mirror (hardware class cpu_many_core = hpc_ral_cpu, gpu_a100 = hpc_a100; local_gpu inherits gpu_a100, local_laptop cpu_many_core); `record_class` returns (class, decision_id, limitations); `planned_setups` derives from the designations plus the hold.
3. `catalogue/designation_holds.json`: the datacube/delaunay hpc_a100 hold (provisional optimal/secondary, citing the 2026-10-31 decision) and the planning metadata kept from the retired file (gpu_hosts, instrument_scoped_setups).
4. Delete `catalogue/provisional_designations.json`; coverage_matrix.py, tests, READMEs, V3 limitations and phase-2 campaign comments repointed; regenerate catalogue, coverage, README.
