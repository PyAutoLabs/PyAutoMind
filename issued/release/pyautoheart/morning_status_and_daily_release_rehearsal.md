# Morning status message + routine cron re-enable + daily release in rehearsal mode

Type: release
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBuild
- PyAutoMind
- PyAutoFit
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised

## Original request (verbatim)

I recently disabled a number of nightly (or less than daily) auto runs because it was bloating my email. However, PyAutoHeart is now green, CI is passing and I think it would be good to have a nightly task which gives me an email (or ideally a Slack message, but make this follow up if it requires faff with manual inputs) that every morning says 'all is ok' or 'this is a problem'. Also: review all nightly / routine builds and work out if there is a better or more optimal setup. I want to get automated daily release back very soon too, perhaps set up but temporarily publishing to test PyPI (via rehearsal) mode for a bit, then switch over.

## Fable review of the routine-build landscape (2026-07-08)

Every routine cron was paused org-wide on 2026-07-06 with a uniform
`--- PAUSED 2026-07-06 ---` comment marker; each workflow keeps its
`workflow_dispatch` trigger. Inventory of paused crons:

| Workflow | Cadence (paused) | Notes |
|---|---|---|
| `PyAutoBuild/release.yml` | daily 02:00 UTC weekdays | Already has a `rehearsal` input: true = build + publish to TestPyPI only, no PyPI/tag/commits. |
| `PyAutoHeart/heart-health.yml` | daily 06:00 UTC | The authoritative health verdict; writes README badge, tracking issue, Pages board. |
| `PyAutoMind/morning_status.yml` | daily 05:00 UTC | Slack **user-facing update digest** (last-24h commits, Claude-summarised). Slack webhook secret `PYAUTO_UPDATE_WEBHOOK_URL` already exists and works — Slack is NOT faff. |
| `PyAutoHeart/workspace-validation.yml` | Mon 03:00 UTC | Weekly smoke. |
| `PyAutoHeart/url-check.yml` | Mon 04:00 UTC | Weekly. |
| `PyAutoBuild/python_matrix.yml` | Mon 03:00 UTC | Weekly, off-cycle from daily release. |
| `PyAutoFit/nss_install_smoke.yml` | Sun 03:00 UTC | Weekly; also runs on PR. |

The email bloat came from per-workflow GitHub failure notifications. The fix is
not fewer checks — it is one aggregated morning verdict and muted per-run email.

## Recommended design (for the start_dev plan to refine)

1. **One morning Slack message, built on Heart.** Re-enable the
   `heart-health.yml` daily cron and append a Slack notifier step (same
   webhook-secret pattern as `morning_status.yml`, likely a dedicated
   dev-channel webhook rather than the user-facing update channel): one line —
   "All is OK" or "Problem: <what>" — plus a link to the Pages board. The
   health job should aggregate the latest scheduled-run conclusions of the
   other routine workflows (release rehearsal, weekly smokes) so a single
   message covers everything; individual GitHub email notifications get muted.
2. **Daily release back in rehearsal mode.** Re-enable the `release.yml`
   weekday cron with rehearsal behaviour controlled by a repo variable (e.g.
   `vars.RELEASE_REHEARSAL`), since schedule events cannot pass
   `workflow_dispatch` inputs. Flipping to real PyPI is then a one-variable
   change with no commit — and stays a human action.
3. **Re-enable the weekly crons** (workspace-validation, url-check,
   python_matrix, nss_install_smoke), staggered ahead of the Monday morning
   message so their results are covered by it.
4. **`morning_status.yml` (user digest)** is a separate audience
   (science users, not organism health); re-enabling it is a one-line
   uncomment and can ride along, but keep it a distinct message/channel.

Sequencing on a weekday: release rehearsal 02:00 → heart-health 06:00
(covering the rehearsal outcome) → one Slack message ~06:15 UK morning.

Open questions for planning: which Slack channel/webhook for the health
message (new secret vs reuse); whether heart-health polls sibling repos' run
conclusions via `gh api` or the workflows report inward.

Follow-up (explicitly deferred by the user): only if Slack turns out to need
manual setup faff, fall back to a single daily email — but the existing webhook
suggests it will not.

The TestPyPI → real-PyPI switch is **human-only**; this task sets up rehearsal
mode and the flip stays with the user.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake; header + body hand-fixed by Fable (title, difficulty small→medium, priority normal→high, repos expanded) -->
