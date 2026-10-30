# HPC campaign epic: run large modelling campaigns efficiently, token-cheaply and low-carbon

Type: research
Target: autofit
Repos:
- PyAutoFit
- PyAutoNerves
- PyAutoCortex
- PyAutoBrain
- autolens_assistant
- euclid_strong_lens_modeling_pipeline
Themes:
- hpc
- euclid
- carbon
Difficulty: large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself
Epic: hpc-campaign
Filed: 2026-09-27

Research report and phased epic plan: `hpc_campaign_epic_report.md` alongside this file (written 2026-09-27 by the Fable architect session; no code edited).

## Hard constraint (human, 2026-09-30)

Every phase that builds submit, plan or queue tooling (campaign `plan`/`submit`, the
scheduler adapter, the allowlisted scheduler-action tool, `hpc/sync` verbs, `site.yaml`)
must enforce this rule, not merely document it:

- **Never submit bulk or production CPU-only arrays to RAL's `gpu` partition** — including
  `--partition=ral,gpu` and `gpu,ral`, and even when `ral` nodes are drained or busy; the jobs
  wait for `ral` instead.
- Why: on 2026-09-30 euclid_dr1 CPU arrays submitted with `ral,gpu` occupied all 124 CPUs on
  both euclid-ral-gpu-1 and gpu-2; all 8 A100s sat idle but unschedulable for hours, with
  3,938 CPU tasks queued eligible for those nodes. The human called it bad practice that must
  never happen.
- Narrow exemption: small bounded CPU timing legs (e.g. autolens_profiling quiet-node timing)
  may use `gpu` without `--gres` only if all three hold: ≤8 CPUs per task, array throttle
  ≤`%2`, and no GPU jobs pending at submit time (`squeue -p gpu -t PD` shows none requesting
  gres/gpu).
- Diagnosis: a partition name does not tell you the device. Before calling a job a "GPU run",
  check its TRES for `gres/gpu` with `scontrol show job`; for a stuck A100 job compare the
  node's `AllocTRES` cpu with `CfgTRES`.
- Never reorder, hold or cancel another campaign's jobs without the human's OK.
- Suggested enforcement: submit tooling lints every `#SBATCH --partition` (and any
  `--partition`/`-p` override) and refuses a partition list containing `gpu` for a script
  that requests no `gres/gpu`, unless the exemption's three conditions are checked and met
  at submit time. `site.yaml` should mark `gpu` as GPU-only so the planner never packs CPU
  tasks there.

## Phases (amended 2026-10-28)

Maps report §5 to the order set by the final scoping review
(`Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/REVIEW.md`
§C–§D). Library first; one issue per repo per phase; run concurrently with
results-library (human decision, 2026-10-28). PyAutoFit hooks are the
search-extensibility A-series (`FitContext`/`run(ctx)`, `Checkpointer`,
`open_atomic`), not the 09-27 line references.

0. **Integrity primitives (report #A)** — issued as **results-library phase 0**
   (one PyAutoFit issue, PRs 0a/0b; issue number recorded below when filed).
   Not re-issued here. The `fit()` failure record moved to phase 1.
1. **Status record** — PyAutoFit `autofit/non_linear/status/`: per-fit
   `status.json` + `status.jsonl` (≤2 KB, tmp-then-rename, beside the zip),
   `progress()` protocol, resource probe (cgroup `memory.peak` → `getrusage`;
   NVML), SIGUSR1/SIGTERM → checkpoint flush, **failure record** on exception,
   **`states.py`** (run states, failure classes, product names; imported by
   results-library). PyAutoNerves `site.yaml` layer + `Config.push_site(name)`,
   example `site/ral.yaml` with `unverified: true` markers (`gpu` marked
   GPU-only). autofit_workspace docs. Merges after results-library PR 0a.
2. **Campaign core** — PyAutoFit `autofit/campaign/`: `campaign.yaml`,
   `Scheduler` protocol, `FakeScheduler`, `LocalScheduler`, `SlurmScheduler`
   (batched sacct/squeue/sinfo, sbatch with `aftercorr`, `--mem-per-cpu`,
   `--signal=B:USR1@600`), collector → `digest.json`/`digest.md` (≤2 KB),
   triage, propose-only `resubmit --class`, disk forecast, **partition lint**
   (refuses `gpu` in a CPU job's partition list unless the three timing-leg
   conditions hold) and **retrospective mode from a sacct dump**.
3. **Evidence + plan + pilot** (was report phase 4) — readers for
   `profiling-summary@3`, `walltime-validation@1`, `inference-summary@2` by
   path/URL with **evidence grades** (measured-current / provisional /
   superseded / estimated / unsupported); `campaign plan` and `campaign pilot`.
   Never designates `optimal`.
4. **Carbon + report** (was report phase 5; parallel with 3) — Green-Algorithms
   model, usage + allocation bases, ranges from site bounds, optional NESO
   fetch; `campaign report`. Nerves carbon keys.
5. **Organism integration** (was report phase 3) — fold pipeline `hpc/sync`
   drift into the assistant template first, then template v2 + sync verbs +
   skill; Cortex `sync-runs` under decision 62; Brain conductor + governance
   hook; pipeline adoption only after DR1 v1.0 ships.
6. **Generalisation** — other workspaces, PBS on demand. Low priority.

## Rulings (human, 2026-10-28)

Human's words, verbatim: "F1 your recommendations, F2 ok, F3 yes, 4. yes do the 50 task thing, F5 ok, F6 ok, F7 ok, F8 ok as long as its 500 datasets i dont mind us using dr1 but whatever seems easiest, F9 ok F10 ok F11 ok F12 should be Claude and codex. F4a yes, F4b yes"

- **F3 (Cortex decision 62):** yes — `cortex sync-runs --digest` may flip `open→running` and call `done finished/failed` with counts; `result`/`lesson` stay human; two states kept.
- **F4 (witness campaign):** yes to both — (a) one read-only `sacct --parsable2` dump of the DR1 campaign is authorised; (b) the 50-task sky-orientation re-render pilot under a read-only collector, from a private venv checkout, is authorised. No new modelling runs; never the shared venv; `ral` only.
- **F5 (escalation):** propose-only (timeout → p95+25 %, OOM → peak×1.5); the human approves every resubmit.
- **F6 (RAL site constants):** ranges until the human confirms CPU model, building/PUE and A100 form factor; CI central = South England regional, national and DESNZ as bounds.
- **F12 (governance hook):** **Claude and Codex** harnesses (not Claude only); prose for other agents; AUTONOMY.md says so.
- Shared: F1 (phase 0 owned by results-library), F9 (paper claim tiers per review §E.1/E.3), F11 (two concurrent PyAutoFit worktrees with §D.4 ownership).

## Ledger

- 2026-10-28 — STARTED, concurrent with results-library (human decision). Final scoping review adopted; human ruled F1–F12 (above). Phases amended (above): phase 0 issued as results-library phase 0; failure record + `states.py` + Nerves `site.yaml` in phase 1; partition lint + retrospective sacct mode in phase 2; evidence/plan ahead of organism integration. Next: phase 1 via `/start_dev`, merging after results-library PR 0a.
- 2026-10-28 — phase 0 #A issued as results-library phase 0: PyAutoFit#1734. Phase 1 ISSUED: PyAutoFit#1735 + PyAutoNerves#206 (task `hpc-campaign-p1-status-record`, branch `feature/hpc-campaign-p1-status-record`); merges after PR 0a; autofit_workspace docs leg deferred (repo claimed by `compact-colab-setup`).
- 2026-10-29 — `compact-colab-setup` completed and released its autofit_workspace claim; see `complete/2026/10/compact-colab-setup.md`. The docs leg is no longer blocked by that claim.
- 2026-10-29 — phase 1 SHIPPED to PR: PyAutoFit#1738 (status record, failure record, `states.py`), PyAutoNerves#207 (`site.yaml`, `Config.push_site`, `site/ral.yaml`), autofit_workspace#179 (cookbook `search.py` Status Record / Batch Job Time Limits / Turning It Off + `general.yaml` keys). Full suites green (Fit 3,955, Nerves 280), smoke autofit+autolens_test 47/47 on the combined worktree. Merge order: #1736 (results-library PR 0a) → #1738; #207 independent; #179 after release. Test-merge of #1738 onto #1736: no conflicts. Phase 0 PRs: #1736 (0a) open, #1737 (0b) open and held (see results-library ledger). Unverified: the `exec python` Slurm advice in the docs has not been tried on a real job.
- 2026-10-29 — PHASE 1 COMPLETE (human /prm): PyAutoFit#1738 (after #1736; merge result 3,976 passed), PyAutoNerves#207, autofit_workspace#179 MERGED; Fit + Nerves pending-release. Issues PyAutoFit#1735 + PyAutoNerves#206 closed; record `complete/2026/10/hpc-campaign-p1-status-record.md`. Phase 0 (shared) also COMPLETE (results-library record). NEXT: phase 2 (campaign core + adapters + collector + partition lint + retrospective sacct mode) via `/start_dev`.
- 2026-10-30 — PHASE 2 PRs OPEN (human /prm in order): PyAutoFit#1741 (2a campaign.yaml + Fake/Local/Slurm + partition lint) → #1742 (2b collector + digest + proposals + retro, stacked). Issue #1740. Witness W2 (F4a dump, read-only): 61,078 Slurm tasks, 709.8k CPU-h (29 % failed/repeated), sed 12 % timeouts, memory requests 2–4× peak, 568 CPU tasks on `gpu` (09-30 incident) — `Workspace/Science/scratch/hpc_campaign_p2_w2/`. Decisions flagged: mixed ral,gpu always refused; cancelled/unrecorded stay campaign strings. NEXT after merge: phase 3 (evidence + plan, W3) ∥ phase 4 (carbon + report, W4 from the W2 digest).

## Original request (verbatim)

# Deep research: an epic for running large HPC modelling campaigns efficiently, token-cheaply and low-carbon

You are Fable, acting as architect for the PyAutoLabs ecosystem. Research and design an **epic**
that builds everything needed to run large HPC modelling campaigns efficiently into the source
code (PyAutoFit first, so it is generic across all modelling problems) and into
`autolens_assistant`, the AI science-assistant workspace. Your output is a research report plus
a phased epic plan. Do not edit code; the plan will go through the normal `start_dev` workflow.

## The motivating campaign (real, 25–27 Sep 2026)

The Euclid DR1 strong-lens campaign runs a three-stage chain per lens on the RAL Slurm cluster:
- `vis_lp`: parametric fit.
- `vis_pix`: pixelized source, Numba sparse CPU route.
- SED: multi-band Sérsic, seeded from `vis_lp`.

Scale: a priority batch of 250, then 5,000 lenses as 5 arrays × 1,000 per stage, with ~15,000
possible. The science project is a separate repo (`euclid_dr1`) with an `hpc/sync` CLI
(push / submit / jobs / tail / pull), run manifests (one tile per array index), submit scripts
in `hpc/batch_cpu/`, and outputs in `output/` and `output_sed/`. Run state is recorded in several
places: the PyAutoCortex ledger (`organs/PyAutoCortex/projects/euclid_dr1.md`), dated wiki
journals, the agent's memory files, and Slurm itself.

**Cluster facts:**
- `ral` partition: 28 nodes of 236–252 cores and ~920–976 GB RAM each, 6,976 CPUs, Slurm
  `sched/backfill` with `CR_CORE_MEMORY`.
- `gpu` partition: 2 nodes × 4 A100.
- Shared `/mnt/ral` filesystem at 153/171 TB (90%).

**What happened: the workflow was submit → user asks "how's it going?" → agent investigates →
tune → resubmit.**

- **Over-reserved memory, twice.** Every task was submitted at 8 CPUs / 64 GB / fixed walltime.
  Measured afterwards:
  - `vis_lp`: peak 4 GB, 53% of 8 cores.
  - `vis_pix`: peak 11 GB, 83% of 8 cores, median 9.1 h (3.5–12.5 h).
  - SED: peak 3.7 GB, 72% of 8 cores, median 11 min with a long tail.

  Each node's memory was 100% reserved while only 112 of 252 cores were used. The partition
  showed ~3,400 idle CPUs, with us as effectively the only user. This was only discovered
  because the user said "I'm surprised so few are running". The fix was an `scontrol update` of
  pending tasks (16 GB `vis_pix`, 8 GB SED, then 12 GB / 4 CPU for `vis_lp`). It only takes
  effect as running tasks drain, because a requeue keeps the old memory request.
- **Array caps left the cluster idle.** The first cap (120 per array × 5) left ~25% of the
  cluster idle. The minimum possible runtime is roughly total CPU-hours ÷ free CPUs: ~60
  CPU-h per `vis_pix` lens × ~4,600 lenses ≈ 280k CPU-h, about 2 days. The cap stretched that to
  2.7 days.
- **Walltime too short.** SED's 6 h walltime timed out 44 of 250 (18%) in the long tail. That is
  wasted compute that has to be rerun. Users can raise walltime here (partition max 27 days),
  but nobody knew to.
- **Failures only surfaced downstream.**
  - A truncated `vis_lp` result zip (16 of 31 files, no samples) failed at the SED stage.
  - One tile whose `vis_lp` timed out failed at SED with "no seed".
  - Stage chains are enforced by file guards in bash scripts and `afterany` dependencies, so
    a downstream stage runs even after an upstream failure.
- **Status was expensive and fragile.**
  - Every status check needed a fresh set of `squeue`/`sacct`/`scontrol`/`sinfo` calls.
  - `du` on a 5,250-tile output tree timed out.
  - Log locations depend on the directory the job was submitted from.
  - Manifest indexing is 0-based (task N = line N+1).
  - Slurm priority vs nice was confused (`%Q` vs `%y`).
  - The newcastle jump host rejected the SSH key mid-session.
  - Journals were a day behind.
- **Agent safety model.** The agent's permission classifier blocked `scontrol update` and
  requeue on running jobs until the user explicitly approved. That was correct, but it suggests
  a narrow, auditable action surface for scheduler changes.
- **Disk.** Nobody knew the project's footprint (~3–30 MB of `output/` plus ~17 MB of
  `output_sed/` per tile, so ~0.25 TB for 5,000). The risk is actually the shared filesystem at
  90%. `hpc_mode` (PyAutoFit `remove_files`) zips completed searches and deletes the unzipped
  tree. That is the main disk lever, but it breaks anything that reads loose files.

## The three asks (critique each, don't just accept it)

1. **A single point of reference for run state, updated by the runs themselves.** Faster updates,
   and far fewer tokens than scraping output directories and the scheduler.
   - Evaluate the design space:
     - a per-fit status record written by PyAutoFit: state, stage, search progress, best
       logL, ETA, measured RSS/CPU, failure class;
     - aggregation without shared-file contention on NFS for 5,000 writers;
     - joining with scheduler accounting (Slurm first, abstracted for others);
     - a compact digest the agent reads in one call;
     - how it feeds the Cortex ledger instead of duplicating it.
   - Decide what belongs in PyAutoFit, what in a scheduler adapter, and what in the project
     `hpc/sync` template or a PyAuto organ.
   - Survey prior art: Snakemake/Nextflow reports, Parsl, FireWorks/Balsam, MLflow,
     Weights & Biases, Slurm `seff`/`jobstats`, XALT, and similar.
2. **Resource-aware planning before submission.** Replace submit-then-tune with a planned
   conversation:
   - discover cluster capacity and current load;
   - run a short calibration pilot that measures per-task CPU efficiency, peak memory and a
     walltime distribution per stage;
   - right-size CPUs, memory, walltime (tail-aware), array caps and priorities to fill the free
     capacity without starving other users;
   - forecast ETA and disk;
   - agree the plan with the user, then submit;
   - monitor for drift and propose (not silently apply) changes.

   Include how to handle multi-stage chains, validating each stage's output before the next,
   and resubmitting failed subsets without redoing work.
3. **Energy and carbon.** Give users estimates of energy and CO₂e for a campaign and for each
   alternative:
   - CPU vs A100 route;
   - 4 vs 8 cores;
   - lighter vs full sampler settings;
   - reruns caused by timeouts.

   Nudge them toward low-carbon choices. Research:
   - the methodology: the Green Algorithms model (cores × power per core × usage + memory
     power, × PUE × grid intensity) and alternatives;
   - where per-node power and PUE numbers come from for a site like RAL;
   - whether to use UK grid carbon intensity (National Grid ESO API) for carbon-aware
     scheduling;
   - how to present uncertainty honestly;
   - how to report a campaign's footprint in a paper.

## Then go further

Propose other features that would make large-scale analysis better. Candidates to evaluate
(add your own):
- a declarative **campaign file** as the single source of truth: tiles, stages, dependencies,
  resources, and a success check for each stage;
- automatic failure triage (timeout vs bad input vs missing seed vs out-of-memory) with a
  proposed fix for each class;
- integrity checks on stage outputs, e.g. zip completeness;
- guarantees that interrupted fits resume;
- disk lifecycle and forecasting;
- fairness to other cluster users;
- an allowlisted, logged scheduler-action tool for agents;
- notifications;
- an auto-generated end-of-campaign report covering compute, carbon, failures and results;
- making the pattern work beyond Slurm/RAL and beyond lensing (galaxy, CTI, generic PyAutoFit
  users).

## Constraints

- Generic first: fit-level machinery lives in PyAutoFit (`fit/PyAutoFit`); lensing-specific
  guidance lives in `lens/autolens_assistant`.
- Respect the organism's architecture:
  - PyAutoCortex keeps science run state;
  - PyAutoNerves owns config;
  - the Brain's Cortex agent reads the ledgers;
  - PyAutoHeart holds release health (don't overlap it).
- Library changes ship first. No hard dependency on any one scheduler or site.

## Deliverables

1. Research findings with citations, including prior art and carbon methodology.
2. A critique of each ask: keep, reshape or drop, and why.
3. The recommended architecture: components, data formats, where each piece lives, how the
   agent consumes it, and the expected token and latency savings for a status check.
4. A phased epic plan: phases, one issue per repo per phase, dependencies, what "done" means,
   and a first pilot on the Euclid DR1 campaign.
5. Risks and open questions for the human.
