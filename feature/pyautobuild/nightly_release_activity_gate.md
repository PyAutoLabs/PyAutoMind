# Nightly releases with an activity gate

Type: feature
Target: pyautobuild
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised

Nightly/routine releases with an activity gate: switch from ad-hoc manual
releases to a scheduled dispatch of the release pipeline (cron in
`release.yml` or a Heart/Brain-driven routine). The nightly run must first
judge whether any work merged in the past 24h (commits/merged PRs across the
release-relevant repos — libraries, workspaces, HowTo) and bypass the release
entirely on quiet days, reporting "no activity, skipped" rather than cutting
an identical version. Releases still require Heart GREEN, and a scheduled
release that would ship a known-red item should stop and page the human
instead. Design first, then implement behind human review.

## Design constraints (from the 2026-07-09 session that conceived this)

- **Releases stay `human-required` under the autonomy contract** — this task
  automates the *dispatch cadence*, not the human accountability. The design
  must say explicitly where the human sits: e.g. the nightly run prepares and
  validates everything and pages for a one-tap approval, or the human
  pre-authorises a bounded window; pick one and defend it.
- **Activity gate**: "work merged in the past 24h" needs a concrete definition
  — merged PRs / pushed commits to `main` across the 5 libraries, 3
  workspaces, 3 HowTo repos (the release-relevant set from `repos.yaml`).
  Version-stamp/notebook-regeneration commits made by the release pipeline
  itself must not count as activity (else every release triggers the next).
- **Heart GREEN is the gate, unchanged** — the nightly path must call the same
  `pyauto-heart readiness` release gate as a manual release; STALE/YELLOW do
  not pass for releases. A known-red item (e.g. an open release-blocking
  issue like PyAutoBuild#126) stops the run and notifies (reuse the morning
  Slack webhook plumbing for paging).
- **Skip must be loud**: a bypassed night reports "no activity, skipped"
  through the same notification channel, so silence always means something
  broke.
- **Version scheme**: nightly cadence fits the date-based YYYY.M.D.B scheme;
  the design should cover the build-number choice and what happens on
  same-day re-runs.
- Interactions to cover: rehearsal vs live (`RELEASE_MODE`, `rehearsal`
  input), TestPyPI rehearsal as the nightly's dry-run mode option, and how
  this composes with `pre_build` (which currently asks a human for the minor
  version).

Phase 1 = design note reviewed by the human (this prompt's deliverable);
phase 2 = implementation behind that reviewed design.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake; header hand-corrected (docs/workspaces/small/safe → feature/pyautobuild/large/human-required) per the known intake-override limitation -->
