## version-check-compat-floor
- issue: https://github.com/PyAutoLabs/PyAutoConf/issues/118 (closed)
- completed: 2026-07-08
- prs: PyAutoConf#119 (merged 452f0f7)
- notes: |
    R2 of the version-pinning design review (PyAutoBuild#118). check_version
    enforces a compatibility floor, not exact match: floor precedence
    minimum_library_version -> workspace_version (legacy, as floor) ->
    version.txt; installed < floor raises; newer passes with git-pull warn
    beyond 30 days; unparseable warns; advice never suggests == pins.
    117 tests (7 new). Heart YELLOW 6-reason set acked in-session at ship.
    Follow-up: workspace general.yaml adoption of the new key.
