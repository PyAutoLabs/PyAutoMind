## euclid-version-bump-2026-5-1-4
- completed: 2026-05-08
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/13
- repos: euclid_strong_lens_modeling_pipeline
- notes: |
    One-time catchup for a missed release. Surfaced as 6 of 6 euclid
    smoke "failures" during the PR #301 (PyAutoArray) validation run —
    every euclid script raised WorkspaceVersionMismatchError because
    config/general.yaml pinned workspace_version=2026.4.13.6 against
    library 2026.5.1.4, and there was no version.txt. Bumped both files
    to 2026.5.1.4 to match the convention used by autofit_workspace,
    autogalaxy_workspace, autolens_workspace, and HowToLens.

    Root cause was a one-time gap, not a structural issue:
    pre-2026-05-01 this repo lived under Jammy2211/ and PAT_PYAUTOLABS
    couldn't push, so it was excluded from the release_workspaces matrix
    in PyAutoBuild's release.yml. PyAutoBuild PR #81 restored the
    matrix entry on 2026-05-01 14:56 UTC — but ~3 hours after the
    2026.5.1.4 release dispatched at 11:33 UTC, so the bump didn't
    auto-land. Future drift will auto-correct via the now-restored
    matrix entry; this is a single-shot catchup, not the start of a
    maintenance pattern.

    All 6 smoke scripts pass with the bumped version, no other
    failures uncovered.
