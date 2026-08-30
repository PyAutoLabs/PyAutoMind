# Batch phase 0b — intake writes the grades, and the autonomy experiment

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: high
Status: shipped 2026-08-30 — PyAutoBrain branch claude/autonomous-task-batching-k8lw9t
Epic: two-slot-batching
Phase: 0
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30
Blocked-by: phase 0a (the faculty must emit the grades before intake can write them)
Witness: the before/after `Autonomy:` distribution over all 137 draft prompts, computed as a DRY RUN and pinned in the PR body — no prompt file is written in this phase.

Depends on 0a. Read the epic for the reasoning; this is the conductor side.

## 1. Intake writes the new headers

`agents/conductors/intake/_intake.py` gains `Consequence:`, `Witness:`,
`Review-minutes:` and `Unattended:` in `parse_header`'s key set and in
`_render_header`, sourced from the faculty. Add the first three to the
`HEADER_FIELDS` hygiene set so a prompt missing them renders in the dashboard's
Hygiene section; leave `Unattended:` out of hygiene, as it is derived and always
available.

Document all four in `PyAutoMind/REFERENCE.md`'s "Prompt file format" beside
`Difficulty:`/`Autonomy:`, and state the `Witness:` default explicitly: **no
witness declared means tier `judge`.**

## 2. Fix `infer_autonomy`

`_intake.py:276` returns `supervised` whenever `repo_count > 1`. Nearly every
real task names a library plus its workspace, which is why 120 of 137 prompts
are `supervised`. Repo count is blast radius; this field is supposed to encode
judgement required.

Replace the trigger set with `architectural_risk`, `human_judgement`, and
difficulty at `large` and above. Multi-repo stays a `Difficulty:` input, where it
already is (`+2` per repo beyond the first).

## 3. Ship it as a dated experiment, not a graduation

**Do not cite "238 rows, zero rejected".** The epic sets out why it fails:
the log is July human-in-session work with about seven rows for all of August
against 332 completions; `rejected` is structurally unreachable (a withdrawn
five-PR mechanism was logged `reverted`, a human-rejected recommendation
`amended`); two rows say verbatim "NOT a clean row for graduation purposes"; and
every clean row was produced *with this guard on*, by a July review that raised
the work-type caps **because** the guard was conservative.

Write the experiment's terms into `AUTONOMY.md`, dated:

- 20 unattended launches under the new rule.
- The adversarial review leg mandatory for them (phase 3; until it exists, the
  experiment does not start — say so rather than starting anyway).
- Calibration rows written **per work-type**, since the graduation rule is
  per-work-type and the cited figure is an aggregate.
- A new `rejected-at-review` outcome the **human** stamps in the slot, so the
  demotion trigger can fire. An experiment that cannot fail is not evidence.
- An explicit revert condition: if the window is not clean, the change reverts.

## Constraints

- **Write no prompt files in this phase.** The bulk re-grade is 0c. Here the
  distribution is computed as a dry run and reported, so the change to the rule
  is reviewable on its numbers before it touches 137 files.
- Never overwrite a human-declared value; report disagreement.

## Done when

- The dry-run before/after distribution is in the PR body.
- `AUTONOMY.md` carries the experiment, dated, with its revert condition.
- Existing intake and dashboard tests pass, with new cases for the header
  round-trip and the changed rule.
