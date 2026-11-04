# Nightly release driver dies at the 60-minute mark: the single App token expires during the Stage 3 `gh run watch`, and the 401 is paged as "Stage 3 failed"

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Themes:
- release-validation
- ci
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: a manually dispatched `nightly-release.yml` run (`dry_run=true`) reaches step 5 (the readiness gate) with Stage 2 and Stage 3 both completed and no `HTTP 401` anywhere in its log, more than 60 minutes after the token mint; and a driver test shows a `gh run watch` that fails while the watched run's conclusion is `success` is classified `driver-error` (exit 1, paged as a credential failure), never `blocked` (exit 2, "Stage 3 failed").
Lane: any
Review-minutes: 10
Unattended: never
Filed: 2026-11-04
Issued: 2026-11-04
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/577

## Observed

Every scheduled nightly from 2026-10-29 to 2026-11-04 ends the same way, about 60
minutes after the job starts, while the driver is watching the PyAutoHeart
`release-integrate.yml` run (Stage 3):

```
failed to get run: HTTP 401: Bad credentials (https://api.github.com/repos/PyAutoLabs/PyAutoHeart/actions/runs/41804300905?exclude_pull_requests=true)
nightly: failed run's artifact 'release-stage-report' not downloadable
🚨 *nightly release stopped* — Stage 3 (release-fidelity integration) failed — <...runs/41804300905|run>
##[warning]The driver stopped at a gate (exit 2); no release was made. This is the gate working
Token expired, skipping token revocation
```

| Nightly run (PyAutoBrain) | Start | 401 at | Heart integrate run it was watching | Its real conclusion |
|---|---|---|---|---|
| 40840009792 | 2026-10-29 08:08 | 09:08 | 40842185049 | success |
| 41024762702 | 2026-10-30 08:11 | 09:11 | 41026647430 | failure (autogalaxy guides, real) |
| 41183039794 | 2026-10-31 08:03 | 09:04 | 41184365143 | failure (autogalaxy guides, real) |
| 41290517021 | 2026-11-01 08:50 | 09:51 | 41291876649 | success |
| 41416875388 | 2026-11-02 08:58 | 09:58 | 41419508621 | success |
| 41608230314 | 2026-11-03 09:06 | 10:06 | 41611102721 | success |
| 41801624733 | 2026-11-04 08:43 | 09:43 | 41804300905 | success |

Five of the seven nights the integrate run actually passed; the page said it failed.
No nightly has reached step 5 (the readiness gate) since the activity anchor
`NIGHTLY_LAST_WINDOW_END` = 2026-10-22T07:13:10Z, so the 2026-11-01 release had to
be dispatched by hand. The standing grant is armed (`NIGHTLY_RELEASES=true`) but
inoperative.

## Cause

`@PyAutoBrain/.github/workflows/nightly-release.yml` mints **one** GitHub App
installation token (`actions/create-github-app-token@v3`, step `app_token`) and
hands it to `@PyAutoBrain/agents/conductors/release/nightly.sh` as `GH_TOKEN` for
the whole run. App installation tokens live 60 minutes. The driver's Stage 2
rehearsal takes about 20 minutes and the Stage 3 integrate run 40 to 80 minutes,
so the token expires inside `dispatch_and_await`'s `gh run watch` (nightly.sh,
around line 341). `gh run watch` returns non-zero, the function returns 2, and the
Stage 3 branch at line ~410 pages "Stage 3 (release-fidelity integration) failed"
and exits 2 — the outcome the workflow classifies as `blocked` ("the gate
working").

The step 0b token sanity check (`gh api rate_limit`, line ~167) only catches a
token that is dead at the start; it cannot see mid-run expiry. Nothing
distinguishes "the watched run failed" from "I lost the ability to watch".

## Ask

Two defects, one PR:

1. **Keep a valid token for the whole run.** Options to weigh in the plan, not
   decided here: mint a fresh token before Stage 3 (and before step 6) — e.g. the
   driver re-mints from `APP_CLIENT_ID` / `APP_PRIVATE_KEY` via the App JWT flow
   when the token is older than ~50 minutes, or the workflow splits the stages
   into separate jobs that each mint their own token and pass artifacts between
   them, or `dispatch_and_await` retries `gh run watch` after re-minting on a 401.
   Whatever is chosen, the token's permission set must stay exactly the one the
   workflow documents (actions write, contents read, issues read, variables
   write) — no PAT fallback, no widening.
2. **Classify a lost watch honestly.** When `gh run watch` fails, re-read the
   run's `conclusion` with a working token before judging: `success` → continue;
   `failure` → the existing Stage 3 page; could not read → page as a driver
   credential error (exit 1, `driver-error`), never as a gate stop. The Slack
   page and the Actions warning must not say a stage failed when it passed.

Add a test beside the existing driver tests (`tests/` in PyAutoBrain) for the
classification, and verify the token fix with one manual `dry_run=true` dispatch
that runs past the 60-minute mark.

## Not in scope

- The `NIGHTLY_LAST_WINDOW_END` anchor is behaving as designed (it advances only on
  a shipped or empty window); after the fix the first green night will release
  the whole window since 2026-10-22, which is intended.
- The 10-30 and 10-31 integrate failures were real (autogalaxy guides scripts) and
  are already fixed on main.
- Heart's own readiness verdict is unaffected; it reads the rehearsal and
  integrate artifacts regardless of the driver.

## Evidence pointers

- Nightly runs: https://github.com/PyAutoLabs/PyAutoBrain/actions/workflows/nightly-release.yml
- Latest: https://github.com/PyAutoLabs/PyAutoBrain/actions/runs/41801624733
- Heart integrate it was watching (passed): https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/41804300905
- Found 2026-11-04 in the release check-in session (release board review).
