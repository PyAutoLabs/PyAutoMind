Likelihood lifecycle phase 3, day-zero write 2/4: the day_zero baseline is stamped and Pulse holds a frozen day_zero snapshot.

- Merged: https://github.com/PyAutoLabs/autolens_profiling/pull/500 (`e4811a2`, 2026-11-01, human /prm; lint green on `0ecee87`) and https://github.com/PyAutoLabs/PyAutoPulse/pull/85 (`60d5a96`, 2026-11-01, human /prm; lint + dashboard refresh green on `fccedc2`). Issue https://github.com/PyAutoLabs/autolens_profiling/issues/499 closed. Heart RED development override invoked by the human 2026-11-01.
- Human rulings 2026-11-01 (AskUserQuestion): stamp the tag only (`2026.10.25.1`); include the held datacube/delaunay A100 group; the Pulse snapshot is the stamped records + planned_cells + a manifest, not a full copy.
- autolens_profiling: `catalogue/day_zero.json` (schema day-zero v1: tag, §3.6 rule, frozen against `8c40e7d` and the Pulse designations `bcaf6b86`). build_catalogue stamps every current record of a cell that is optimal/secondary, standard regime, on a reference host, on the tag, with a parity match and a fit figure; validate_lifecycle refuses a stamp off the rule. 480 records over 116 cells; all 39 designations have a stamped current optimal; 20 held rows included; nothing re-measured.
- PyAutoPulse: `pulse/freeze.py` + `pyauto-pulse freeze --instance K --label day_zero --commit <sha>` (stamped records + planned_cells + manifest; never rewritten); `check` verifies frozen snapshots offline; v3 rule: day_zero only on a current record. `snapshots/day_zero/lens.json` frozen from autolens_profiling `e4811a2`: 480 records, 116 cells, 39 decision_ids resolved.
- Next: day-zero write 3/4 — `wiki/campaigns/<dataset_type>/<variant>/day_zero.md` rule pages.

## Original prompt

# Likelihood lifecycle phase 3, day-zero write 2/4: stamp day_zero and freeze the Pulse day_zero snapshot

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/499
Consequence: judge
Witness: dashboard/catalogue.json carries day_zero "2026.10.25.1" on exactly the 480 current records whose cell meets the §3.6 rule (all 39 designations with a stamped current optimal); build_catalogue --check --validate-with ../PyAutoPulse passes; PyAutoPulse snapshots/day_zero/lens.json holds those 480 records from the merged autolens_profiling commit with a manifest, pyauto-pulse check verifies it and refuses an overwrite
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 3
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-01

## Request (human, 2026-10-31, verbatim)

"2. Stamp day_zero on the frozen rows and take the Pulse day_zero snapshot." — then "yes start task 2 and research it".

## Human rulings (AskUserQuestion, 2026-11-01)

- Heart RED: "Override + create issue" (development only; merge via /prm).
- Stamp value: the tag only, `2026.10.25.1`; the profiling and Pulse commits live in `catalogue/day_zero.json` and the snapshot manifest.
- Scope: include the held datacube/delaunay A100 group — 480 records (283 optimal, 177 named secondary, 20 held provisional) over 116 cells. Size variants and experimental rows stay unstamped.
- Snapshot: the stamped records + planned_cells + a manifest (source commit, tag, sha256 of the full catalogue at that commit), not a full copy.

## Rule (report §3.6, as implemented)

A current record is stamped when it is class optimal or secondary, regime standard, on a reference host (hpc_ral_cpu / hpc_a100), its release_pin is the day-zero tag, and its cell has a current parity record with status match and a fit figure. A cell is stamped whole (runtime, breakdown, compile, memory_host, parity).

## Plan

1. autolens_profiling: `catalogue/day_zero.json` (tag, rule, frozen-against commits); build_catalogue stamps passing cells; validate_lifecycle refuses a stamp off the rule; regenerate; limitations text. PR, human /prm.
2. PyAutoPulse (after 1 merges): `pyauto-pulse freeze --instance lens --label day_zero` writes `snapshots/day_zero/lens.json` (+ manifest) from the merged commit, refusing to overwrite; `check` verifies it (validation, every record carries the tag, decision_ids resolve, manifest digest); additive validator rule: day_zero non-null ⇒ current. PR, human /prm.
