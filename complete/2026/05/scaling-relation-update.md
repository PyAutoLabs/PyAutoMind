## scaling-relation-update
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/141
- completed: 2026-05-10
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/142
- repos: autolens_workspace
- notes: |
    Refreshed imaging/features/scaling_relation/modeling.py to modern API
    (MGE + Isothermal + shared scaling_factor*L^scaling_exponent), added
    paired imaging simulator, and added new group/features/scaling_relation
    feature with three-tier modeling.py + standalone modeling_for_luminosities.py
    mirroring the SLaM source_lp[0] step.

    Two follow-up prompts queued:
      - workspaces/scaling_relation_csv_loader.md (CSV-driven centres/luminosities)
      - workspaces/autogalaxy_extra_galaxies_audit.md (autogalaxy_workspace parity)
