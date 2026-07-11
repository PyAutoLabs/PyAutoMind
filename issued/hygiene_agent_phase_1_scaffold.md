# Hygiene agent — phase 1: scaffold + boundaries

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of the hygiene conductor (umbrella + settled design:
`feature/pyautobrain/hygiene_agent.md`; decision:
`research/pyautobrain/hygiene_agent_decision.md`). Make the conductor **real,
routable, and correctly bounded** with its modes stubbed — no behaviour yet.
Mirror the profiling conductor's wiring exactly.

**Build:**
- `agents/conductors/hygiene/AGENTS.md` — tier: conductor; the *code-quality
  upkeep* function (dev-loop cost + tidiness, distinct from Heart's proof-of-
  works and profiling's modeling speed). Modes table (all five described,
  implemented in later phases): `perf` / `tidy` / `noise` / `deps` / `docs` +
  default prioritized worklist. Emits a `HygieneDecision`. Boundaries section
  (see below). Consults the vitals faculty like every conductor; never issues
  health verdicts, never touches Build.
- `agents/conductors/hygiene/hygiene.sh` — skeleton mirroring `profiling.sh`:
  arg-parse the mode set + `--json`, print a "staged — implemented in phase N"
  notice per not-yet-built mode, exit-code convention consistent with the other
  conductors. Stdlib/bash only (no importing the JAX stack).

**Wire (mirror profiling, grep `profiling` to find every site):**
- `bin/pyauto-brain` — add to the dispatch map (`[hygiene]=…/hygiene.sh`), the
  one-line description, the usage-comment block, and `CONDUCTOR_ORDER`.
- `skills/hygiene/hygiene.md` — the `/hygiene` human-veneer wrapper (like
  `skills/profiling/profiling.md`); install the `~/.claude/commands/hygiene.md`
  symlink via the existing `bin/install.sh` path.
- `skills/COMMANDS.md` — add the `/hygiene` row and the veneer list entry.

**Boundaries to correct in this phase (the reason it is phase 1):**
- `agents/conductors/profiling/AGENTS.md` — rewrite the `## vs hygiene` block
  (currently only "Heart observes noise / Brain `repo_cleanup` mutates", stale
  once hygiene is a real conductor) to the measured-thing split: profiling =
  modeling/compute speed on the science grid; hygiene = developer-loop cost.
  **Move** profiling's staged future mode "hunting generally-slow functions
  flagged by integration tests" out of its Future-modes list and into hygiene's
  `perf` mode (documented as arriving in phase 3).
- `skills/repo_cleanup/SKILL.md` — update the "Future Cleanup Agent" note to
  point at the now-built hygiene conductor (repo_cleanup becomes its `tidy` mode
  in phase 2; leave the skill working standalone until then).

**Out of scope (later phases):** any real mode behaviour — absorbing
repo_cleanup + cli_noise_clean and consulting dep_audit + audit_docs is phase 2;
the `perf` mode + optional PyAutoHeart legs (`import_time` / `cli_noise`) is
phase 3. This phase ships the shell and the corrected boundaries only.

**Done when:** `bin/pyauto-brain hygiene` and `/hygiene` resolve and print the
staged mode menu; the conductor's AGENTS.md states the boundaries; profiling's
boundary + future-mode list and repo_cleanup's pointer are updated; nothing
else changed.

<!-- phase 1 of 3, filed 2026-07-11 from the settled hygiene_agent umbrella;
     phases 2 (absorb skills as modes) and 3 (perf mode + Heart legs) filed as
     this nears shipping, per the no-bulk-issue-queues doctrine. -->
