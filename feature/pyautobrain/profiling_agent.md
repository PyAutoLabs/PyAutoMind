# Profiling agent

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- autolens_profiling
- PyAutoHeart
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Profiling agent. Grow a PyAutoBrain agent that owns performance measurement for the organism, using autolens_profiling as its workspace — the endpoint the polish series (autolens_profiling#52/#54/#56) was building toward. Not lensing-specific: it understands PyAutoFit (searches, likelihood functions, latents), JAX (jit/vmap compile vs steady-state, backend selection), and the CPU / laptop-GPU / HPC-A100 hardware tiers. What it orchestrates, all demonstrated by the polish phases: campaign dispatch (sweep.py instrument matrix, cheapest-first), vram-first validation and probe ingest (probe JSONs -> VMAP_BATCH/VMAP_BATCH_SPARSE with provenance), pinned-value maintenance (pin newly measured instruments; triage pinned_drift flags with the PyAutoHeart profiling_drift vitals leg, merged as Heart#38), baseline snapshots (build_baseline.py, PreOptimizationTimes convention), dashboard refresh, and HPC dispatch/ingest cycles when RAL is available. Future capabilities from the parent prompt: JAX compilation-time profiling of likelihood functions, and hunting generally-slow functions flagged by integration tests. Design questions to settle first: conductor vs faculty per the demonstrated-need doctrine (evidence now exists — three phases ran this workflow through the generic dev-flow with heavy manual orchestration); boundary rules against the health agent (observes verdicts, does not run campaigns) and the hygiene-agent debate (research/pyautobrain/hygiene_agent_decision.md — profiling is performance measurement, not repo hygiene); and whether the agent's first increment is just the campaign/ingest conductor with the future capabilities staged as follow-ups. Implementation is ordinary feature/pyautobrain work per ROUTING.md. Blocked until the clone-mitosis-agent task ships (PyAutoBrain claimed).

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake;
     re-homed maintenance/autofit -> feature/pyautobrain in conversation: agent
     implementations are feature/pyautobrain per ROUTING.md; PyAutoFit was a
     knowledge-domain mention, not the target -->

---

## Design decision (phase 1, read-only — 2026-07-09)

Settled against `PyAutoBrain/AGENTS.md` doctrine ("a side-effecting decider is
a conductor; a side-effect-free opinion is a faculty") using the polish
series (#52/#54/#56) as the demonstrated-need evidence:

**Verdict: conductor.** `agents/conductors/profiling/` — the *Measurement
Agent*. The work is decide-AND-act at every step (dispatch sweeps, ingest
probe tables, edit pins, snapshot baselines, refresh dashboards), recurs on a
real cadence (PreOptimization now, PostOptimization later, per-release trend
runs, RAL dispatch/ingest cycles), and has a distinct reasoning shape
(hardware tiers, JAX compile-vs-steady-state, the CPU-usability policy,
matrix scoping under RAM/wall-clock constraints — every one of which required
live judgment during phases 1–3). A faculty cannot do this work: it mutates.

**First increment — three modes over the autolens_profiling workspace:**
- `campaign` — plan the matrix (CELLS × tier × usability policy), dispatch
  the local leg (sweep --skip-existing --per-run-timeout), stage HPC submits.
- `ingest` — probe JSONs → VMAP_BATCH/VMAP_BATCH_SPARSE + PROVENANCE; pin
  newly measured instruments; build_baseline + build_readme.
- `triage` — read Heart's profiling_drift leg; stale pin → re-pin here;
  library regression → file `bug/` via intake (never debug libraries in the
  profiling repo — the phase-2 boundary rule).

**Boundaries:**
- vs **health**: Heart observes and verdicts (incl. the profiling_drift leg,
  Heart#38); the profiling conductor runs campaigns and owns the performance
  data lifecycle. Heart never dispatches campaigns; profiling never issues
  health verdicts. Consults the vitals faculty like every conductor.
- vs **hygiene**: unrelated remits (performance measurement ≠ repo hygiene);
  note the hygiene question itself appears substantially settled by the
  2026-07-09 hygiene split (Heart observes noise / Brain `repo_cleanup`
  mutates, PyAutoHeart PR #42) — see research/pyautobrain/hygiene_agent_decision.md.
- vs **build**: campaigns are not releases; `profile.yml`'s on-release runs
  stay CI/Build territory.

**Deferred (future modes, per the parent prompt):** JAX compilation-time
profiling of likelihood functions; hunting generally-slow functions flagged
by integration tests. A read-only *profiling faculty* (opine on regressions /
next optimization targets from the results tree) splits out only when a
second conductor demonstrates consult demand — doctrine says let faculties
multiply behind conductors, not ahead of them.

**Implementation remains blocked** on the PyAutoBrain claim
(clone-mitosis-agent, sign-off pending on PyAutoBrain#57); this decision
makes the task implementation-ready the moment it clears.

