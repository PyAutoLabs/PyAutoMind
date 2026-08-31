# PyAutoNerves emits a false "workspace is stale, git pull" warning…

Type: bug
Target: PyAutoNerves
Repos:
- autolens_workspace
- PyAutoNerves
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: a regression test in PyAutoNerves asserting that `check_version("2026.8.17.1", workspace_root=<workspace with minimum_library_version: 2026.7.9.1>)` emits no warning - i.e. an installed library arbitrarily newer than the floor is the passing case, not a staleness signal. The existing below-floor case (install older than the floor raises `WorkspaceVersionMismatchError`) must still pass unchanged.
Review-minutes: 20
Unattended: ready

PyAutoNerves emits a false "workspace is stale, git pull" warning on an up-to-date main workspace clone.

Running `python scripts/imaging/start_here.py` from a freshly-pulled autolens_workspace main prints:

    UserWarning: The workspace at .../autolens_workspace records library version 2026.7.9.1,
    but the installed library is 2026.8.17.1 - more than 30 days newer. The workspace examples
    and configs may lag the installed API. Pull the latest workspace:
        cd .../autolens_workspace && git pull origin main

The workspace IS on latest main (fd80ada0). Pulling again does nothing, so the remedy the warning suggests cannot ever clear it.

Root cause: `autonerves/workspace.py` (`check_version` / `_stale_workspace_message`) treats `version.minimum_library_version` from `config/general.yaml` as a proxy for how fresh the workspace clone is, and warns when the installed library's date-version is more than `_STALENESS_WINDOW_DAYS` (30) newer than it. But since PyAutoBuild#120 / PyAutoNerves#118 that key is a deliberately-bumped compatibility FLOOR - the oldest library the workspace scripts work against - not a per-release stamp of the clone's age. A workspace whose scripts require no API newer than 2026.7.9.1 keeps that floor indefinitely, so every library release more than 30 days later fires the warning permanently, on an entirely current clone. The floor's age carries no information about clone staleness.

Fix direction: decouple the staleness signal from the floor. Either drop the staleness branch entirely (the floor already covers the actionable case - an install older than the floor raises `WorkspaceVersionMismatchError`), or derive clone freshness from something that actually tracks it (workspace git commit date, or a separate release-written stamp) and only then suggest a pull.

Note `autolens_workspace/config/general.yaml` already carries a comment telling main-branch users to set `workspace_version_check: False`. That is a documented workaround for this false positive, not a fix - it disables the whole check, including the floor guard that is genuinely useful.

Type: bug
Target: PyAutoNerves
Witness: a regression test in PyAutoNerves asserting that `check_version("2026.8.17.1", workspace_root=<workspace with minimum_library_version: 2026.7.9.1>)` emits no warning - i.e. an installed library arbitrarily newer than the floor is the passing case, not a staleness signal. The existing below-floor case (install older than the floor raises `WorkspaceVersionMismatchError`) must still pass unchanged.

Difficulty: medium
Priority: normal

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs-autolens-workspace/587689b4-8d34-458f-88dd-437453d4d748/scratchpad/intake_raw.md -->
