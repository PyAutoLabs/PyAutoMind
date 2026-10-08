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
