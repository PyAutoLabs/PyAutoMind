# Make the hierarchical guide backend declarations consistent

Type: bug
Target: health_fixes
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft — blocked at Heart RED entry gate

Primary repository: @autolens_workspace.

## Incident evidence (2026-10-10)

Health workflow then bug health completed. Supported vitals tick ingested release-integrate
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/38038078541 .
Heart at 2026-10-10T16:21:14.391928+00:00: RED, score 60; exact release RED:
`release validation FAILED (stage integrate)`.
Version 2026.10.10.1.dev81101: 726 passed, 2 failed, 85 skipped, zero timeouts;
installation A–F passed. Same two failures recur from run 37907620652.
Local evidence: workspace-root `tmp/heart-red-investigation/` (artifacts, logs,
status-refreshed.json, health-refreshed.json, door.json).

## Workflow boundary

Draft only. start-dev step 0a stopped at Heart RED before planning, issue creation,
claims or source edits. Requires live scoped RED authorization. No merge or release
is authorized. Preserve Scientist adoption and Broca expansion plans. Recheck claims
and remote refs before starting. Do not modify other sessions' worktrees.

## Bounded defect and owner

`scripts/guides/modeling/advanced/hierarchical.py:250` fails backend agreement:
FactorGraphModel is_jax=False, AnalysisFactor0/1/2 is_jax=True.
The graph and HierarchicalFactor explicitly use NumPy; AnalysisImaging(dataset=...)
uses its JAX default. Confirm intended tutorial backend and align declarations
without weakening PyAutoFit's whole-graph agreement guard or changing science.
Current origin/main still contains this mismatch. Fix locus candidate: genuine
workspace example configuration. Acceptance: guide passes release profile, smoke
and applicable notebook generation, then fresh wheel integration clears this row.

## Existing-work dependency and non-duplication

A1 PyAutoFit issue #1674 / PR #1675 introduced the backend agreement gate and is
merged (0dbf258c). `complete/2026/10/search-ext-a1-declare-gate.md` explicitly records
rejection of NumPy graph/JAX children as intended. No active Mind claim/open workspace
PR addresses this guide. Pending release-blocker findings in epic review 05 concern
different paths and do not repair these declarations.
`draft/bug/health_fixes/samples_parameter_paths.md` / PyAutoFit#1327 mentions the same
guide but traces a July sample KeyError, not this SearchException; do not conflate.
Read lensing assistant guidance before finalizing the repair plan. Local workspace
main is 11 commits behind origin/main; preserve it and create an isolated worktree
from fetched current main after the gate/claim checks.

## Original user request (verbatim)

Investigate and resolve the current PyAutoHeart RED before we resume the PyAutoScientist adoption pilot. Use the health workflow first, then the bug/start-dev workflow for any fixes.

Fetch the relevant repositories, read their AGENTS.md instructions, and inspect Heart’s latest authoritative verdict and underlying evidence. Distinguish current failures from stale evidence, expected in-progress work, and unrelated problems.

Specifically check whether the failures are caused by, or already being addressed by, the ongoing PyAutoFit refactor. Find its Mind task records, issues, branches, worktrees, PRs and CI results. Trace each relevant Heart failure to concrete evidence; do not assume the refactor explains everything. Avoid duplicating work, modifying its claimed worktrees, or interfering with another session.

Briefly report each RED reason, its likely cause, related existing work, and the next action. If the refactor already covers a failure, record that dependency and identify what completion or validation will clear it. For independent failures, create bounded tasks and implement the necessary fixes through the existing workflow. Make routine decisions autonomously; ask only for genuine blockers or required Heart RED authorization, quoting the exact reasons and requested scope.

Refresh Heart through its supported procedures after fixes or completed upstream work. Do not suppress failures, weaken checks, or mark unresolved evidence green. Finish with the authoritative verdict, validation evidence, remaining blockers, and whether the Scientist dashboard phase can start.

Leave the Scientist adoption and Broca expansion plans unchanged during this work. Their implementation resumes after Heart is sorted
