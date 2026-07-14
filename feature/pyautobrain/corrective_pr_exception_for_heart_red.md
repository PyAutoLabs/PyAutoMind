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
