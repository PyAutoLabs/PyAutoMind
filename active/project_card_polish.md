# Cortex project card polish

Targets: @PyAutoBrain
Type: feature
Filed: 2026-10-15
Issued: 2026-10-15
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/527
Difficulty: small

## Original request (verbatim)

Looks good, improvements are dont have Locations be a drop down by make its info the top 2 pices when I click drop down on a project , but above them have in the same color font a "Registered: yyyy-mm-dd" with which replaces Registered 2026-10-15 (PyAutoCortex#67), dont include the PyautoCortex#67 as the PR number isnt useful to a humna. then under those 3 piees of information have the "current positions" with the info, have the icon with "resume subhalo" to the right of this information and just revmove the "resume subhalo" and other text as we know what an icon like that means.    I think these things are okelaunay_adapt_split_pl_eff_0: job B, numba chain at the standard 1250-pixel Delaunay mesh (8c / 96gb / 48 h); reloads job A 342231_1; the 09-07 ruling: run all datasets at 1250, no more pix1000 but anything that makes them even more human readable is appreciateed.

## Approved scope and plan

User authorized continuation: "Proceed, I override" after the layout summary and Heart RED gate.
- Show Registered, Local and RAL immediately on expanding a project, with consistent accent styling; remove the nested Locations disclosure.
- Show Current position below, with the unchanged resume payload on an icon-only copy button at the right. Retain accessible label/title and keyboard interaction.
- Improve long run description scanning through presentation only; preserve full scientific text.
- Verify focused renderer cases and phone/desktop layout, then open a PR. Human merge remains required.

Tier: undeclared — merge mode: human /prm

## Detailed implementation plan

Only PyAutoBrain source changes. Update agents/conductors/cortex/_cortex.py card renderers and scoped CSS. Extract an explicit leading Registered YYYY-MM-DD (optional Cortex PR reference) from Now for display; otherwise use an explicit ledger-opened log date, otherwise state not recorded. Never infer registration from newest update. Keep raw ledger/census/state payloads unchanged. Put Registered, Local and RAL above Current position; retain ledger access in the existing full-log link. Keep Markdown useful without JavaScript. Use the shared copy button and its existing handler, with descriptive accessibility text but no visible resume label. Render semicolon-separated clauses on separate lines in run descriptions without rewriting scientific assertions, retaining full-text expansion and escaping. Add focused tests in tests/test_cortex_conductor.py for metadata, missing dates, escaping and payload preservation. Run the Cortex tests and Brain suite, plus a mobile/desktop browser witness against actual ledger renderings. Publish through the existing Cortex refresh only after human merge.

## Branch survey

PyAutoBrain main clean; PyAutoMind main clean after fast-forward. Cortex has an active science-task claim, so no Cortex source or ledger edits. Proposed feature/cortex-project-card-polish; worktree .worktrees/cortex-project-card-polish/PyAutoBrain.

## Heart RED override

User: "Proceed, I override". Applies to this development task only, not merge or release. Exact gate reasons recorded in the issue and shipping evidence.
