# Enrich #pipreleases Slack post with full PyAutoLens release notes

**Target:** @PyAutoBuild
**Work type:** feature (release infrastructure)
**Autonomy:** safe
**Difficulty:** small

## Original request (verbatim)

> We made it so on SLACK in #pipreleases we have updates posted, for example:
> PyAuto Updates [7:47 PM] :package: PyAuto 2026.7.9.1 released to PyPI —
> autoconf / autofit / autoarray / autogalaxy / autolens. Upgrade with:
> pip install --upgrade autolens, but can you include all the notes on what is
> included in the SLACK post when a release is successful (like are posted on
> GitHub, include GitHUB URL links but also the full notes for PyAutoLens)

## Goal

On a successful **LIVE** release, the `#pipreleases` Slack post should carry the
**full PyAutoLens release notes** (which already aggregate upstream
Fit/Array/Galaxy changes via the "Upstream Changes" section) plus **links to all
four GitHub release pages** (Fit / Array / Galaxy / Lens) — not just the current
one-line summary + Actions-run link.

Scope decision (user, 2026-07-10): **Full PyAutoLens notes** option — one
aggregated body, four release-page links.

## Current state (`PyAutoBuild/.github/workflows/release.yml`)

- `announce_release` job posts the one-liner to `#pipreleases`
  (`PYAUTO_RELEASE_WEBHOOK_URL`); `needs: [resolve_mode, version_number,
  release]`, `if: always() && rehearsal != 'true'`. Failure branch pages loudly.
- `publish_release_notes` job runs `autobuild/generate_release_notes.py` in a
  matrix over Fit/Array/Galaxy/Lens, creating GitHub Releases with full markdown
  notes. PyAutoLens's release body already includes upstream changes.
- The two jobs run in parallel and don't communicate.

## Plan

1. New helper `autobuild/slack_release_notes.py`:
   - Args: `--version`, `--result`, `--run-url` (and optional `--repo`,
     default `PyAutoLabs/PyAutoLens`).
   - On success: `gh release view <version> --repo <repo> --json body,url` to
     pull the already-generated notes + release URL. Fetch the four release URLs
     (Fit/Array/Galaxy/Lens) for the "Releases:" links line.
   - Convert GitHub markdown → Slack mrkdwn: `[t](u)` → `<u|t>`, `## H`/`### H`
     → `*H*`, keep `-`/`•` bullets, strip `---` rules.
   - Emit the Slack JSON payload to stdout: headline + upgrade line +
     `*Releases:*` links + full PyAutoLens body.
   - **Graceful fallback** to today's one-liner if the release can't be fetched
     (notes leg failed / not yet published).
   - Failure `--result` branch: preserve today's `:rotating_light:` message.
2. Wire `announce_release` to `needs: [..., publish_release_notes]` (keep
   `always()` so failures still page); call the helper to build `payload.json`,
   then `curl` it as today.
3. No change to `generate_release_notes.py` (reuse its GitHub Release output).

## Testing

- Unit-test the markdown→mrkdwn conversion and payload assembly with a captured
  PyAutoLens release body fixture (no network) — `gh` calls mocked/injected.
- `--dry-run`-style local invocation printing the payload for eyeball check.

## Notes

- No workspace impact (build-infra only).
- Slack `text` field limit ~40000 chars — generous for aggregated notes.
- Effective level under `--auto`: safe (feature cap, small difficulty) → proceed
  to PR-open; merge/close human.
