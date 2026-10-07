## pulse-public-links
- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/25
- completed: 2026-10-02
- epic: profiling-organ-birth
- library-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/26
- library-pr: https://github.com/PyAutoLabs/.github/pull/26
- summary: The two public-surface one-liners left from the PyAutoPulse organ birth: `.github/profile/README.md` organ table regenerated from the body map (`organ_public_table(bold=True)`) so the Pulse row sits after Hands — clears the Heart "public front-door organ tables" drift reason; hub `index.html` gains "The Pulse board" link beside the Eyes board link. Neither repo has CI; the human approved both merges.
- traps: `repos_sync.load_manifest(mind_dir)` returns a tuple whose dict member is the repos map — pick it before calling `organ_public_table`; regenerating ONE front-door table this way avoids the whole-workspace `--write` spill.
- follow-ups: autolens_profiling cockpit-feed identity + `pulse-refresh` dispatch sender (both filed under `draft/feature/autolens_profiling/`, blocked on task evaluation-grid-cap-field); phase 4 waits for a real second `_profiling` producer.

## Original prompt

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
