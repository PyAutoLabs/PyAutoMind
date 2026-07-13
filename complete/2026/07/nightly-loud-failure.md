## nightly-loud-failure
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/67
- completed: 2026-07-10
- library-pr: PyAutoBrain#69 (merged 2026-07-10)
- summary: nightly driver hardening — token probe, fetch errors page (never 💤), anchor validation w/ 24h fallback, no anchor advance on error nights or dry-runs; 12 unit tests + three live --no-dispatch path validations; found via the 2026-07-10 silent-skip incidents (secrets were also missing on PyAutoBrain — set by human same day; anchor manually reset to 2026-07-09T06:05:39Z)
