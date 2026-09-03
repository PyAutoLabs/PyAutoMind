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
Filed: 2026-08-31

**Make every backlog prompt reviewable: a `Witness:` line on each draft.** A
witness is the machine-checkable claim whose truth settles the task — the thing
a reviewer reads first and, when it holds, often the only thing they need to
read. Today 151 of 153 backlog prompts grade `judge` because they carry none;
given one, the same backlog grades 33 `notify` / 104 `glance` / 16 `judge`. That
is the whole distance between "every task costs a PI's hour" and "a fifth of it
costs nothing", and it is a property of how prompts are written, not of how they
are scheduled: a witnessed prompt is cheaper to review whether it ships alone,
in a bundle, or under `--auto`. Measured from the other side too — the tasks
that reviewed in minutes on 2026-08-31 were the ones with pre-registered
witnesses.

## The work

Sweep the `Unattended: ready` prompts in `draft/`, adding a `Witness:` line —
a machine-checkable claim whose truth makes the task reviewable in minutes
("ids bit-identical", "31-rule byte-equality", "smoke suite green with the new
default", "Δlog-evidence < 5") — in passes of ~15 prompts, proposed
to the human for approval before any header is written.

**The no-invention rule stands and is the whole point: witnesses are
human-declared.** A pass proposes candidate witnesses where the prompt's own
text implies one; the human accepts, edits, or strikes each. A prompt whose
witness cannot be stated stays `judge` — that is a finding about the prompt,
not a failure of the sweep.

This is fill work: zero review-minutes of its own (the review *is* the human's
accept/strike pass, which is the approval itself), and every pass permanently
lowers the review cost of the prompts it touches.

## Done when

- Every `Unattended: ready` prompt either carries a human-approved `Witness:`
  or a one-line `Witness: none —` reason.
- The regrade (`sizing` faculty) is re-run and the glance/notify counts are
  recorded in this prompt, pass by pass, so the campaign's effect on the
  backlog's review cost is visible without re-deriving it.
