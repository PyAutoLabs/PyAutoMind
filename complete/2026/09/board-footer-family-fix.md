## board-footer-family-fix

- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/450
- completed: 2026-09-28
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/242 (branch tip `e365e47`, merged 2026-09-28)
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/292 (branch tip `3a7a715`, merged 2026-09-28)

Heart and Hands board-footer tests expected the old six-organ family after PyAutoBrain added the Nerves and Gut boards (PyAutoNerves#172, PyAutoGut#9), leaving Heart main CI red and PyAutoHeart#240/#241 and PyAutoHands#291 showing a pre-existing red. Test files only; no API change, no workspace impact.

**Shipped**
- PyAutoHeart `tests/test_dashboard.py` and PyAutoHands `tests/test_board.py`: the footer-family expectation is derived from the Brain (`theme().board_links("", BOARD_KEY)`, i.e. `config/policy.yaml` `board: boards:`), the same read the renderer makes; policy order, Cortex present and self omitted are still asserted, so the next organ birth cannot re-break them.
- Full suites outside the bundle env: Heart 1063 passed, Hands 472 passed; footer tests 3/3 each against the PyAutoBrain#427 (eyes-organ-order) branch and a scratch policy with an `eyes` board after `memory`.

**Traps / notes**
- Worked under a human-approved parallel claim alongside eyes-organ-order (#439) and autolens-visualization-rebirth (#446); no file overlap.
- Tier `notify`: shadow row not appended at close-out (the human's merged-unchanged / after-substantive-change answer was not available to the close-out agent); append with `lifecycle.py shadow-row` once answered.

## Original prompt

# Heart and Hands board-footer tests expect the old six-organ family after Nerves and Gut joined

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoHands
Difficulty: small
Autonomy: safe
Priority: high
Lane: local-dev
Status: formalised
Issued: 2026-09-28
Consequence: notify
Witness: In both PyAutoHeart and PyAutoHands, `pytest tests/test_dashboard.py -k footer` is green, and the expected family list is derived from PyAutoBrain (`_theme.py` ORGANS / the policy board list), not a hard-coded literal.
Review-minutes: 0
Unattended: ready

## Why

Verified 2026-09-28 by two independent runs. `tests/test_dashboard.py::test_the_family_footer_carries_the_cortex_in_the_canonical_order`
fails on PyAutoHeart main (a95ebc9; Heart main CI is red), and the equivalent footer test fails on
PyAutoHands main (reproduced on a detached origin/main worktree).

Cause: PyAutoBrain main added Nerves and Gut to the board family (PyAutoNerves#172, PyAutoGut#9), so
the rendered footer's `data-organ` attributes are now
`brain, mind, cortex, memory, hands, nerves, gut, organism`, while both tests still expect the old
six-entry `FAMILY_WITHOUT_HEART` list. The Heart assertion (tests/test_dashboard.py:1088):

    assert re.findall(r'data-organ="(\w+)"', footer) == FAMILY_WITHOUT_HEART

fails with "At index 5 diff: 'nerves' != 'organism'; Left contains 2 more items".

Consequence today: PyAutoHeart#240, PyAutoHeart#241 and PyAutoHands#291 CI show this pre-existing red,
and Heart's main CI is red — two organ mains red.

## What

- Update the expected family list in the Heart and Hands footer tests to the canonical organ order:
  Brain, Mind, Cortex, Memory, Eyes, Heart, Hands, Nerves, Gut (PyAutoMind#439 lands Eyes after
  Memory), with the repo's own organ omitted from its own footer (Heart omits Heart; Hands omits Hands).
- Preferably derive the expectation from PyAutoBrain's `_theme.py` ORGANS / the policy board list
  instead of a literal, so the next organ birth cannot re-break these tests.

## Claims

PyAutoHeart and PyAutoHands are currently claimed by #439 (eyes-organ-order) and #446 — a
**parallel claim is needed** to work this fix alongside them (or fold it into #439, which already
touches the organ order).

<!-- formalised by the Intake (Conception) Agent on 2026-09-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/128f9a68-533e-4b45-b404-b6807b2c6900/scratchpad/board_family_footer_test_stale_after_nerves_gut.md -->
