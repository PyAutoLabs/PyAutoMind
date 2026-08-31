# Retire parked-at-ship for batch members: supervised resolves to decide-and-flag

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- batch
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: never
Epic: two-slot-batching
Filed: 2026-08-31

Human direction (2026-08-31-pm slot, verbatim):

"""
I dont really want these parked at ship judgements, ideally we send off a batch
and then dont think about it again, the parked thing is an annoying middle
ground which requires human time.
"""

Doctrine change to AUTONOMY.md (human-required — this is a gate edit, to be made
with the human in the loop, not by an unattended run):

Under a **batch launch**, an effective-`supervised` member reaching the ship
checkpoint does not park. It resolves to **decide-and-flag**: open the PR
(never merge), flag the decision in the PR body per the existing one-per-PR
rule, and the slot's packet presents it as an ordinary reviewable member. The
batch review IS the human approval the supervised level exists to provide, so a
mid-shift park is a redundant second checkpoint that costs the human a
GitHub-issue round-trip.

Evidence from batch 2026-08-31-pm: two supervised-capped members took the
decide-and-flag branch (PyAutoFit#1554, PyAutoMemory#76) and produced exactly
the desired experience — everything at a PR, one review surface; three members
took the park branch (PyAutoHands#272, PyAutoFit#1552, euclid#47) and each
requires a separate human judgement before a PR even exists.

Scope: batch launches only — interactive supervised runs keep the park
behaviour. `human-required` and `Unattended: never` are unchanged and never
enter a batch. `Blocked-by:` unchanged.

Witness: AUTONOMY.md's "Leg under a batch launch" section states the rule with
a dated entry and revert condition, and the next batch containing a supervised
member ends with a PR, not a park.
