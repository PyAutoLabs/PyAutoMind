## rst-to-myst-md
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1245
- completed: 2026-05-04
- library-prs:
  - https://github.com/PyAutoLabs/PyAutoFit/pull/1246
  - https://github.com/PyAutoLabs/PyAutoGalaxy/pull/383
  - https://github.com/PyAutoLabs/PyAutoLens/pull/487
  - https://github.com/PyAutoLabs/PyAutoArray/pull/294
- notes: Converted prose `.rst` docs to MyST `.md` across all four libraries using `rst-to-myst`; kept `docs/api/*.rst` as native RST since autosummary directives don't gain readability from the conversion. Branches sat for ~3 days while main advanced 7-15 commits per repo (jax cleanup, weak-lensing additions, EP cavity-message factor, etc.). Caught up via merge: the only docs-touching commits on main were two automated `2026.5.1.1`/`2026.5.1.4` Colab URL-tag bumps. Resolved modify/delete conflicts on the `.rst` siblings by keeping the deletions; ported the URL bump (`2026.4.13.6` → `2026.5.1.4`) to 1 file in PyAutoFit, 7 in PyAutoGalaxy, 7 in PyAutoLens; PyAutoArray merged clean. PRs squash-merged library-first.
