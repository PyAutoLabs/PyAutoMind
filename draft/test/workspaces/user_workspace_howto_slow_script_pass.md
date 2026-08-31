# User workspace + HowTo slow-script pass, driven by the ingested timings

Type: test
Target: workspaces
Repos:
- workspaces
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 8

User workspace + HowTo slow-script pass, driven by the ingested timings.

The user-facing repos (autolens_workspace 462 scripts / ~37 smoke entries, autogalaxy
182/16, autofit 39/8; HowTo repos opt-out everything-minus-no_run: HowToLens 57+50nb,
HowToGalaxy 39+32, HowToFit 20+15) run the same reusable smoke workflow with a different
env profile: `PYAUTO_SMALL_DATASETS=1` plus skip vars the _test repos lack
(PYAUTO_SKIP_FIT_OUTPUT, PYAUTO_SKIP_VISUALIZATION, PYAUTO_SKIP_CHECKS). Fast-mode numpy
scripts run 5-12s, mostly the ~5-7s import floor — autolens import time was already
reduced recently, so there is less low-hanging fruit — but the user suspects some big
bottlenecks remain.

Using the phase-1/2 per-script timing surface and the phase-4 digest: identify the slowest
scripts/notebooks per user-facing repo, diagnose each (import floor vs compile vs
execution vs output/plot work the skip vars should already suppress), and fix the genuine
bottlenecks WITHOUT degrading the user-facing prose or realism — these are teaching
surfaces; content changes are conservative and levers are profile/env/dataset-cap side
first. Where a fix belongs in shared machinery (profile yaml, autonerves, PyAutoHands
runner) route it there rather than per-script hacks. Existing adjacent drafts to fold in
or supersede explicitly: `draft/test/workspaces/slowest_smoke_gate_scripts.md`,
`draft/test/pyautoheart/smoke_relevance_gate.md`.
