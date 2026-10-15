Cortex project cards now open with Registered, Local and RAL in consistent accent text, then Current position with an icon-only resume copy button at the right. The explicit registration prefix and registration PR reference are removed from the displayed Current position. Registration uses the explicit prefix or a ledger-opened note; absent dates say not recorded. Source ledgers, copy payloads and state feeds are preserved. Runs split literal semicolon-separated clauses onto readable lines; full wording remains available. Markdown mirrors the metadata order and retains the copyable prompt.

Merged PyAutoBrain#528 (545c69d; merge a21e902f030f9fec15f7bafd1e75aec93fcca601) on 2026-10-15 through human /prm; issue #527 closed. All 1274 local Brain tests passed. Both Python 3.12/3.13 CI jobs passed, including discovery and tenant-firewall steps. Four actual-ledger Chromium checks passed at 390/1280px in light/dark mode (keyboard disclosure/copy, icon geometry, expanded overflow); author visual/diff review passed. Scientific workspace smoke not applicable to a renderer-only change. Development-only Heart RED override recorded verbatim in issue, PR, active registry and autonomy log; merge separately authorized by /prm.

Cortex Dashboard Refresh dispatched at https://github.com/PyAutoLabs/PyAutoCortex/actions/runs/38795269947; Pages run https://github.com/PyAutoLabs/PyAutoCortex/actions/runs/38795298602 succeeded. Live HTML verified the registration date, unfolded locations, removal of the registration PR prose, and 9 accessible icon-only resume buttons. Preview and screenshots remain under tmp/cortex-card-polish/ in the workspace, outside the removable task worktree. Phase-2 output accounting remains separate and unimplemented.

Close-out check: task-scoped lifecycle validation passes. The global check reports an unrelated pre-existing orphan active/hst_mge_pilot_qualification.md (introduced in 37b04992); left unchanged. Reconcile reports no suspects.

## Original prompt

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

## PR ready

https://github.com/PyAutoLabs/PyAutoBrain/pull/528 — 545c69d. Full Brain suite 1274 pass; four real-ledger Chromium cases pass; author diff and visual review. Preview: tmp/cortex-card-polish/preview.html and screenshots under the workspace root. Heart RED override recorded in issue, PR, active registry and autonomy log. Human merge remains required; after merge dispatch Cortex dashboard_refresh.yml and verify the live card metadata and icon controls.
