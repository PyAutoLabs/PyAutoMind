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
