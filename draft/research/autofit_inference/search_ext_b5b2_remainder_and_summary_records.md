# `@autofit_inference` B5b-2: pull and judge the wave-2 remainder, settle the summary-records schema, refresh the Insight snapshot

Type: research
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: B5b-2
Witness: every row of RAL job 409930 (980 probe-first remainder runs, Zeus JAX + NSS 50-step) is pulled and judged under `gaussian_x3@2` at the PyAutoFit pin df6d218f1, and the probe-sourced legs leave `open` and take a catalogue position (or a recorded `failed` verdict) once all 250 of their runs have rows; the wave-2 records reach PyAutoInsight under the schema the human chose on autofit_inference#10 (recommended: move the `fit` instance to `inference-summary@2`; alternatives: per-leg `@1` records, or the 84 MB file via LFS), `pyauto-insight check` passes online and the `fit` snapshot is refreshed from `main`; the catalogue-ordering question (sort key by expected wall per right answer vs a §8 protocol rule — DynestyStatic at 14 % success currently leads the blend evidence task) is ruled and the protocol amended or the ruling recorded in `state.md`; Cortex run line for 409930 moved into the log with walls.
Review-minutes: 30
Unattended: needs-slicing
Filed: 2026-10-15

Authority: `complete/2026/10/search-ext-b5b-score.md` (its "Compute (for B5b-2)" block and decisions); autofit_inference#10 Shipped comment and the size-options comment; protocol `wiki/project/protocol_gaussian_x3.md` §7–§11; `PyAutoMind/policy/hpc_ral.md` (CPU arrays `--partition=ral` only; private pin under `/mnt/ral/jnightin/autofit_inference/.pyauto_pin/`, never the shared mirror; never touch another campaign's jobs).

## Request

B5b (search-ext-b5b-score, merged 2026-10-15) pulled and judged the 11,750 scored wave-2 runs but left three things open, which this task closes:

1. **Remainder.** RAL job `409930_[0-19]%20` (`submit_wave2_remainder`, `--partition=ral`, excluding `euclid-ral-compute-[1-4]`, no gres, pin guards) runs the 980 probe-first runs with timeouts NSS 600 s / Zeus 1168 s from `results/calibration/gaussian_x3_wave2_probe.json`. Pull its rows (login-node rsync is ~0.16 files/s — use the per-directory tar pattern from B5b, not plain rsync), judge under `@2`, close the probe-sourced legs, extend the `gaussian_x3@2` catalogue section. `output/` stays on RAL unless the laptop disk allows a selective pull (4 GB free at filing). `cortex done` on the run line.
2. **Summary records.** The full wave-2 `inference-summary@1` export (`--wave2-records --output <path>`) is ~84 MB (63 MB compact), above GitHub's 50 MB warning and copied by every Insight refresh, so B5b committed only the 223 pilot records with the wave-2 accounting marked `records: withheld`. The human rules the schema on #10; implement it (Insight contract bump if `@2`), publish the records, refresh the `fit` snapshot from `main`, and make `pyauto-insight check` green online.
3. **Ordering.** The catalogue's ordering is its own sort key (expected wall per right answer, then success rate; overlapping bootstrap intervals tied `=n`; only legs with ≥1 right answer get a position). Decide whether §8 should carry it as a rule, or a minimum-success floor, and amend the protocol or record the ruling.

Carried, untouched: pilot `@1` rows are not re-judged (B5b ruling 1, `_protocol.PILOT_NOT_REJUDGED`); LBFGS on blend numpy still +inf at the pin; B5c (`search_ext_b5c_second_model_family.md`) is blocked by this task.
