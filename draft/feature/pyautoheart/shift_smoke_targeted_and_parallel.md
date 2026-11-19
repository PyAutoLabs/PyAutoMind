# Shift workers' smoke leg runs only the affected workspaces, in parallel

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Consequence: judge
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in the cockpit for shift 2026-11-19-am, after asking "Are smoke tests or the things these orchestrator tasks running slower than they have been or they are for normal development?": "yes file it and then implement it, this is over testing and makes things too slow."

## Why

Measured in shift 2026-11-19-am (task `jax_grad_of_sersic_stellar_mass_deflections`, PyAutoGalaxy): the worker's smoke leg ran every workspace one after another — autofit nb 1.2 min, autogalaxy nb 2.5, autolens nb 5.9, autolens_workspace_test 12.8 (CI median 7.2), euclid 1.6, HowToLens ~5.8, autocti ~4.1, autocti_test — about 35–40 min of a 75-min shift, which delayed the next named task on the library. Per-script speed is normal (at or below CI medians, except autolens_workspace_test's cold-cache scripts); the cost is scope and serial order.

Sources: Heart `skills/smoke_test/SKILL.md` ("Default: run ALL six workspaces … Run a subset only when the user explicitly passes workspace names"); Brain `AUTONOMY.md` autonomous-ship gate leg 2 ("all six workspaces by default"); `pyauto-heart smoke` runs the selected workspaces serially. Shift workers are inconsistent: some ran all workspaces (213 scripts, #724), others the affected ones (99 scripts, #726).

## Proposed shape (to be planned)

- **Targeted:** select workspaces whose `chain:` in Heart `config/repos.yaml` `smoke:` contains a repo the branch changed (e.g. a PyAutoGalaxy change skips autofit, autocti, autocti_test). A `pyauto-heart smoke --changed <repos>` (or `--affected-by`) option does the selection.
- **Parallel:** `pyauto-heart smoke --jobs N` runs the selected workspaces concurrently (each already has its own cached env), with a laptop-safe default cap and per-workspace thread caps; wall time ≈ the slowest workspace.
- AUTONOMY.md leg 2 and the Heart skill default for autonomous/shift ships become "affected workspaces, in parallel"; the full serial sweep stays the default for a human `/smoke_test` and for Heart's release validation.
