# HPC campaign phase 5d: the Euclid pipeline runs its three stages from one campaign.yaml

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- hpc
- euclid
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: (1) pipeline CI (tests.yml + smoke_tests.yml) green; (2) `python -m autofit.campaign` on the new `hpc/campaign/dr1.yaml` with the FakeScheduler (or LocalScheduler on 3 fixture tiles) prints a plan whose vis_lp → vis_pix → SED chain uses per-index `aftercorr`, whose every stage passes the partition lint (`ral` only, no `gpu` in any CPU stage), and whose digest is ≤2 KB; (3) a table in the PR maps every retired `hpc/batch_cpu/submit_*` script to the campaign stage or kept tool script that replaces it, with nothing dropped silently
Review-minutes: 20
Unattended: ready
Verified: 2026-11-16 65b32e85 (euclid_strong_lens_modeling_pipeline)
Lane: any
Epic: hpc-campaign
Phase: 5d
Filed: 2026-11-16
Gate: MET — human ruling 2026-11-16: "Dr1 is now public" (the epic ledger's "pipeline adoption only after DR1 v1.0 ships"). Human 2026-11-16: "Supervised, in this shift" — runs unattended to PR-open with the decision-taken label; merge is human /prm.
Merge-order: coordinate with results-library phase 5d (pipeline scripts shrink, same repo, same DR1 v1.0 gate) — one PR at a time on euclid_strong_lens_modeling_pipeline, whichever the human orders first; rebase the other.

## What

Report item C9 / #J (`draft/research/autofit/hpc_campaign_epic_report.md` §5 "Phase 3 — Organism integration";
the ledger renumbered it phase 5d). Phases 0–4 and 5a–5c are merged and released: PyAutoFit `autofit.campaign`
(2026.11.1.1+), Nerves `site.yaml`, the autolens_assistant hpc template v2 (`hpc/batch_cpu/stage`,
`hpc/batch_cpu/template`, `hpc/template.py`, `hpc/campaign.yaml.example`, `hpc/sync` verbs
`status/plan/pilot/act/resubmit/report`, `skills/hpc_campaign.md`), Cortex `sync-runs` and the Brain scheduler
action guard. This phase makes the public Euclid pipeline the first real adopter.

In `euclid_strong_lens_modeling_pipeline` only:

1. Bring the pipeline's `hpc/sync` and batch template up to the assistant template v2 (the pipeline's drift was
   folded into the template in 5a step 0, so this is a copy back plus pipeline-specific config), keeping
   `sync.conf.example` and the pipeline's `restrict_pull_dirs` behaviour.
2. Add `hpc/campaign/dr1.yaml` for the three DR1 stages (vis_lp, vis_pix Numba sparse CPU route, SED), with
   per-stage resources from the W2/W3 evidence (vis_lp 4 CPU / 8–12 GB, vis_pix 8 CPU / 16–20 GB, SED 2–8 CPU /
   8–16 GB; walltimes from the W3 plan, tail-aware), per-index `aftercorr` chaining, a success check per stage
   (zip completeness, seed present for SED), `--signal=B:USR1@600`, `set -euo pipefail`, `PYTHONUNBUFFERED=1`,
   `numba.cache: false` on NFS, and partition `ral` only.
3. Retire the 35 hand-written per-batch `hpc/batch_cpu/submit_initial_lens_model_*` and `submit_sersic_*`
   scripts (count on main 2026-11-16), the chain drivers `submit_vis_pix_rest_chain.sh` and
   `submit_vis_pix_v2grade_overnight.sh`, and their hand manifests in favour of the campaign stages. Keep
   one-off tool scripts (catalogue, release, north-up, WCS, magnitudes) unless they map cleanly onto a stage;
   list each in the PR table.
4. `hpc/README.md` rewritten for the campaign flow (plan → pilot → human go → `hpc/sync act submit` → `status`
   → `report`) in the `PyAutoBrain/skills/WRITING_STYLE.md` register.
5. Tests: offline only (FakeScheduler / LocalScheduler, fake ssh as in the assistant's tests).

Out of scope: any RAL submission, the `euclid_dr1` science clone (the human chooses later whether to trial
there first — report risk 7), results-library's pipeline shrink, the sky-orientation phases 3–5 (euclid#115),
phase 6 generalisation.

## Done

PR open against `euclid_strong_lens_modeling_pipeline` with the witness above in its body; ledger line in
`draft/research/autofit/hpc_campaign_epic.md`. Merge is human `/prm`. The 10-tile RAL dry run through
`hpc/sync act submit` (report §5 #J "Done") is a separate, human-triggered step after merge: `ral` only, private
venv, never the shared install, never `gpu` for CPU stages (hard constraint 2026-09-30).
