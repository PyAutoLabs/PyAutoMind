## What shipped
PyAutoBrain#591 (commit 147609a) + PyAutoMind#541: `pyauto-brain intake looks-shipped` / `reconcile --strong` flags drafts with strong evidence of shipping — a Witness-named test/function added or changed after `Filed:` in a target repo; a ship-claiming commit (or cached merged-PR body) naming the draft; a completion record whose `## Original prompt` near-duplicates it. Flags only; `--apply` writes `looks_shipped.json`; dismissals live in `looks_shipped_dismissed.md`. Dashboard "Looks shipped — confirm" section + state.json items; `batch plan` rejects flagged drafts. Daily `.github/workflows/looks_shipped.yml` (06:41 UTC). Real run: 0/271 today; 5/295 (all genuinely shipped) on the pre-sweep Mind. 10 tests.

## What the filed scope missed
Recall is low by design (4 of the 2026-11-05 sweep's 27); the merge-time hook (Ask item 4) was not built.

## Follow-ups
Check the workflow's first run (private / `Jammy2211/*` clones may fail under the org token); optional `--pr-cache` builder where API access exists; merge-time warning hook.

## Original prompt

# Close-out guard: catch shipped work whose Mind draft was never closed, whatever…

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-11-05
Consequence: judge
Witness: a fixture Mind + fixture commit/PR history where (i) a draft's Witness test name now exists in its target repo, (ii) a merged PR body or commit message names the draft's path or slug, and (iii) a completion record's `## Original prompt` duplicates an open draft — the guard flags all three as `looks-shipped` with the evidence cited, flags none of a control set (shared vocabulary only), writes nothing under draft/, and the batch planner drops flagged drafts from its proposals; `pytest PyAutoBrain/tests -q` and the Mind suite green.
Review-minutes: 15
Unattended: ready

## Why (measured 2026-11-05)

A queue check-in picked five tasks and found four already shipped. A full sweep of all 280
drafts then closed **27 shipped/superseded drafts** and re-scoped 24 partly-done ones
(PyAutoMind#539). This morning's batch (`batches/2026-11-05-am.md`) had proposed two of the
shipped ones. Every case bypassed `/prm`, whose close-out already runs a folder-scoped
`intake reconcile` (`skills/prm/reference.md` §4):

- fixed directly on main with no issue or PR (Mind 679b1319f, 4d8290555);
- merged by a session that never ran the close-out (PyAutoBrain#564 shipped
  `rtd_organism_currency` and `board_without_gh_phase2_legs`; PyAutoMemory#143);
- re-filed as a duplicate — several completion records carry an open draft's twin as their
  `## Original prompt` (e.g. `workspace-freshness-stamp`, `autocti-viz-render-from-mains`), and
  `ell_comps_joint_disk_constraint` was filed four days after its work merged.

`intake reconcile` exists but is read-only, opt-in and vocabulary-based (2026-08-25: 24 suspects
of 138, mostly weak), so nothing runs it across the whole backlog with strong evidence.

## Ask

Add a detector that runs outside `/prm` and only *flags* (retiring stays human, as now):

1. **Strong evidence signals** in `intake reconcile` (or a sibling mode), graded above the
   existing vocabulary signals:
   - the draft's Witness names a test/function that now exists in the target repo
     (search API or the checked-out organs);
   - a merged PR body / commit message on an organism `main` since `Filed:` names the draft's
     path, filename or slug;
   - a `complete/` record's `## Original prompt` duplicates an open draft (title or body
     near-match).
2. **Schedule it**: a daily Mind workflow (beside `registry_reconcile.yml`, odd minute) that
   writes the strong-evidence suspects into a dashboard **"Looks shipped — confirm"** section
   (state.json too), each with its evidence line and a one-line close command.
3. **Batch backpressure**: the Batch Agent excludes `looks-shipped` drafts from proposals until
   a human confirms or dismisses them.
4. Optional, decide in the plan: a merge-time hook (`ship_*` / `prm`'s tiered path already
   close out; the gap is merges outside them) — e.g. warn in the PR when a branch's commits
   name a draft that the PR does not retire.

## Not in scope

Auto-closing anything; the 34 sweep `UNCLEAR` drafts (runtime/CI checks, separate work).

## Original request (chat 2026-11-05)

"/prm and file the close out guard" — following the recommendation: "make `/prm` or the merge
workflow refuse to finish while the task's draft is still in `draft/`".

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/closeout_guard.md -->
