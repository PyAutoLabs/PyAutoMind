## morning-status-release-rehearsal (morning Slack digest + release rehearsal — RESOLVED)
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/39 (STAYS OPEN for the RELEASE_MODE=live leg)
- completed: 2026-07-09 (resolved); active.md entry retired 2026-07-14 (/morning, human-directed)
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 — all MERGED.
- summary: Morning-status Slack digest + health webhook restored and delivering. User re-set both May-17 secrets (webhook + CLAUDE_CODE_OAUTH_TOKEN); morning_health dispatched → Slack POST success. Digest needed 3 further Mind-main CI fixes (checkout, show_full_output, allowedTools Write; 51e869e/d042289/0b78d5f) → fully green. Resolution detail: issues/39#issuecomment-4924031684.
- residual (not blocking retirement): PyAutoHeart#39 intentionally stays OPEN for the human-gated `vars.RELEASE_MODE=live` flip on PyAutoBuild (TestPyPI → live PyPI), to be flipped when the maintainer is satisfied with the release train. The tracking entry is retired because the rehearsal/Slack scope is done and no repo claim remains.
