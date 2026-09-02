- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/383 (closed completed 2026-09-01)
- completed: 2026-09-01
- workspace-pr: PyAutoCortex https://github.com/PyAutoLabs/PyAutoCortex/pull/4 (`3cadb0e`, merge `3346da2`) →
  PyAutoMind https://github.com/PyAutoLabs/PyAutoMind/pull/384 (`f8c3a57`, merge `cb1e362`) →
  autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/206 (`2a2bc41`, merge `385de50`),
  merged in that order. Plus **no PR** for `subhalo_validation`: `014c349` + `f432c8d` pushed direct to `main`
  on its private remote (a Science-folder tree, not a workspace repo — the phase-3 pattern).
- classification: feature (pyautocortex) — epic `cortex-birth`, phase 4 of 7. Gates: phases 2 (SHIPPED #380)
  and 3 (SHIPPED #382). Gates phases 5 and 6.
- heart: YELLOW 80 at ship, acknowledged on the `active.md` entry — `PyAutoArray: open PR 10d old` and
  `release validation incomplete: no rehearsal for current source`. Both pre-existing and structurally
  unrelated to a markdown/ledger migration.

- summary: **the migration** — the science half of the organism leaves the Mind and becomes the Cortex's.

  **PyAutoCortex** now holds **21 phases** (euclid 4 gated on euclid#48 + euclid#49, 5–7 `planned` with
  `Ready when:`; inference_programme 1–11 — the REWIND as one ruling on a synthetic phase, the four
  2026-08-31-am rejections, the three pm rulings, the `342091` refs redo awaiting its ruling, and cluster
  phase 11; subhalo_validation one phase per lens; slope_hierarchy and ic50_workspace phase 1), **12 rulings
  of record** (`R-20260831-01..08`, `R-20260901-01..04` — the human's words verbatim, `Reviewed-at` 13:34Z /
  15:13Z, all 12 chain heads), the **two 2026-08-31 science batches** transcribed in the Cortex grammar with
  their reviews and archived packet copies, and **four `epics.md` entries** carrying `mind-half:`. Every
  migrated file names its Mind source in `Migrated-from:`. The two "find it" job ids (339070 `mge_fp64`,
  339071 `delaunay_fp64`) were resolved from the baselines' `source_artifact` and the mirror logs, not guessed.

  **PyAutoMind** — eight science prompts removed (their history stays here; the Cortex names them), the
  subhalo follow-up active entry closed with `complete/2026/09/subhalo-followup-moved-to-cortex.md`, euclid
  phases renumbered (3a/3b → 3/4, 6c/7 → 8/9) with the split recorded in the epic ledger, four `epics.md`
  entries given `cortex-half:`, queue #3 retired and #9 noted, the jax-compile-stall phantom follow-up struck,
  the malformed `ep_campaign.md` header fixed, the missing `batches/reviews/2026-08-31-pm.md` written and the
  pm record given its three missing fields. One science vocabulary in `reviews/AGENTS.md` and
  `packets/TEMPLATE.md`.

  **autolens_profiling** — one appended `DECISIONS.md` entry maps each 2026-08-31/2026-09-01 decision to its
  ruling id and Cortex phase path (`R-20260831-01..05`, `R-20260901-01..04`; the `342091` redo awaits a
  ruling), **editing nothing above it**; `CORTEX.md` lists the ids and drops the "no ruling id to cite yet"
  clause.

  **subhalo_validation** (private) — the wiki cites the Cortex rulings of record, the three landed witnesses
  are recorded as facts, and `pl_eff_1_outer`'s ruling of record was corrected to **R-20260831-08**: the human
  made one leave-to-finish call over both `pl_eff` lenses, and the fan-out files one ruling per phase, so that
  single call is recorded as -07 and -08 with the same body.

- decisions: **53** `Migrated-from:` becomes a schema key on `PHASE_KEYS`/`RULING_KEYS` — a migrated file
  names its Mind source, so the move is auditable from the file rather than from a commit message.
  **54** intra-Cortex sequencing is expressed as `status: planned` + a prose `Ready when:` line, not as a
  gate — gates are GitHub refs, and a phase waiting on a sibling phase has no ref to point at.
  **55** a Cortex-spawned **dev** follow-up gets its GitHub issue **at filing**, without leaving `draft/`:
  the prompt carries an `Issue:` line and `create_issue` reuses it rather than opening a second. Written into
  `REFERENCE.md` and `skills/create_issue/SKILL.md`. Three issues opened that way —
  euclid_strong_lens_modeling_pipeline#49 (the 3b gate), autolens_profiling#205 (the `output/legacy_point/`
  sweep from R-20260901-03), PyAutoGalaxy#594 (the W10 `ell_comps` joint disk constraint).
  **56** legacy-born encodings: one subhalo phase per lens; batch records transcribed with the Mind originals
  kept intact as the verbatim history; both records point at their Cortex transcriptions.

- inventory corrections to the prompt: the phase prompt was written before the trees were read, and the
  inventory corrected it in these places — each fix is in the shipped files, not only here.
  1. `euclid#48` is a **merged PR**, not an open issue — the gate reads as satisfied, not pending.
  2. There was **no euclid 3b issue** at all; opened at filing as euclid#49 (decision 55).
  3. Cluster phase 11 lives under `draft/research/autolens/`, not `draft/feature/autolens/`.
  4. The 2026-08-31-**am** rulings existed **only in the review file** — no ledger entry carried them.
  5. `Migrated-from:` had no key in the schema; adding one is decision 53.
  6. `cortex.py new` **cannot create a `pulled` phase** — the migrated running phases had to be created and
     then moved.
  7. `cortex.py rule` has **no `--now`** — `Reviewed-at` is passed explicitly.
  8. The subhalo runs were **further along** than the prompt assumed: all three witnesses had landed, so the
     phases were migrated as finished-and-awaiting-ruling rather than as running.
  9. The `2026-08-31-pm` **review file did not exist** in the Mind at all; it was written as part of this
     phase from `DECISIONS.md` and the record.
  10. **Both** prompts the prompt called nonexistent really were absent (`legacy_point_output_sweep.md`,
      `ell_comps_joint_disk_constraint.md`) — filed, with issues, rather than struck.
  11. The `Phase:` collisions were **worse** than the prompt recorded (see the follow-ups below).
  12. `draft/research/graphical_ep/ep_campaign.md` had a **malformed header**, fixed here.
  13. `phases/` did not exist in the Cortex before this phase — the migration creates the whole tree.

- deviations from the phase prompt, each recorded in the files: **12 rulings not 11** (`--also` files one
  ruling per phase); **8 am members not 7** (one subhalo phase per lens); **`Follow-ups accepted` is a `###`
  block**, not `##` — `check` requires every `##` in a review file to name a member of the slot's batch
  record, so the review grammar in `batches/reviews/AGENTS.md`, `REFERENCE.md` and `batches/packets/TEMPLATE.md`
  now says so; the REWIND ruling and the carried failed-submissions ruling carry **no `Batch:`** (neither was a
  batch member); run pointers are **mirror-relative** (the review happens at the laptop);
  autolens_profiling's mapping covers `R-20260831-01..05` + `R-20260901-01..04` only — `-06..08` are
  subhalo_validation's and are cited in that project's wiki, not in `DECISIONS.md`.

- witness: `cortex.py check` OK and `pytest tests -q` → **131 passed** on the branch and again on canonical
  `main`. Post-merge census: 21 phases (accepted 3 · awaiting-ruling 4 · dropped 7 · gated 1 · planned 6),
  12 rulings (12 heads), 11 projects, 2 batch records + 2 reviews, 4 epics. `_cortex.py dashboard --check`
  current; `https://pyautolabs.github.io/PyAutoCortex/` returns **200** after `pages_dashboard.yml`. Mind:
  `lifecycle.py check` OK, `pytest tests -q` → 307 passed, `Dashboard Refresh` + `Lifecycle Drift` +
  `Spawn Drift privacy` green. autolens_profiling: `lint` green.

- trap (new, worth knowing): the Mind dashboard's `generated … on <date>` stamp is rendered on the **local**
  clock. A laptop still on 2026-09-01 (EDT) produces a page that Actions — rendering on 2026-09-02 (UTC) —
  reads as stale, and the PR's `Dashboard Refresh` fails on the two date lines alone. Regenerate with
  `TZ=UTC` when the local date and the UTC date differ (commit `f8c3a57`).

- follow-ups NOT filed (named here so they are findable, none of them blocking):
  - The Mind dashboard renderer **ignores `cortex-half:`** — the four epics carry the key and nothing renders
    it. A small `_intake.py` change would put the Cortex link on the epic row.
  - `queue.md` **#9 carries two `note:` lines** ("leg A only …" and "superseded by cortex-birth (phase 5
    retires it)"); the schema shows one.
  - `complete/2026/07/slope-hierarchy.md` cites `draft/research/graphical_ep/slope_hierarchy_n25_scale_up.md`,
    a path this migration removed. Left as written: a completion record is history, not a live pointer.
  - The **`Phase: 10` collision** stands — `draft/docs/workspaces/cluster_regime_narrative.md` and
    `draft/feature/workspaces/cluster_pixelized_analysisfactor.md` both claim phase 10 of the cluster arc.

- next: phases **0–4 of `cortex-birth` are SHIPPED** (#377, #379, #380, #382, #383).
  **Phase 5** (`draft/feature/pyautocortex/cortex_batch_member_kind.md`) is the next phase and is **not yet
  unblocked**: it gates on Cortex phase 2 (SHIPPED #380) **and** on the two-slot-batching `collect` verb, and
  `draft/feature/pyautobrain/batch_conductor.md` still reads `Status: in progress — … remaining: the collect
  verb (queued — queue.md #8) and slice`. Build `collect` once with both member kinds, per that prompt.
  **Phase 6** (`cortex_public_surfaces.md`) gates on phases 4 **and** 5 plus one real Cortex batch reviewed,
  so it is blocked behind 5 — not unblocked by this merge.

## Original prompt

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
