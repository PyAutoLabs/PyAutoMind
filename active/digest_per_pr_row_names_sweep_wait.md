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
