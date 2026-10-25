# Pre-release documentation and configuration consistency

Type: refactor
Target: autogalaxy_workspace
Repos:
- HowToFit
- autofit_workspace
- autogalaxy_workspace
Consequence: judge
Autonomy: supervised
Issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/261
Issued: 2026-10-25

## Original request

"Can we do more heart and hygeine work before release to properly clean up loads"
"Ok do all that and the continue"

## Scope and plan

Clean the non-overlapping part of the verified hygiene findings: three adjacent documentation boundaries in HowToFit tutorial_7_the_details.py; two boundaries in autogalaxy_workspace pixelization modeling/fit scripts; six missing config keys in autofit_workspace and nineteen in autogalaxy_workspace. No changes to scientific code, output identifiers, thresholds or existing workspace overrides. Source-only main snapshots are used in session clones.

1. Combine the five adjacent documentation blocks, preserving all prose and executable AST.
2. Add only absent YAML leaves from the corresponding library defaults, preserving comments and existing values. Verify effective merged values unchanged.
3. Regenerate notebooks/catalogues through PyAutoHands; check notebook prose and code preservation and run the required workspace smoke validation where supported.
4. Keep remaining autolens_workspace work blocked by the active matrix-free task; do not take its repo claim.
5. Prepare reviewable diffs and verification. Heart remains RED; development shipping needs task-specific current authorization, separate from the earlier Nerves corrective approval. No merge, release or rehearsal.

Tier: judge — merge mode: human /prm.

## Completion

All five documentation findings removed and 25 mirror gaps accounted for without changing effective config or executable statements. Generated artifacts verified; smoke results and limitations stated. Source PRs require the existing Heart gate, never a waived test.

## Session checkpoint — 2026-10-25

Five documentation boundaries and 25 config leaves repaired locally. Executable AST, all prose, notebook code cells and effective config preserved; notebooks regenerated through Hands main and catalogues unchanged. Smoke: HowToFit 19 scripts, AutoFit 8 scripts, AutoGalaxy 14 scripts pass. AutoFit two notebook checks cannot start a kernel; empty-kernel reproduction gives `Operation not permitted (src/ip_resolver.cpp:542)`. Missing runtime evidence, not demonstrated source defect; no waiver. Required compatible-runtime notebook validation precedes any Heart RED shipping ask. Source edits remain uncommitted in the registered local branches and embedded in the health report.

Related diagnosis: HowToLens CI timing includes success workflows whose actual smoke job was skipped (run 39951551703). Full runs 39850351606 and 40092843981 execute substantially more work. Collector uses successful workflow-level duration without execution coverage, confounding the claimed 4.83x slowdown; keep finding ci_timing:HowToLens/Smoke Tests open pending comparable full-run analysis.

## Approval and runtime handoff — 2026-10-25

User: "Ok continue i approve". Retain approval to continue issue #261; no repeated approval sought for preparation or validation. Source shipping remains blocked by required notebook evidence. TCP empty-kernel launch aborts in ip_resolver; IPC empty-kernel launch also fails socket bind with Operation not permitted. This host cannot provide Jupyter validation; no tests waived or scientific source altered.

Smallest handoff: apply the preserved autofit_workspace config patch from the health report to the registered feature branch in a supported dev runtime; preserve all existing edits, inspect claims and use the normal library/Hands environment. From autofit_workspace root run `python .github/scripts/run_smoke.py`; require all eight script and two notebook records to pass, retaining exact source head, environment and JSON report. Alternatively the notebook-only shared Hands invocation may complete the missing leg if unchanged script evidence remains applicable. No release workflow required. Return this evidence to issue #261; do not mark task complete or merge. Current Heart release reasons remain install verification FAILED (testpypi; checks F) and release validation FAILED (stage integrate).

## Partial ship — 2026-10-25

Live user: "Ok do final bits and inprovememtns  and then prm what weve done". Independent passing branches shipped: HowToFit PR #76 (59e22b669f8f67f9d8d2c15613683760c3cc7e0d), autogalaxy_workspace PR #262 (801a8cef57467b0371bebb9a9d0242ba753cfd4c). Five documentation repairs plus 19 AutoGalaxy config mirrors are in PRs; six AutoFit config mirrors remain local and blocked on notebook validation. No close-out until all sibling branches are resolved. Exact RED reasons and authorization retained in active registry, autonomy log, issue and both PR bodies. No release/rehearsal; required exact-head CI and current-turn human merge authority govern prm.

## Partial merge receipt — 2026-10-25

User: "Prm but make their cu fully pass?". HowToFit #76: every exact-head workflow completed successfully, all eight jobs passed including Python 3.12 and 3.13 smoke; clean merge state. Merged and confirmed via API at bfca6a40420004b489b7ba257c415687b09249c2 (source head 59e22b669f8f67f9d8d2c15613683760c3cc7e0d). AutoGalaxy #262: 7/8 jobs passed, only Python 3.12 smoke running; no red check, no rerun or speculative source fix. Required MCP prm stop on pending. Task not complete: AutoGalaxy unmerged and AutoFit notebook evidence missing. No release, test waiver, cleanup or background action.

## AutoGalaxy merge receipt — 2026-10-25

User: "Prm I am good for you to do it". AutoGalaxy #262 confirmed merged at c40228890eabd6eaad599fea3f849026d2cf711d, source head 801a8cef57467b0371bebb9a9d0242ba753cfd4c. All three workflows completed successfully; eight jobs passed, including both Python smoke legs, all navigator checks and size guard. Clean merge state before merge. Both published PRs now merged: five doc repairs and 19 config mirrors delivered. Released their active repo claims; retained the AutoFit claim and recoverable six-leaf config patch. Task/issue remains open because AutoFit notebook runtime evidence is unavailable. No test changes, waiver, source cleanup or release.

## AutoFit validation-only draft — 2026-10-25

Explicit human "Yeah do it" to the validation-only exception. AutoFit draft PR #176, head 4778b42a1f0ce4616cd72f456e2af70a19d28852, contains exactly six additions across three config files; no scripts/notebooks/workflows modified. Existing CI is the compatible runtime for missing notebook smoke evidence. Local eight script smoke checks and effective config invariants passed. Draft/unmerged until exact-head required runs and both notebook checks pass. No test waiver, release or rehearsal; same Heart RED reasons remain.
