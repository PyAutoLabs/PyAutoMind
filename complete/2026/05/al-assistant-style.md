## al-assistant-style
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/160
- completed: 2026-05-16
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/161
- merge-commit: fd80fa45
- summary: |
    Added autolens_workspace/skills/al_assistant_style.md as the canonical
    writing guide for PyAutoLens-Assistant skills (four required properties,
    adaptive depth, Orient → Ask → Branch → Combine conversation arc, voice
    do/don't rules). Rewrote skills/al_load_results.md against it: same
    technical content, restructured from "Steps 1..7" into a conversation
    arc with six narrative sub-task branches. Updated skills/README.md to
    reframe the folder as PyAutoLens-Assistant and flag the style guide as
    "read first."

    Style guide is treated as iteration round 1 — expected to evolve as
    more skills land. Future skills surfaced by name in al_load_results'
    "Skill combinations" section: al_load_results_many (bulk), al_compare_fits,
    al_refit_with_perturbation, al_plot_caustics.

    Shipped in parallel with jax-phase3-adoption (which also held
    autolens_workspace) via a separate worktree on disjoint files (skills/
    only). No merge conflicts.
