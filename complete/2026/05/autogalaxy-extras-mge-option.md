## autogalaxy-extras-mge-option
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/65
- completed: 2026-05-10
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/66
- repos: autogalaxy_workspace
- notes: |
    Audit follow-up to PyAutoGalaxy#392. Added MGE Option B (commented out)
    alongside the existing SersicSph Option A (default) in
    extra_galaxies/modeling.py, rewrote the wrap-up MGE paragraph to point at
    the inline option, and added a "scaling_relations not applicable" section
    to extra_galaxies/README.md with cross-links to the autolens examples.
    No new scaling_relation directory in autogalaxy -- explicitly declined
    (mass-only relation; light-only analogues need velocity dispersion).
