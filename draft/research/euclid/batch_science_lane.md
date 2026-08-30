# Batch phase 8 — the laptop lane

Type: research
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- autolens_assistant
- PyAutoMind
Themes:
- hpc-gpu
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Epic: two-slot-batching
Phase: 8
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

**Decided 2026-08-30: science projects stay on the laptop, and the laptop lane is
accepted rather than engineered away.** In the human's words: mobile sessions
cannot easily reach RAL, and if the HPC is down they are stuck. A canonical home
on RAL trades a dependency they control for one they do not.

That closes several options this epic was holding open, and closing them is the
point of this prompt. What remains is to make the lane **first-class** — a
declared, detected property of the work — instead of a thing the batch layer
trips over.

## What is now out of scope, and why

- **RAL as canonical home for the science project.** Refused above. The datasets
  and `output/` stay under `/mnt/c/…/Science/`.
- **A git-courier cron on the RAL login node.** Its value collapses once the
  laptop is canonical: the laptop has to be on to hold and push the data anyway,
  so a courier saves almost nothing. It was the right answer to a question no
  longer being asked.
- **Globus Compute endpoint / self-hosted GitHub runner on the login node.**
  Same reasoning, plus both are persistent login-node processes needing an
  operator conversation. Not worth it for a lane the human is happy to drive.
- Recorded so nobody re-derives them: SSH from a Claude container is a
  non-starter in every variant (HTTPS-only proxied egress, no keys); Open
  OnDemand is an admin-installed inbound portal; Cirun cannot reach someone
  else's SLURM. And phases 4, 6a and 6b of `euclid-dr1-prep` say in their own
  prompts that they are human-driven and supervised with a judged verdict as the
  deliverable — **no transport was ever going to make those unattended.**

## What survives, and matters more now

### Leg A — the prepare / execute recut

Now the *main* lever, because it is the only thing that moves science work into
the lane that can run unattended. Re-cut the remaining euclid phases along the
seam: submission scripts, analysis code, plotting, catalogue tooling and library
audits (phase 6c is already flagged as "the only phase that can plausibly land as
a fast standalone fix") are ordinary cloud work. Only the run itself is bound.

Deliverable: every remaining euclid phase carries a `Lane:`, and the `any`-lane
halves enter the normal queue immediately.

### Leg B — manifest-first results

Still worth doing, for a changed reason. It is no longer about reaching RAL; it
is about letting a **cloud** session reason about outcomes while the laptop is
off. The laptop pushes small result JSONs (already the `results/searches/**`
convention), catalogue CSVs and downsized PNGs whenever it is on; a cloud session
then reads those and can plan, file follow-ups, and prepare the next submission
without ever opening a FITS file. Phase 4's own deliverables are a few MB of CSV
and PNG. `draft/feature/autofit_assistant/remote_mcp_deployment_tiers.md` is the
in-repo precedent.

## The lane, made first-class

Express it in the vocabulary `PyAutoBrain/skills/WORKFLOW.md` already defines
(`local-dev` / `web-github` / `ci-only` / `analysis-only`) rather than inventing
a parallel one:

```
Lane: any | local-dev
```

`local-dev` means the work needs the local dataset and output trees, an SSH
endpoint, or the human physically at the machine. Default `any`.

Three rules, and the first is the one the human asked for:

1. **A session detects its own lane and refuses to plan the other one.** The
   probe already exists in spirit — `bin/_pyauto_root.sh` resolves the checkout
   layout and `bin/_gh.sh` is the organism's existing honest answer to "can I
   even ask?". `batch plan` in a cloud session reports, rather than silently
   dropping: *"4 local-dev tasks are ready — run this from the laptop."*
2. **A `local-dev` batch is dispatched from the laptop, by the human, and only
   there.** It is not a third daily hour: it is drained opportunistically in a
   laptop slot, which is when they are doing science anyway. Because they are
   present, it can be more interactive than a cloud shift — the honest ceiling
   for the science phases was always *supervised*, not unattended.
3. **The queue holds both lanes in one ordered file.** One wishlist, not two
   backlogs to keep in sync. The planner filters; the human does not.

`WORKFLOW.md`'s standing advice applies: *detect* environment, do not branch the
whole workflow on it. The lane changes who dispatches and where, not how the work
is done.

## Done when

- Every remaining euclid phase carries a `Lane:`, and the `any` halves are queued.
- `batch plan` names its detected lane and reports the other lane's ready count
  rather than hiding it.
- The dropped options above are recorded here with their reasons, so the next
  person to have the idea reads why it was closed instead of re-researching it.
