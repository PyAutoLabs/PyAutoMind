# Scientist project relationships and expandable cards

Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/55
Type: feature
Target: PyAutoScientist
Repos:
- PyAutoScientist
Difficulty: medium
Autonomy: safe
Consequence: judge
Priority: normal

Implement phase 1 of `draft/feature/pyautoscientist/collaborator_led_pyautoscientist_adoption_pilot.md`, authorized by James on 2026-10-11. Use @PyAutoScientist's existing dashboard and shared Brain presentation. Resolve repository identities from Mind repos.yaml. Keep instance-specific project names and resource associations in versioned configuration, separate from renderer logic. Represent software families separately from Cortex investigations. Resources are optional lists: software, shared dependencies, workspaces, tutorials, documentation source/published locations, assistants and organ records. Allow shared resources and projects without assistants. Do not copy owner records, collect quality evidence or infer readiness from inventory presence.

Coordinate the resource vocabulary with the agreed Broca communication/documentation scope; full Broca rollout is separate. Project sources remain authoritative. Scientist links; Broca will own communication relationships/upkeep evidence; Ears listens, Memory holds knowledge, Cortex science, Heart readiness and Hands releases. Do not contact or configure the collaborator.

## Plan

1. Add an explicit versioned project/resource configuration and resolver using the canonical repository map, with stable IDs, typed relationships and safe public links.
2. Add collapsed project cards to the current dashboard, using its disclosure layout and Brain theme. Group optional resources by purpose and preserve organ refresh, focus, work panel and no-JavaScript access.
3. Populate verified PyAuto software families, including shared dependencies and an assistant-free project. Document ownership, public visibility, configuration and remaining portability limits.
4. Validate malformed identities/links, optional lists, shared resources, renamed synthetic instances, fixture rendering and responsive keyboard/browser behavior; open a bounded PR.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

- `config/projects.json`: instance-owned version-1 configuration of projects and shared resources. Repository references are keys in Mind's map, not duplicated GitHub identities. Source locations use optional ref/path; published locations use explicit HTTPS URLs. Explicit publication opt-in; omitted/private items must not enter public output.
- `scripts/project_resources.py`: load/validate configuration and canonical YAML identity map, resolve resources without network collection, fail clearly on malformed configuration or unresolved identities. Stable project/resource identifiers independent of display names. CLI-selected paths allow independently named instances without guessing prefixes.
- `scripts/organism_board.py`: integrate project snapshot and cards; retain Brain hero/panel, reuse existing disclosure layout. Project cards link owner records and describe inventory only; no synthetic green/freshness verdict.
- `.github/workflows/organism_board.yml` and `board_tests.yml`: make canonical Mind identity input available during rendering and fixture checks; install the parser dependency. Do not deploy from this task.
- `tests/`: fixture/unit coverage plus browser verification of 390/768/1440px, light/dark, disclosures, safe links, focus, no overflow and retained state during organ refresh.
- `PROJECTS.md`: configuration and ownership contract, Broca compatibility, upgrade-preservation boundary and deferred starter/optional-organ scope.

## Branch survey and authorization

Scientist main and Mind main clean after fetch; Scientist no open PRs or active claim. Prior Scientist cockpit PR #53 and DNA PR #51 merged. Old DNA worktree left untouched. Branch `feature/scientist-project-resources`; isolated worktree inside workspace `.worktrees/scientist-project-resources`. User explicitly requested routine autonomous implementation through validation and PR; merge not authorized.

## Phase-1 handoff — 2026-10-11

Implemented at `3010f0b` on `feature/scientist-project-resources`; PR https://github.com/PyAutoLabs/PyAutoScientist/pull/56 awaits human merge. Six project cards resolve canonical identities, share resources and support assistant-free projects. Public configuration projection preserves owner records; overall instance portability remains deferred.

Validation: 38 Python tests, 6 Node tests, 6 browser viewport/theme cases plus no-JavaScript passed. Independent review CLEAN. Evidence is in `.worktrees/scientist-project-resources/evidence/`. Heart YELLOW exact reason: `manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml`; James explicitly acknowledged it (“I ackwnoeldge”). Separate STALE reason: `release validation incomplete: no rehearsal for current source`. Cortex science changes remain untouched.

Next: human /prm checks and merge; existing dashboard publication then renders the cards. Start the recorded minimal-starter task after inspecting the merged foundation. Optional organs, upgrades and real collaborator validation remain separate drafts; Broca contract/pilot work is separately recorded. No collaborator access or project details assumed.
