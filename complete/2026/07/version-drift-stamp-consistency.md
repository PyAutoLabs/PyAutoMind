- issue: none (the prompt was never issued — the fix shipped inside a `/wake_up` session's branch)
- delivered-by: **PyAutoBrain#144** — commit `e26ab17` *"fix: version_drift checks stamp consistency, not equality-to-release-tag"* (2026-07-19, branch `claude/wake-up-u53v8z`)
- classification: library (PyAutoBrain) — bug
- LEDGER BACKFILL, not new work: this record was written 2026-08-08 when the prompt was
  picked up for development and found already delivered. No code was written for it.
  PyAutoBrain#144 had **no** completion record until this one, so the ledger carried a gap.
- prompt Status was stale: it read `fix-implemented-on-branch (claude/wake-up-u53v8z) —
  pending review/merge`. That branch merged 2026-07-19; the status was never advanced,
  which is what made the prompt look open.

## What was wrong

`bin/version_drift.sh` compared each library/workspace's committed source version stamp
(`*/__init__.py` `__version__`, workspace `version.txt`) against the latest PyAutoLens
**release tag** and flagged any mismatch as drift. The release design deliberately
abandoned that invariant: `release.yml` stamps `__version__` into the wheel build tree
only and does **not** commit it back, because daily "Update version to X" commits to
every library main were the noise engine behind the June/July 2026 accidental-release
cascade (PyAutoBuild#118 / #120). pip users get the version from the stamped wheel;
source checkouts stay frozen.

So the check reported drift after **every** release, indefinitely — pure `/wake_up`
noise, and misleading, since it read as a release defect when the release was fine.

## What shipped

**Option 2 of the three the prompt offered** — honour the freeze, flag only
*non-uniform* stamps:

- The invariant is now "every coupled repo carries the SAME stamp as its siblings";
  a repo out of step with the consensus is flagged. The latest release tag is shown
  for context only, with a consensus trailing the tag reported as the expected freeze
  rather than drift.
- `gh` became optional — the reference tag is informational, so the consensus check
  runs on local stamps without it, which is what makes the script usable in web/CI
  sessions.
- Fixed a stale stamp path left by the organ rename: `PyAutoConf/autoconf` →
  `PyAutoNerves/autonerves`.
- Both documentation updates the prompt required: the `version_drift.sh` header comment
  (which still described the tag-equality model) and the `/wake_up` skill step-5 wording.

Verified in that PR: uniform frozen stamps read clean; a single out-of-step stamp is
still flagged — i.e. the reframe did not simply disable the check.

## Verification done before retiring the prompt (2026-08-08)

- `git merge-base --is-ancestor e26ab17 origin/main` → true, so the fix is on main.
- Read the shipped `bin/version_drift.sh`: header now documents the freeze and the
  consensus invariant; no `== latest release tag` comparison survives.
- Read `skills/wake_up/wake_up.md` step 5: reworded to "version-stamp *consistency
  across the coupled libs + workspaces* … the latest release tag is shown for context
  only". Both doc requirements satisfied.

## Note

Option 3 (retire the script in favour of Heart's `version_skew` check) was not taken
and remains a live option — `version_drift.sh` still exists. Nothing depends on
revisiting it; recorded only so a future reader knows it was considered and left open
rather than overlooked.

## Original prompt

# version_drift.sh reports permanent false drift — asserts an abandoned invariant

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: fix-implemented-on-branch (claude/wake-up-u53v8z, PyAutoBrain) — pending review/merge

`PyAutoBrain/bin/version_drift.sh` compares each library/workspace's committed
source version stamp (`*/__init__.py` `__version__`, workspace `version.txt`)
against the latest PyAutoLens **release tag**, and flags any mismatch as drift.
That invariant (committed source stamp == latest release tag) was **deliberately
abandoned** by the release design.

Evidence (2026-07-19 wake-up): reference tag `2026.7.19.1` (published 13:52),
but every stamp — PyAutoNerves / PyAutoArray / PyAutoFit / PyAutoGalaxy /
PyAutoLens and the autofit/autogalaxy/autolens workspace `version.txt` — reads
`2026.7.9.1`. Verified against GitHub `main` **and** the `2026.7.19.1` tag
commit (identical blob SHA `19b7d518`): the source stamp is frozen there too, so
this is not container/mirror staleness — the stamp genuinely is not bumped on
release.

Root cause (working as intended, NOT a release bug): `PyAutoHands/.github/
workflows/release.yml` (step "Stamp version in build tree", ~L394-403) seds
`__version__` into the **wheel build tree only** and does not commit it back.
The inline comment is explicit: *"the stamp is NOT committed back to the library
repo. Daily 'Update version to X' commits to every library main were the
stale-CI/noise engine behind the June/July 2026 accidental-release cascade
(PyAutoBuild#118 / #120); pip users get __version__ from the stamped wheel,
source checkouts use PYAUTO_SKIP_WORKSPACE_VERSION_CHECK."* So PyPI wheels are
correctly versioned; the committed source stamp is intentionally frozen.

Consequently `version_drift.sh` will report drift after **every** release,
indefinitely (the source stamp is never advanced again) — pure noise in the
`/wake_up` digest, and misleading: it reads as a release defect when the release
is fine.

Fix options (pick during triage):
1. **Re-point the reference to what pip users actually get** — compare the
   published PyPI / wheel version per package against the latest release tag
   (the meaningful post-cascade invariant), not the deliberately-frozen source
   stamp.
2. **Honor the documented skip semantics** — treat a uniformly-frozen source
   stamp as expected (mirror `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK`), only
   flagging *non-uniform* stamps (one repo out of step with the others), which
   is the real drift worth catching.
3. **Retire the script** if Heart's `version_skew` check (pinned-dep skew,
   already green) covers the remaining need.

Whichever is chosen, update the `version_drift.sh` header comment (it still
describes the tag-equality model) and the `/wake_up` skill step 5 wording.

Note: this is the same class of defect as the origin drift-check false-positive
fixed on the `claude/wake-up-u53v8z` branch (repos_sync.py `normalize_remote`
made host-agnostic) — a wake-up check encoding an invariant that reality no
longer holds. Found during the 2026-07-19 `/wake_up` version-pin investigation.

<!-- formalised from a /wake_up investigation, 2026-07-19 -->
