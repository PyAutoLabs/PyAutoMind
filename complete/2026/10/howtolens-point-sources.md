# Tutorial 4 point sources

Merged https://github.com/PyAutoLabs/HowToLens/pull/108 on 2026-10-31 as ebb5b435886a6483689efcbda47f64c21e422ba0. Issue #107 closed.

All fifteen approved blocks applied, with iterative triangle explanation, workspace guide link, corrected point-source science and combined image-property output. Notebook, executed Markdown and catalogue regenerated.

All eight CI jobs passed including Python 3.12 and 3.13 smoke. Local smoke 49/49, actual solver/plots, notebook parity, navigator and tutorial completion checks passed.

Human authorized merge via prm. No release performed. Worktree cleanup awaits the human's decision about generated datasets/output. Tutorial 5 point-data addition is separate follow-on work.

## Original prompt

# Review Tutorial 4: point sources

Type: docs
Target: @HowToLens
Consequence: judge

## Original request
ok lets move on to tutoroail 4 on point sources

Yes I approve development on heart red for tutorial 4, show me the first 5 blocks for review

## Scope and review
Continue the Chapter 1 editorial review in batches of five coherent narrative/code blocks. Show proposed wording before applying it. Retain the existing numerical example, update transitions after the Tutorial 3/5 merge, clarify point-source observables and distinguish evaluating the lens equation from solving for image positions. Flag scientific corrections explicitly. Source changes and workspace setup follow approval; merge remains human /prm.

First batch: introduction, compact-source setup, compact-source image, point-source definition, point-source tracer.

## Heart RED development override
Human explicitly approved development on Heart RED for Tutorial 4. Development only; no release or failed-check bypass.
Reported reasons: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; Release readiness: release validation FAILED (stage integrate); autogalaxy: red; Release validation: NOT release_ready — v2026.10.31.1.dev85201 profile=release (2026-10-31T08:04:07+00:00); validation_report/stages/integrate: fail; autolens_profiling: red; Worktree drift: 0 orphan / 0 missing / 1 dirty.

Issue: https://github.com/PyAutoLabs/HowToLens/issues/107
Issued: 2026-10-31

All fifteen blocks approved, including the brief triangle explanation and workspace guide link. User authorized applying the changes and running checks. Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-point-sources/HowToLens; branch feature/howtolens-point-sources.

## Applied and validated — 2026-10-31
- All fifteen approved blocks applied; numerical example retained, combined image-property printout added.
- Notebook and executed Markdown/figures regenerated, catalogue and Colab links updated.
- Actual tutorial execution: four images, finite magnifications/delays, maximum source-plane residual 0.0005011 arcsec.
- Official Heart smoke: 49 passed, zero failures (Python 3.12); notebook format/source parity, navigator, contents, 38 tutorial completion checks and whitespace checks pass.
- Commit: 2843ea7785412ec3293c7b344cdeb72472c2abe0
- PR: https://github.com/PyAutoLabs/HowToLens/pull/108
- Current exact Heart RED reason: `release validation FAILED (stage integrate)`. Existing human development-only override applies. No release or failed-check bypass.
- Review copies: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_point_sources_2026-10-31/.
- Logs: scratch/tutorial4_runtime.log, scratch/tutorial4_render.log, scratch/tutorial4_heart_smoke.log.
- Next: human /prm after required PR checks pass; no merge authority this turn.

Close-out reference sweep: the point-solver figure-placement and grid-extent drafts still refer to the Tutorial 4 source as separate future work; neither is completed by this prose rewrite.
