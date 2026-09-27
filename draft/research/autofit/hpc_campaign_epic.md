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
Status: draft
Filed: 2026-09-27

Research report and phased epic plan: `hpc_campaign_epic_report.md` alongside this file (written 2026-09-27 by the Fable architect session; no code edited).

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
