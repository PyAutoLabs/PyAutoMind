# Witness campaign — make the backlog reviewable by construction

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Review-minutes: 15
Unattended: ready
Epic: two-slot-batching
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-31

The single highest-leverage item in the batch design, promoted from a fill
remark to owned work (epic, independent review amendment 2). Today 151 of 153
backlog prompts grade `judge` because they carry no `Witness:`; the epic's dry
run showed a witnessed backlog grades 33/104/16 — the whole distance between
two-member batches and real ones. The 2026-08-31 review session measured the
same thing from the other side: the members that reviewed in minutes were the
ones with pre-registered witnesses.

## The work

Sweep the `Unattended: ready` prompts in `draft/`, adding a `Witness:` line —
a machine-checkable claim whose truth makes the task reviewable in minutes
("ids bit-identical", "31-rule byte-equality", "smoke suite green with the new
default", "Δlog-evidence < 5") — in batches of ~15 prompts per pass, proposed
to the human for approval before any header is written.

**The no-invention rule stands and is the whole point: witnesses are
human-declared.** A pass proposes candidate witnesses where the prompt's own
text implies one; the human accepts, edits, or strikes each. A prompt whose
witness cannot be stated stays `judge` — that is a finding about the prompt,
not a failure of the sweep.

This is fill work: zero review-minutes at dispatch (the review is the human's
accept/strike pass, which is the approval itself), and it directly grows every
future batch.

## Done when

- Every `Unattended: ready` prompt either carries a human-approved `Witness:`
  or a one-line `Witness: none —` reason.
- The regrade (`sizing` faculty) is re-run and the glance/notify counts are
  recorded in the epic ledger.
