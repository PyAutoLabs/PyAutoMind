# Define the cloud worker: a declared repo bundle, a preflight, a slim profile, and rules that travel

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: human-required
Priority: normal
Status: draft
Filed: 2026-11-10
Epic: autonomous-orchestrators
Consequence: judge
Witness: in a fresh cloud session holding only the declared bundle, (a) `pyauto-brain doctor` prints, per verb, which sibling repos resolve and which are missing; (b) one small task runs from start to an open PR, with every step that needed a laptop written down; (c) the worker's first API call is measured and reported (today 44k tokens for a subagent, target about 25k); (d) the session's instruction attachment lists the always-apply rules
Review-minutes: 30
Unattended: never
Lane: any

Source: the ecosystem review of 2026-11-10, findings BRAIN-1, TOK-2 and TOK-3, each confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, sections B2 and B5, the cloud design section and Appendix A.

This is an input to `draft/feature/pyautobrain/shift_watcher_in_the_cloud.md`: it settles what a worker is before the watcher that starts workers is designed.

**What was measured.**
- **No agent runs alone (BRAIN-1).** All 21 Brain agents reference at least one sibling checkout, Mind most often. The resolver (`agents/_repo_paths.py`, `agents/_common.sh`) is local-filesystem only. A few already degrade instead of failing: vitals reads the published Heart board when Heart is absent, community reads the published Ears feed. No preflight reports which verbs a given set of clones can run.
- **Fixed load (TOK-2).** A session's first call carries a median 54,938 tokens and a subagent's about 44,000. Tool schemas are about 27.6k of it, the skill listing 9.4k, MEMORY.md 8 to 9k and growing, AGENTS.md 1.7k. These are laptop figures; a cloud worker's load has not been measured.
- **The always-apply rules do not reliably load (TOK-3).** Since 2026-10-29 the workspace `AGENTS.md`, which holds the safety rules, is auto-loaded in 0 of 53 workspace sessions, because a `CLAUDE.md` in the home folder suppresses it. The workspace root is not a git repository, so a cloud clone never sees that file or the workspace hooks. Two of the four rules already travel in every repo's generated block; "plan before editing" and "paths stay inside this workspace" are in none.

**The change.**
1. **Bundle.** Declare the cloud worker unit as Brain plus Mind plus the task's repos (the prompt's `Repos:` header) at pinned commits under one root, with Heart read through its published feed. The organs' own CI already does this on hosted runners.
2. **Preflight.** A read-only `pyauto-brain doctor` that prints, per verb, which siblings resolve, so the orchestrator refuses to dispatch a verb its bundle cannot run.
3. **Profile.** A worker agent type with a restricted tool set, no MEMORY.md index and no general skill listing: the repo's `AGENTS.md` plus the dispatcher's brief. Report the measured fixed load per shift in the digest.
4. **Rules that travel.** Put the always-apply rules into the generated shared block every repo's `AGENTS.md` already carries, or into the worker brief, and add a check that asserts the expected instruction set from the transcript. On the laptop, decide deliberately where those rules live now that the home pointer suppresses the workspace file.

`judge` because items 1 and 4 decide what an unattended worker is allowed to be and which rules bind it. Item 4's laptop half touches the human's own home folder and is theirs to make.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
