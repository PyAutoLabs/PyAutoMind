# Hygiene agent decision

Type: research
Target: PyAutoBrain
Repos:
- autolens_profiling
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: decided

Hygiene agent decision. Research and debate whether PyAutoBrain should grow a dedicated hygiene agent — a conductor for the maintenance/ work-type, which today routes through the dev-flow via the Feature Agent (gap surfaced by the profiling-polish-design run, autolens_profiling#52). Weigh three questions before any implementation: (1) does maintenance work (dependency updates, hygiene sweeps, cleanup, small technical debt, lint/format campaigns, stale-doc fixes) recur often enough and with a distinct enough reasoning shape to justify a conductor, per the 'added only on demonstrated need, never for symmetry' doctrine in COMMANDS.md; (2) does this work instead belong to the health agent — but health diagnoses and dispatches from the Heart vitals loop, it does not own recurring upkeep; (3) does it belong to the future profiling agent sketched in maintenance/autolens_profiling/polish.md — but that agent is about performance measurement, not repo hygiene. Instinct going in: maintenance is different from both — review and settle that here. Deliverable: a written decision (grow a hygiene conductor now, keep routing through the dev-flow, or fold into an existing agent) with the boundary rules between hygiene, health and profiling, plus follow-up implementation prompts only if the decision is to build.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake;
     re-homed maintenance/ -> research/ in conversation: the deliverable is a design
     decision (investigation before implementation), maintenance is the subject -->

<!-- 2026-07-09 update: substantially pre-answered by the hygiene split shipped
     in a parallel session (Heart observes noise dashboard + 7-day nudge;
     Brain repo_cleanup skill mutates — PyAutoHeart PR #42). The debate's
     remaining question is whether that split needs a conductor at all, or is
     complete as observe+skill. See also the profiling-agent boundary note in
     feature/pyautobrain/profiling_agent.md. -->

---

## Decision (2026-07-11, /remote-control conversation with user)

**Grow a hygiene conductor now — and it needs NO new paired repo.** This
settles all three questions the prompt posed:

1. **Distinct enough for a conductor? Yes.** The demonstrated need is not a
   single polish series but the *accumulation of scattered hygiene skills* —
   `repo_cleanup` (whose SKILL.md already foreshadows a "Future Cleanup Agent"),
   `cli_noise_clean`, `dep_audit`, `audit_docs` — plus recurring manual
   perf-hygiene work (unit-test / integration-script / import timing). Unifying
   and prioritizing these is decide-AND-act on a real cadence: conductor shape.
2. **Belongs to health? No.** Heart *observes* (its `script_timing` / `test_run`
   legs already track dev-loop timing; extend with `import_time` / `cli_noise`
   if wanted); hygiene *acts* on those observations. Same split the health
   conductor follows.
3. **Belongs to profiling? No — but the boundary needed sharpening.** Split by
   *what is measured*: profiling = modeling/compute speed (likelihood on the
   science grid, GPU tiers, A100); hygiene = developer-loop cost (unit tests,
   TEST_MODE/SMALL_DATASETS scripts, import time). **Profiling's staged future
   mode "hunting generally-slow functions flagged by integration tests" moves
   to hygiene.**

**Why no repo:** a repo is earned by a persistent reusable-artifact lifecycle
(Heart = check functions + verdict history; profiling = timing tables/baselines/
pins in autolens_profiling). Hygiene's tracking substrate already exists in
Heart; its actions ship through `ship_*` and delegate fixes to `bug`/`refactor`;
its output is a prioritized worklist that lives in Mind issues. Nothing for a
repo to hold — it is an orchestrator, not an organ. (This is the user's
"hygiene is smaller in scope than Heart" instinct, and it is correct.)

**Follow-up implementation prompt filed:** `feature/pyautobrain/hygiene_agent.md`
(conductor at `agents/conductors/hygiene/`; modes perf/tidy/noise/deps/docs;
absorbs repo_cleanup + cli_noise_clean, consults dep_audit + audit_docs;
updates profiling's `## vs hygiene` boundary; may add Heart legs). -->

