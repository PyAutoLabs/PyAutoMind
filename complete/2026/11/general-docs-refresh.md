# General documentation refresh

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/847 (closed)
Completed: 2026-11-12

## Merged scope

Refreshed General documentation for Lens and Galaxy: workspace navigation, practical configuration examples, model composition, likelihood guides, scientific citations, papers and credits. Kept AI assistance optional. Corrected the positions API and source-radius prior, regenerated the affected diagram, and retained old page anchors. Added 26 Lens and four Galaxy literature applications. The likelihood README now indexes 37 current notebooks.

Installation, Overview, Tutorials and Community were not modified by this task. Galaxy's root toctree only gained its existing Papers page under General. No runtime library APIs changed.

## Merge receipts

- https://github.com/PyAutoLabs/PyAutoLens/pull/848 — f0ce4e3c92efa47b177cc5da679c158f7c1677a8
- https://github.com/PyAutoLabs/PyAutoGalaxy/pull/708 — 7872fdf9d3ea7457b3b39079c63596863ad6033a
- https://github.com/Jammy2211/autolens_likelihood_function/pull/1 — f670d8fe5825a4f3c62275784f2981159df5b08c

Each feature head is confirmed as an ancestor of origin/main. Both library PRs passed Docs, Python 3.12, Python 3.13 and no-JAX checks. The likelihood repository has no CI; the live human explicitly authorized merging it. Freeze clear. No merge-blocking review findings; same-session review, not independent-model approval.

## Validation

39 Python example blocks passed, including real result/positions calculations on synthetic data. Full Sphinx builds succeeded without warning regression; focused General builds had zero warnings. 821 local links/fragments, legacy anchors, 83 workspace paths and 101 protected files passed. 198 external URLs returned 200; 19 publisher/Slack URLs returned 403 and remain unverified. No 404s. Full numerical suites passed in GitHub CI, not rerun locally for this docs-only task.

## Authorization and release state

Development shipping used the recorded live Heart RED override, "I authroize". The separate live merge command was: "Check Lens CI again. If it's all green, merge all three PRs, including the likelihood repo with no CI, and close out the task." Heart RED was not cleared and no release was performed.


## Evidence and follow-up

Human review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/general_rtd_audit_2026-11-12/applied/.
Merge receipts and validation evidence retained under /home/jammy/Code/PyAutoLabs/.task-logs/general-docs-refresh/.
No remaining implementation work. Release tracking remains with the normal release workflow.

## Original prompt

# General documentation refresh

Consequence: undeclared — human review; local application only, no PRs.

## Request

Review the General sections of the PyAutoLens and PyAutoGalaxy Read the Docs sites.

Use the recently merged New User Guides as the editorial reference:
PyAutoLens PR #839 and PyAutoGalaxy PR #705.

Aim for short introductions, plain headings, practical examples and clear next steps. Remove repeated explanations, promotional language and excessive AI framing. AI assistance should be optional and briefly introduced, with a useful prompt where appropriate.

Preserve scientific explanations, equations and examples that readers need. Do not shorten technical material merely to reduce word count. Suggest diagrams only where they explain something more clearly.

Read PyAutoBrain’s people-facing writing guidance. Audit the actual pages, links and relevant source code. Identify duplication, outdated claims and material that belongs elsewhere. Keep Lens and Galaxy consistent while preserving their scientific differences.

First show me your findings and proposed structure. Then draft previews for review before applying changes. Do not raise PRs or modify Installation, Overview or Tutorials.

## Approval

Looks good, apply these changes and run the example and Sphinx checks. Keep Installation, Overview and Tutorials untouched, and don't raise any PRs yet.

## Local implementation

- Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/general-docs-refresh
- Branch: feature/general-docs-refresh in PyAutoLens, PyAutoGalaxy and autolens_likelihood_function.
- Apply approved General drafts and bibliographies; expose Galaxy Papers in the General toctree; repair the likelihood README.
- Run all edited Python snippets, check configuration overrides, build full and focused Sphinx sites, preserve old anchors, check links and protected-file identity.
- General-only scope is disjoint from installation-docs-polish, following the user's explicit instruction to leave those sections untouched.
- External issue/PR and shipping steps deferred: the current deliverable is local applied changes and validation, not publication. No merge authority.
- Validation scripts and logs: worktree validation/ directory. Human bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/general_rtd_audit_2026-11-12/applied/.

## Shipping authorization

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/847
Issued: 2026-11-12

User: "Looks good, commit and push these changes and open PRs for Lens, Galaxy and the likelihood repo. Don't merge yet."

User authorized the surfaced Heart RED development-only override: "I authroize". No merge or release.

## Open PRs

- PyAutoLens: https://github.com/PyAutoLabs/PyAutoLens/pull/848 (`49fa6e5ce`)
- PyAutoGalaxy: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/708 (`7b054c80`)
- Likelihood: https://github.com/Jammy2211/autolens_likelihood_function/pull/1 (`08c484a`)

All open; no merge, release or auto-merge.
