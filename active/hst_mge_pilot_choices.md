# HST/MGE pilot: prepare Pulse collection choices

Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/58
Type: docs
Target: @PyAutoPulse
Difficulty: small
Autonomy: safe
Consequence: judge

## Original request

> ok, keep doing this whole task in --auto

Scope clarification, verbatim:

> Keep #417 with its current session; prepare Pulse choices here

## Scope and plan

Prepare a Pulse decision document for the existing HST/MGE CPU pilot, retaining
all unapproved choices as proposals. Do not touch the concurrently claimed
project correctness audit autolens_profiling#417 or run its witness.

1. Record the hashes, FITS header shapes and committed-byte identity of the
   existing dataset/imaging/hst candidate, and the project driver's plan-only
   result. A local candidate is not an approved production dataset or known origin.
2. Present hardware, software lock, full resolved settings, background-load
   method, window and resource decisions, with verified/proposed/unknown labels.
   Link independent correctness choices to #417, without prescribing tolerances.
3. Add tasks/hst_mge_cpu_pilot_choices.md as a supporting decision document linked
   from the existing pilot task; update its ledger next step and the campaign.
   No duplicate task/campaign; keep last_checkin and measurement clocks unchanged.
4. Regenerate/check the board, run Pulse tests and ruff, obtain independent review
   and Heart readiness, and open a PR under the autonomous ship gate.

Tier: judge — merge mode: human /prm.

No profiling or witness execution, hardware allocation, freeze, acceptance,
baseline/default changes or new experiment direction. No project code edits.
Full profiling operating instructions are retained in the preceding completion
record complete/2026/10/pulse-checkin-2026-10-13-evening.md.
