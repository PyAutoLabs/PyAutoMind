## bug-agent
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/18
- completed: 2026-07-08
- repos: PyAutoBrain (PR #20, merge-committed)
- branch: feature/bug-agent
- validation:
  - CLI modes: specific / selection (severity-first) / difficulty-constrained
    (--difficulty/--model/--budget/--ambitious/--impact) / health — all pass;
    --json emits a valid BugDecision; line-count guard passes; Feature Agent unaffected
  - health mode: consults the vitals faculty (verdict) + scans filed PyAutoHeart
    issues (#27/#19/#10/#7), per-issue category hint, routes to bug/health_fixes/
  - Copilot review: 13 findings, all real, all fixed in 65a70ce (JSON stdout
    pollution, exec-vs-trap temp leak, dead bug/ in-flight down-ranking, single-file
    scope, docs/research re-home, doc/code honesty on health-mode claims)
- notes: |
    New PyAutoBrain conductor agents/conductors/bug/ — the organism's immune
    system (organism-facing: Immune Agent). Reuses the Feature Agent core by import
    (parse/difficulty/memory/down-rank), adds classify/reproduction/fix_locus/
    health_mode. Conductor-only with a documented seam for a future read-only
    diagnosis faculty; consults vitals, never Heart directly. Fundamental principle:
    a precise response with NO AUTOIMMUNITY — user-facing workspace scripts are
    documentation, so prefer a general library-source fix. /bug promoted from a
    work-type entry to a real conductor across the command surface. Follow-up filed:
    bug/pyautobrain/feature_agent_infra_target_resolution.md (Feature Agent can't
    resolve the pyautobrain infra target; misfired research-first on this prompt).

## Original prompt

Implement the initial PyAutoBrain Bug Agent.

Context

The PyAuto ecosystem now uses an organism architecture.

Current architecture:

PyAutoMind stores intent, tasks and workflow state.
PyAutoMemory stores long-term knowledge and prior decisions.
PyAutoBrain contains specialist reasoning agents.
PyAutoHeart performs health checks and readiness validation.
PyAutoBuild performs execution, build and release operations.

Existing or planned PyAutoBrain agents include:

Health Agent
Build Agent
Feature Agent

The next specialist agent should be the Bug Agent.

The Bug Agent handles regressions, failing tests, incorrect behaviour, broken workflows and health issues that require fixes.

Goal

Implement the initial Bug Agent.

The Bug Agent should reason about bugs and produce a clear repair workflow.

It should not directly duplicate PyAutoHeart checks or PyAutoBuild execution.

Core responsibilities

The Bug Agent should:

accept a specific bug report, failing test, GitHub issue or PyAutoHeart finding,
classify the bug,
determine likely owning repository or repositories,
consult PyAutoMemory for relevant historical context,
consult PyAutoHeart for reproduction / health-check context,
decide whether the bug is small, medium, large or ambiguous,
decide whether it can be fixed directly or requires investigation first,
produce a repair plan compatible with the PyAuto workflow,
route execution through PyAutoBuild where appropriate,
require PyAutoHeart validation before shipping.

Inputs

The Bug Agent should support:

/bug issue #123
/bug failing tests in PyAutoArray
/bug health issue from PyAutoHeart
/bug regression after PR #456
/bug choose an important bug to fix
/bug choose an easy bug suitable for limited tokens

Modes

1. Specific bug mode

The user provides a known issue, failing test or error.

The Bug Agent should:

inspect the report,
identify reproduction steps,
classify severity,
find likely affected repos,
identify relevant tests,
produce a fix plan.

2. Health issue mode

The bug comes from PyAutoHeart.

The Bug Agent should:

read the PyAutoHeart finding,
understand which check failed,
determine whether this is a real bug, flaky test, config problem or expected failure,
decide whether the fix belongs in the affected repo, PyAutoHeart, PyAutoBuild or PyAutoBrain.

3. Selection mode

The user asks the agent to choose a bug.

The Bug Agent should:

inspect open bug issues,
inspect PyAutoMind bug prompts,
consider priority and severity,
consider model/token constraints,
choose a suitable bug,
explain why.

4. Difficulty-constrained mode

The user may ask for:

easy bug,
high-impact bug,
low-risk bug,
bug suitable for weak model,
bug suitable for strong model,
bug suitable for overnight run.

The Bug Agent should estimate complexity before selecting.

Classification

The Bug Agent should classify bugs by:

severity:
  critical | high | medium | low

scope:
  single-file | single-repo | multi-repo | ecosystem

type:
  test-failure | runtime-error | wrong-result | docs-error | workflow-error | config-error | release-error | flaky | unknown

confidence:
  high | medium | low

Relationship to PyAutoHeart

PyAutoHeart measures health.

The Bug Agent reasons about failures.

The Bug Agent should use PyAutoHeart to:

reproduce failing checks,
identify affected validation workflows,
confirm whether a fix worked,
obtain GREEN/YELLOW/RED readiness after patching.

The Bug Agent must not reimplement PyAutoHeart checks.

Relationship to PyAutoMemory

The Bug Agent should consult PyAutoMemory when useful.

Examples:

recurring failures,
previous fixes,
known flaky tests,
architectural decisions,
scientific assumptions,
previous debugging notes.

If PyAutoMemory influenced the plan, summarise the relevant context.

Relationship to PyAutoMind

Bug work should be tracked in PyAutoMind.

The Bug Agent should understand paths such as:

bug/autoarray/...
bug/autofit/...
bug/autolens/...
bug/workspaces/...

If a bug report is actually a feature, refactor, docs issue or research task, reclassify it.

Relationship to PyAutoBuild

PyAutoBuild executes.

The Bug Agent should route execution through PyAutoBuild when it is time to:

create branches,
make code changes,
open PRs,
ship fixes.

The Bug Agent should not bypass the established workflow.

Development workflow

The Bug Agent should support a lifecycle like:

bug report
  -> classify
  -> reproduce or identify validation check
  -> consult Memory if needed
  -> decide fix strategy
  -> start_dev
  -> patch
  -> PyAutoHeart validation
  -> ship_library / ship_workspace

Output format

The Bug Agent should produce structured output:

Bug:
<description or issue path>

Mode:
specific | health-issue | selection | difficulty-constrained

Classification:
severity:
scope:
type:
confidence:

Likely owner:
<repo or workflow>

Reproduction:
<known / unknown / PyAutoHeart check>

Relevant context:
<PyAutoMemory context if used>

Fix strategy:
<direct fix | investigation first | split into phases | defer>

Recommended workflow:
<library | workspace | combined | infrastructure>

Health validation:
<PyAutoHeart checks required>

Risks:
<main risks>

Next action:
<single concrete next step>

Claude skill constraints

If implemented as Claude skills or markdown agent definitions:

keep every .md file below 200 lines,
follow Claude skill guidelines,
keep the main Bug Agent instruction file concise,
move long examples and architecture notes into supporting docs.

Validation

Validate that the Bug Agent can:

classify a known bug,
consume a PyAutoHeart finding,
choose a bug when none is specified,
respect difficulty constraints,
produce an output compatible with start_dev,
require PyAutoHeart validation before shipping.

PR

Create one PR titled:

Implement initial PyAutoBrain Bug Agent

---

## Extra directives (from the user, verbatim)

Also make sure it has a specific prompt or context for just scanning Heart for
issues here: https://github.com/PyAutoLabs/PyAutoHeart/issues .

Also think about if the bug agent is just a conductor or also could use some
faculties. Do deep research.

One important aspect of the bug agent is that when it's editing workspace
scripts, it should know that workspace scripts are **user-facing documentation**
and therefore bug fixes should avoid changing the scripts in ways that make their
contents less clear to a user when possible. Without this context, agents often
change the script in weird ways (e.g. adding test environment variables in the
scripts or manually overwriting paths). The bug agent should critically assess if
a script ever needs changing or if the fix is better done in the source code in a
way that fixes things more generally.

---

## Design decisions agreed in the planning session (2026-07-07)

These reconcile the spec above with the real PyAutoBrain organism (conductors vs.
faculties, the vitals faculty, the existing Feature Agent core). Sources:
`PyAutoBrain/AGENTS.md`, `agents/conductors/feature/`, `agents/faculties/vitals/`.

**Organism metaphor — the immune system.** The Bug Agent is the organism's
**immune system** (organism-facing name: *Immune Agent*): it recognises a pathogen
(a bug, regression, failing test or PyAutoHeart finding), tells it from benign
self, types the threat, recalls whether it has met it before (PyAutoMemory as
immune memory), and mounts a *targeted* response — neutralising the defect at its
source without harming healthy tissue. This framing goes at the top of its
`AGENTS.md`. Mapping: recognise pathogen → accept report; self-vs-non-self →
real-bug vs expected/flaky/mis-filed; type threat → severity/scope/type/confidence;
immune memory → PyAutoMemory; targeted response / spare healthy tissue → fix-locus;
autoimmunity → the failure mode to avoid.

**Tier: conductor** (mirrors the Feature Agent). It decides and drives a plan into
the dev-flow, so it lives at `agents/conductors/bug/`. It **consults the existing
read-only `vitals` faculty** (`--check-health`) and **never queries Heart
directly**. Ship as a conductor only for v1; document a clean seam for a future
read-only `diagnosis` faculty (pure classify + locate + fix-locus reasoning,
reusable by Feature re-homing and the Health conductor) rather than building it now
— matching how Release stayed a mode of Build with a seam to split later.

**Boundary with the Health conductor.** The Health conductor drives the assess →
triage → dispatch loop toward GREEN; its current cut is explicitly "validation +
recommend, no edit-in fixes." The Bug Agent is that deferred edit-in-fix arm: Health
hands it a red that is a genuine *code* failure, and the Bug Agent turns it into a
repair plan. No duplicated triage.

**Deterministic core reuse.** `_bug.py` imports the Feature Agent's shared helpers
(`scan_mind` / `score_difficulty` / `downrank_inflight` / `emit_json` from
`_feature.py`) — minimal refactor, no standalone copy of the difficulty heuristic —
and adds only `classify()`, `reproduction()`, `fix_locus()`, `health_mode()`.
Stdlib-only, never writes (same contract as `_feature.py`). Selection adds a
severity weighting on top of the difficulty score.

**Two health inputs (health-issue mode).** (1) the live **vitals verdict** (what is
RED now, via the vitals faculty) and (2) **filed PyAutoHeart GitHub issues**
scanned with `gh issue list --repo PyAutoLabs/PyAutoHeart` — the durable, detailed
findings Heart authored (e.g. #27 release-fidelity, #19/#7 degraded-health, #10
url-check). Both route to `PyAutoMind/bug/health_fixes/` (whose README already cites
Heart issue #27). Give the issue-scan its own context/sub-mode.

**Fundamental principle — a precise response, no autoimmunity.** The most delicate
tissue is the **user-facing workspace scripts — they are documentation**. A fix that
injects test env-vars, hard-codes a path, mutates `os.environ`, or drops a silent
guard into a tutorial script is an **autoimmune reaction** — it damages what it
exists to protect. Before proposing any patch the Bug Agent asks *where the fix
belongs* and strongly prefers a **general fix in library source** that resolves the
whole class of failure. It edits a workspace script only when the defect truly lives
there, never in a way that reduces clarity; sanctioned knobs go through
`config/build/env_vars.yaml` / `no_run.yaml`, not inline edits. This becomes an
explicit `Fix locus:` field in the BugDecision output.

**Output — a BugDecision**, adopting the spec's fields but JSON-consistent with the
Feature Agent's `FeatureDecision` shape, plus the `Fix locus:` field above.

**Files.** New: `agents/conductors/bug/{AGENTS.md, BUG_TAXONOMY.md, bug.sh,
_bug.py}`. Edits: register `bug` in `bin/pyauto-brain` (AGENT_SCRIPT / AGENT_DESC /
CONDUCTOR_ORDER); promote `skills/bug/bug.md` from work-type entry to a real
conductor command; move `/bug` from the "work-type entries" tier into "real
conductors" in `skills/COMMANDS.md`, `README.md`, and `AGENTS.md`. Keep every `.md`
under 200 lines (guarded by `bin/check_skill_line_counts.sh`).

**Validation.** `pyauto-brain bug bug/autoarray/rect_adapt.md` (classify + fix-locus
= library source); `pyauto-brain bug` (selection over `bug/**` + open GitHub bug
issues, down-ranks in-flight); `pyauto-brain bug select --difficulty easy` /
`--impact`; `pyauto-brain bug health` (vitals + scan PyAutoHeart issues →
`bug/health_fixes/`); `--json` emits BugDecision; line-count guard passes.
</content>
</invoke>
