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
2. `draft/feature/pyautocortex/cortex_conductor_and_dashboard.md` — Brain
   `agents/conductors/cortex/`: census, stdlib dashboard render + Pages
   workflows, daily gate grading, the Cortex admission rule, collect scoring
   against the witness, the packet member format, the outside-workspace body-map
   resolver, and the Mind badge. **Brain PR merges before any Cortex/Mind PR**
   (renderer contract). Gate: 1.
3. `draft/feature/pyautocortex/cortex_project_remotes_and_registration.md` —
   `Lane: local-dev`. Private remotes + `.gitignore` for the Science-folder
   projects, `projects.yaml` rows, witness files tracked. Gate: 1. May overlap 2.
4. `draft/feature/pyautocortex/cortex_migration_split_epics.md` — the
   migration map below; rulings backfilled with ids; the 2026-08-31 science batch
   records move; the missing pm review is written; the stale pointers are fixed;
   reciprocal epic links; both dashboards regenerated. Gates: 2, 3.
5. `draft/feature/pyautocortex/cortex_batch_member_kind.md` — the second member
   kind in the batch conductor, separate records + `review-at:` per surface, the
   rolling board, carry-forward formalised Cortex-side, `AUTONOMY.md` leg 4 reads
   the member's own organ record. Gates: 2, **and** the two-slot-batching
   `collect` verb (`draft/feature/pyautobrain/batch_conductor.md`).
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
  a dev-only `collect` that phase 5 then reopens.
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
