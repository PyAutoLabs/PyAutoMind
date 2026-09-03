# Retire parked-at-ship under `--auto`: supervised resolves to decide-and-flag

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: never
Filed: 2026-08-31

Human direction (2026-08-31, verbatim):

"""
I dont really want these parked at ship judgements, ideally we send off a batch
and then dont think about it again, the parked thing is an annoying middle
ground which requires human time.
"""

Doctrine change to AUTONOMY.md (human-required — this is a gate edit, to be made
with the human in the loop, not by an unattended run):

Under an explicit **`--auto` launch**, an effective-`supervised` run reaching the
ship checkpoint does not park. It resolves to **decide-and-flag**: open the PR
(never merge), and flag the decision in the PR body per the existing one-per-PR
rule. The contract already ends every autonomous run at PR-open with merge left
to the human, so **the PR review IS the human approval the supervised level
exists to provide**. A mid-run park is a redundant second checkpoint: it costs
the human a GitHub-issue round-trip before a PR even exists, and then asks them
for the same judgement again at merge.

Evidence, 2026-08-31: two supervised-capped `--auto` runs took the
decide-and-flag branch (PyAutoFit#1554, PyAutoMemory#76) and produced exactly
the desired experience — everything at a PR, one review surface; three runs took
the park branch (PyAutoHands#272, PyAutoFit#1552, euclid#47) and each required a
separate human judgement before a PR existed.

Scope: `--auto` launches only — interactive supervised runs keep the park
behaviour, because there the human is present and the round-trip is free.
`human-required` and `Unattended: never` are unchanged and never run unattended.
`Blocked-by:` unchanged.

Witness: AUTONOMY.md's supervised ship-checkpoint section states the rule with a
dated entry and a revert condition, and the next `--auto` run with a
supervised-capped member ends with a PR, not a park.
