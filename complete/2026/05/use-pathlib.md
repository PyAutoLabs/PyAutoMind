## use-pathlib
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1257
- completed: 2026-05-07
- library-prs:
    - https://github.com/PyAutoLabs/PyAutoConf/pull/104
    - https://github.com/PyAutoLabs/PyAutoFit/pull/1258
    - https://github.com/PyAutoLabs/PyAutoArray/pull/300
    - https://github.com/PyAutoLabs/PyAutoGalaxy/pull/388
    - https://github.com/PyAutoLabs/PyAutoLens/pull/497
- workspace-prs:
    - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/59
    - https://github.com/PyAutoLabs/autolens_workspace/pull/128
    - https://github.com/PyAutoLabs/autolens_workspace_developer/pull/50
    - https://github.com/Jammy2211/autofit_workspace_developer/pull/15
    - https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/12
- notes: |
    Replaced os.path.* and bare path.* with pathlib.Path across 5 libraries
    and 5 workspaces. ~700 references converted. 3,188 library unit tests
    pass; 36/36 workspace smoke tests pass. No public API changed.
    Canonical autogalaxy_workspace and autolens_workspace pull skipped due
    to in-progress smoke-test-optimization dirty state — will land when
    that task ships.

## Original prompt

Most examples now use Pathlib, but there are still some os.path.join uses from
legacy.

Can you update all source code and workspaces to not use path.join at all
and always use Pathlib?

This should aspan all source code, workspaces, etc, no more os.path!