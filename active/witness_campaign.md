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
Status: active
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-08-31
Issued: 2026-09-10

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

## Campaign log

Counts are over `draft/` only, so the campaign's own prompt drops out of the
denominator once it moves to `active/` (110 → 109). Two readings are recorded
because they can disagree: **derived** is `estimate_consequence` re-run over the
prompt, **declared** is the `Consequence:` header, which is what `dashboard.md`
and the batch planner actually read.

### Method correction (2026-09-10, before pass 1)

The prompt above says "adding a `Witness:` line". That alone moves nothing on
most of the target set. 89 of the 110 `Unattended: ready` prompts declare
`Consequence: judge` in their header — 74 of them among the 89 unwitnessed —
and `effective_consequence` lets a declared value beat the derived one.

That declaration is not a human judgement the heuristic lacks; it is a cached
derivation. `PyAutoBrain/agents/conductors/intake/_intake.py` puts `consequence`
and `review-minutes` in the "DERIVED … hygiene set" that `intake formalise`
fills in, while deliberately excluding `witness` because nothing can derive one.
The stamp was correct when written (no witness → `judge`) and goes stale the
moment a witness lands. Striking it instead is not an option either: the
dashboard reads `header.get("consequence", "-")` (`_intake.py:1568`), never a
live derivation, so a struck field renders `-` and the planner keeps budgeting
20 review-minutes for a task that now costs 0 or 3.

**So each pass writes three fields together — `Witness:`, `Consequence:`,
`Review-minutes:` — and leaves `Unattended:` alone.**

### Baseline (2026-09-10, before pass 1)

| Reading | ready | witnessed | notify | glance | judge |
|---|---|---|---|---|---|
| derived | 110 | 21 | 5 | 12 | 93 |
| declared (dashboard) | 110 | 21 | 1 | 7 | 89 + 13 unset |

Fully witnessed, the same 110 would derive **28 notify / 74 glance / 8 judge**.
That is the campaign's ceiling, and it reproduces the 33/104/16 in the prompt
above (measured there over the whole 153-prompt backlog, not the ready subset).

### Pass 1 — `workspaces`, 15 prompts (2026-09-10, issue #398)

Chosen as the largest single-target group and the biggest `notify` yield. All 15
were pinned at `Consequence: judge` with no witness. Human accepted all 15 as
proposed.

| | notify | glance | judge | review-minutes |
|---|---|---|---|---|
| before | 0 | 0 | 15 | 300 |
| after | 7 | 8 | 0 | 24 |

Backlog after pass 1: 109 ready, 36 witnessed, 73 not — derived **12 notify /
19 glance / 78 judge**; declared **8 / 15 / 73** + 13 unset.

Two witnesses are weaker than the other thirteen and are flagged here rather
than in the prompts, so a later pass can revisit them without re-deriving the
doubt: `group_los_halos` and `group_subhalo_sensitivity` both gate on "the
imaging version needs improving and padding out first", a leg with no stated
done-condition anywhere. Their witnesses cover only the group leg. The honest
alternative was `Witness: none —` on both; the human chose to accept them.

Also worth a later look: seven of the fifteen grade `notify` (0 review-minutes)
via rule 5 — `docs` work-type, no library repo touched. Two of those seven
(`interferometer_dirty_images_call_sites`, `propagate_shear_galaxy_idiom_to_group_cluster`)
change figures across 11 and 4 lens examples and say in their own text that a
human should look at the figures. The heuristic cannot see that. Declaring
`Consequence: glance` on such a prompt is the documented way to hold it.

### Remaining passes

`autoarray` (10) · `autolens` (9) · `autofit` (8) · `autolens_workspace` (6) ·
`autolens_profiling` (5) · then a tail pass over the ~26 singleton targets.
