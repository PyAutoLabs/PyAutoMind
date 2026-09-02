# Cortex phase 4 — migration: split the epics, backfill the rulings, move the science batch records, fix the stale pointers

Type: feature
Target: pyautocortex
Repos:
- PyAutoCortex
- PyAutoMind
- autolens_profiling
Themes:
- mind-workflow
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `lifecycle.py check` and `cortex.py check` both exit 0; the Mind dashboard's Epics section shows euclid-dr1-prep with phases 0–3b, 6c, 7 only and a "cortex half" link; the Cortex dashboard shows euclid-dr1-prep phases 4, 5, 6a, 6b `gated` on euclid#48 + the 3b issue; every ruling in DECISIONS.md since 2026-08-31 cites an `R-` id that resolves
Review-minutes: 30
Unattended: needs-slicing
Epic: cortex-birth
Phase: 4
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01
Issued: 2026-09-01

Phase 4 of 7 in the PyAutoCortex birth epic. **Gates: phases 2 and 3.** Gates
phase 6. Slices if needed: (a) epics + prompts, (b) rulings backfill, (c) batch
records + stale pointers.

Nothing here changes science state — it relocates the record of it. Every move
is a `git mv`-shaped edit with the source path recorded in the destination's
header (`Migrated-from:`), so the Mind's history and the Cortex's join up.

## Task

### (a) Split the epics — the migration map from the epic ledger

| Moves to the Cortex | From | `Gates:` it carries |
|---|---|---|
| euclid-dr1-prep 4, 5, 6a, 6b | `draft/research/euclid/{dr1_prelim_10_lens_science_run,sersic_index_recovery,magnification_robustness}.md`, `draft/feature/euclid/resimulate_fitted_lens_simulator.md` | 4: euclid#48 (3a) + 3b's issue; 5: phase 4's ruling; 6a/6b: phase 5's ruling |
| jax-inference-profiling (whole) | `epics.md` entry; PROGRAMME.md stays in `autolens_profiling` as commentary | autolens_profiling#200, #201 |
| graphical-ep phases 3, 4 science halves | `draft/research/graphical_ep/` (split each into a Mind dev prompt + a Cortex phase) | the dev halves' issues, when opened |
| cluster-strong-lensing phase 11 | `draft/feature/autolens/` arc member | phase 10's issue |
| subhalo-followup-adapt-split-rectangular | `active.md` + `active/follow_up_wave_adapt_split_and_rectangular.md` | none — runs 342093/342094/342095 already in flight; state `running` or `pulled` per the current pull |

Rules: Cortex phase numbers are distinct integers within a project (euclid 5
stays 5; 6a/6b become 6 and 7 — record the renumbering in both ledgers). The
Mind keeps its `Phase:` integers but fixes its own collisions (3a/3b → 3/4,
6c/7 → 8/9 — or whatever preserves order; document it). The euclid science
prompts' `Autonomy: safe` / `Unattended: ready` headers are wrong (ledger:
"supervised, never an autonomous ship gate") — they die with the move; the
Cortex phase files have no autonomy header at all. Mind `epics.md` entries gain
`- cortex-half: PyAutoCortex/epics.md#<slug>`; Cortex `epics.md` entries carry
`- mind-half:`. The Mind's `active.md` subhalo entry closes with a pointer to
the Cortex phase (no `complete/` record — it never had an issue; write a
one-line `complete/2026/09/subhalo-followup-moved-to-cortex.md` so
`lifecycle.py check` stays clean).

Stays in Mind (ruled): euclid 0–3b, 6c, 7; every dev phase of every epic; the
`numba-vs-jax-sparse` verdict; the pyautoreduce local-data research prompts
(default: stay — decide and record).

### (b) Backfill the rulings

- Every ruling in `autolens_profiling/results/notes/inference/DECISIONS.md`
  from **2026-08-31 onward** (the REWIND entry, the batch-am rulings, the
  2026-09-01 pm rulings) becomes a Cortex ruling `R-…` with the human's words
  verbatim; the DECISIONS entry gains a trailing `Ruling of record: R-…` line
  (append a correction entry — never edit the original text, per its own rule).
  Earlier entries are commentary and stay untouched.
- The subhalo rulings (`pl_sersic_0` ACCEPTED 2026-08-31, `pl_eff`
  leave-to-finish, the 2026-08-31 tweak rulings) become `R-…` entries; the
  journal and `results_summary.md` cite them.
- The three pm legacy-reuse rulings (`mge-pos-ref-reuse`,
  `mge-fp64-retro-baseline`, `delaunay-fp64-retro-baseline` REJECTED) become
  rulings with the `legacy`/`legacy_wrong` run states recorded on the phase.

### (c) Move the batch records and fix the stale pointers

- `PyAutoMind/batches/2026-08-31-am.md` + `packets/2026-08-31-am.html` +
  `reviews/2026-08-31-am.md` move to the Cortex (an all-science slot; the one
  dev retrospective member `euclid-phase2-pr46` stays listed with a note). The
  Mind keeps a one-line stub record pointing across so `ledger_merge` and the
  packet archive's stable-path rule are not broken: the HTML stays at the Mind
  Pages URL (localStorage notes are keyed by path) and the Cortex copy is the
  archive of record from now on.
- `batches/2026-08-31-pm.md`: the two carried science members and three ruling
  members are recorded in a new Cortex batch record `2026-08-31-pm.md`; the
  Mind record keeps its 9 dev members and gains the missing `reviewed-at:`,
  `review-minutes-actual:` and `review:` fields; **write
  `PyAutoMind/batches/reviews/2026-08-31-pm.md`** from the DECISIONS.md
  rulings (dated as the human's review, 2026-09-01 15:13, marked
  "transcribed") so the citation resolves.
- Fix: `queue.md` #3 path (`draft/research/subhalo_validation/…` → the Cortex
  phase; then retire the entry — science leaves the Mind queue); `queue.md` #9
  (superseded by this epic — phase 5 retires it; leave a note now);
  `epics.md` jax-compile-stall's nonexistent `draft/research/ci/` follow-up
  (file it or strike the sentence); DECISIONS.md's nonexistent
  `draft/maintenance/autolens_profiling/legacy_point_output_sweep.md` and
  PROGRAMME W10's nonexistent
  `draft/feature/autogalaxy/ell_comps_joint_disk_constraint.md` (file both as
  Mind drafts with their issues created — they are Cortex-spawned dev
  follow-ups, and the gate rule says the ref exists at filing);
  `batches/reviews/AGENTS.md:24` and `packets/TEMPLATE.md:64` collapse to the
  one Cortex vocabulary for science members (dev vocabulary untouched).
- Regenerate both dashboards (`pyauto-brain intake dashboard --apply`,
  `pyauto-brain cortex dashboard --apply`); Brain is already merged (phase 2).

## Acceptance

- The witness above; `git log --follow` on every moved file reaches its Mind
  history via the `Migrated-from:` header; no science prompt remains under
  `PyAutoMind/draft/research/` or `active/`.
- PRs: PyAutoCortex, PyAutoMind, autolens_profiling (DECISIONS correction
  entries + CORTEX.md), subhalo_validation (journal citations; commits on main).

## Out of scope

- Rulings before 2026-08-31 (commentary; not backfilled).
- The batch conductor (phase 5). This phase moves records; it does not change
  how the next batch is planned.
- Any RAL action. `legacy_point/` relocation directed 2026-09-01 is a laptop
  action already queued in the science ledger, not part of this phase.
