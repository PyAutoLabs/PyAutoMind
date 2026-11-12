# Coordinated public framing: the three autos

Targets: @PyAutoLens @PyAutoGalaxy @PyAutoFit
Type: docs
Consequence: judge
Status: approved narrow six-introduction implementation.
Issued: 2026-11-12
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/832

## Original request (verbatim)

Review the public-facing GitHub pages, READMEs, documentation and introductory material for PyAutoLens, PyAutoGalaxy and PyAutoFit. Update their framing around **automated modelling, automatic differentiation and increasingly autonomous workflows**—the “three autos”—as a consistent but understated theme.

Explain these capabilities through concrete scientific uses, with emphasis appropriate to each package. Preserve useful existing content and avoid repeating the slogan everywhere or overstating current capabilities.

Stop presenting **PyAutoLens-JAX** as a separate product or current name: use **PyAutoLens**, describing JAX as its numerical backend where relevant. Preserve historical titles and citations. Apply the same naming principle to PyAutoGalaxy and PyAutoFit.

Audit the relevant surfaces, propose a coordinated edit plan, and distinguish released capabilities from work in progress before making changes.

## Audit checkpoint — 2026-11-12

- Public content unchanged; plan awaits human approval. No issue, PR, commit or push.
- Review artifact: /mnt/c/Users/Jammy/Workspace/Science/scratch/three_autos_public_framing_2026-11-12/audit_and_plan.html
- Verified live PyPI version 2026.11.12.1 for all three libraries; inspected matching release tags and current remote main.
- Proposed passes: library READMEs/docs; workspace introductions and assistant descriptions; shared homepage/organization profile. No core API work.
- Additional shared target: PyAutoLabs/.github profile/README.md (read remotely; checkout survey pending).
- Preserve historical titles/citations, existing Lens paper edit and untracked Lens workspace dataset.
- Heart at entry YELLOW, release YELLOW/monitoring RED; experimental methods and EP readiness must not be advertised as generally stable.
- Active claim guard passed; unregistered prior worktree warnings recorded in review artifact. Recheck before worktree setup.
- RTD web retrieval was cached; direct live access 403. Galaxy assistant SSH fetch failed; public README read through GitHub connector.
- Next: human approves coordinated editorial scope; then follow create_issue/start_library/start_workspace in bounded repository phases.
- Tier: judge — merge mode: human /prm.

## Approved scope supersedes broad audit

Edit only README.md and docs/index.md in the three libraries. Bold only auto in automated, autodifferentiable and increasingly autonomous; retain explicit GPU acceleration. Preserve all other content and historical citations. User approved the narrowed plan and requested this typography/GPU emphasis. No API, tutorial, workspace, assistant or shared homepage edits.

## Implementation checkpoint — 2026-11-12

- Completed only README.md + docs/index.md in PyAutoLens, PyAutoGalaxy, PyAutoFit; bold auto prefixes, explicit GPU support and Lens naming correction.
- Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/three-autos-public-framing; branch feature/three-autos-public-framing in all three. Changes uncommitted; no PRs.
- Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/three_autos_public_framing_2026-11-12/revised_introductions.html; three patches and six rendered excerpts alongside.
- Validation: diff --check clean; exactly six files, content from Getting Started onward unchanged; CommonMark/Sphinx renders all 18 bold auto prefixes. No numerical/API edits.
- Both base and edited Sphinx excerpt builds have exactly one existing Galaxy top-level substitutions deprecation warning; -W exits 1 on both. No full docs or numerical suite run. Author review complete, no independent review claimed.
- Logs: worktree .doccheck/build.log, .doccheck-baseline/build.log, .doccheck/heart-readiness.json.
- Heart RED 2026-11-12T17:13:20.478039+00:00: "PyAutoLens: 1 uncommitted source change(s)"; "PyAutoLens: 6 commit(s) behind origin"; "install verification FAILED (testpypi; checks F)"; "release validation FAILED (stage integrate)".
- Await live human development-only shipping override for #832 before commit/push/PR; merge/release not authorized. Preserve unrelated canonical paper changes.

## User review checkpoint — revised titles

User paused shipping and then requested preview before committing. Do not act on the earlier commit/push authorization until review resumes.
- Exact Lens README title: PyAutoLens: **Auto**mated, **Auto**differentiable and **Auto**nomous Gravitational Lensing.
- Galaxy uses the same title pattern ending Galaxy Modelling.
- Removed the added feature paragraphs in both READMEs and docs/index.md; retained two-sentence introductions with JAX, GPU acceleration and assistants. PyAutoFit unchanged in this revision.
- Reread Brain docs conductor and WRITING_STYLE; title exceptions are explicitly user-directed. Automated intro-length counts are inaccurate; direct inspection confirms two sentences per README intro.
- Updated revised_introductions.html with both full README previews; patches and rendered Sphinx excerpts refreshed in the existing scratch folder.
- No commits, pushes or PRs for the library edits. Diff checks pass; Sphinx excerpt build succeeds with the existing Galaxy metadata warning.

## Final Lens/Galaxy approval

Plain titles and concise introductions approved. Live #832 override authorizes commit/push/PR; clarification authorizes Lens/Galaxy merge after checks pass in this turn, no release. PyAutoFit stays uncommitted for later review. Prior pause superseded for Lens/Galaxy only.

## PRs open

- Lens ab0492620: https://github.com/PyAutoLabs/PyAutoLens/pull/833
- Galaxy b15de28d: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/703
- Both pending-release labels verified; required docs and unit-test jobs running. No release requested.
- Fit remains uncommitted. Keep this task/worktree open for Fit review after Lens/Galaxy merge.

## Lens/Galaxy merged; Fit remains for review

- Lens PR #833 merged fdf569cd786bcdd78566dc3dee54fff63dc2873c; Galaxy PR #703 merged 8e68a6a7edfd65692e34b9bf8072b7c19f387b92. Both branch ancestries proved against origin/main.
- All exact-head jobs passed for each: Docs, Python 3.12, Python 3.13 and no-JAX. Merge states CLEAN, freeze clear; live explicit clarification authorized merging. No release/rehearsal.
- Lens/Galaxy repo claims released; pending-release links retained. Fit remains uncommitted in the original worktree. Issue #832 remains open for this uncompleted scope.
- Next: discuss a concise PyAutoFit title/intro; no Fit shipping or merge is authorized yet. Do not remove the bundle while it contains these edits.
