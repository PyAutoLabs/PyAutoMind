# The 3-script twin of the jax_likelihood pin prompt, filed five days earlier

Retired unstarted on 2026-08-27 by a dashboard-drift audit. This prompt is a
near-duplicate of `draft/bug/autolens/jax_likelihood_smoke_pins_stale.md`, which
was retired the day before as
[`complete/2026/08/jax-likelihood-smoke-pins-stale.md`](jax-likelihood-smoke-pins-stale.md).
That record adjudicates all three scripts this one names, by name. Nothing here
was left unanswered — the answer was simply written against the other copy of
the question, and this copy kept rendering as pickable backlog.

## Why there were two

Same finding, two filings, five days apart, in two different folders:

| | this prompt | its twin |
|---|---|---|
| path | `draft/bug/workspaces/jax_likelihood_pins_stale_by_1e4.md` | `draft/bug/autolens/jax_likelihood_smoke_pins_stale.md` |
| filed | 2026-08-14 (smoke gate for PyAutoFit#1473) | 2026-08-19 (control run during `lazy-heavy-imports`, #1505) |
| scripts | 3 | 4 (the same 3, plus `imaging/jax_likelihood/lp.py`) |
| retired | this record | `f3324d80`, 2026-08-26 |

Both were written from a `pyauto-heart smoke autolens_test` run against the same
failing gate, by sessions that did not know about each other. Neither names the
other; the 08-19 filing's own "Provenance" says it was written from a control
run, which is exactly the state in which you do not go looking for a prior
filing.

## Disposition — verified at retirement

`autolens_workspace_test` main `69ee97c` (2026-08-27), read directly:

- **`interferometer/jax_likelihood/rectangular.py`** — pin `-3164.286252` is
  unchanged at lines 274 and 387, and the script is in `smoke_tests.txt`. The
  08-14 miss (`-3163.8939…`, 1.24e-4 against rtol 1e-4) was environment drift in
  the control run, not a stale pin. `99d63b3` (08-21) re-verified it green
  including the TransformerNUFFT cross-check. **No re-pin, no tolerance change.**
- **`interferometer/jax_likelihood/mge.py`** — repinned `-7.94439429e08` →
  `-3.97221282e08` by `197ce6e` (autolens_workspace_test#257, 2026-08-19), and
  `-3.97221282e08` is what lines 204 and 278 carry today. It was a
  PositionsLH-doubling casualty of PyAutoLens#700, not independent pin drift.
- **`multi_dataset/jax_likelihood/mge.py`** — never a pin problem. Its
  `EXPECTED_VMAP_LOG_LIKELIHOOD = -2173221.43685875` is untouched since the
  `multi` → `multi_dataset` rename (`d7cc60c`). It was commented out of
  `smoke_tests.txt` on 08-22 (#262) for hanging to the 300s cap — the XLA compile
  stall, not a likelihood value — and is back in the gate as of `69ee97c`, after
  the stall work shipped (autolens_workspace_test#281,
  `complete/2026/08/jax-vmap-materialisation-hang.md`).

So the prompt's central instruction — "decide per script whether the pin is stale
or the drift is a real regression; do not blanket re-pin" — was followed, by
someone else, and came out: one environment artefact, one real bug with a
different root cause, one timing problem wearing a pin problem's clothes.

## Key traps / findings

- **Retiring one prompt does not retire its twin.** The 08-26 sweep verified the
  finding thoroughly and retired the filing it was working from. The duplicate
  survived because it sits under a different work-type/target
  (`bug/workspaces/` vs `bug/autolens/`) and carries a different headline
  ("stale by ~1.24e-4" vs "4 scripts fail smoke"), so neither a folder scan nor a
  slug match connects them. **On retiring a prompt, grep the backlog for the
  artefacts it names — here, the three script paths — not for its own slug.**
- **The `Filed:` date is the tell.** The surviving copy was the *older* filing.
  A retirement sweep that starts from the newest evidence naturally walks
  forward, and never looks behind the prompt it is holding.
- **This drift is invisible to every guard.** `lifecycle.py check` passes (its
  invariant is about `active.md` slugs with records, and this prompt was never
  active), `orphans` and `index --check` pass, and `intake reconcile` did not
  flag it — the duplicate's `rare-topic-overlap` and `shared-identifiers`
  signals compare a prompt against *records*, and the record that covers it was
  written under a slug with no token overlap. The signal that would have caught
  it is prompt-to-prompt: two live prompts naming the same source files.

## Follow-ups

- **A duplicate-detection signal for `intake reconcile`.** Every existing signal
  scores a prompt against the completion archive. Nothing scores prompts against
  *each other*, and near-duplicate filings from independent sessions are a
  standing hazard of a backlog this size with several sessions filing into it.
  A shared-file-path or shared-identifier pass over the 134 live prompts is
  cheap and would have surfaced this pair the day the second one was filed.
  Filed as `draft/feature/pyautobrain/reconcile_duplicate_prompt_signal.md`.

## Original prompt

# Three `jax_likelihood` pins are stale by ~1.24e-4 and fail the smoke gate on main

Type: bug
Target: workspaces
Repos:
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-14 (backfilled from git)

Three `autolens_workspace_test` JAX-likelihood scripts fail their pinned-value
assertions on `main`, marginally over tolerance. They fail every local smoke
run, so the `autolens_test` workspace can never come back clean.

## Failing scripts

```
interferometer/jax_likelihood/rectangular.py
interferometer/jax_likelihood/mge.py
multi_dataset/jax_likelihood/mge.py
```

## The failure

```
AssertionError: Not equal to tolerance rtol=0.0001, atol=0
interferometer/rectangular: JAX vmap likelihood mismatch
 [0]: -3163.8939270532364 (ACTUAL), -3164.286252 (DESIRED)
Max absolute difference among violations: 0.39232495
Max relative difference among violations: 0.00012399
```

**1.24e-4 against an rtol of 1e-4** — 24% over the tolerance, not a
qualitatively broken computation. The likelihood has drifted slightly since the
constants were pinned (or the pin was recorded at lower precision: `-3164.286252`
is 10 significant figures while the computed value carries 17).

## Confirmed pre-existing

Reproduced with `pyauto-heart smoke autolens_test` under two roots — a feature
worktree and canonical `main` — producing **byte-identical** ACTUAL and DESIRED
values in both. Not caused by any in-flight branch.

## Scope

- Decide per script whether the pin is stale (re-pin) or the drift is a real
  regression (investigate). **Do not blanket re-pin** — the point of an absolute
  pin is to notice exactly this, and 4e-4 on an interferometer likelihood may be
  a genuine numerical change worth understanding first. Bisect the value before
  overwriting it.
- Check whether the pins were recorded at reduced precision; if so, the fix is
  to re-record at full precision rather than to widen the tolerance.
- Widening `rtol` is the tempting move and the wrong first move — it would hide
  the next drift too.
- Audit the **other** `jax_likelihood` pins in the same sweep; three failing
  together suggests a shared cause, and the rest may be sitting just inside
  tolerance.

## Provenance

Found while running the smoke gate for PyAutoFit#1473 (MultiStartGradient NaN
step diagnostics). Unrelated to that change — the failing scripts contain no
`MultiStart` reference, and the control run against `main` matched exactly.

Related but distinct: `draft/test/workspaces/restore_workspace_test_likelihood_baselines.md`
covers restoring *removed* NumPy baselines; this is about *existing* JAX pins
having drifted out of tolerance.
