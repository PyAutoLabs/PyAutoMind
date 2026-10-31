# Likelihood lifecycle phase 2b/2c: ingest the quiet-node RAL CPU reruns (follow-up PRs)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: the quiet rows of the 38 2b RAL CPU legs and the 2 2c solved RAL CPU legs are committed as current (or each non-quiet leg is named with the human's ruling); the shared _common.py quiet-node gate and --exclusive option are reviewed and merged; coverage, catalogue and campaign pages regenerated; build_catalogue --check --validate-with ../PyAutoPulse valid
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-29
Issued: 2026-10-31
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/493

- Status: split out of `likelihood-lifecycle-p2b-interferometer` and `likelihood-lifecycle-p2c-point-source` at close-out 2026-10-29. Both campaigns shipped and are recorded in `complete/2026/10/likelihood-lifecycle-p2b-interferometer.md` (autolens_profiling#471, #483, #481) and `complete/2026/10/likelihood-lifecycle-p2c-point-source.md` (#480, #481); this is what remains: the quiet-node reruns queued on RAL the same day.
- Blocked-by: the RAL jobs below finishing.

## Why

Human 2026-10-29 "do the reruns now": the published 2b batch-1 RAL CPU legs and the 2 2c solved RAL CPU runtime legs ran on loaded nodes, so their per-call numbers may be noisy. The reruns hold each leg until the node is quiet and run it `--exclusive`.

## In flight (queued 2026-10-29)

| Campaign | RAL job | Array | Legs | Branch (pushed, **no PR**) | RAL checkout → output |
|---|---|---|---|---|---|
| 2c solved CPU runtime | 413319 (was 413267) | `[0-1%2]` 1:00:00 | 2 | `feature/likelihood-lifecycle-p2c-quiet-rerun` f99c70ed (was eb8b3237) | `/mnt/ral/jnightin/profiling/autolens_profiling_p2c_rerun` → `output/p2c_quiet/` |
| 2b sma | 413320 (was 413268) | `[0-13%2]` 1:00:00 | 14 | `feature/likelihood-lifecycle-p2b-quiet-rerun` 7c682ccb (was bd0dca1d) | `/mnt/ral/jnightin/profiling/autolens_profiling_p2b_rerun` → `output/p2b_quiet/` |
| 2b alma | 413321 (was 413269) | `[0-7%2]` 1:00:00 | 8 | same | same |
| 2b alma_high | 413322 (was 413270) | `[0-7%2]` 1:00:00 | 8 | same | same |
| 2b jvla | 413323 (was 413271) | `[0-7%2]` 4:00:00 | 8 | same | same |

- All chained `afterany` (2c first, then 2b sma → alma → alma_high → jvla), `--exclusive`, at most 2 nodes at once. 38 2b legs + 2 2c legs.
- Submit log: `/mnt/ral/jnightin/scratch/p2_quiet_rerun_submit.log` (first submission 413267-413271, held JobHeldUser, never started; CANCELLED 2026-10-29 20:38 GMT).
- RESUBMITTED 2026-10-29 20:38 GMT on the jax 0.11.2 venv with the XLA:CPU workaround (human option "All JAX CPU legs"): both branches merged main fe81b1f4 (#486: `--xla_cpu_multi_thread_eigen=false` appended to XLA_FLAGS on every JAX_PLATFORMS=cpu leg, recorded in `device.xla_flags`) and re-rendered their quiet submits. Script `/mnt/ral/jnightin/scratch/p2_quiet_rerun_resubmit_jax0112.sh`, log `p2_quiet_rerun_resubmit_jax0112.log` (marker P2QUIETRESUBMITDONE). Guards that ran: venv reads jax/jaxlib 0.11.2, both HEADs == SHAs, clean trees, pin 2026.10.25.1, every quiet submit has the flag + `--exclusive` + quiet gate + `%2`, datasets present, no quiet output, each held array PENDING JobHeldUser before the scancel. Same afterany chain 413319 -> 413320 -> 413321 -> 413322 -> 413323.
- ENV CHANGE: RAL venv `/mnt/ral/jnightin/PyAuto/PyAuto` upgraded jax/jaxlib/jax-cuda12-{plugin,pjrt} 0.10.2 -> 0.11.2 (human 2026-10-29; log `scratch/jax0112_upgrade.log`; freezes `scratch/pyauto_venv_freeze_{before,after}_jax0112_20261029.txt`). The quiet rows are therefore NOT like-for-like with the published 2b/2c rows they replace (those were jax 0.10.2, no flag): this changes two things at once (load and jax/flag); the ingest must say so and the human rules whether they replace or sit alongside (phase-3 Q7).
- Local worktrees: `~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2b-quiet-rerun`, `~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2c-quiet-rerun` (kept at close-out; do not remove until the ingest PRs merge).

## How to tell a row is quiet

- In the row: `device.provenance.loadavg_at_import[0] <= 8` **and** the host is not `euclid-ral-compute-1`.
- In the job's `.out`: the gate prints `QUIET:` when it ran on a quiet node, and `QUIET-WAIT TIMEOUT` when it gave up waiting (that leg is **not** quiet; report it, do not publish it as current without a human ruling).

## What to do

1. Wait for 413319–413323 to finish (`sacct`); never touch another campaign's jobs.
2. Review first: both rerun branches change the shared `scripts/misc/campaigns/_common.py` (quiet-node gate, `--exclusive` option). Open them as PRs with that change called out; `imaging_p2a.py --check`, `interferometer_p2b.py --check` and the other campaign `--check`s must stay byte-identical or the diffs explained.
3. Pull `output/p2{b,c}_quiet/`; classify every leg quiet / not quiet as above.
4. Ingest the quiet rows as **follow-up PRs** (one per campaign is fine): replace the published RAL CPU rows (prior rows → `history/` via the catalogue builder), keep parity `match`, regenerate catalogue / coverage / dashboard, update the 2b and 2c campaign pages' verdict if a number moves, refetch the Pulse receipt.
5. 2b's matrix-free alma 192² leg 413191_6 stays missing by human ruling (2026-10-29); it is not part of this rerun.

## Rules (every phase-2 sub-issue; epic ledger "Phase 2" card)
- The coverage matrix (`python scripts/misc/tooling/coverage_matrix.py` → `dashboard/coverage.md`) names this campaign's missing and stale cells; those cells are the work list.
- Every cell is measured at the standard size (Delaunay 1250, rectangular 35² = 1225; human ruling 2026-10-23) on a pinned released tag, from a private RAL checkout (never the shared mirror). CPU arrays go on `--partition=ral` only; A100 runs use `--gres`. **The human gives a go for each RAL batch.** Never touch another campaign's jobs.
- Every cell lands as `current`, carrying runtime and breakdown, provenance, `fit.png` (phase 1B renders it automatically) and a `parity.json` against a reference log-likelihood. Prior rows on the key become `superseded` through the catalogue builder.
- A campaign page at the mirrored wiki path (`wiki/campaigns/<dataset_type>/<variant>/`) records the rule and the expected verdict before the runs, then the result.
- Pulse receipt refetched after merge. Phase 2 ends only on the human's "campaigns complete" confirmation (the gate for phase 3).
