# Queued epics drive shifts, and briefs allow RAL by default

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- autonomy
- orchestration
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: autonomous-orchestrators
Filed: 2026-11-19
Issued: 2026-11-19
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/696
Consequence: judge
Review-minutes: 15
Unattended: never
Lane: local-dev
Witness: on the 2026-11-19 Mind state, `batch plan --brief` for a brief made by an unedited `batch brief --new` (a) passes `brief --check` with `ral` in `lanes:` and a `ral-allowance:` block, and (b) with queue.md holding only epic ledgers, takes `draft/feature/autofit/results_library_p5c_dr1_census.md` and `draft/research/autolens_inference/numba_wtilde_validation_legs_stall_nautilus.md` as queued members (no "not in queue.md … beyond queue.md" rejection), while still refusing phases that are not next; and the plan names, per queued epic, why nothing of it starts when nothing does.

## Request (human, verbatim, 2026-11-19)

"make sure this RAL issue doesnt ever copy up by defaulty, we also need to make it so we can queue up epics in this way with less friction as this is how I intend to use this for the most part."

## What happened (shift 2026-11-19-pm2, PyAutoMind#591)

The human queued four epic ledgers (likelihood-lifecycle, hpc-campaign, results-library, cti-upkeep) and launched a shift "to do the autopilot queue" with `backlog: scoped` to those epics. Nothing from the epics started:

1. **RAL excluded by default.** `batch brief --new` writes `lanes: any` (`NEW_BRIEF_DEFAULTS`, `agents/conductors/batch/_batch.py`), so every `Lane: ral` member was rejected "lane ral not in the brief's lanes". RAL was available; the human expected it to be used. Fixed for that shift by hand (`lanes: any local-dev ral` + `ral-allowance: packets 2, partition ral, cpu-hours 64`).
2. **Queuing an epic does not queue its phases.** `queue_rank` matches queue entries by path/basename only. The queued ledger itself is `Autonomy: human-required` ("would park at ship"), and its next-phase member prompts count as unqueued, so `scoped_reach_why` (ruling 2026-11-16: beyond queue.md only small single-repo tasks) rejects every medium or multi-repo phase — e.g. `results_library_p5c_dr1_census.md` (phase 5, medium, 2 repos) and `numba_wtilde_validation_legs_stall_nautilus.md` (likelihood-lifecycle phase 4, medium).
3. **Why an epic is idle is not said.** The plan lists hundreds of per-file rejections; the human cannot see at a glance "cti-upkeep: next phase 2 — both members human-required" or "hpc-campaign: 3 phase-5 drafts lack a Witness".

## Want

- **RAL by default.** `brief --new` writes `lanes: any local-dev ral` and a default `ral-allowance:` (packets 2, partition ral, cpu-hours 64), both editable. Update the schema text in Mind `batches/AGENTS.md` and the batch conductor docs that state `lanes: any` as the default.
- **A queued epic queues its phases.** A queue.md entry that resolves to an epic (its `Epic:` header, or the `- ledger:` path in epics.md) makes every member of that epic count as queued at the ledger's rank (`queue_rank`, and the scoped-dip/`scoped_reach_why` exemption). Every other gate stays: phase order (`pool_gate` "phase N is not next"), `Autonomy: human-required`, `Unattended: never`, `Blocked-by:`, Witness, lane, repo holds, budget. The 2026-11-16 ruling is narrowed, not dropped: the human queuing an epic is the human queuing its work.
- **Say why a queued epic is idle.** `batch plan` (text and `--json`), `brief --check` and the shift digest carry one line per queued epic: what it contributes this shift, or why nothing (next phase N; its members and their gate words; or "no draft prompt for phase N — run the epic's Continue prompt in an attended chat to file it").
- Docs: Mind `queue.md` header and Brain `skills/queue` say a queued epic ledger queues its phases.

## Out of scope

- A shift worker that continues an epic from its ledger and files the next phase prompt itself (the ledger is human-required); note it as a follow-up if the idle-epic line shows it is the common case.
- Any change to the phase-order, autonomy or Unattended gates.

## Notes

- PyAutoBrain is a self-organ: a shift never edits it. Merge only after the 2026-11-19-pm2 watcher stops (review-at 22:15Z + 45 min).
