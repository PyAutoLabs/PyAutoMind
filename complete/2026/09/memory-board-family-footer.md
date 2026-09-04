## memory-board-family-footer

- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/87
- completed: 2026-09-04
- library-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/88

`scripts/board.py` no longer carries its own hard-coded `BOARD_FAMILY` tuple.
The knowledge board's footer now reads the canonical board family from the
PyAutoBrain theme's `board_links(base, current)` helper (added upstream in
PyAutoBrain#353), so it carries the Cortex chip and the ruled organ chip order
that the rest of the family renders. The snapshot owner's base URL derivation is
unchanged, and the legacy tuple survives only as a fallback for an older
PyAutoBrain checkout that has no `board_links` yet.

- Files: `scripts/board.py`, `tests/test_board.py`
- Tests assert the footer carries Cortex and the canonical chip order.
- CI green on every run and every leg for head `a583dfa5` (validate, push +
  pull_request); `mergeStateStatus` CLEAN; merged as `5aaf7470`.
- One of three sibling close-outs behind PyAutoBrain#353 (Heart, Hands, Memory).
- Organ repo, not a library: no pending-release chain and the Heart freeze
  window does not gate it.

## Original prompt

# Memory board footer reads the canonical board family instead of a stale tuple

Type: feature
Target: pyautomemory
Repos:
- PyAutoMemory
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-09-04

`scripts/board.py:572` carries a hard-coded `BOARD_FAMILY` tuple listing five sibling
boards in an ad-hoc order. It predates PyAutoCortex, so the Memory board's
footer has no Cortex chip, and its chip order does not match the ruled organ
order the rest of the family renders.

The canonical list already lives in `PyAutoBrain/config/policy.yaml` under
`board: boards:` (brain, mind, cortex, memory, heart, hands, organism), and
this renderer already imports the shared theme from
`PyAutoBrain/board/_theme.py` via its `theme()` locator — its CI job checks
PyAutoBrain out beside the repo.

- Replace `BOARD_FAMILY` with the theme's new `board_links(base, current)`
  helper, keeping the base URL derivation this file already does (the snapshot owner).
- Keep the old tuple as a fallback for an older PyAutoBrain checkout that has
  no `board_links` yet.
- Update the board tests to assert the footer carries Cortex and the canonical
  chip order.

Library-first: depends on the PyAutoBrain PR that adds `_theme.board_links`;
CI here may only go green once that has merged.
