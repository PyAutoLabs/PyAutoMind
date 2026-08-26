# The jax_likelihood smoke-pin bug was already fixed when it was filed

Retired unstarted on 2026-08-26 by a `/start_dev` research pass. Never issued
as a GitHub issue and never developed: the four failures the prompt describes
had all been resolved on `autolens_workspace_test` main by 2026-08-22, most of
them within hours of the prompt being written. Recorded rather than deleted
because the *reason* it went stale is the reusable finding.

## Verified state at retirement

`autolens_workspace_test` main `8be3d59`, Smoke Tests run
[32922456742](https://github.com/PyAutoLabs/autolens_workspace_test/actions/runs/32922456742)
(2026-08-26 02:24 UTC), green on both Python 3.12 and 3.13:

```
Running 22 listed scripts
  scripts/imaging/jax_likelihood/lp.py ...              PASS (9.8s)
  scripts/interferometer/jax_likelihood/rectangular.py  PASS (21.1s)
  scripts/interferometer/jax_likelihood/mge.py ...      PASS (12.6s)
  ... 22/22 PASS
```

The prompt's headline — "every workspace_test smoke sweep reads 20/24 until
this lands" — is now 22/22. The denominator moved too: two further entries
left `smoke_tests.txt` for reasons unrelated to pins.

## Disposition of each claim

- **`imaging/jax_likelihood/lp.py`, pin `-1.34797827e09` is double.** Fixed.
  Repinned to `-6.74165366e08` in `197ce6e` (autolens_workspace_test#257) on
  2026-08-19 — the same day the prompt was filed.
- **"The unmerged fix `fb1aefe0b` sits in the orphan worktree
  `~/Code/PyAutoLabs-wt/positions-lh-penalty-accumulation`; landing it and
  re-pinning must happen together."** Both had already happened. `fb1aefe0b`
  is the head SHA of [PyAutoLens#700](https://github.com/PyAutoLabs/PyAutoLens/pull/700)
  ("sum PositionsLH penalties instead of doubling the last entry", fixes
  PyAutoLens#699), merged 2026-08-17 — two days *before* the prompt called it
  unmerged. `197ce6e` is precisely the paired re-pin the prompt asked for, and
  it repinned five scripts, not four (it also caught
  `interferometer/jax_likelihood/lp.py` and both `imaging/substructure/subhalo.py`
  pairs).
- **`interferometer/jax_likelihood/rectangular.py` misses pin `-3164.286252` by
  0.0124% vs rtol 1e-4.** Passing. The pin literal is *unchanged* to this day,
  and `99d63b3` (2026-08-21) re-verified the script green including its
  TransformerNUFFT cross-check. So the 08-19 miss was environment drift in the
  control run, not a stale pin — nothing to recalibrate and no tolerance to
  widen.
- **`interferometer/jax_likelihood/mge.py`, "same stale-pin family".** Fixed by
  the same `197ce6e`: `-7.94439429e08` -> `-3.97221282e08`, i.e. it was a
  PositionsLH-doubling casualty, not an independent drift.
- **`multi_dataset/jax_likelihood/mge.py`, "same stale-pin family".** Never a
  pin problem. Commented out of `smoke_tests.txt` on 2026-08-22 (#262) for
  hanging to the 300s cap — the family-wide XLA compile stall tracked in
  autolens_workspace_test#245. Its pin (`EXPECTED_VMAP_LOG_LIKELIHOOD =
  -2173221.43685875`) is untouched since the `multi` -> `multi_dataset` rename
  (`d7cc60c`) and has never been shown wrong.

## Key traps / findings

- **A control-test finding has a shelf life measured in hours.** This prompt
  was written from a control run taken during `lazy-heavy-imports` (#1505) and
  was obsolete before the day was out — `197ce6e` landed 2026-08-19 10:25 EDT.
  Filing a finding is not the same as checking whether someone is already on
  it; a pass over recent commits touching the named files would have caught it.
- **"Orphan worktree" is a claim about a laptop, not about a repository.** A
  local worktree whose branch has been merged and deleted upstream looks
  identical to one holding genuinely unlanded work. The check that settles it
  is the branch's head SHA against the remote's merged PRs — here `fb1aefe0b`
  resolved straight to a PR merged two days earlier. Adjudicate an orphan from
  the remote, never from the worktree's own state.
- **One root cause can wear several symptom labels.** Three of the four listed
  scripts were the *same* bug (the 2x-last PositionsLH penalty), not a
  "stale-pin family". Grouping symptoms by folder invented a class of drift
  that did not exist and would have sent the fix in the wrong direction —
  widening tolerances on correct pins.
- **A script leaving the smoke gate changes the denominator.** A pass/total
  target like "20/24" is not a stable goal: `multi_dataset/jax_likelihood/mge.py`
  and `multi_dataset/jax_likelihood/shared_preloads.py` both left the list for
  timing reasons, so the sweep now reads 22/22 without any pin having been
  touched for that.

## Follow-ups

- **Local debris only.** `~/Code/PyAutoLabs-wt/positions-lh-penalty-accumulation`
  is a stale worktree over a merged-and-deleted branch on the laptop; it is a
  `/repo_cleanup` item, not code work, and no cloud session can see or clear
  it.
- **Latent, owned elsewhere.** `multi_dataset/jax_likelihood/mge.py`'s pin has
  never been verified against a post-PyAutoLens#700 library. If
  autolens_workspace_test#245's XLA stall is fixed and the script returns to
  the gate, re-derive its pin as part of that re-enable rather than trusting
  the pre-rename literal. Deliberately not filed as its own prompt — it has no
  standalone trigger.

## Original prompt

# autolens_workspace_test jax_likelihood pins: 4 scripts fail smoke on main

Type: bug
Target: autolens
Repos:
- @PyAutoLens
Difficulty: low
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-08-19 (backfilled from git)

## Finding (2026-08-19, control-tested during lazy-heavy-imports #1505)

`pyauto-heart smoke autolens_test` fails 4/24 on canonical main (verified twice,
worktree and canonical identical):

- `imaging/jax_likelihood/lp.py` — vmap result is ~half the hardcoded pin
  `-1.34797827e09`. This is the positions-LH penalty-doubling: the unmerged fix
  `fb1aefe0b` ("sum PositionsLH penalties instead of doubling the last entry")
  sits in the orphan worktree `~/Code/PyAutoLabs-wt/positions-lh-penalty-accumulation`
  (PyAutoLens). The pin was calibrated against the doubling behaviour — landing
  that fix and re-pinning must happen together.
- `interferometer/jax_likelihood/rectangular.py` — misses pin `-3164.286252` by
  0.0124% vs rtol 1e-4 (stale-pin drift).
- `interferometer/jax_likelihood/mge.py`, `multi_dataset/jax_likelihood/mge.py` —
  same stale-pin family.

## Task

Adjudicate the orphan positions-LH worktree (land or discard `fb1aefe0b`), then
recalibrate the four scripts' hardcoded pins against current main and widen
tolerances where the value is legitimately environment-sensitive. Every
workspace_test smoke sweep reads 20/24 until this lands.
