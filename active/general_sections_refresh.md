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
