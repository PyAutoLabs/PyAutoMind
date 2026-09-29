# Hands release.yml fires the visualization re-render dispatches

Type: feature
Target: pyautohands
Repos:
- PyAutoHands
Themes:
- visualization
- infrastructure
Difficulty: small
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: draft
Consequence: judge
Witness: after a release run, `gh run list -R PyAutoLabs/autolens_visualization -w render.yml` and `-R PyAutoLabs/autogalaxy_visualization -w render.yml` each show a `repository_dispatch` run carrying the released version
Review-minutes: 5
Epic: pyautoeyes-birth
Filed: 2026-09-29

## Why

The `<lib>_visualization` project repos re-render their tracked figures on a library
release: `autolens_visualization`'s `render.yml` listens for `repository_dispatch`
type `pyautolens-release`, and `autogalaxy_visualization`'s (PyAutoEyes phase 3) for
`pyautogalaxy-release`; each then fires `eyes-refresh` at PyAutoEyes so the dashboard
picks up the new render.

Today **nothing sends either event** (verified 2026-09-29: the PyAutoLens,
PyAutoGalaxy and PyAutoHands workflows contain no `repository_dispatch` sender). The
galleries therefore only re-render on a manual `workflow_dispatch`, and the Eyes
dashboard's freshness column drifts behind every release.

## Plan

In PyAutoHands `release.yml`, after the libraries publish to PyPI, add a step that
sends:

- `pyautolens-release` to `PyAutoLabs/autolens_visualization`, and
- `pyautogalaxy-release` to `PyAutoLabs/autogalaxy_visualization`,

each with `client_payload.version` set to the released version, via
`gh api repos/<owner>/<repo>/dispatches -f event_type=<event> -f client_payload[version]=<v>`
using `GH_TOKEN: ${{ secrets.PAT_PYAUTOLABS }}` (a `GITHUB_TOKEN` dispatch never
triggers downstream workflows). Skip cleanly when the secret is empty, and do not
fail the release if a dispatch fails. Keep the event names in step with PyAutoEyes
`registry.yaml` `dispatch_event`.

Human prerequisite: `PAT_PYAUTOLABS` must include both visualization repos (a
newborn repo missing from its list 403s the dispatch).
