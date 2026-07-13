# PyAutoBrain Intake Agent (organism-facing: the Conception Agent)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft

## Why we want this

PyAutoMind is the Mind, but raw intent currently enters it two unsatisfying ways:
either I text-vomit a bullet into `@PyAutoMind/ideas.md` (which then rots — see the
literal state of that file today), or I hand-write a prompt under
`<work-type>/<target>/<name>.md` and try to remember the conventions. Neither
consistently produces a *formalised, grouped, machine-legible* Mind object.

The evidence that the current approach isn't working:

- Of ~84 un-issued prompts, only **6** carry the optional `Type:/Target:/Status:`
  header (`@PyAutoMind/README.md` "Prompt file format"). ~7% adoption. The
  convention exists; humans don't use it. **The fix is not to nag humans — it is
  to have an agent write the header consistently.**
- `ideas.md` holds orphan bullets ("teacher mode", "refactor agent", "optimize
  agent", a workspace guide) that never became prompts.
- Mind GitHub issue #18 (3D/cube dataset modelling) has no formal prompt behind it.
- `bug/` holds ~28 un-started prompts with no age/priority signal.

So we want a Brain conductor that turns **raw input → a formal, grouped, headed
PyAutoMind prompt**, and a census/repair mode that finds everything already in a
half-formed state and runs it through the same path.

## What it is (placement + analogy)

A new **conductor** in `@PyAutoBrain/agents/conductors/intake/`. It *acts* (it
writes prompt files), and the tier rule in `@PyAutoBrain/AGENTS.md` is explicit:
"a side-effecting decider is a conductor; a side-effect-free opinion is a faculty."

- **Engineering name: Intake Agent.** Chosen over "idea" because its front door
  takes in *any* raw input — a bug report, a refactor thought, a doc gap — not
  just feature ideas. "idea" pre-commits to the feature framing and reads wrong
  the moment a bug is dumped in.
- **Organism-facing name: the Conception Agent** — the *conceptive function*. A
  task is **conceived** here (raw stimulus → a formed concept the Mind can hold)
  before the **Growth Agent** (the Feature Agent's organism name) grows it into
  code. Lifecycle metaphor: **Conception → Growth**. Model this exactly on the
  Feature Agent's `Tier: conductor` header and its "Growth Agent" naming note in
  `@PyAutoBrain/agents/conductors/feature/AGENTS.md`.

## The boundary — position it against what already exists

This is the part that must be crystal-clear, because three existing things are
adjacent and intake must not duplicate any of them:

```
/route   → infer work-type, DISPATCH to a command (starts dev now)   [execute now]
intake   → infer work-type, FILE a formal prompt (does NOT start dev) [capture, defer]
triage/  → where intake files anything it can't confidently classify  [REUSE, don't reinvent]
create_issue / start_dev → the pipeline intake feeds; intake sits strictly BEFORE it
```

One-sentence definition to put at the top of the agent's `AGENTS.md`:
**intake is "route-to-a-filed-prompt-without-executing."** Low-confidence
classification writes into the existing `@PyAutoMind/triage/` folder — reuse that
machinery, do not build a parallel unclassified bucket. Intake never opens an
issue and never starts dev; `create_issue` (the Mind's issue primitive) and
`/start_dev` remain the next, separate step.

## What it does

Read raw input, classify it, and (under `--apply`) write a formal prompt:

1. **Group it** — pick the **work-type folder** (`feature/ bug/ refactor/ docs/
   test/ release/ maintenance/ research/ experiment/`, or `triage/` when unsure).
   This *is* the "group it" the user asked for — the first-folder taxonomy in
   `@PyAutoMind/ROUTING.md` already is the grouping.
2. **Target it** — pick the second folder (the affected repo/domain), inferred
   from `@RepoName` mentions and target words. Must resolve the organism targets
   too: `pyautomind`, `pyautobrain`, `pyautoheart`, `pyautobuild`, `pyautomemory`
   (the Feature Agent's known miss — it mis-routed a `pyautobrain` target as
   research-first because it couldn't resolve the infrastructure target; see
   PyAutoBrain Bug Agent issue).
3. **Write** the prompt at `<work-type>/<target>/<name>.md` with the lightweight
   header (below), free-form prose body, `@RepoName/path` references preserved.
4. **Emit an `IntakeDecision`** — mirror the shape/fields of the Feature Agent's
   `FeatureDecision` (`@PyAutoBrain/agents/conductors/feature/AGENTS.md`), so the
   downstream Feature/Bug/etc agents consume a familiar object.

### Modes (align exit codes + dry-run to house style)

```
pyauto-brain intake "<raw text>"          # classify + (with --apply) write one prompt
pyauto-brain intake --file path/to/raw.md
pyauto-brain intake ideas                 # scan ideas.md; propose one prompt per separable bullet
pyauto-brain intake census                # read-only: find half-formed / stale / drifted state
pyauto-brain intake repair                # census + (with --apply) fix it
pyauto-brain intake dashboard             # regenerate the Mind backlog dashboard
```

- All modes support `--json`.
- **Writes are guarded behind `--apply`; dry-run is the default.** `--apply` is a
  flag, not a new exit code.
- **Exit codes follow the existing convention** (`feature.sh`): `0` produced a
  decision · `4` nothing to formalise / could-not-resolve Mind · `5` bad usage.
  Do NOT invent the 3/6 codes from the ChatGPT sketch.

## The metadata header — extend the existing convention, do NOT add YAML

`@PyAutoMind/README.md` "Prompt file format" **explicitly forbids YAML
frontmatter** and blesses a light, human-writable header as "a convention, not a
schema." Respect that. Intake writes an *extended* version of that same header:

```markdown
# Short task title

Type: feature            # matches the work-type folder
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
Difficulty: medium       # small | medium | large | too-large
Autonomy: supervised     # safe | supervised | human-required
Priority: normal         # low | normal | high
Status: formalised       # raw | formalised | planned | issued | active | complete
```

`Difficulty`, `Autonomy`, `Priority` are the "inputs at the top" the user wants
(difficulty, whether an agent can safely handle it, planned state). This stays
greppable without a schema. **One prerequisite edit:** bless these three extra
keys in `@PyAutoMind/README.md` (and mirror in `AGENTS.md`) so the convention is
documented before the agent starts writing it. No YAML, no required fields.

## Difficulty is assessed BY intake (decision — do not put it in the Feature Agent)

Difficulty is a function of scope, and scope is decided during the intake
back-and-forth. So the estimate is freshest the moment intake finishes — intake
is its owner. The Feature Agent runs later at selection/execution time and should
**trust the persisted `Difficulty:`**, re-deriving only if the prompt changed.

To stop two divergent estimates drifting (intake persists a number; the Feature
Agent currently computes its own in `@PyAutoBrain/agents/conductors/feature/_feature.py`):

- **Extract the sizing heuristic** out of `_feature.py` into a shared component
  both consult — a small importable module, or a read-only `sizing` faculty under
  `@PyAutoBrain/agents/faculties/` (faculties are read-only opinion sinks, which
  is exactly what a sizing estimate is). Given we are now *persisting* the number,
  this moves from "optional" to **required scope** — a persisted value that a
  second agent silently recomputes is a drift bug.
- Split of ownership: **moment of assessment → intake; the logic → shared
  faculty/module; Feature Agent → trusts-then-refreshes.**

## Census / repair — grounded in real findings

`intake census` is read-only and reports; `intake repair --apply` fixes and only
mutates `@PyAutoMind` files (never a source repo, never Heart — same discipline as
`feature/AGENTS.md` "what this agent must never do"). It scans for:

- raw `ideas.md` bullets not yet formalised (mark converted bullets, don't
  silently delete until trusted: `- [formalised → feature/…/x.md] <bullet>`);
- prompts missing the header (78 of 84 today);
- `planned.md` / `active.md` entries whose issue/PR links are already merged/closed;
- completed work still sitting in `active.md`;
- Mind GitHub issues with no formal prompt (issue #18 today);
- aged prompts (flag the ~28-deep `bug/` backlog by filed-date);
- **doc/reality drift** — `README.md` and `AGENTS.md` reference a `priority.md`
  that does not exist on disk; `overview.md` exists but is absent from the README
  layout. Census should catch exactly this class of drift.

## Dashboard — a Mind *backlog* view, distinct from Heart's *health* view

Do not duplicate `/health status` (the Heart-owned active/planned/complete health
dashboard). Split by *what is shown*:

- **Health / readiness / in-flight** stays with Heart (`/health status`) — untouched.
- **Backlog / intent** ("everything currently on our mind": raw ideas,
  formalised-but-unplanned, planned, hygiene warnings) is the Mind's own concern.

`intake dashboard` generates `@PyAutoMind/DASHBOARD.md` (reasoning lives in Brain;
the file lives in Mind) and it is linked from the README rather than bloating the
23 KB README body. Frame it explicitly as the **intent/backlog** view, distinct
from Heart's **health** view, so the organism boundary stays clean. A GitHub
front-page render is fine as long as it is the generated file, not hand-maintained.

## Files to create / edit

Create (model on the feature conductor's shape — concise `AGENTS.md` with a
`Tier:` line, a deterministic entrypoint, an audit doc of the surface it drives):

```
@PyAutoBrain/agents/conductors/intake/AGENTS.md
@PyAutoBrain/agents/conductors/intake/INTAKE_TAXONOMY.md   # like feature's MIND_TAXONOMY.md
@PyAutoBrain/agents/conductors/intake/intake.sh
@PyAutoBrain/agents/conductors/intake/_intake.py           # stdlib-only analysis core
@PyAutoBrain/agents/faculties/sizing/                       # extracted difficulty heuristic (if faculty route)
```

Edit:

```
@PyAutoBrain/bin/pyauto-brain        # register `intake` in AGENT_SCRIPT / CONDUCTOR_ORDER
@PyAutoBrain/skills/COMMANDS.md      # add the /intake door + the boundary vs /route
@PyAutoBrain/skills/intake/intake.md # thin command body (installed as /intake)
@PyAutoBrain/AGENTS.md               # describe the Intake/Conception conductor
@PyAutoBrain/README.md               # command-surface table row
@PyAutoMind/README.md                # bless Difficulty/Autonomy/Priority header keys; link DASHBOARD.md
@PyAutoMind/AGENTS.md                # mirror the header keys
@PyAutoBrain/agents/conductors/feature/_feature.py  # consume shared sizing; trust persisted Difficulty
```

## Build order (ship as small PRs, not one)

1. Bless the extended header keys in `@PyAutoMind/README.md` + `AGENTS.md` (docs
   only — no behaviour change).
2. `intake --json` as a read-only classifier (raw text / `--file`) emitting
   `IntakeDecision`. No writes.
3. `--apply`: write formal prompts; conservative `ideas.md` reconciliation.
4. Extract the shared sizing component; wire both intake and the Feature Agent to it.
5. `census` + `repair` + `dashboard` (Mind backlog view).
6. Backfill: `ideas.md`, Mind issue #18, the `bug/` backlog.

## What it must never do

- Edit source repos, open issues/PRs, or start dev — those are `create_issue` /
  `start_dev` / `ship_*`, strictly downstream.
- Query PyAutoHeart directly, or generate a *health* dashboard (that is Heart's).
- Introduce YAML frontmatter or a required schema — light header only.
- Silently delete raw ideas before the mechanism is trusted.
- Just pick the first plausible work-type — classify, and explain the choice in
  the `IntakeDecision` (mirror the Feature Agent's "explain the ranking" rule).

Come up with a plan to implement the Intake (Conception) Agent following this
build order.
