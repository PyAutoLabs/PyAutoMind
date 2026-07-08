# Hygiene agent decision

Type: maintenance
Target: PyAutoBrain
Repos:
- autolens_profiling
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Hygiene agent decision. Research and debate whether PyAutoBrain should grow a dedicated hygiene agent — a conductor for the maintenance/ work-type, which today routes through the dev-flow via the Feature Agent (gap surfaced by the profiling-polish-design run, autolens_profiling#52). Weigh three questions before any implementation: (1) does maintenance work (dependency updates, hygiene sweeps, cleanup, small technical debt, lint/format campaigns, stale-doc fixes) recur often enough and with a distinct enough reasoning shape to justify a conductor, per the 'added only on demonstrated need, never for symmetry' doctrine in COMMANDS.md; (2) does this work instead belong to the health agent — but health diagnoses and dispatches from the Heart vitals loop, it does not own recurring upkeep; (3) does it belong to the future profiling agent sketched in maintenance/autolens_profiling/polish.md — but that agent is about performance measurement, not repo hygiene. Instinct going in: maintenance is different from both — review and settle that here. Deliverable: a written decision (grow a hygiene conductor now, keep routing through the dev-flow, or fold into an existing agent) with the boundary rules between hygiene, health and profiling, plus follow-up implementation prompts only if the decision is to build.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake -->
