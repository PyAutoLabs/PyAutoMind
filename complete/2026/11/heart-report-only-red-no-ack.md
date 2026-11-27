Merged PyAutoBrain#730 (human /prm, 2026-11-27). M3.6h.

`batch brief --check` now gates a shift launch on Heart:

- **R1 (human, 2026-11-17).** A RED made only of report-only reasons (Heart class `local-checkout` and a "report only" action), none naming a touched repo, needs no `heart-ack:`. The reason set is written under `## Heart`, with stale reasons marked "not judged".
- **Human rulings, 2026-11-27, recorded in AUTONOMY.md:**
  - **(a)** An unacknowledged RED or YELLOW is refused mechanically. So is a grey, unreadable, missing or over-6 h read, unless there is a `heart-ack:`.
  - **(b)** R1 also covers a report-only YELLOW.
  - **(c)** The touched set is the named tasks plus the plan's members. A topic `Target:` is ignored. A prompt with no known repo fails closed. Later picks keep the scoped dev-ship gate.
- **Write safety:** no writes into a main git checkout; a record already on origin/main gets a note. The tests-only probe switch works only under pytest.

35 brief tests, 21 of them new. Each round's new tests fail on the previous head. Full suite 2604 passed. Independent Opus review over 4 rounds: two majors became rulings (a) and (c), and the last minors were fixed. Heart dev-ship GREEN.

## Original prompt

# M3.6h A Heart RED made only of report-only reasons needs no shift acknowledgement

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-17
Issued: 2026-11-27
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: `python -m pytest tests/test_batch_brief.py -q` passes with new tests that fail on today's main: (1) `brief --check` on a brief with no `heart-ack:` and a Heart RED whose every reason is `report only` and names no repo the brief touches passes and writes the reason set into the record; (2) the same with one reason naming a touched repo refuses; (3) the same with one human-only reason (an open PR, release validation) refuses; and `grep -n "2026-11-17" AUTONOMY.md` shows R1 under "Leg 4 under a batch launch"
Lane: any
Unattended: ready

## Why

At the launch of shift 2026-11-16-pm, Heart read RED. Every local-checkout reason was `report
only` (seven library checkouts behind or dirty, five manifest-drift legs), and none named a
repo the brief touched. The human still had to acknowledge it ("Heart ack so its ok") before
the shift could start.

**Human ruling R1 (2026-11-17):** a Heart RED made only of report-only reasons, none naming a
repo the brief touches, needs no acknowledgement; the brief records the reason set. Anything
else still needs the human's word.

## What

1. Write R1 into AUTONOMY.md, dated, under "Leg 4 under a batch launch".
2. `brief --check` and the watcher's Heart read apply it: when every reason is `report only`
   and none names a touched repo, no `heart-ack:` is needed and the reason set is written to
   the record (under `## Heart`, as today).
3. Anything else (a human-only reason, a release-scope reason, or a reason on a touched repo)
   still needs a `heart-ack:` from the human.

## Out of scope

- Heart counting behind or dirty local checkouts as RED in the first place (infrastructure
  review).
- Any change to the dev-ship gate outside a shift.
