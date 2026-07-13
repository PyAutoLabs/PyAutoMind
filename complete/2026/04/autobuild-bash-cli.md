## autobuild-bash-cli
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/67
- completed: 2026-04-30
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/68, https://github.com/Jammy2211/admin_jammy/pull/14
- repos: PyAutoBuild, admin_jammy
- notes: Added `bin/autobuild` dispatcher (16 subcommands + help system) wrapping every PyAutoBuild operation under one shell entry point alongside the existing Claude skills. `tag_and_merge.py` ported to bash; `script_matrix.py` deliberately kept Python (called by release.yml — workflow ABI). README version-bump sed step folded from the `/pre_build` skill into `pre_build.sh` (+ inferred `readme_pkg` for `autogalaxy_workspace_test`, `HowToGalaxy`, `HowToFit` which the old skill table didn't list). `/pre_build` skill collapsed to a thin wrapper around `autobuild pre_build`, mirroring `/verify_install`. The skill's old soft "stale `no_run.yaml` patterns" report was dropped — can be added back to the bash CLI later if useful.
