## group-slam-prior-clamp
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/131
- repos: autolens_workspace
- notes: |
    Cluster C of the recent release-prep triage. Two group SLaM scripts
    (scripts/group/features/{linear_light_profiles,pixelization}/slam.py)
    crashed with PriorException at `mass.einstein_radius = af.UniformPrior(
    lower_limit=0.0, upper_limit=min(5 * 0.5 * total_luminosity**0.6, 5.0))`
    when PYAUTO_TEST_MODE=2 produced zero linear-light intensities, making
    upper_limit==lower_limit==0. PR #117 (Cluster F triage, merged 2026-05-02)
    fixed exactly this pattern in `linear_light_profiles/slam.py`'s
    `source_lp_1` (line 246) but missed two siblings: `mass_total` in the
    same file (line 704) and `source_lp_1` in `pixelization/slam.py` (line
    234). Verbatim mechanical port of PR #117's clamp prefix
    (`luminosity_cap = ...; upper_limit = min(luminosity_cap, 5.0) if
    luminosity_cap > 0 else 5.0`) to both missed sites. Verified locally —
    `linear_light_profiles/slam.py` now reaches `mass_total[1]` (the
    previously-buggy phase) and completes; previously crashed there.
