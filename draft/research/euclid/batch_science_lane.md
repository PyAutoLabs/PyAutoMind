# Batch phase 8 — the science lane: get the laptop out of the loop

Type: research
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- autolens_assistant
- PyAutoMind
Themes:
- hpc-gpu
- mind-workflow
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Epic: two-slot-batching
Phase: 8
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

Everything else in this epic assumes a task can run in a container. Science runs
cannot. This phase establishes how small the exception really has to be.

## Start from the honest ceiling

`euclid-dr1-prep` phases 4, 6a and 6b say in their own prompts that they are
"human-driven and supervised", run over "wall-clock timescales of days", and
"must never be handed to an autonomous ship gate"; their deliverable is a judged
verdict, not a merged PR. **No transport changes that.** The ceiling for these is
*phone-supervised* — the agent submits, polls, and summarises; the human judges —
and the goal of this phase is to reach that ceiling, not to pretend at
unattended.

What a bridge *can* remove is the laptop.

## Leg A — the prepare / execute recut (do this first, no infrastructure)

Re-cut the science phases along the seam between preparation and execution.
Submission scripts, analysis code, plotting, catalogue tooling and library audits
(phase 6c is already flagged as "the only phase that can plausibly land as a fast
standalone fix") are ordinary cloud work and belong in ordinary batches. Only the
run itself is bound.

Deliverable: a re-cut of the remaining euclid phases into `Lane: cloud` and
`Lane: laptop` halves, with the cloud halves entering the normal queue
immediately. Expect this alone to move most of the remaining epic into the batch
workflow.

## Leg B — manifest-first results (do this second, needs nobody's permission)

Make the agent able to reason about a run's outcome without touching the data.
It reads small result JSONs (already the `results/searches/**` convention),
catalogue CSVs and downsized PNGs, committed or pushed; it never opens a FITS
file. Phase 4's own deliverables are CSVs and PNGs of a few MB, and the catalogue
tile format is thirteen small files, so this covers most of "inspect results,
decide the next submission".

In-repo precedent to build on rather than duplicate:
`draft/feature/autofit_assistant/remote_mcp_deployment_tiers.md`, the read-only
results surface, design-complete and build-gated.

## Leg C — assess the bridge (research, no build without a decision)

Ranked, with the verdicts already established at filing:

1. **Git-courier cron on the RAL login node** — a periodic job, not a daemon:
   pull a requests branch, run the `hpc/sync` verb it names, push back logs and
   manifests. Outbound HTTPS git only, no inbound port. A cron is far more
   defensible against typical login-node policy than a persistent process, and
   minutes of latency are irrelevant to jobs measured in days. It matches the
   Mind's own file-as-work-unit idiom. Bespoke, but small.
2. **Globus Compute single-user endpoint** — the best off-the-shelf fit:
   pipx-installable unprivileged, outbound-only, SLURM provider can `sbatch`,
   drivable over HTTPS from a phone. Caveat: it *is* a persistent login-node
   daemon, so ask the operators.
3. **Self-hosted GitHub Actions runner** — outbound 443 long-poll, no inbound,
   ephemeral and JIT modes exist, and a self-hosted job may run for five days.
   **Must be scoped to private repositories**: GitHub's own guidance is that
   forks of a public repository can run code on a self-hosted runner, and can
   even edit `runs-on` to capture it. Several PyAuto repos are public. Needs
   cooperation.
4. **Echo/Ceph S3 at RAL via an IRIS allocation** — the service exists and
   `euclid-saas` is IRIS infrastructure, so an allocation is not far-fetched;
   the container proxy would also need to permit the endpoint.
5. **Non-starters, established:** Open OnDemand (admin-installed inbound portal),
   Cirun (provisions VMs on your own cloud account, cannot reach someone else's
   SLURM), and SSH from a Claude container in any form (HTTPS-only proxied
   egress, no keys).

Useful context for the ask: `euclid-saas.roe.ac.uk` is IRIS federated OpenStack
(`astrodb/euclid-saas` — "Euclid SaaS branch of P3-appliances"): OpenHPC plus
SLURM, federated Ceph, CVMFS with per-site Squid proxies, OpenVPN mesh across
Edinburgh, Cambridge and RAL — which is why a ROE login host carries RAL storage
at `/mnt/ral`. The operators are Euclid UK colleagues rather than a central-IT
queue, so the ask about (1) and (2) together is cheap. No public documentation of
any access method beyond SSH exists, and no public login-node policy.

## Leg D — move the canonical home (decision, not code)

The science project's source of truth is currently
`/mnt/c/Users/Jammy/Science/euclid` on a Windows laptop. If it moves to RAL, with
only small manifests in git, then with legs B and C the laptop becomes a
convenience rather than a dependency. That is a real decision with real risk —
backup, provenance, the fact that `/mnt/ral` is NFS-slow — and belongs to the
human, not this prompt. State the trade honestly and let them decide.

## Also worth fixing while here

`hpc/sync` is not a tool. It is roughly 560 lines of bash copied verbatim into six
or more repos with no shared source, configured per project by `sync.conf`, and
untested anywhere because it needs a real SSH endpoint. Any courier built on it
inherits that. File the consolidation separately rather than folding it in — but
file it.

## Done when

- The remaining euclid phases carry `Lane:` headers and the cloud halves are in
  the queue.
- A written recommendation on legs C and D, with the operator ask drafted if the
  recommendation is to make it.
- Explicitly: no bridge is built in this phase without a human decision.
