The two M3.7e review follow-ups (PyAutoBrain#694), filed as drafts and approved by the human on 2026-11-19. The workspace sweep's failing-read streak starts fresh on a new shift (the slot name is stored with the last read), when no shift is stored, or after a gap of more than 2 hours (`SWEEP_STREAK_GAP_S = 7200`), so a failure left from the previous shift does not make the next shift's first failed read "unknown" at once, while slow ticks inside one shift still reach the 30-minute hold. A PR held by an unknown sweep reads "waiting: workspace sweep unknown since <t>" in its own per-PR digest row. Also covers `active/digest_per_pr_row_names_sweep_wait.md`.

## Merge receipts

- PyAutoBrain#695: ff9a0d338 (merged by the human's /prm, 2026-11-19)

Feature head bfa046c is an ancestor of origin/main. Organ repo: no release obligation.

## Validation and review

Tests first (43 tests in `tests/test_shift_end_sweep.py`); full Brain suite 2527 passed, 1 skipped; line budget, firewall and discovery OK; Heart scoped verdict green; PR CI GREEN. Independent review (Opus 5.5) round 1 FINDINGS (medium: a 10-minute gap rule measured between tick starts let a hanging outage restart the streak every tick; nit: digest fallback), fixed as suggested. Tier: judge (no shadow row).

## Original prompt

# Watcher: the sweep's failing-read streak survives the gap between shifts

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) an orchestrator test: the previous shift's last `gh run list` of the workspace sweep failed, the next shift's first tick hours later also fails, and no PR is held as "workspace sweep unknown" on that tick; (2) the same test with 30 minutes of continuous failures inside one shift still holds PRs; (3) the Brain suite passes
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat: "file the two M3.7e follow-ups as drafts and do them".

## Why

Review round 3 of M3.7e (PyAutoBrain#693), low note 1: `_sweep.py` keeps `fail_since` from the last shift. When the last read of one shift failed, the next shift's first failed read is already "unknown", with no 30-minute grace. Since round 2 that is a wait that one good read releases, so the impact is small, but the grace should mean what it says.

## Shape

Reset the failing streak when the previous read attempt is more than 10 minutes old (a gap between ticks or shifts), so the 30 minutes always count continuous failures inside one run of ticks. Tests as in the Witness. Record the rule in the S4 text of `AUTONOMY.md` and batch `AGENTS.md` "The watcher".

## Second prompt (folded)

# Digest: a PR held by an unknown sweep says so in its own row

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) a digest test: a PR held in `counters["sweep_waits"]` at close has a per-PR row reading "waiting: workspace sweep unknown since <t>", not the generic state; (2) the "Workspace sweep" section is unchanged; (3) the Brain suite passes
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat: "file the two M3.7e follow-ups as drafts and do them".

## Why

Review round 3 of M3.7e (PyAutoBrain#693), low note 2: the digest's per-PR branches (`_digest.py`, around line 267) do not know `sweep_waits`, so a PR held by an unreadable sweep falls to the generic state in its row. The "Workspace sweep" section does list it.

## Shape

Add a `sweep_waits` branch to the per-PR row, beside the merge-order wait. Test as in the Witness.
