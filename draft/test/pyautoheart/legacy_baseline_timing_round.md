# Legacy baseline timing round: snapshot pre-rebuild timings of every CI test surface

Type: test
Target: PyAutoHeart
Repos:
- PyAutoHeart
- workspaces
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: ci-timing-fast-tests
Phase: 4

Legacy baseline timing round: snapshot the pre-rebuild timings of every CI test surface.

With phases 1-3 live, do the first full timing round across the workspace, _test workspace
and HowTo repos plus unit tests and import times: trigger/collect a complete pass, verify
every repo reports, and record the snapshot in the phase-2 durable history explicitly
LABELED AS THE LEGACY RECORD. The user's framing: the epic's later phases (the _test
physical+fast rebuild, CI caches) will change script content, datasets and pinned
likelihoods, so this round is a legacy reference — NOT the starting point of the long-term
tracking history, which begins after the rebuild lands. Mark it so in the stored record and
on the board (a labeled epoch boundary, so post-rebuild drift warnings do not fire against
pre-rebuild baselines).

Deliverables: the labeled snapshot committed to PyAutoHeart; a short written digest of
where the time currently goes (slowest scripts per repo, slowest unit tests, import
floors, compile-dominated vs execution-dominated classes) — this digest is the input
evidence for phases 5, 6, 8 and 9 of the epic.
