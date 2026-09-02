# PyAutoCortex — the science organ: split science runs out of the Mind

Type: feature
Target: pyautocortex
Repos:
- PyAutoCortex
- PyAutoMind
- PyAutoBrain
- PyAutoScientist
- pyautolabs.github.io
Themes:
- mind-workflow
- hpc-gpu
- dashboard
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cortex-birth
Filed: 2026-09-01

Parent tracker for a 7-phase programme that births a new organ, **PyAutoCortex**,
and moves every science run (RAL submissions, long waits, results pulled to the
laptop, inspected, ruled on) out of the PyAutoMind development dashboard onto a
science surface of its own. This file is never routed to `start_dev` directly —
each phase below is its own prompt, issued **ONE AT A TIME** as its predecessor
nears shipping (no bulk issue queues).

## Why (the human's three reasons, 2026-09-01)

1. **Batches go out of sync.** Development members finish in a shift and are
   ready to review; science members take hours to days. The review ends up
   deferring the science member to another batch (2026-08-31-pm: both laptop
   members CARRIED, three refreshes across 14 h, "Ruled 0 of 12" while the dev
   members sat reviewed).
2. **The reviews are different in kind.** Dev review is PRs and code
   descriptions. Science review needs the laptop, a pull from RAL, and inspection
   of `.err` / checkpoints / witness JSONs / PNGs.
3. **The Mind dashboard is already large.** Mixing two distinct kinds of run
   makes it bulkier and harder to read.

Both kinds of work must keep the batch-processing API — it is the right way to
manage them; they just cannot share one batch.

## The decision (ruled by the human 2026-09-01)

- **A new repo and a new organ: `PyAutoLabs/PyAutoCortex`, "the Cortex".** The
  cerebral cortex is where sensory input is interpreted and hypotheses are tested
  against the world. Boundary prose, to be written into `ORGANISM.md` verbatim:
  *the Mind decides what to build, the Brain routes the work and executes
  nothing, the Cortex learns what is true.* It owns state no organ owns today:
  the science body map (`projects.yaml`) and the rulings ledger. It passes the
  `PyAutoBrain/AGENTS.md` organ test ("owns state or effects no existing organ
  can") on that basis. Rejected names: PyAutoScience (collides with
  PyAutoScientist), PyAutoLab (collides with the org), PyAutoEyes (the Eyes
  conductor exists).
- **The Cortex is NOT a second PyAutoMind.** Mind is PR-shaped all the way down
  (completion records, `active.md`, "delivered = PR with diff and checks",
  `mind_commit_guard.py`, `lifecycle.py`); 125 of 332 August records already name
  no PR. The Cortex is a run-and-ruling registry: **project → phase → runs →
  rulings**, with the state model `planned / gated / ready / submitted / running
  / pulled / awaiting-ruling / accepted / rerun / dropped`, plus `legacy` and
  `legacy_wrong` as quarantine states (the 2026-08-31 REWIND made those real).
  Mind stays PR-shaped and keeps every development task.
- **Rulings of record — Option A.** The Cortex rulings ledger is canonical: *a
  verdict recorded only outside the Cortex does not exist.* Project ledgers
  (`autolens_profiling/results/notes/inference/DECISIONS.md`, `RESULTS.md`,
  `subhalo_validation/wiki/project/state.md`) remain as scientific commentary —
  evidence, reasoning, consequences — and cite the ruling id. Append-only,
  supersede-never-edit, exactly DECISIONS.md's existing culture. Why: on
  2026-09-01 one ruling was written in up to three places and one of them was
  never written (`DECISIONS.md` cites `PyAutoMind/batches/reviews/2026-08-31-pm.md`,
  which does not exist).
- **Gates are declared Cortex-side only, as GitHub issue/PR refs**, using the
  existing `Blocked-by:` grammar (`scripts/lifecycle.py` `GATE_REF_RE`; clears
  when every ref closes). A Cortex phase lists the dev issues it waits on. A
  Cortex-spawned dev follow-up gets its GitHub issue **at filing time** so the
  ref exists before the next phase is written. Mind learns nothing about the
  Cortex beyond a render-time badge, "gates a Cortex phase". One grammar, one
  direction.
- **Remotes.** Each Science-folder project (`subhalo_validation`, the private
  `euclid` tree, the future `euclid_dr1_prelim`) gets a **private PyAutoLabs
  remote** holding code, config, wiki and witness result files only; outputs,
  checkpoints and mirrors stay local and gitignored; **no Euclid data files of
  any kind**, private repo or not. The `inference_programme` laptop mirror stays
  remote-less ("holds data, not science"). PyAutoLabs rather than a personal
  account so the organ's sweeps and `repo_settings.yml` enumerate them; the
  personal-repo convention applies to papers, not projects.
- **Epics split by slug across both dashboards, with reciprocal links.** Each
  half's card links the other. Euclid keeps 0–3b, 6c, 7 in Mind and moves 4, 5,
  6a, 6b to the Cortex with the dev issues as gates; `jax-inference-profiling`
  moves whole (its dev phases are shipped); `graphical-ep` phases 3/4 science
  halves and `cluster-strong-lensing` phase 11 (the go/no-go verdict) move; the
  subhalo `active.md` entry (`issue: none — science project`) becomes a Cortex
  phase.
- **Batching.** One batch conductor in Brain, **two member kinds**, separate
  batch records and a separate `review-at:` per surface. Dev batches keep
  review-at-once. Cortex batches are a **rolling live board**: a member joins the
  review when its results are pulled, nothing mid-flight is reviewable, and the
  board is the live view of run progress (the human's note,
  `/mnt/c/Users/Jammy/Science/prompt.md`). Science "delivered" = `.err` clean +
  wall < budget + version stamp + `checkpoint.hdf5` sane — never `sacct
  COMPLETED`.

## Findings this epic rests on (from the 2026-09-01 audits)

- `PyAutoBrain/agents/conductors/batch/_batch.py` is **`plan`-only** (`:317`);
  dispatch, collect, the packet and the retrospective member are prose
  (`skills/batch/batch.md`, `batches/packets/TEMPLATE.md`), executed by hand on
  both 2026-08-31 batches. Generalising batching to two registries is a design
  job on unbuilt code, which is why now is the cheap moment.
- **`batch plan` can never propose a science run**: `_sizing.py:934-937` caps
  `research`/`experiment` at `supervised` and `plan()` rejects `!= safe`
  (`_batch.py:190`). Every science member so far was a human override.
- `queue.md:10` says `batch plan` reads it; `_batch.py:134` globs `draft/**`
  only. `kind: epic-slice|theme-sweep` entries have no consumer.
- `PYAUTO_MIND` is honoured only by `agents/_common.sh` and hygiene;
  `_sizing.py:92` hardcodes `BRAIN_HOME.parent/PyAutoMind/repos.yaml` at import
  and ignores `--mind`. `_intake.py` carries Mind literals at `:58, :744-746,
  :1631, :1988, :1997, :2294`. `_theme.py:70-110` keys the palette by organ.
  `policy.yaml:163-167` lists the board family. `install.sh:53,:70,:188` hold
  the organ arrays. `mind_commit_guard.py` keys on the literal dir name.
  `worktree.sh` uses a third env var `PYAUTO_MAIN`. `_pyauto_root.py:2-26`
  forbids absolute paths outside the workspace — the Science-folder projects
  live outside it.
- `Blocked-by:` is never a dashboard gate (only excludes from auto-bundles,
  `_intake.py:918-945`); `registry_reconcile.yml:34` runs `lifecycle.py issues`
  without `--drafts`, so declared gates are never auto-graded; all 5 current
  uses cite already-closed refs.
- Science state already lives outside Mind by rule (`epics.md`: "slices ship as
  autolens_profiling issues/PRs, not Mind prompts"); three projects keep three
  incompatible ledger formats and three incompatible `hpc/sync` CLIs.
- `ORGANISM.md:63-72`: a new organ costs an `AGENTS.md`, a `CLAUDE.md` stub,
  install wiring, a body-map row and boundary prose. Mechanically: `category:
  organ` + `organ: <Name>` in `repos.yaml` → `repos_sync.py --write` regenerates
  every organ's AGENTS.md map block, both public READMEs and the hub blurb check.
  **Nothing in the organism creates org repos** — the human makes the repo by
  hand on github.com.

## Phases (order is load-bearing)

0. **SHIPPED 2026-09-01** — `complete/2026/09/cortex-birth-organ-row.md` (PyAutoMind#377; theme/mark + policy board row deferred to phase 2, `install.sh` arrays to phase 1) — the human
   creates `PyAutoLabs/PyAutoCortex`; body-map organ row + `repos_sync.py
   --write`; `ORGANISM.md` row and boundary prose; `docs/organs/cortex.md`;
   theme palette + mark; `policy.yaml` board family; `install.sh` arrays; hub
   blurb. Gates nothing; gated by nothing. **Human-gated (repo creation).**
1. **SHIPPED 2026-09-01** — `complete/2026/09/cortex-schema-skeleton.md` (PyAutoMind#379; PyAutoCortex#1 + PyAutoBrain#329) — the Cortex
   repo skeleton: `projects.yaml`, phase file format + state model, `rulings/`
   ledger with ruling ids, `batches/` with rolling-board semantics and ONE
   review vocabulary, gates grammar, `cortex.py` lifecycle script, ledger-merge
   and never-rewrite-history policy, session-hook propagation. Gate: 0.
2. **SHIPPED 2026-09-01** — `complete/2026/09/cortex-conductor.md` (PyAutoMind#380; PyAutoBrain#330 → PyAutoCortex#2 → PyAutoMind#381) — Brain
   `agents/conductors/cortex/`: census, stdlib dashboard render + Pages
   workflows, daily gate grading, the Cortex admission rule, collect scoring
   against the witness, the packet member format, the outside-workspace body-map
   resolver, and the Mind badge. **Brain PR merges before any Cortex/Mind PR**
   (renderer contract). Gate: 1.
3. **SHIPPED 2026-09-01** — `complete/2026/09/cortex-registration.md` (PyAutoMind#382; PyAutoCortex#3, PyAutoBrain#331, autolens_profiling#204, plus subhalo_validation direct to its new private remote) —
   `Lane: local-dev`. Private remotes + `.gitignore` for the Science-folder
   projects, `projects.yaml` rows, witness files tracked. Gate: 1. May overlap 2.
4. **SHIPPED 2026-09-01** — `complete/2026/09/cortex-migration.md` (PyAutoMind#383; PyAutoCortex#4, PyAutoMind#384, autolens_profiling#206, plus subhalo_validation direct to its private remote) — the
   migration map below; rulings backfilled with ids; the 2026-08-31 science batch
   records move; the missing pm review is written; the stale pointers are fixed;
   reciprocal epic links; both dashboards regenerated. Gates: 2, 3.
5. `draft/feature/pyautocortex/cortex_batch_member_kind.md` — **SHIPPED 2026-09-02**
   (PyAutoBrain#334 → PR#335, PyAutoCortex#5; `complete/2026/09/cortex-batch-member-kind.md`) — the second member
   kind in the batch conductor, separate records + `review-at:` per surface, the
   rolling board, carry-forward formalised Cortex-side, `AUTONOMY.md` leg 4 reads
   the member's own organ record. Gates: 2, **and** the two-slot-batching
   `collect` verb (`draft/feature/pyautobrain/batch_conductor.md` — SHIPPED
   2026-09-02, PyAutoBrain#332, `complete/2026/09/batch-collect.md`; gate open).
6. `draft/feature/pyautocortex/cortex_public_surfaces.md` — RTD organ page,
   PyAutoScientist row, hub, and the retrospective: what the first Cortex batch
   taught; the explicit deferred list. Gates: 4, 5.

## Migration map (phase 4 executes this)

| Moves to the Cortex | From | Gates it carries |
|---|---|---|
| euclid-dr1-prep phases 4, 5, 6a, 6b | `draft/research/euclid/`, `draft/feature/euclid/resimulate_fitted_lens_simulator.md` | euclid#43/#45 closed; 3a euclid#48; 3b's issue when opened |
| jax-inference-profiling (whole epic) | `epics.md` entry; ledger stays `autolens_profiling/results/notes/inference/PROGRAMME.md` as commentary | autolens_profiling#200, #201 |
| graphical-ep phases 3 (slope_hierarchy N=25–50 on A100) and 4 (IC50 EP) science halves | `draft/research/graphical_ep/` | their dev halves' issues |
| cluster-strong-lensing phase 11 (go/no-go verdict) | `draft/feature/autolens/` arc members | phase 10's issue |
| subhalo-followup-adapt-split-rectangular | `active.md` (`issue: none`), `active/follow_up_wave_adapt_split_and_rectangular.md` | none (already running: 342093/342094/342095) |
| `batches/2026-08-31-am.md` + `packets/2026-08-31-am.html` + `reviews/2026-08-31-am.md` | `PyAutoMind/batches/` (all-science slot) | — |
| pm's two carried science members + 3 legacy-reuse ruling members | `batches/2026-08-31-pm.md` members list (record stays in Mind for its 9 dev members) | — |

Stays in Mind: euclid 0–3b, 6c, 7; every dev phase of every epic; the
`numba-vs-jax-sparse` research verdict (a reading, not a run); the
pyautoreduce local-data research prompts (local data, not RAL — decide at phase 4
whether "runs on the laptop" is enough to move them; default: stay).

Stale pointers phase 4 fixes: `queue.md` #3 path (`draft/research/subhalo_validation/…`
moved to `active/`); `epics.md` jax-compile-stall's nonexistent
`draft/research/ci/` follow-up; `DECISIONS.md`'s nonexistent
`draft/maintenance/autolens_profiling/legacy_point_output_sweep.md` and
PROGRAMME W10's nonexistent `draft/feature/autogalaxy/ell_comps_joint_disk_constraint.md`
(file them or strike the citations); `batches/2026-08-31-pm.md` lacking
`reviewed-at:` / `review-minutes-actual:` / `review:`; euclid 6a/6b headers
(`Autonomy: safe`, `Unattended: ready`) contradicting the ledger's "supervised,
never an autonomous ship gate"; the euclid 3a/3b and 6a/6b/6c integer `Phase:`
collisions; the two review vocabularies (`batches/reviews/AGENTS.md:24` vs
`packets/TEMPLATE.md:64`).

## Cross-epic reconciliation — two-slot-batching

- Its "Placement — no new organ" ruling is about the **batch layer** and stands:
  queue, batch records, planner, conductor and board stay where they are; the
  graduation trigger to `PyAutoRhythm` is untouched. The Cortex is not the
  batch layer; it is the registry the batch layer reads for science members, as
  the Mind is for dev members.
- Its **phase 8** (`draft/research/euclid/batch_science_lane.md`, "the laptop
  lane" — `Lane:` on every remaining euclid phase, `queue.md` #9) is
  **superseded by this epic**: the euclid science phases move to the Cortex,
  where the laptop lane is the only lane. Its recorded closures (RAL as
  canonical home, git courier, Globus, self-hosted runner: all refused) carry
  over verbatim into the Cortex `AGENTS.md`. Its leg B (manifest-first results)
  is what `projects.yaml`'s witness-file column formalises. Phase 5 here marks
  it superseded in the two-slot ledger and retires `queue.md` #9.
- Its `collect` verb (phase 2, `batch_conductor.md`, `queue.md` #8) is a hard
  gate on phase 5 here. Build `collect` once, with two member kinds, rather than
  a dev-only `collect` that phase 5 then reopens. **Shipped 2026-09-02**
  (PyAutoBrain#332, `complete/2026/09/batch-collect.md`) kind-neutral: the
  `dev` kind plus the `KINDS` registry phase 5 registers `cortex` on.
- `queue.md` #2 (carry-forward formalisation, `batch_carry_forward.md`) is
  absorbed by phase 5 here on the science side; the dev side keeps whatever the
  two-slot prompt decides.

## What this epic does NOT do

- **No dispatcher.** Dispatch of science members is the human at the laptop
  (`hpc/sync push-submit`, `run_chain.sh`), by the 2026-08-30 ruling.
- **No unification of the three `hpc/sync` CLIs** (profiling pull-only; subhalo
  push/pull/submit/wait-and-pull; euclid push/pull/sync/status). `projects.yaml`
  records which one each project has; unifying them is a follow-up filed at
  phase 6 if the first Cortex batch shows the divergence costs review minutes.
- **No Cortex template / `spawn.py` entry** until a fork asks for one.
- **No fold-in of the Eyes conductor** (figure review). Inspecting result PNGs is
  half of a science review, so it is a plausible later home — recorded as an
  open question at phase 6, explicitly out of scope here.
- **No move of the science project trees themselves.** They stay under
  `/mnt/c/Users/Jammy/Science/`; the Cortex points at them.

## Notes for whoever resumes this

- Phases 0 and 3 need the human (repo creation; laptop + remotes). Phases 1, 2,
  4, 5, 6 are ordinary development and can run as cloud members once their gates
  close.
- Renderer changes: **Brain PR merges before the Cortex or Mind PR** — the Cortex
  dashboard workflow checks out Brain `main`, exactly like
  `dashboard_refresh.yml`, and token pushes fire no downstream events, so the
  Pages workflow must be redispatched explicitly.
- Phase-number rule for Cortex phases: distinct integers only. The euclid
  3a/3b, 6a/6b/6c collisions are the reason.
- The human wants to be able to look at one epic and see both halves. The slug
  is the join key; every card links across.

## What the first Cortex batch taught (phase 6 — 2026-09-02)

**Nothing yet, and saying so is the finding.** No Cortex batch has been planned
and reviewed through the phase-5 door. The two records in
`PyAutoCortex/batches/` are both `2026-08-31`, transcribed at phase 4 from the
Mind's records of a slot that was hand-driven before the second member kind
existed, and **neither carries a numeric `review-minutes-actual:`** — the am
record reads *"excluded — workshop session (the framework was built and
polished mid-review)"*, the pm record *"(not given)"*. There is therefore no
calibration point, and the phase-5 record says the same in its own words: the
first one is `review-minutes-actual:` on a conductor-opened record, at the
laptop.

The prompt asked for facts. The honest fact is that the evidence does not
exist yet, so this section is a **stub**, not a retrospective, and it is
written down rather than left blank so nobody re-runs the search. When the
evidence lands, answer these four:

1. **Planned vs actual minutes on the first conductor-opened record.** The
   only two numbers on file are estimates from before the door existed
   (`review-minutes-planned: 121` and `74`), and both slots' actuals were
   never taken. The question the budget rests on — does a science slot cost
   what the phase seeds say it costs — is still unmeasured.
2. **Did the rolling board remove the CARRIED pattern?** The pattern this epic
   was filed against is `2026-08-31-pm`: eight science members, three ruled,
   five carried, "Ruled 0 of 12" on the mixed Mind slot. The rolling board plus
   `- carried:` / `- carried-from:` is meant to make that ordinary rather than
   a stall. Compare the first two conductor-opened slots against those numbers.
3. **Did any gate flip automatically?** `gates_grade.yml` has run daily since
   it shipped with **phase 2** (2026-09-01) — one day earlier than the first
   real phases, so it has graded a non-empty registry for barely a day. As of
   2026-09-02 **no phase carries a `Gates-cleared:`** and exactly one phase is
   `gated`: `phases/euclid/dr1_prelim_10_lens_science_run.md`, waiting on
   `euclid_strong_lens_modeling_pipeline#48, #49`. The first automatic flip is
   still ahead; when it happens, check that the phase arrived in `ready`
   without a human touching the file.
4. **What did the human do by hand that the design said would be automatic?**
   That list is the real product of a retrospective. Phase 2 already logged
   three of its own (Pages enablement, `delete_branch_on_merge`, the
   `PAT_PYAUTOLABS` admin gap on PyAutoCortex); a slot run end-to-end is what
   surfaces the rest.

**What unblocks this section:** the first `batch plan --kind cortex --apply`
record closed with a review at the laptop. Until then there is nothing to
calibrate against and nothing to compare.

**No follow-up prompts filed — facts first.** The prompt allowed up to three;
filing them on intentions rather than evidence is exactly the re-derivation
this ledger exists to prevent.

## Deferred (recorded so nobody re-derives it)

Five things this epic deliberately did not do. Each carries the reason, so a
later session decides on the reason rather than re-opening the argument.

- **Eyes conductor fold-in (figure review as part of a science review).**
  Inspecting result PNGs is half of a science review, so the Eyes conductor is
  a plausible later home for that half — but which half, and whether the
  packet or the conductor owns it, is not answerable from zero slots. **Open
  question; decide only after two Cortex batches have been reviewed.**
- **`hpc/sync` unification across the three projects.** They diverge today
  (profiling pull-only; subhalo push/pull/submit/wait-and-pull; euclid
  push/pull/sync/status) and `projects.yaml` records which one each project
  has, which is enough for `collect --pull` to work. **File it only if the
  retrospective shows the divergence cost review minutes** — unifying three
  working CLIs on aesthetics is not a task.
- **A Cortex template / `spawn.py` entry.** The Cortex is an instance organ;
  its shape is documented in `REFERENCE.md` and on the RTD organ page.
  **Not until a fork asks for one** — a template maintained against no
  consumer rots.
- **The batch board strip showing both kinds.**
  `draft/feature/pyautobrain/batch_board.md` (two-slot-batching phase 6,
  `small`/`safe`) is still unshipped and renders the *Mind's* batch state on
  the Mind dashboard. Teaching it a second kind is that prompt's business, not
  this epic's, and there is nothing to render side by side until a Cortex slot
  is live. Meanwhile the Brain board already carries the Cortex counts row
  phase 2 shipped. **Deferred to `batch_board.md`.**
- **A `cortex: true` flag on `repos.yaml` `category: project` rows
  (`autolens_profiling`) for the badge resolver — decided: not needed.**
  Phase 2 built the resolver the other way round
  (`complete/2026/09/cortex-conductor.md`): it probes `PYAUTO_CORTEX` or a
  sibling `PyAutoCortex`, reads every Cortex phase's `Gates:`, and badges any
  Mind prompt whose issue or PR ref appears there — render-only, no new
  imports, silent when no Cortex resolves. It never consults `repos.yaml`, so
  a Mind-side flag would be a **second source for a fact the Cortex already
  declares**, against this epic's "one grammar, one direction" ruling.
  Revisit only if something needs to answer "is this repo science?" *before*
  reading the phases.
