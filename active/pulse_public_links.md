# Pulse public links: org-profile organ row and the hub's Pulse board link

Type: docs
Target: PyAutoPulse
Repos:
- .github
- pyautolabs.github.io
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: active
Consequence: notify
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check --only "public front-door organ tables"` green; `pyautolabs.github.io/index.html` links `https://pyautolabs.github.io/PyAutoPulse/` beside the Eyes board link
Review-minutes: 2
Unattended: ready
Filed: 2026-10-02
Issued: 2026-10-02
Epic: profiling-organ-birth

## Request (verbatim)

> ok do the still opens

## Context

Phase 0 (PyAutoMind#463) left the `.github/profile/README.md` organ-table row as a human act (the
`repos_sync --write` spill into the canonical `.github` checkout was reverted and the patch not kept).
Phase 3 (PyAutoBrain#450) added the cockpit card but not the hub front page's link to the Pulse board,
which Eyes has (`index.html:360`).

## Task

1. **`.github`** `profile/README.md`: regenerate the `<!-- repos_sync:organs:begin/end -->` table from
   the body map (`repos_sync.py --write` limited to that target, or copy the generated row from
   `PyAutoScientist/README.md` with bold links as the other `.github` rows use) so the Pulse row sits
   after Hands. No other edits.
2. **pyautolabs.github.io** `index.html`: one line beside the Eyes board link —
   `<a href="https://pyautolabs.github.io/PyAutoPulse/">The Pulse board</a>` — with the same
   surrounding markup.

## Out of scope

Anything inside PyAutoPulse; the cockpit (done in phase 3).

## Ship policy

Supervised: two one-line PRs, end at PR-open, merge human (`/prm`).
