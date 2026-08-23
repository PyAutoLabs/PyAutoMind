# PyAutoConf rename leftovers in Brain functional surfaces

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-19 (backfilled from git)

Found by the 2026-08-19 readability census (#237). The PyAutoConf → PyAutoNerves
rename (package `autoconf` → `autonerves`) was fixed in the reader-facing docs
(ORGANISM.md, docs/example.md, skill prose), but these FUNCTIONAL sites still
carry the old name and need per-site verification, not a blind rename:

- @PyAutoBrain/config/policy.yaml:74 — unit-test location map entry
  `autoconf: PyAutoConf/test_autoconf`. Is the map keyed by package (should the
  key become `autonerves: PyAutoNerves/test_autonerves`?) and does anything
  still resolve the old path?
- @PyAutoBrain/config/policy.yaml:84 — the nightly activity gate's
  `relevant_repos` lists `PyAutoConf`. A renamed GitHub repo answers via
  redirect for some API calls but not all — verify whether activity on
  PyAutoNerves is being COUNTED by the gate today, then update the list (and
  check `tests/test_activity_gate.py:143`, which pins the old name in its
  fixture).
- @PyAutoBrain/bin/ensure_workspace_labels.sh:20 — comment names
  `rhayes777/PyAutoConf`; verify the script's live repo list.
- @PyAutoBrain/agents/conductors/health/health.sh:208 — comment example only.
- @PyAutoBrain/skills/repo_cleanup/reference.md:128 — "Owner mapping:
  PyAutoConf/PyAutoFit → `rhayes777`" is stale beyond the name: the body map
  says PyAutoLabs owns PyAutoNerves and PyAutoFit. Fix the mapping, and check
  whether any repo_cleanup behaviour actually keys on it.

Acceptance: grep for PyAutoConf/autoconf across PyAutoBrain returns only
deliberate historical references; the activity gate demonstrably counts a
PyAutoNerves commit; tests updated.
