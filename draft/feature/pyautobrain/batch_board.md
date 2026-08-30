# Batch phase 6 — the batch board

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- dashboard
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: two-slot-batching
Phase: 6
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

The surface the human opens at the top of a slot. The second dashboard: the Mind
dashboard is *everything that could be done*, this is *everything currently in
flight and what it produced*.

## The contract

Same doctrine as the Brain board: a **thin collect feeding pure renders**,
composing signals that already have an owner, never recomputing and never
mutating. It decides nothing; every chip routes back through a real door.

## What it renders

One card per member of the open batch, ordered **failures first, then
decisions-taken, then clean**:

- one line: what changed and why
- delivery: PR link, `+n/-m`, files touched
- the four gate legs, each shown as *ran and passed* / *ran and failed* / **did
  not run** — never a single green tick. Absence of a finding is not a finding.
- `## Decisions taken` from the PR body, if any (phase 3)
- what the run flagged as uncertain
- actions: **Merge** (`/prm <PR>`), **Tweak** (one line of human text → an agent
  drafts the follow-up prompt and puts it at the top of `queue.md`), **Reject**
  (route to `condemned.md`)

Then a footer strip: batch points, delivered count, usage-window reading, and
the backpressure state — is the next batch clear to launch?

The **Tweak** path is the one that must be one tap. The human types "the guard
should be at the caller, not inside the loop" and never writes a prompt file;
drafting it is the machine's job.

## Built before the slot, not during it

A scheduled run 30 minutes before each slot executes `batch collect` and
publishes, so the board is finished when the human opens it. Waiting for a
surface to assemble is exactly the attention cost this epic exists to remove.

## Where it renders

Two viable targets; pick by measurement, not taste.

- **GitHub Pages**, exactly like `dashboard.html` and the Brain board — the
  known-good path: phone-first, copy chips, already-solved publishing.
- **A Claude Code Artifact** — available on Pro/Max, published from a session,
  updatable in place at a stable URL. The documentation's own first listed use
  case is walking a reviewer through a pull request with annotated diffs.
  Caveat that decides it: **comments on artifacts require Team/Enterprise**, so
  on Max the board can render but cannot collect the human's replies; every
  action must still route to GitHub or to a Claude session.

Default to Pages. Prototype the Artifact only if the Pages version proves too
static.

## Not in scope

Review itself. The board orders and presents; the human judges.
