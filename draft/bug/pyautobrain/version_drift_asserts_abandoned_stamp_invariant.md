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
