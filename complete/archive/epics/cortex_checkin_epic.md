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

## Where the three phases landed (2026-09-03)

All three are at **PR-open and unmerged**, stacked in both repos. Nothing of
this epic is on `main`.

| Phase | Issue | Branch (both repos) | Base | PyAutoBrain PR | PyAutoCortex PR |
|---|---|---|---|---|---|
| 1 — shed the review-slot and gate apparatus | PyAutoCortex#9 | `feature/cortex-checkin-p1-shed-review-slot` | `main` | #348 | #10 |
| 2 — the `/cortex` check-in door | PyAutoBrain#349 | `feature/cortex-checkin-p2-the-door` | p1's branch | #350 | #11 |
| 3 — by-project summary + the two missing prompts | PyAutoCortex#12 | `feature/cortex-checkin-p3-project-summary` | p2's branch | #351 | #13 |

**Recommended merge order — six PRs, strictly in this sequence:**

1. `PyAutoBrain#348`
2. `PyAutoCortex#10`
3. `PyAutoBrain#350`  ← retarget to `main` once #348 has merged
4. `PyAutoCortex#11`  ← retarget to `main` once #10 has merged
5. `PyAutoBrain#351`  ← retarget to `main` once #350 has merged
6. `PyAutoCortex#13`  ← retarget to `main` once #11 has merged

Two rules produce that order. **Brain before Cortex within a phase:** the
Cortex `dashboard_refresh.yml` workflow renders the board through PyAutoBrain
**main**, so a Cortex PR whose pages were rendered by a newer conductor stays
red until the matching Brain PR has landed (phase 1 saw exactly this, and the
workflow's own comment names the skew). **p1 → p2 → p3:** each phase's branch
is cut from the one below it, so a merge out of order replays that phase's
diff against a base it was never written on.

Heart was **RED and unacknowledged** at all three ship times — red `release
validation FAILED (stage integrate)`, yellow `PyAutoArray: open PR 11d old`,
both release-chain facts about other repos, neither of which is in the release
chain. Every phase stopped at PR-open. A human ack (or a green Heart) is owed
before any of the six merge.

## Explicitly OUT of scope

- Collapsing the 10-state phase machine (`pulled`+`awaiting-ruling`,
  `gated`→`planned`): touches 32 phase files and 22 rulings for little gain;
  revisit only if the door finds the states in its way.
- `Migrated-from:` headers (spent, harmless) and `docs/schema_decisions.md`
  (cheap history). Leave.
- Rewriting the seven per-project `hpc/sync` CLIs to a common manifest; the
  door writes the pull manifest itself instead.

## Closed 2026-09-04 — all three phases on `main`

Every one of the six PRs merged on 2026-09-04, in the recommended order, Brain
before Cortex in each phase:

| # | PR | Merge sha |
|---|---|---|
| 1 | PyAutoBrain#348 | `fc1cb32f6e226ddd2da24448769f1f77ebed6421` |
| 2 | PyAutoCortex#10 | `6cd6220e8e86711919c8261d3230564f22b09036` |
| 3 | PyAutoBrain#350 | `9a039d92a5ac2c9c1ebce52636bc3b42acedd4e8` |
| 4 | PyAutoCortex#11 | `284097de3787aac22156dd1337e2c6749a9d5088` |
| 5 | PyAutoBrain#351 | `5427234f56597b24f819622f1be4f3af2c0e01cc` |
| 6 | PyAutoCortex#13 | `7ea86aa8bd64983b3820b148188400e29e1913a7` |

Issues PyAutoCortex#9, PyAutoBrain#349 and PyAutoCortex#12 are closed as
completed. Records: `complete/2026/09/cortex-checkin-p1-shed-review-slot.md`,
`…-p2-the-door.md`, `…-p3-project-summary.md`.

GitHub retargeted each phase's PRs to `main` on its own as the phase below it
merged — the manual `gh pr edit -B main` the plan anticipated was never needed.

Two things the merge order did not predict:

- **PyAutoCortex#10 arrived `CONFLICTING`.** `main` had moved under the branch
  overnight — the dashboard self-heal commit `1a39784` and the gate-grade commit
  `1815c69`. The only conflicted paths were the two generated pages. Resolved
  with a merge commit (`2ddb47b`) that keeps `main`'s gate flip on
  `phases/euclid/dr1_prelim_10_lens_science_run.md`, drops the `Gates-cleared:`
  key phase 1 retires, and regenerates `dashboard.md` + `dashboard.html` with
  the phase-1 renderer instead of hand-resolving them.
- **PyAutoCortex#11 fired no workflow at all.** Its effective diff against
  `main` is three documentation files, which match no path filter in either
  Cortex workflow. Path-filtered by design, not a missing check.

The Brain-before-Cortex rule held exactly as written: PyAutoCortex#10's and #13's
`refresh` checks were red on the Brain-main skew and went green on a re-run once
the matching Brain PR was on `main`.

Heart was RED at merge time with two reasons — "release validation FAILED (stage
integrate)" and "PyAutoArray: open PR 12d old" — both release-chain facts about
other repos, neither of which is in the release chain. The human acknowledged
them and authorised all six merges; the ack is recorded on each phase's record.

One backlog prompt was falsified by phase 1 and retired unimplemented at this
close-out: `draft/feature/pyautobrain/the_batch_conductor_s_plan_kind_cortex.md`
asked for a `--board` form of `plan --kind cortex`, a verb phase 1 deleted
outright. Record: `complete/2026/09/batch-plan-kind-cortex-admits-only-ready.md`.

The three phase prompts named under "Phases" above were issued from `active/` and
now live under `complete/2026/09/`; the `draft/` paths there are historical.

## Retired from epics.md (2026-09-04)

## cortex-checkin
- title: Cortex check-in — one door, shed the review-slot and gate apparatus
- ledger: draft/maintenance/pyautocortex/cortex_checkin_epic.md
- status: COMPLETE 2026-09-04 — all three phases merged (Brain#348/#350/#351,
  Cortex#10/#11/#13), in that order, Brain before Cortex in each phase. Merged under a
  human-authorised acknowledgement of a RED Heart whose two reasons — "release validation
  FAILED (stage integrate)" and "PyAutoArray: open PR 12d old" — are release-chain facts
  about other repos, neither of which is in the release chain. Records:
  complete/2026/09/cortex-checkin-p1-shed-review-slot.md, -p2-the-door.md,
  -p3-project-summary.md. The sole interface to the Cortex is now the chat check-in.
- notes: three phased prompts from the 2026-09-03 Cortex assessment — (1) delete the
  review-slot apparatus for the cortex kind (plan --kind cortex, packets, partial reviews,
  carried members, status box, --push integration, slot/shift vocabulary), gate grading,
  rule --also, Lane:, the restricted-YAML parser; decouple collect from the batch record;
  (2) the `/cortex` check-in door — pull every active project, score, render, push, summary;
  (3) by-project dashboard section with folders + the accept→next-phase and rerun prompts.
  Issue ONE at a time, in order; later phases stack on earlier branches until merged.
