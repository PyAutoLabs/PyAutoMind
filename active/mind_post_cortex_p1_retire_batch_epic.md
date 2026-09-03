# Retire the `two-slot-batching` epic — keep three pieces as standalone prompts

Type: maintenance
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- mind-workflow
Difficulty: small
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Witness: `python3 scripts/lifecycle.py check` clean; `epics.md` has no `two-slot-batching` entry and its ledger sits under `complete/archive/epics/`; `grep -rl "Epic: two-slot-batching" draft/ active/` returns nothing; `active.md` no longer lists silence-colab-cli-message, autofit-prodigy-49, resampling-info-summary-section, numba-vs-jax-sparse or memory-queue-filing-gate and each has a `complete/2026/09/` record; the dashboard regenerates without those rows
Review-minutes: 15
Unattended: ready
Epic: mind-post-cortex
Phase: 1
Filed: 2026-09-03
Issued: 2026-09-03

Phase 1 of `mind-post-cortex` (ledger `draft/maintenance/pyautomind/mind_post_cortex_epic.md`).
Everything here is ledger material (`draft/`, `active/`, `complete/`, root
registries, dashboard) so the push auto-merges via `mind_ledger_merge.yml` —
confirm with `python3 scripts/ledger_merge.py classify --base origin/main`
before pushing; if anything classifies as code, split it out.

## Why

The epic (`epics.md` entry `two-slot-batching`, ledger
`draft/feature/pyautomind/two_slot_batching_epic.md`) was born to solve "the
human waits on chats and review never blocks". Only two dev slots ever ran
(`batches/2026-08-31-am.md`, `-pm.md`); in the pm slot all nine dev members
were merged one at a time through `/prm` with `decision: UNREVIEWED` in
`batches/reviews/2026-08-31-pm.md`. Everything load-bearing it built has
shipped as standalone infrastructure with its own owners (`_sizing.py` for the
review-cost model, `AUTONOMY.md` for the gate doctrine, `_status.py` for the
status box, `_batch.py plan/collect` driven by the Cortex). The unbuilt phases
are either declared dead in the ledger's own words or Cortex-shaped.

## Do

1. **Retire the epic.** Set the `epics.md` entry `status:` to begin
   `COMPLETE — retired 2026-09-03 (assessment: only two dev slots ever ran; shipped
   pieces live as standalone infra)` and run the same retirement
   `lifecycle.py epics --retire` performs (ledger → `complete/archive/epics/`,
   entry text appended there, entry deleted). Do it by hand if the subcommand
   needs `main`; the result must match what the workflow would produce.
2. **Recast three drafts as standalone prompts** — strip `Epic:`/`Phase:`/
   `Parent:` headers, rewrite the opening paragraph so it no longer says "phase
   N of the batch epic", keep the `Witness:`:
   - `draft/feature/pyautomind/witness_campaign.md` — Priority stays high;
     reframe as "make every backlog prompt reviewable: a `Witness:` line on
     each draft", value independent of batching.
   - `draft/feature/pyautobrain/batch_notify_tier_merge.md` (the tier-A
     auto-merge shadow) — add the two measured facts: the shadow table
     (`autonomy_log.md` rows 255-282) holds 2 of the 40 candidates its own
     pre-registered rule requires and nothing has fed it since 2026-08-31.
     Re-anchor the row-append to `/prm` close-out (the human act that
     actually happens) instead of a batch slot, and extend the window past
     2026-09-27 per the rule's own "extend, do not lower the bar". The
     prompt's deliverable becomes: the `/prm` skill appends the shadow row;
     the window re-opens from the first appended row.
   - `draft/feature/pyautobrain/batch_slice.md` — recast as an ordinary
     decomposition tool for `Unattended: needs-slicing` prompts, invoked from
     `/intake` or standalone; drop the batch framing.
   - `draft/feature/pyautobrain/batch_no_park_at_ship.md` — recast as an
     `--auto` rule ("supervised under `--auto` decide-and-flags at ship
     sign-off instead of parking"), not a batch rule. Remove its `queue.md`
     entry's batch framing (keep the entry; it is still wanted).
   - `draft/feature/pyautobrain/the_batch_conductor_s_plan_kind_cortex.md` —
     detach from the epic (headers), otherwise unchanged: it is a Brain
     feature serving the Cortex and stays in the Mind backlog.
3. **Retire to `complete/archive/shelved/`** with a one-line reason at the top
   of each: `draft/feature/pyautobrain/batch_dispatch.md` (ledger says "dead —
   do not resurrect"), `draft/feature/pyautomind/batch_budget_loop.md` (human:
   "I'm very in the loop"; usage-window fields were n/a in both runs),
   `draft/feature/pyautomind/bundle_nightly_claude_pass.md` (parked since
   2026-08-27, never driven), and the **dev half** of
   `draft/feature/pyautomind/batch_carry_forward.md` — the Cortex half shipped
   (`_batch.py carried_members`), so either shelve the file or cut it down to
   what the Cortex still needs; remove its `queue.md` entry if shelved.
4. **Reconcile `active.md`.** These rows are merged/closed on GitHub
   (verified 2026-09-03) but still in flight in the ledger: PyAutoNerves#157
   merged 2026-09-01, PyAutoFit#1555 merged, PyAutoFit#1554 merged,
   PyAutoMemory#76 merged, PyAutoArray#513 closed (research verdict). Write a
   `complete/2026/09/` record for each via `scripts/lifecycle.py record`
   (bare prompt filename — see `complete/AGENTS.md`), which moves the
   `active/` prompt and drops the row. Note the batch member name in each
   record's `batch:` key so the 2026-08-31-pm record's `members` still
   resolve.
5. `pyauto-brain intake --apply dashboard`, `lifecycle.py check`, push.

Do not touch `scripts/`, `REFERENCE.md`, `docs/` or Brain code in this phase.
