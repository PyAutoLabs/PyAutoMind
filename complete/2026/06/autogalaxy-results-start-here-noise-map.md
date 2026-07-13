## autogalaxy-results-start-here-noise-map
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/113
- completed: 2026-06-09
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/112 (merged de9a355)
- repos: autogalaxy_workspace
- notes: The latest full release report failure for `scripts/guides/results/start_here.py` came from a local checkout that was behind `origin/main`. The saved combined FITS stores the noise map with zero-valued masked pixels, so the guide must reload it with `check_noise_map=False`; that fix was already merged in PR #112 as part of `latent-jax-release-failures`. Verified the active worktree on `origin/main` reloads the saved result dataset successfully and fast-forwarded the canonical `autogalaxy_workspace/main` checkout to include the fix. Closed duplicate issue #113 without opening a no-op PR.
