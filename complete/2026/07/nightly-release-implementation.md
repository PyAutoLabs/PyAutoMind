## nightly-release-implementation
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/127 (OPEN — tracker until armed)
- completed: 2026-07-09 (phase 2)
- prs: PyAutoBrain#63 (nightly driver + scheduler) + PyAutoBuild#129 (release.yml cron removed) + PyAutoHeart#47 (release-ci readiness profile) + PyAutoMind#43 (digest watchdog) — all merged 2026-07-09, human-directed
- note: the full nightly-release system per docs/nightly_release_design.md — nightly.sh (kill switch → same-day guard → activity gate → release-blocker check → M1-M4 validate choreography → release-ci GREEN gate, no force → live dispatch → one Slack outcome per path), activity_gate.py + first PyAutoBrain tests/, 02:00 UTC scheduler (dry_run default true), `pyauto-brain release nightly`, consult_vitals_verdict --profile. release-blocker label on 13 repos, applied to Build#126 (verified: gates-only run stops exit-2 naming it). NOT ARMED: NIGHTLY_RELEASES unset + dry_run true; arming checklist on #127. Manual live release 2026.7.9.1 dispatched same session (run 29041595906) as arming step 1.

## Original prompt

# Nightly release implementation (phase 2 of the activity gate design)

Type: feature
Target: pyautobuild
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised

Implement the reviewed nightly-release design —
`PyAutoBuild/docs/nightly_release_design.md` (merged 2026-07-09 via
PyAutoBuild#128, approved by the human; doctrine grant merged via
PyAutoBrain#62). Tracker: PyAutoBuild#127 (phase-1 comments hold the review
trail). Build exactly what the design's §10 sketches; where implementation
reality forces a deviation from the note, update the note in the same PR and
call the deviation out for review.

## Deliverables (from design §10)

- **PyAutoBrain** — `agents/conductors/release/nightly.sh`: steps 0–7 of the
  nightly sequence (design §3) — kill switch (`NIGHTLY_RELEASES`), same-day
  guard, activity gate (§4: 11-repo merged-to-main window, persisted
  window-end anchor, pipeline self-commit exclusion), `release-blocker` label
  check, the Stages 0–3 validate choreography (sequencing `validate.sh`
  Phases A→C with the `gh` dispatches run directly), readiness gate (GREEN
  only, no force input), live dispatch of `release.yml`
  (`rehearsal=false, minor_version=1`), and one Slack outcome message per
  terminal path (§6). Kill-switch/activity/label/notify logic unit-testable.
  Plus `.github/workflows/nightly-release.yml` (cron `0 2 * * *` +
  `workflow_dispatch`, `dry_run` input defaulting `true` until arming,
  secrets `PAT_PYAUTOLABS` + `PYAUTO_RELEASE_WEBHOOK_URL`) and a
  `bin/pyauto-brain release nightly` passthrough for local runs.
- **PyAutoBuild** — `release.yml`: delete the `schedule:` trigger and the
  schedule branch of `resolve_mode`; no other behaviour change. (Closes the
  standing hazard: with the cron alive, flipping `RELEASE_MODE=live` releases
  ungated at 2 AM.)
- **PyAutoHeart** — the release-gate evaluation profile (design §5): a named
  required-evidence set for the nightly gate (`ci_status`, `open_prs`,
  release-validation report, `verify_install`), dev-box-local checks
  (`repo_state`, `worktree_drift`, `script_timing`, local `test_run`)
  n/a-by-scope (never silently green), snapshot assemblable in-run in CI.
  Unknowns among required evidence stay YELLOW and stop the run.
- **Process** — create the `release-blocker` label and apply it to
  PyAutoBuild#126; teach the morning digest (PyAutoMind `morning_health`) to
  expect a nightly outcome and flag its absence.

## Constraints

- The driver is deterministic shell in CI — no LLM in the release gate.
- STALE/YELLOW/RED all stop the nightly; there is no force/ack path
  (AUTONOMY.md standing grant, 2026-07-09).
- Do not arm anything: `NIGHTLY_RELEASES` stays unset and `dry_run` defaults
  `true`. Arming is the human checklist in design §9 (next manual live
  release; #126 fixed; a dry-run nightly observed GREEN end-to-end).
- Open questions §11 were accepted as the note's committed positions
  (every-night schedule, persisted window anchor, `release-blocker` label).
