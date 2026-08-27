# Phase 4: census and reconcile every excluded script across both test workspaces

Type: bug
Target: ci
Repos:
- @autolens_workspace_test
- @autogalaxy_workspace_test
- @PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Epic: jax-compile-stall
Phase: 4
Campaign: bug/ci/jax_vmap_jit_compile_stall.md (Phase 4 — the audit; runs independently of phase 3)
Filed: 2026-08-26

## Why this is a phase and not a chore

**Nobody currently knows what the true excluded set is.** Four separate lists —
`smoke_tests.txt` and `config/build/no_run.yaml`, in each of
`autolens_workspace_test` and `autogalaxy_workspace_test` — each carry their own
comment-form markers, and the campaign has now been bitten three times by
trusting them:

- **A SLOW marker is not evidence of slowness.** Phase 2 measured the first one
  and it was wrong by ~50x. Every 2026-07-14 marker read "flakes at the 1800s
  cap" and recorded no timing at all.
- **The 2026-08-24 retime removed eight markers on N=5 per leg.** For a bimodal
  failure that measures the fast mode and says nothing about the tail. One of the
  eight, `multi_dataset/jax_likelihood/shared_preloads.py`, was falsified by the
  very next weekly run. Every other entry that sweep readmitted carries the same
  unquantified risk.
- **The lists disagree with each other.** `shared_preloads.py` is excluded from
  the PR gate as too heavy and admitted to the mega-run — so a script disabled
  since July was still able to burn a 300s cap in CI.
- **And they hold evidence the campaign ledger does not.** The deterministic
  16/16 reproducer that unblocks phase 3 was written into a `no_run.yaml` comment
  on 2026-08-24 and never reached the ledger. That is the failure mode this phase
  exists to end.

## Deliverable

One table, checked into the campaign, with a row per excluded script:

| repo | list | script | marker + date | stated reason | **measured** status | verdict |

`verdict` is one of: **restore** (evidence does not support exclusion),
**re-mark** (excluded for a real but mis-stated reason — fix the marker),
**keep** (correctly excluded; cite the evidence), **unknown** (needs a
measurement this phase specifies).

Rules for filling it in:

- A marker with no timing in it is `unknown` until measured, not `keep`.
- N=5 is not enough to clear a bimodal entry. State the N behind every
  `restore`, and prefer the higher-cap retime harness
  (`retime.yml` → `retime.py`, shipped in phase 2) over re-reading old runs.
- A script that has **never completed** is `keep` + NEEDS_FIX, not SLOW —
  determinism and slowness are different findings and the lists conflate them.
- Where a script appears in more than one list, say explicitly whether the two
  should agree. `smoke_tests.txt` (fast PR gate) and `no_run.yaml` (mega-run and
  weekly) have legitimately different policies; the bug is undeclared drift, not
  difference itself.

## Then close the loop

- Reconcile the two lists per repo so any remaining disagreement is a written
  decision rather than an artefact of whichever file was edited last.
- Where a marker cites an issue, check the issue is still open and still says
  what the marker claims.
- **Decide where this evidence lives.** The root problem is that primary findings
  land in config comments and never reach the campaign. Either the markers become
  pointers to the ledger, or the ledger gets a generated section fed from the
  markers — but the current arrangement, where both hold partial truth and
  neither knows it, must not survive this phase.

## Scope boundary

This phase **measures and records**; it does not fix the hang. Restoring a script
that phase 3's root cause explains is phase 3's close-out, not this one's. What
this phase can do on its own is stop the organism from being wrong about which of
its tests are running.

## Acceptance

- Every excluded script in all four lists appears in the table with a verdict.
- No `restore` rests on fewer measurements than the entry's own failure
  probability warrants, and each states its N.
- Every disagreement between a repo's two lists is either resolved or recorded as
  a deliberate policy difference.
- A stated decision on where campaign evidence lives, so the 2026-08-24 loss
  cannot repeat.
