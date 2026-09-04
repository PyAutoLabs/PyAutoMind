## board-family-helper
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/352 (closed, completed)
- completed: 2026-09-04
- classification: feature (pyautobrain) — organ repo, not a library; no pending-release obligation
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/353 (MERGED 2026-09-04T16:44:23Z, f5e30761)
- shipped: |
    The board family stopped being one list. Membership and order live once, in
    `config/policy.yaml` `board: boards:` — brain, mind, cortex, memory, heart,
    hands, organism, the ruled organ order — and the Brain's own renderers
    (`_intake`, `_cortex`, `_board`) read it. The three sibling organs did not:
    PyAutoHeart, PyAutoHands and PyAutoMemory each carried a hard-coded
    `BOARD_FAMILY` tuple written before the Cortex had a board, so their footers
    linked five siblings in an ad-hoc order and silently missed the sixth. A copy
    that drifts still renders, which is why nobody noticed.

    `board/_theme.py` gains the one read they can all call —
    `board_links(base_url, current=None) -> dict[str, str]` — using the same
    stdlib regex over the one-pair-per-line block that `_intake._board_links`
    uses. **No yaml import**: the theme module is presentation-only and these
    boards also render in workflows that install nothing. File order is
    preserved, so editing `policy.yaml` reorders every footer at once; `current`
    (the page's own key) is dropped so the result goes straight into
    `boards_footer`; an unreadable config returns `{}`, which renders as no
    footer rather than a broken one.

    `bin/morning.sh` also ticks and publishes the **Heart's** dev-box board
    beside the Brain's. The Heart Pages board was rendering its eight dev-box
    check families grey ("not observed here — dev box last looked 6d ago")
    because the observation expires after 48 h and `pyauto-heart publish` was
    last run by hand on 28 Aug. Same `--no-publish` guard, same non-fatal
    "skipped" fallback, path resolved from the script's own location so a
    worktree run resolves through the symlink.
- verified: |
    `tests/test_board_theme.py` (new, 38 lines) pins the ruled order (brain,
    mind, cortex, memory, heart, hands, organism), the dropped current key, the
    trailing-slash tolerance, the end-to-end footer, and the empty-on-missing-config
    path. Suite at ship time: `test_board_theme.py test_board.py
    test_board_degraded.py test_morning_timer.py test_intake_dashboard.py` —
    205 passed. Footer chip order was observed in each rendered sibling board
    with this branch as `PYAUTO_BRAIN`.

    CI at close-out: head `cf669f11`, the only run for the sha (Brain Tests,
    `pull_request`) completed/success on both pytest legs; `mergeStateStatus`
    CLEAN. `pyauto-heart freeze --show` reported not frozen, and PyAutoBrain is
    an organ repo (not `category: library` in `repos.yaml`), so the freeze gate
    does not apply to it either way.
- downstream: |
    This was the library-first base for three sibling footer tasks, which stay
    open and unchanged: `heart-board-family-footer`
    (PyAutoLabs/PyAutoHeart#201), `hands-board-family-footer`
    (PyAutoLabs/PyAutoHands#277), `memory-board-family-footer`
    (PyAutoLabs/PyAutoMemory#88). Each keeps its legacy tuple as a fallback for
    an older PyAutoBrain checkout, so they merge in any order — but their CI
    checks out PyAutoBrain `main`, so their new footer assertions only go green
    once this PR has merged. Their failed runs were re-run at this close-out
    (attempt 2: Heart 33895854984, Hands 33896388763, Memory 33896393367). None
    of their `active.md` rows carried a `blocked-by:` key, so nothing needed
    repointing.

## Original prompt

# Shared `board_links` helper in the board theme + Heart publish in morning.sh

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-09-04

The one-tap board family's canonical list lives in `PyAutoBrain/config/policy.yaml`
under `board: boards:` (brain, mind, cortex, memory, heart, hands, organism — the
ruled organ order). PyAutoBrain's own renderers read it. Three sibling renderers
(PyAutoHeart, PyAutoHands, PyAutoMemory) each carry a stale hard-coded
`BOARD_FAMILY` tuple: no Cortex chip, wrong order.

Give the shared theme one helper the siblings can call:

- `board/_theme.py` gains `board_links(base_url, current=None) -> dict[str, str]`,
  reading the `boards:` block of `config/policy.yaml` with the same stdlib regex
  `_intake._board_links` uses (the theme module stays stdlib-only — no yaml
  import), preserving file order, skipping `current`, returning
  `{key: f"{base_url}/{repo}/"}`.
- A unit test in `tests/test_board_theme.py` pins the order
  (brain, mind, cortex, memory, heart, hands, organism) and that the current
  key is dropped.

Second, the Heart Pages board renders its eight dev-box check families grey
("not observed here") because `pyauto-heart publish` was last run 28 Aug and the
observation expires after 48 h. `bin/morning.sh` already publishes the Brain
dev-box board daily; it should tick and publish the Heart one beside it —
skipped under `--no-publish`, failure non-fatal with the same "skipped" message
pattern.

Library-first: this PR is the base the PyAutoHeart / PyAutoHands / PyAutoMemory
footer PRs depend on.
