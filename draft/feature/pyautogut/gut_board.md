# Birth a PyAutoGut board (Pages) so the footer family can carry the Gut

Type: feature
Target: pyautogut
Repos:
- PyAutoGut
Difficulty: medium
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-09-04

The one-tap board family (`PyAutoBrain/config/policy.yaml`, `board: boards:`)
currently names seven boards: brain, mind, cortex, memory, heart, hands,
organism. Two organs in the ruled order have no board at all — **Nerves** and
**Gut** — so the cross-board footer cannot carry them and neither has a palette
entry in `PyAutoBrain/board/_theme.py` `ORGANS`.

The Gut is the one with obvious board-shaped content: condemned self-material
held as durable git refs through a transit window, what is in transit, what is
due to be voided on the next sweep, and what a sweep just released. That is a
list of rows with a 📋 copy-for-Claude payload each — exactly the one-tap board
shape.

Work:

- Decide whether the Gut board is warranted now, and what its rows are (transit
  window contents, next sweep, recoverable refs, last sweep's releases).
- If yes: render it with the shared theme (`PyAutoBrain/board/_theme.py`) the way
  the Heart/Hands/Memory boards do, add a `gut` palette entry to `ORGANS` and a
  mark to `MARKS`, add `gut: PyAutoGut` to `config/policy.yaml` `board: boards:`,
  and wire a Pages publish workflow.
- Decide separately whether **Nerves** gets a board. Nerves is a configuration
  and serialization layer with little standing state; it may be right that it
  never grows one. Record the decision either way so this question is not
  re-asked.

Filed from the board-family footer work (2026-09-04), which made the footer read
the canonical list — the family is now only as complete as `boards:` is.
