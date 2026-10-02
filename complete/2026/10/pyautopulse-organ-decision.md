# PyAutoPulse organ decision

Type: research
Target: PyAutoPulse
Repos:
- PyAutoPulse
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: decided

PyAutoPulse organ decision. Settle the identity of the cross-project
profiling dashboard layer above the `<lib>_profiling` project repos — its
name, its place in the organism, the state it owns, and the boundary rules
against the Brain's profiling conductor, the project repos, the Heart and the
Mind. Design authority: `PyAutoBrain/docs/research/profiling_inference_organs.md`
(Brain #444) on `PyAutoBrain/docs/research/ecosystem_levels.md` (Brain #440);
this record applies them and does not re-derive them. Implemented by the
`profiling-organ-birth` epic (phase 0: PyAutoMind#463).

## The demonstrated need

The human asked on 2026-10-02 (verbatim):

> Yesterday we filed an intake about building a pyauto organ (name tbh) which
> is the dahsboard layer above the _profiling repos. Can we begin that work

Three facts make that more than a preference:

1. **A real producer already publishes.** `autolens_profiling` writes
   `dashboard/series.json`, `dashboard/state.json` and its own Pages page, and
   since phase 1 (`complete/2026/10/profiling-summary-v1.md`,
   autolens_profiling#360) a versioned `dashboard/summary.json`
   (`profiling-summary` v1, grammar in `autolens_profiling/dashboard/README.md`).
   The exchange format exists; nothing reads it across projects.
2. **Every library is timed.** The libraries the run-time board covers sit on
   one stack, so a second `<lib>_profiling` producer is a matter of when; a
   per-project dashboard would be copied once per producer.
3. **There is no cross-project view.** No organ answers "how fast does the
   software run right now, across every profiled project, and what changed
   since the last release?" — the Heart answers whether it is healthy, the
   Eyes what it shows, not how fast it runs.

## Decision (human, 2026-10-02)

- **Name `PyAutoPulse`, organ key `pulse`, display name `Pulse`.** The pulse
  is a rate read over time, which is what the run-time-over-release board
  shows. The cockpit key is `pulse`, not the legacy wire label `profiling`
  that `autolens_profiling/dashboard/state.json` emits today (spec, "Two
  interfaces": that label is not proof the project is an organ). An earlier
  repo of this name was renamed to PyAutoHeart; the name was free again.
  Candidates not chosen: PyAutoMuscle, PyAutoReflex, PyAutoMetabolism.
- **Fresh repo, not a rename.** Unlike the Eyes, nothing is promoted:
  `autolens_profiling` stays a project. The human created
  `PyAutoLabs/PyAutoPulse` (public, empty).
- **Canonical organ order: after Hands, before Nerves** — Brain, Mind,
  Cortex, Memory, Eyes, Heart, Hands, Pulse, Nerves, Gut.
- **`config/policy.yaml` `boards:` entry deferred to phase 2**, when the
  organ's Pages board exists (the Eyes precedent, Brain `6a65f21`: no dead
  Pages link, no board-order test churn). The Brain board card and the
  cockpit transition are phase 3.

## Why an organ — the growth rule

`PyAutoBrain/ORGANISM.md`: a new organ "must earn that by owning state or
effects no existing organ can". A dashboard alone does not make an organ
(spec, "Decision"); the Pulse earns its repo with state no organ holds today:

- **The profiling instance registry** — which projects publish a summary,
  where, under which contract version.
- **The `profiling-summary` read contract** — the versioned exchange envelope
  every `<lib>_profiling` project produces and the organ validates.
- **The ingest receipts** — the resolved commit per project per render, so a
  board row can always be traced to the evidence it was built from.
- **The cross-project board** — one row per registered project, showing
  missing and refused evidence alongside valid data.

It is the fourth capability to earn an organ under the growth rule, after the
Nerves, the Cortex and the Eyes, and the same layering as the Eyes over the
`<lib>_visualization` project repos.

## Boundaries

- **vs the Brain's profiling conductor** — mirror **Heart ↔ vitals** and
  **Eyes ↔ Eyes conductor**: the organ holds the cross-project view; the
  conductor (`triage`) is the only judge of an observation, with the human.
  The Pulse never judges a timing.
- **vs the project repos** — `autolens_profiling` (and any later
  `<lib>_profiling`) keeps its producers, results, pins, drift policy and its
  own Pages page. The Pulse validates the exchange contract only — the project
  validates domain semantics. It never moves pins, combines unmatched
  timings, applies the compile threshold to runtime (the runtime 2x / 1 ms
  rule and the compile 1 s floor stay distinct, per source policy) or
  computes an ecosystem-wide speed score. Do not manufacture empty
  `<lib>_profiling` siblings; a fixture tests the reader (phase 2), a real
  second adopter is phase 4.
- **vs the Heart** — the Pulse issues no readiness verdict; its cockpit
  status summarizes its own monitoring scope, never release readiness.
- **vs the Mind** — findings become Mind prompts through intake/bug/start_dev;
  the Pulse holds evidence, not intent. Scientific lessons are recorded by the
  Cortex on the human's instruction.

## Lifecycle note

Decision taken in the 2026-10-02 session that filed the `profiling-organ-birth`
epic. Phase 1 (`profiling-summary` v1 in autolens_profiling) shipped first;
this record is written by phase 0 (PyAutoMind#463), which registers the organ
row. Phase 2 builds the skeleton (registry, reader, receipts, board,
workflows) and adds the `boards:` entry; phase 3 the Brain board strip and
cockpit transition; phase 4 waits for a real second producer.
