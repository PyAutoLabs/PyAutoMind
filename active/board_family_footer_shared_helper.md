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
