Timing-noise audit phase 3 (fix phase 2 of the inventory): dashboard qualification (P6) and drift wording (P7). Issue autolens_profiling#362 stays open for fix phases (3)–(6).

**Shipped:** autolens_profiling#405 (merged 2026-10-08, f6e6982). `scripts/misc/tooling/build_dashboard.py`:
- `qualify` checks in this order:
  1. above the load-average cap → refused;
  2. no provenance;
  3. not a reference host class (`is_reference_host_class`, `REFERENCE_HOST_CLASS_PREFIXES = ("hpc_",)`) → "not a reference host class; laptop rows never qualify as trend points";
  4. no load average;
  5. no host;
  6. off the pinned node.

  Steps 2–6 make the row unqualified with that reason, never refused.
- `_summary_comparison` maps the internal `steady` status to `insufficient` when either endpoint is single-sample. The reason given is "single-sample endpoint(s): within the 2x policy band is not a measured null". It maps `steady` to `flat` ("within the 2x policy band; not a measured null") only when both endpoints carry `single_jit_repeats >= 2`. No producer writes that field yet, so all current points are single-sample. `single_jit_median_s` does not count, and `_point` must carry the field once a producer writes it.
- Unchanged: the status vocabulary and the v1 grammar.
- Wording: the limitations, the badge headline and the page table were reworded.
- Docs: audit note P6/P7 → SOUND-with-caveats (counts 15 / 8 / 8), plus a "Fix phase 2 — shipped" block; the wiki campaign page and index row; `dashboard/README.md`; a full dashboard re-render.

**Witness:** 11 new deterministic synthetic tests:
- laptop with provenance, provenance with no load average, and hpc with no host → unqualified;
- the refusal and no-provenance rules are kept;
- the RAL reference rows stay qualified;
- a qualified 1.9× comparison → `insufficient`;
- `flat` only when both endpoints have repeats;
- drifted / improved keep their status, with the caveat;
- the vocabulary is pinned;
- every qualified record in the real tree is an hpc row on `euclid-ral-gpu-2` with a load average.

Full `scripts/misc/test` suite: 1169 passed, 6 skipped. Effect on `dashboard/summary.json`:
- 159 records; 2 qualified before and after (`point_source_source/source_plane_solved` @2026.8.17.1, `hpc_ral_cpu_fp64` and `hpc_a100_fp64`); no record changed;
- comparisons: `flat` 4 → 0, `insufficient` 135 → 139, `improved` 6 with the caveat;
- PyAutoPulse v1 `validate()` returns [].

The independent Opus review was CLEAN, with 5 of 5 claims basis-cited.

**Human decisions 2026-10-08:**
- `drifted` / `improved` keep their status and gain "single-sample endpoint(s)". Not taken: mapping them to `insufficient`.
- Heart YELLOW: the human acknowledged the reason set, 8 manifest-drift reasons plus the missing rehearsal, for this PR only. The run had parked at leg 4 before the acknowledgement.

**Correction recorded:** the live PyAutoPulse registry reads `dashboard/catalogue.json` (profiling-summary@2; registry switched 2026-10-05, PyAutoPulse 3c7bed2). Its producer, `build_catalogue.py`, hard-codes `qualified: False`, so P6's gap never reached Pulse live, and this was not a Pulse contract change. A future v2 qualification must reuse `is_reference_host_class`.

**Remainder:** fix phase (3), INCONCLUSIVE states for the A/B go / lever / NO_LEVER rules (C7, C10, then C1/C3/C4/C5, P2); then fix phases (4)–(6). Pulse task `timing_noise_audit`.

## Original prompt

# Timing-noise audit phase 3: dashboard qualification and drift wording (P6 + P7)

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- measurement-tools
Difficulty: moderate
Autonomy: supervised
Priority: high
Consequence: judge
Status: active
Filed: 2026-10-08
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Depends-on: complete/2026/10/timing-noise-audit-p2-overhead-verdict.md (fix phase 1 of the audit note)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (chat 2026-10-08)

"do the next step" — fix phase (2) of `results/notes/timing_noise_audit_2026_10.md`, launched with
`--auto`; plan approved in chat 2026-10-08.

## What is wrong (audit rows P6 and P7)

- P6 `build_dashboard.qualify`: a laptop `local_cpu_*` row with provenance is qualified; a row with
  provenance but no load average is qualified; an `hpc_*` row with `host: None` passes the host pin.
- P7 `build_dashboard.drift`: the internal `steady` status publishes as `flat`, which reads as a
  measured null, although both endpoints are single samples (P8: one 10-call block mean).

## Scope (fix phase 2 of the audit note)

1. `qualify()` stricter, with explicit reasons (unqualified, not refused): non-reference host class
   (laptop `local_*` rows never qualify as trend points); provenance without a load average; an
   `hpc_*` row with no host. The reference-host-class rule is a small named function/constant a
   future v2 producer can reuse. The above-cap refusal and the no-provenance rule stay.
2. Drift wording: `steady` → `insufficient` with reason "single-sample endpoint(s): within the 2x
   policy band is not a measured null" when either endpoint lacks a repeat summary; `flat` with
   reason "within the 2x policy band; not a measured null" only when both carry one. `drifted` /
   `improved` keep their status (gross-band signals) and gain a "single-sample endpoint(s)" reason
   (human decision 2026-10-08: "Ill go with your recomendation"). Status vocabulary and v1 summary
   grammar unchanged; PyAutoPulse's v1 validator must still pass (read-only).
3. Deterministic synthetic tests in `scripts/misc/test/test_build_dashboard.py`.
4. Audit note (P6/P7, Downstream, counts, "Fix phase 2 — shipped"), `wiki/campaigns/measurement_tools.md`
   and `wiki/index.md`. Record the correction: the live Pulse registry reads
   `dashboard/catalogue.json` (profiling-summary@2), whose producer hard-codes `qualified: False`;
   this is not a Pulse contract change.
5. Full dashboard re-render from a clean worktree.

## Witness

`pytest scripts/misc/test/test_build_dashboard.py`, `build_dashboard.py --check`, Pulse v1
validator on the regenerated `dashboard/summary.json`, `list_timing_assertions.py --check`, ruff,
before/after `summary.json` diff (expected: qualified records unchanged at 2; the 4 laptop `flat`
comparisons → `insufficient`).
