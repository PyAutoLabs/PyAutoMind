## corrective-pr-heart-red (human-authorized corrective-PR exception for Heart RED — MERGED)
- completed: 2026-07-14
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/112 (CLOSED)
- prs: PyAutoBrain#113 (AUTONOMY.md exception + ship-skill links + contract test; main 1ae5ec8) + PyAutoMind#78 (- corrective-red: active.md schema note; main 66eb361) — both MERGED (squash) 2026-07-14.
- summary: Resolved the Heart-RED ship deadlock — RED forbids commit/push/PR-open at every autonomy level, but Heart can't clear a RED until the fixing source reaches main + wheels rebuild + release-integration validation passes, so the fix for the named RED defect couldn't ship. Added a narrow, auditable, HUMAN-AUTHORIZED corrective-PR exception to `AUTONOMY.md`: trigger (RED + a source fix repairing a named reason); contemporaneous human authorization quoting the exact RED reason + approving the specific corrective issue; permits ONLY commit/push/one pending-release PR mapped to that reason; forbids automatic merge/close/release/rehearsal/unrelated-scope (merge stays human, every release blocked while RED); four record sinks (issue, PR body, active.md `- corrective-red:` block, autonomy_log.md `corrective` row); names one reason when RED has several; parks without shipping on mixed-scope/stale-reason/missing-evidence/not-causal; recovery = human merge → fresh wheels + release-integration validation → new Heart verdict. Ship skills (ship_library/ship_workspace/WORKFLOW) link the exception, no policy duplication. Follow-up (same PR): the AGENT provides the quote — surfaces the exact RED reason string(s) verbatim from `pyauto-heart readiness` so the human authorizes what's shown, not a reconstructed string. 12-test deterministic contract test (`tests/test_corrective_red_exception.py`); 59 tests pass.
- key traps / findings: Design decisions (confirmed with human): HUMAN-ONLY (never under --auto; the invariant "Heart YELLOW/RED is never acknowledged autonomously" stays verbatim) + NAME-ONE-OF-SEVERAL RED reasons (PR scopes which reason it clears; siblings remain, release blocked until all clear). IRONY: this PR *builds* the corrective mechanism but doesn't qualify for it (repairs none of the named RED reasons) — so it shipped through organism-scoped Heart RED under the human's pre-existing "nothing branch-related" judgment (same call as the jax-gradient-optimizer-benchmark PR), authorized in-session ("Ship through the RED"). API Changes: none (doctrine/docs + tests). Contract-test seam: ship skills legitimately reference `autonomy_log.md` (calibration append) — the no-duplication test pins only exception-distinctive tokens (`- corrective-red:`, "park without shipping", "recovery sequence").

## Original prompt

# Corrective PR exception for Heart RED

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Corrective PR exception for Heart RED

This is a workflow deadlock bug in @PyAutoBrain/AUTONOMY.md and the ship_library / ship_workspace workflow: Heart RED currently forbids commit, push, and PR-open at every autonomy level, even when the proposed source fix directly repairs the exact defect named by the RED reason. Heart cannot clear that RED until the fix reaches main, fresh wheels are built, and release integration validation succeeds, so the gate makes recovery impossible without violating policy. Design and implement a narrow, auditable corrective-PR exception. It must require explicit, contemporaneous human authorization naming the Heart RED reason and approving the specific corrective task. It may permit only commit, push, and opening a pending-release feature PR whose issue, plan, and diff directly address that named reason. It must not permit automatic merge, issue close, release, release rehearsal, or unrelated scope; merge remains a separate human act and every release stays blocked while Heart is RED. Record the authorization, exact RED reason, causal mapping, tests, and validation plan in the GitHub issue, PR body, PyAutoMind active state, and autonomy calibration log. Require fresh post-merge wheel and release integration validation, followed by a new Heart verdict, before release work resumes. Define failure behavior for mixed-scope diffs, stale or changed RED reasons, multiple RED reasons, missing evidence, and a review finding that the patch is not causal: park without shipping. Update the canonical autonomy doctrine and affected ship skills without duplicating policy, add deterministic contract tests, and document the recovery sequence. This changes a hard invariant and therefore needs supervised human judgment despite being mechanically small.

Original user request verbatim: "ok, use intake to make prompt IO can run to address circular hole"

<!-- formalised by the Intake (Conception) Agent on 2026-07-14 from user-intake -->
