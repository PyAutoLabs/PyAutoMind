# Cortex check-in — one door, shed the review-slot and gate apparatus

Type: maintenance
Target: pyautocortex
Repos:
- PyAutoCortex
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-03

Umbrella ledger for the `cortex-checkin` epic (registered in `epics.md`). Never
issued; the three phase prompts are, ONE at a time, in order. Phases 2 and 3
build on phase 1's deletions in the same files, so each later branch is cut
from the previous phase's branch (stacked PRs) until merged.

## Original request (verbatim, 2026-09-03)

> The way PyAutoCortex should work, which is how its being devdeloped, is
> basically when I want to check in on science runs I open an AI chat, I tell
> PyAutoCortex to use my laptop + RAL (or other HPCs) to download all results,
> give me a summary of where every project is in terms of runs and what
> folders I should check out, update the dashboard on GitHub, and then give me
> starting claude prompts to begin to continue work on any individual project
> (e.g. say results are good and go to next phase, get it to rerun stuff, and
> so on).
>
> This is really the only way we need to interface with Cortex, I dont think
> we over engineered much else about it but do assess if we have implemented
> anything or it does anything which is a bit over the top now this is how we
> are going to use it.
>
> ok go

## The assessment (2026-09-03, two read-only Opus audits)

The core is right-sized and works: `projects.yaml`, phase files, append-only
rulings, `cortex.py check/move/rule/new`, `collect`'s six-leg scorer and its
`--pull` shell-out, `dashboard --apply`, the self-healing dashboard workflow,
ledger auto-merge, the board's counts strip. What is over the top is
everything that models the human as a reviewer working a scheduled shift
through a packet page: all 22 rulings were reached in a live session and the
three batch records were backfilled by hand (0 conductor-opened; the one real
slot's notes say `plan --kind cortex` proposed the wrong four members; 0
rulings came from a packet; 0 partial-review files; `review-minutes-actual`
never filled). Gate grading has 2 gated refs, 0 flips, `Gates-cleared:` /
`Gate-override:` never written, and schema decision 54 routes sequencing via
prose `Ready when:` lines anyway. `rule --also` never used; `Lane:` is
`local-dev` on 32/32 phases; the restricted-YAML parser has a PyYAML-parity
test proving it redundant. Missing: a single check-in door (`/cortex` is
advertised in COMMANDS.md but not installed), a pull over every active
project (today `collect --pull` needs a batch record and pulls only
submitted/running phases), a by-project summary naming folders (`## Where to
look` is never rendered), an owned dashboard push, and two of five starting
prompts (accept → next phase, rerun).

## Phases

1. **Shed the review-slot and gate apparatus** —
   `draft/maintenance/pyautocortex/cortex_checkin_p1_shed_review_slot.md`
   (PyAutoCortex + PyAutoBrain).
2. **The `/cortex` check-in door** —
   `draft/feature/pyautobrain/cortex_checkin_p2_the_door.md`
   (PyAutoBrain + PyAutoCortex; installs the slash command).
3. **By-project summary + the two missing prompts** —
   `draft/feature/pyautocortex/cortex_checkin_p3_project_summary_prompts.md`
   (PyAutoBrain + PyAutoCortex).

## Explicitly OUT of scope

- Collapsing the 10-state phase machine (`pulled`+`awaiting-ruling`,
  `gated`→`planned`): touches 32 phase files and 22 rulings for little gain;
  revisit only if the door finds the states in its way.
- `Migrated-from:` headers (spent, harmless) and `docs/schema_decisions.md`
  (cheap history). Leave.
- Rewriting the seven per-project `hpc/sync` CLIs to a common manifest; the
  door writes the pull manifest itself instead.
