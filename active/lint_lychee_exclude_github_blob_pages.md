# Lint: exclude github.com blob pages from lychee (Pulse main red, Eyes exposed)

Type: bug
Target: PyAutoPulse
Repos:
- PyAutoPulse
- PyAutoEyes
Themes:
- ci
- profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: notify
Witness: `lint` workflow green on PyAutoPulse main and on the PyAutoEyes PR; lychee output shows the five `github.com/.../blob/...` links as Excluded, not Errors
Review-minutes: 3
Unattended: ready
Filed: 2026-10-02
Issued: 2026-10-02
Epic: profiling-organ-birth

## Request (verbatim)

> fix loose end then go to next phase

## Context

`lint.yml` in PyAutoPulse (merged 2026-10-02 in PyAutoPulse#2) and in PyAutoEyes runs lychee over
the prose markdown. On 2026-10-02 every `https://github.com/<org>/<repo>/blob/<ref>/<file>` URL
returned **503 Service Unavailable** to any non-browser client (curl/lychee, any User-Agent,
from Actions and from a laptop; cpython's own README too) while githubstatus.com reported all
systems operational — GitHub's page-view bot protection, not API rate limiting. PyAutoPulse#2
lint failed twice on five such links; PyAutoEyes main lint failed the same way at 10:57 after
passing at 10:56. Passing `GITHUB_TOKEN` to lychee (`--github-token`, PyAutoPulse commit
`b2d4a595`) did **not** help: the post-merge lint on PyAutoPulse main still 503'd on the identical
set. PyAutoPulse main is therefore red on `lint`.

## Task

1. **PyAutoPulse** `.github/workflows/lint.yml`: add `--exclude '^https://github\.com/.*/blob/'`
   to the lychee invocation (next to the existing issues/pull/commit/releases exclude). Keep the
   `GITHUB_TOKEN` env (harmless; still helps API-resolvable links). Update the header comment
   (step 4 of the workflow's numbered list) to say why blob pages are excluded.
2. **PyAutoEyes** `.github/workflows/lint.yml`: the same exclude line.
3. No prose edits: the links stay in the markdown (they are correct for humans); only the
   link-rot gate stops fetching them.

## Out of scope

Replacing the links with raw.githubusercontent.com / Pages URLs; any lychee version pin.

## Ship policy

Supervised: corrective PRs, end at PR-open, merge human (`/prm`). PyAutoPulse first (it is the
red main), Eyes independent.
