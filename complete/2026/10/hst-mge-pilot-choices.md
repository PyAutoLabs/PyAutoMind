# HST/MGE Pulse collection choices prepared

Completed: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/58
PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/59
Merge: e47c0f727a53c9aa40af6e68b647071cca062256

Shipped the Pulse collection-choice document, linked the existing pilot task,
updated its campaign/next step and regenerated the board. Candidate FITS files
match pinned project e4266a13; hashes, primary-header dimensions and plan-only
resource bounds were verified. Only two canonical next fields changed; the
all-campaign check-in, measurement timestamps and snapshots remain unchanged.

Validation: 206 Pulse tests, ruff lint/format and offline board checks passed.
Independent Sol review CLEAN at a4ea984364752e930fccc49d063fab2cbe8a8253,
with basis-cited dispositions for input identity, builder declarations, guarded
plan-only behavior, resource arithmetic, cache/load caveats and preserved state.
Both exact-head workflow runs (lint, Dashboard Refresh) and every job passed.
Human $prm authorized this merge and close-out; branch ancestry verified.

No compute, witness execution, scientific tolerance/data/hardware decision,
baseline/default change, campaign freeze or acceptance. The separately owned
correctness audit autolens_profiling#417/#418 was not edited or merged here.
Data origin/suitability, production host/stack/full settings, load method and
independent witness/tolerances remain explicit choices before collection.
Heart at ship was STALE: release validation incomplete: no rehearsal for current source.

Canonical artifact: https://github.com/PyAutoLabs/PyAutoPulse/blob/e47c0f727a53c9aa40af6e68b647071cca062256/tasks/hst_mge_cpu_pilot_choices.md

## Original prompt

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

## Autonomous ship handoff — 2026-10-13

PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/59
Commit: a4ea984364752e930fccc49d063fab2cbe8a8253.
Added the Pulse collection-choice document and linked the existing pilot task;
only two canonical next fields change. Check-in and measurement clocks unchanged.
Validation: 206 tests, ruff lint/format, offline board validation passed.
Smoke n/a: organ documentation only, no downstream API/script surface.
Independent Sol review CLEAN at this commit: verified pinned FITS bytes/hashes,
headers and model declarations; independently guarded plan-only invocation;
resource arithmetic, cache/load caveats, link resolution and byte-identical board
reproduction. Every load-bearing document claim has a cited basis; the review
surface lifted no commit-message claims. Explicit --repo used because --task
resolved no diff in the custom .worktrees location.
Heart STALE: release validation incomplete: no rehearsal for current source.
Autonomous gate passed; judge tier stops at PR-open for human /prm. No scientific
choice, compute, witness execution, collection approval or defaults changed.
The separate correctness audit #417 remains with its own session (now PR #418).
