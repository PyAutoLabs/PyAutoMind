## nightly-release-activity-gate
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/127 (OPEN — phase 2 pending)
- completed: 2026-07-09 (phase 1)
- prs: PyAutoBuild#128 (docs/nightly_release_design.md) + PyAutoBrain#62 (AUTONOMY.md standing grant) — both merged 2026-07-09, human-directed ("go") after design review
- note: phase-1 design for unattended nightly live PyPI releases. Approved design: Brain-scheduled driver (nightly.sh + nightly-release.yml) composing the M1-M4 release-validation machinery; activity gate over 11 release-relevant repos (pipeline self-commits excluded); Heart GREEN required (no force input; needs phase-2 release-gate CI evidence profile); loud skip/stop via PYAUTO_RELEASE_WEBHOOK_URL; NIGHTLY_RELEASES kill switch; release.yml cron REMOVED in phase 2 (live hazard while it survives: RELEASE_MODE=live would release ungated at 2AM). AUTONOMY.md release cap now carries its sole dated exception (grant attaches to the schedule, not the pipeline). Phase 2 = feature/pyautobuild/nightly_release_implementation.md. Arming blockers: next manual live release + PyAutoBuild#126.

## Original prompt

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

- **DECIDED endpoint (user, 2026-07-09): once the next manual release
  succeeds, nightly runs perform FULL LIVE PyPI RELEASES unattended** — no
  per-release human approval. This is a deliberate, scoped exception to the
  autonomy contract's "release is always human-required" invariant, so phase 1
  must include the dated doctrine edit to `PyAutoBrain/AUTONOMY.md`: the
  scheduled-nightly path (activity-gated, Heart-GREEN-gated) is
  human-pre-authorised as a standing grant; manual and agent-initiated
  releases stay `human-required`. The human's role moves to: a kill switch
  (e.g. a `NIGHTLY_RELEASES` repo var to pause the schedule), paging on any
  red/anomaly, and reviewing the morning digest of what shipped. `pre_build`'s
  human minor-version ask must be automated on this path (date scheme derives
  it).
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
