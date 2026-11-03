- epic: autonomous-orchestrators (phase 2 of 7; epic draft/feature/pyautobrain/autonomous_orchestrators_epic.md)
- summary: the organism now parses what phase 1 wrote. Sizing: LANE_VALUES any|local-dev|ral|gpu|wsl-data + lane_is_local (invalid → lane_invalid, read as any). Batch planner: _lane_ok via lane_is_local, lane_counts ("Ready by lane"), other-lane line names resources. New _brief.py: `batch brief --check <file>` (errors name the key; exit 0/1) and `batch plan --brief <file>` (named tasks outrank the queue, dip only what the policy covers, brief review-minutes is the budget). Intake: declared Filed/Epic/Phase/Blocked-by/Closes-when pass through after Status:, Lane: after Unattended:; lane inference RAL/SLURM/sbatch/squeue/euclid_jump → ral, CUDA/laptop GPU → gpu, /mnt/c / Workspace/Science → wsl-data. Census: by_lane, `By lane:` line, dashboard Backlog "Lanes:" line, unknown-Lane hygiene flag. Mind: batches/examples/shift_brief_example.md fixture + lifecycle test that examples/ is never a record.
- decisions (human-approved plan): merge-cap > 0 refused only when every named task is judge AND backlog: none (a dip may still pick glance work); unresolved named tasks warn, never refuse.
- witness: 28/28 clause tests (a)–(e); brief --check OK on the shipped example; census lane total 289 = prompt count; full suites Brain 1437 / Mind 712.
- traps: the Brain CI tenant firewall rejects satellite repo names / owner in NEW organ files (tests included) — first CI run red on both legs; run `repos_sync.py --check --only "tenant firewall (organ code)" --root <worktree>`, not `--root ~/Code/PyAutoLabs` (that checks the canonical Brain). Fixed in f3fc8fc without growing FIREWALL_ALLOWLIST.
- follow-up: draft/bug/pyautobrain/intake_classify_file_drops_declared_epic_phase.md re-scoped to its Memory:-gating half (header half shipped here).
- heart: YELLOW, reason set acknowledged by the human at ship; glance tiered merge.
- next: phase 3 (watcher, dispatch safety, digest) — prompt not yet filed.

## Original prompt

# Autonomous orchestrators phase 2: `Lane:` resource values, the shift-brief validator, intake pass-through and census

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- autonomy
- orchestration
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Epic: autonomous-orchestrators
Phase: 2
Filed: 2026-11-03
Issued: 2026-11-03
Consequence: glance
Witness: `pytest PyAutoBrain/tests -q` green with new tests that (a) parse `Lane: ral`, `gpu`, `wsl-data` and keep `any`/`local-dev`, and reject `Lane: any | local-dev`; (b) assert `_lane_ok("ral","web-github")` is False and `_lane_ok("ral","local-dev")` True for all three new values; (c) `batch brief --check` accepts `PyAutoMind/batches/examples/shift_brief_example.md` and refuses the same file with `review-at:` removed, with `lanes: cloud` and with a `merge-cap:` above 0 for a brief whose named tasks are all `judge`; (d) `intake classify` on a text naming RAL proposes `Lane: ral` and a declared `Epic:`/`Phase:`/`Filed:`/`Lane:` survives `--apply` unchanged; (e) `intake census` prints a lane histogram whose total equals the prompt count
Review-minutes: 5
Unattended: ready
Lane: any

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md ("Lane, not Needs").
Starts only after phase 1 merges (epic phase order; the schema this validates is written
there). Phase 1 wrote the words; this phase makes the organism parse them. It is the code half of
the original phase 1, split out because a prose-only autonomy edit is `judge` and this is
`glance` with a real witness.

## Deliverables

1. **Sizing faculty** (`agents/faculties/sizing/_sizing.py`): `LANE_VALUES = ("any",
   "local-dev", "ral", "gpu", "wsl-data")`; a helper `lane_is_local(lane)` that is True for
   everything but `any`; keep the first-declaration-wins rule.
2. **Batch planner** (`agents/conductors/batch/_batch.py`): `_lane_ok` routes through
   `lane_is_local`; the BatchDecision prints the lane histogram of the pool; the
   "other lane's ready count" line names the resources (`3 ral, 1 gpu`).
3. **`batch brief --check <file>`**: validate a shift brief against the schema phase 1 fixed
   in `PyAutoMind/batches/AGENTS.md`; errors name the key. Ship the example brief under
   `PyAutoMind/batches/examples/` (ignored by `lifecycle.py check`'s drift scan — add the
   exclusion with a test). `plan --brief <file>` restricts the pool to the brief's named
   tasks first, then the dip policy, and reports the review-minute total against the brief's
   budget.
4. **Intake** (`agents/conductors/intake/_intake.py`): propose `Lane: ral` / `gpu` /
   `wsl-data` when the text names RAL/SLURM/`euclid_jump`, the laptop GPU/CUDA, or `/mnt/c`
   / a Science dataset path; pass declared optional headers (`Epic:`, `Phase:`, `Filed:`,
   `Blocked-by:`, `Closes-when:`, `Lane:`) through `_render_header` unchanged (this is the
   bug `draft/bug/pyautobrain/intake_classify_file_drops_declared_epic_phase_filed_headers*.md`
   reports; fix it here or there, not both — whichever lands first closes the other).
5. **Census**: a lane histogram in `intake census` and the dashboard's backlog page.

## Out of scope

The watcher, dispatch and leases (phase 3); any change to merge authority (phase 1 prose
governs; nothing here merges anything).

<!-- filed 2026-11-03 by the autonomous-orchestrators design review; split from phase 1 -->
