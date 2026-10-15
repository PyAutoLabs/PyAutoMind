- summary: B5b-2 of search-extensibility closes scored wave 2. All 20 tasks of RAL 409930 (980 probe-first remainder runs; wall 1:30) pulled with the per-directory tar pattern and judged under `gaussian_x3@2` at the PyAutoFit pin df6d218f1: 12,750 wave-2 rows admitted, 0 refused, 0 missing, 0 operational kills (11,580 rows + 1,170 failed attempts + 250 deferred of 13,000 expected). The four probe-sourced legs closed: NSS blend 158/250 and NSS separated 210/250 rank first for evidence, Zeus JAX separated 190/250 ranks first for posterior, Zeus JAX blend 0/250 is unreliable. The reliability floor (success ≥ 50 % over ≥ 20 attempts; others listed as unreliable with their numbers; every card shows attempts and success rate) is applied and recorded in protocol §8 as a post-hoc presentation convention (2026-10-15) plus note N1; pre-registered verdict rules untouched. Wave-2 records reach PyAutoInsight under `inference-summary@3`: 101 per-protocol-per-leg shards under `dashboard/records/` (largest 1.56 MB, 66 MB total, sha256-indexed so a refresh re-fetches only changed shards); registry `fit` bumped with `migrating_from: inference-summary@1`. Cortex run line 409930 moved into the log with wall. PRs autofit_inference#13 (bea1d8746, `decision-taken`) → PyAutoInsight#31 (d993285c5, `decision-taken`) → PyAutoCortex#68 (27a08fd75), merged 2026-10-15 by human /prm under the recorded Heart RED development override.
- decisions: contract is `@3`, not the ruled `@2` — Insight's `@2` already exists as the setups/prepared-problems contract with `lens` pinned to it (human sign-off on the wording outstanding); shards per protocol and per leg; `migrating_from` keeps the committed `@1` snapshot valid offline until the first `@3` capture; floor is a §8 note + N1, not a protocol version; zero-success closed legs count as unreliable.
- follow-up: post-merge the human lets Insight's Dashboard Refresh capture `fit` under `@3`, runs `pyauto-insight check` online and drops `migrating_from` from `registry.yaml` (B5b-2 could not do this before merge); one round-2 nit left (a "reliable" leg with no wall estimate would fall to the unjudged rows; cannot occur with today's data). B5c (`draft/research/autofit_inference/search_ext_b5c_second_model_family.md`) is now unblocked; cortex-project-readability (planned.md) is unblocked on PyAutoCortex.

### Compute

- compute: RAL 409930_[0-19]%20 `--partition=ral` — all 20 tasks COMPLETED 2026-10-15 16:08–17:38 UTC; every task pulled (results/ only; 980 rows + 20 byte-identical probe rows); `output/` and SLURM logs remain on RAL; nothing running for this epic phase

## Original prompt

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
Issued: 2026-10-15

Authority: `complete/2026/10/search-ext-b5b-score.md` (its "Compute (for B5b-2)" block and decisions); autofit_inference#10 Shipped comment and the size-options comment; protocol `wiki/project/protocol_gaussian_x3.md` §7–§11; `PyAutoMind/policy/hpc_ral.md` (CPU arrays `--partition=ral` only; private pin under `/mnt/ral/jnightin/autofit_inference/.pyauto_pin/`, never the shared mirror; never touch another campaign's jobs).

## Request

B5b (search-ext-b5b-score, merged 2026-10-15) pulled and judged the 11,750 scored wave-2 runs but left three things open, which this task closes:

1. **Remainder.** RAL job `409930_[0-19]%20` (`submit_wave2_remainder`, `--partition=ral`, excluding `euclid-ral-compute-[1-4]`, no gres, pin guards) runs the 980 probe-first runs with timeouts NSS 600 s / Zeus 1168 s from `results/calibration/gaussian_x3_wave2_probe.json`. Pull its rows (login-node rsync is ~0.16 files/s — use the per-directory tar pattern from B5b, not plain rsync), judge under `@2`, close the probe-sourced legs, extend the `gaussian_x3@2` catalogue section. `output/` stays on RAL unless the laptop disk allows a selective pull (4 GB free at filing). `cortex done` on the run line.
2. **Summary records.** The full wave-2 `inference-summary@1` export (`--wave2-records --output <path>`) is ~84 MB (63 MB compact), above GitHub's 50 MB warning and copied by every Insight refresh, so B5b committed only the 223 pilot records with the wave-2 accounting marked `records: withheld`. The human rules the schema on #10; implement it (Insight contract bump if `@2`), publish the records, refresh the `fit` snapshot from `main`, and make `pyauto-insight check` green online.
3. **Ordering.** The catalogue's ordering is its own sort key (expected wall per right answer, then success rate; overlapping bootstrap intervals tied `=n`; only legs with ≥1 right answer get a position). Decide whether §8 should carry it as a rule, or a minimum-success floor, and amend the protocol or record the ruling.

## Rulings (human-delegated to the architect, 2026-10-15; "sort out the left for you")

1. **Summary-records schema → `inference-summary@2`.** Move the Insight `fit` instance to a new contract version whose record set is split per protocol (`records_by_protocol/<protocol_id>.json` or an equivalent per-leg layout) so no single committed file approaches 50 MB and an Insight refresh copies only what changed; `@1` stays valid for the other instances. Bump the Insight contract docs/tests, keep the pilot `@1` records readable, and make `pyauto-insight check` green online.
2. **Catalogue ordering.** Keep expected wall per right answer as the primary key (it already prices failures), but (a) show the success rate and the attempt count on every card, (b) rank only legs whose success rate is ≥ 50 % with ≥ 20 attempts and list the rest below the ranked block as "unreliable" with their numbers, and (c) record this in protocol §8 explicitly as a **post-hoc presentation convention adopted 2026-10-15 after seeing wave-2 data**, never as a pre-registered criterion. The pre-registered §8 verdict rules are untouched.

Carried, untouched: pilot `@1` rows are not re-judged (B5b ruling 1, `_protocol.PILOT_NOT_REJUDGED`); LBFGS on blend numpy still +inf at the pin; B5c (`search_ext_b5c_second_model_family.md`) is blocked by this task.
