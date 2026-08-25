# A retime refuted a stall marker; one day later the script stalled

PyAutoMind#329 → `5eeee59` (closing PyAutoMind#328), merged 2026-08-25.
Evidence-recording task against the `jax-compile-stall` ledger. Filed as a
one-line follow-up ("add `shared_preloads.py` to the family list") from
`complete/2026/08/weekly-smoke-timings-naming.md`; the investigation found
something materially larger.

## What shipped

- **`draft/bug/ci/jax_vmap_jit_compile_stall.md`** gained a
  `## New occurrence — 2026-08-25` section, mirroring the 2026-08-24 precedent:
  run/job ids, a ten-row sibling timing table, the retime refutation, the
  exclusion-list disagreement, the widened affected-set shape, and the channel
  finding.
- **`epics.md`** — the `jax-compile-stall` entry carries a
  `NEW EVIDENCE 2026-08-25` note so the epic's state reflects it.
- Nothing parked, disabled, or re-marked. `autolens_workspace_test` read for
  evidence only.

## The finding

`multi_dataset/jax_likelihood/shared_preloads.py` hit `TIMEOUT (300s)` in
PyAutoHeart `Workspace Smoke` run **32902243623** (job **97978549465**,
2026-08-25) while all nine siblings passed in 8.6–49.3s — a >6x outlier with the
bimodal signature the ledger uses to separate a stall from slowness.

**The 2026-08-24 retime had removed this entry's SLOW marker and returned it to
coverage the day before.** Verified against `autolens_workspace_test` at
`7fc497d`: absent from `config/build/no_run.yaml` (in mega-run/weekly coverage),
still commented out at `smoke_tests.txt` line 15 (out of the PR gate).

## Key traps / findings

- **N=5 cannot refute a bimodal failure.** The retime (5 repeats per leg, 300s
  cap; runs 32741371308 + 32741386752) removed eight PyAutoHeart#74 entries on
  "completed 5/5 on both legs, slowest 54.5s — marker refuted". ~10 executions
  measure the fast mode and say nothing about the tail. The retime was right
  that the script is not *slow*; it was not powered to see that it *stalls*.
  **The other seven entries that sweep readmitted carry identical uncertainty**
  and are in the weekly channel now — the standing follow-up below.
- **The two exclusion lists disagree, and different gates read different ones.**
  `smoke_tests.txt` gates the PR run; `no_run.yaml` gates mega-run/weekly. A
  script disabled since 2026-07-22 was therefore still able to burn a 300s cap
  in CI. Resolve deliberately rather than by whichever file is edited next.
- **First occurrence via the weekly `workspace-validation` channel.** Every
  prior one came from a workspace repo's own `Smoke Tests` gate or from
  `release-integrate`. A different, PyAutoHeart-owned, `script_matrix.py`-driven
  harness reproducing the same signature is cross-harness corroboration that the
  stall is not one repo's runner configuration.
- **The common factor is wider than MGE.** `shared_preloads.py` is not an MGE
  variant, so the ledger's "composite MGE vmap graph" shape no longer covers the
  affected set. What the members share is heavy `multi_dataset` vmap
  composition.
- **A one-line follow-up note was not the whole finding.** The note said "add it
  to the family list". Checking the workspace's actual exclusion state — rather
  than trusting the note — is what surfaced the refutation. Cheap to do, and it
  changed the task's meaning.

## Follow-ups

- **Re-check the seven other entries the 2026-08-24 sweep readmitted.** One of
  eight hung within a day; the rest were cleared by the same under-powered
  protocol and sit in weekly coverage. Now cheaper to settle than before: the
  weekly `smoke-timings-*` dataset (shipped same day, PyAutoHeart#182) makes
  per-script weekly timings globbable, so a few weeks of data answers it without
  a bespoke sweep.
- **Reconcile `smoke_tests.txt` vs `no_run.yaml`** for the entries where they
  disagree — a decision, not code.
- `pyauto-brain bug` returns `owner: unresolved` / `fix locus: unresolved` for a
  prompt whose only repo is `@PyAutoMind`, because Mind is absent from its
  library-repo owner map. Cosmetic; classification was otherwise sound.

## Original prompt

# The 2026-08-24 retime returned `shared_preloads.py` to coverage; it stalled the next day

Type: bug
Target: ci
Repos:
- @PyAutoMind
Epic: jax-compile-stall
Difficulty: small
Autonomy: safe
Priority: medium
Status: issued
Filed: 2026-08-25
Issued: 2026-08-25

Evidence-recording task against the jax-stall ledger
[`jax_vmap_jit_compile_stall.md`](jax_vmap_jit_compile_stall.md). Surfaced
2026-08-25 by the `weekly-smoke-timings-naming` verification sweep
(PyAutoHeart#182), which dispatched a full `workspace-smoke.yml` run and turned
up a stall the ledger does not know about.

## What was observed

PyAutoHeart `Workspace Smoke` run **32902243623** (2026-08-25, `workflow_dispatch`),
job `smoke / run_scripts (3.12, autolens_test, multi_dataset)` (97978549465).
16 of 17 scripts passed:

```
scripts/multi_dataset/jax_likelihood/shared_preloads.py ...   TIMEOUT (300s)
```

Its siblings in the same job, same commit, same runner:

| Script | Result |
|---|---|
| `jax_likelihood/mge.py` | PASS 11.7s |
| `jax_likelihood/rectangular_mge.py` | PASS 20.7s |
| `jax_likelihood/mge_group.py` | PASS 49.3s |
| `jax_likelihood/delaunay_mge.py` | PASS 20.2s |
| `jax_likelihood/rectangular.py` | PASS 15.8s |
| `jax_likelihood/shared_preloads.py` | **TIMEOUT (300s)** |

A >6x outlier against the slowest sibling, with every other member of the family
completing comfortably — the bimodal signature the ledger already uses to
separate a stall from slowness.

## Why this is not just another occurrence

**The 2026-08-24 retime refuted this entry's SLOW marker and put it back in
coverage. It hung on the next weekly run.**

`shared_preloads.py` sat in the PyAutoHeart#74 "flakes at the 1800s cap" SLOW
family. On 2026-08-24 that family was retimed (5 repeats per Python leg, 300s
cap; runs 32741371308 + 32741386752) and eight entries "completed 5/5 on both
legs (slowest 54.5s) and were removed — marker refuted, scripts back in mega-run
coverage" (`autolens_workspace_test/config/build/no_run.yaml`, and
`complete/2026/08/smoke-surface-retime-sweep.md`).

Verified 2026-08-25 against `autolens_workspace_test` at `7fc497d`:

- `config/build/no_run.yaml` — **no `shared_preloads` entry**. It is in mega-run
  and weekly coverage.
- `smoke_tests.txt` line 15 — still **commented out**, "disabled 2026-07-22:
  exceeds the 300s smoke cap (measured 300s+ in CI, autolens_workspace_test#196)
  … it is the heaviest entry here and does not belong in the fast PR gate."

So the two exclusion lists now disagree about this script, and the list that
readmitted it did so on ~10 executions at ≤54.5s. **A 10-execution sample at
~50s cannot exclude a low-probability hang** — which is exactly the claim the
retime's "marker refuted" conclusion rests on. The retime was right that the
script is not *slow*; it was not powered to see that it *stalls*.

That is the ledger's own phase-2 question (§ Task step 1: "a slow script has a
tight timing distribution, a stalling one is bimodal") landing on the other side
from where the retime put it.

## Also new: the channel

Every occurrence in the ledger comes from a workspace repo's own `Smoke Tests`
gate or from `release-integrate`. This is its **first from the weekly
`workspace-validation.yml` sweep** — a different harness (PyAutoHeart-owned,
`script_matrix.py`-driven, honouring `no_run.yaml` and *not* `smoke_tests.txt`)
reproducing the same signature. That is corroboration the stall is not an
artifact of one repo's runner configuration.

It also means the weekly channel runs scripts the PR gate deliberately excludes,
which is how a script disabled in `smoke_tests.txt` since July was still able to
burn a 300s cap in CI.

## Task

Record this in the ledger — do not park the script.

1. Append a `## New occurrence — 2026-08-25, multi_dataset/jax_likelihood/shared_preloads.py`
   section to [`jax_vmap_jit_compile_stall.md`](jax_vmap_jit_compile_stall.md),
   in the shape of the existing § "New occurrence — 2026-08-24" section: run and
   job ids, the sibling timing table, and the affected-set consequence.
2. State the retime refutation explicitly, so phase 2's written answer is not
   left contradicting the evidence: this entry was readmitted to coverage on a
   sample too small to exclude a stall, and the readmission is now falsified.
3. Extend the ledger's affected-set shape to name `shared_preloads.py`, and note
   the `smoke_tests.txt` / `no_run.yaml` disagreement about it.
4. Add the "first occurrence on the weekly `workspace-validation` channel" point,
   with the cross-harness corroboration it gives.

**Deliberately out of scope:** re-adding `shared_preloads.py` to `no_run.yaml`.
The ledger's own § "This is why quarantining is the wrong end state" argues
against whack-a-mole parking that strips coverage of the heaviest JAX paths, and
the 2026-08-24 precedent for `multi_dataset/jax_likelihood/mge.py` was to record
and deliberately **not** park. Any re-marking is phase 3's call with a root cause
in hand, not this task's.

## Acceptance

- The ledger names `shared_preloads.py` in its affected set, with the run/job
  evidence and the sibling timings.
- The 2026-08-24 retime refutation for this entry is recorded in writing, so a
  reader of phase 2's conclusion sees the counter-evidence beside it.
- No script is parked, disabled, or re-marked by this task.
- `lifecycle.py check` clean; PyAutoMind is the only repo touched.
