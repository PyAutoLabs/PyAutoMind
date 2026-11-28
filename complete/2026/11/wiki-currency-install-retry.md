Each assistant's reusable `wiki-currency.yml` (autolens, autogalaxy, autofit, autocti) now retries the pinned install of the released stack: `--no-cache-dir`, up to 10 attempts 30 s apart, exact pin only, `::error::` + exit 1 after the last. At release 2026.11.22.1 PyAutoHands' `wait_for_released_stack` saw the release on its runner while the autolens/autocti wiki jobs, a minute later on other runners, could not install it (PyPI CDN inconsistency), turning the run red and filing false issues (autolens_assistant#188, autocti_assistant#44 — both closed after green re-runs against 2026.11.22.1).

Verified: YAML parses x4; the extracted step under `bash -e` with a fake pip: present → 1 call; late → success on attempt 3; absent → 10 calls, `::error::`, exit 1. PR CI green on all four. Live proof pending: the next release's wiki-currency legs.

## Original prompt

# Wiki-currency install races PyPI's CDN across runners

Type: bug
Target: assistants
Repos:
- autolens_assistant
- autogalaxy_assistant
- autofit_assistant
- autocti_assistant
Difficulty: small
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-11-25
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/193
Lane: any

At release 2026.11.22.1 (PyAutoHands run 45013510824), PyAutoHands' `wait_for_released_stack` job found every package on PyPI at 11:02:47Z, yet one minute later the autolens and autocti `wiki-currency` reusable workflows, on other runners, failed `pip install "<lib>==2026.11.22.1"` with "No matching distribution found". PyPI's CDN is not consistent across runners, so a single poll on one runner proves nothing for the next. The failure turned a shipped release red and opened false "could not complete" issues (autolens_assistant#188, autocti_assistant#44).

Fix: in each assistant's `.github/workflows/wiki-currency.yml` "Install the released stack" step, retry the pinned install with `--no-cache-dir` (about 10 attempts, 30 s apart), keep the exact pinned version, never fall back to an older or unpinned install, and fail loudly after the last attempt. Keep PyAutoHands' `wait_for_released_stack` as the first line of defence (PyAutoHands#334).

autolens_assistant is shared with likelihood-lifecycle-p5g (autolens_assistant#192), which edits the same file in a different hunk (sparse checkout ~L100); human-approved 2026-11-25. Plan approved by the human in the release check-in chat on 2026-11-25.
