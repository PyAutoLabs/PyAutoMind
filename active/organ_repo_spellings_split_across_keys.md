# Organ repo spellings split across two normalised keys

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-24
Issued: 2026-08-26

Found while shipping the refactor witness-map audit (@PyAutoBrain#269 / PR #271).

## The defect

The bare spellings of the organ repos do not normalise to the same key as their
repo spellings, so a policy map keyed on one is invisible to the other.

@PyAutoBrain/agents/faculties/sizing/_sizing.py (`_target_sets.names_for`)
registers BOTH spellings of every `PyAuto*` repo as known targets
(`name.lower()` and `name.lower()[2:]`), but the `repo_aliases` table in
@PyAutoBrain/config/policy.yaml only joins them for the libraries:

| mention | normalises to | resolves? |
|---|---|---|
| `@PyAutoBrain` | `pyautobrain` | yes |
| `@autobrain` | `autobrain` | no — a known target with nothing filed under it |

Same for the bare Heart, Memory, Mind and Gut spellings. `@autohands` was joined
in PR #271 because `extra_organism_targets` declares it explicitly and it
reaches real code today; the rest are latent — no prompt in the Mind history
uses them yet.

## Decide before fixing

This is NOT a blind alias sweep. Should organs key on the bare form
(`autobrain`) or the prefixed form (`pyautobrain`)? `target_signals` keys the
prefixed form (`pyautobrain`, `pyautomind`, `pyautoheart`, `pyautobuild`), and
after #271 `test_witness` keys organs prefixed but libraries bare. Whichever way
it goes has to hold across both maps at once, so answer the question first and
let the edit follow.

## The wider question this raises

Three separate repos have now hit this same defect class — PyAutoNerves
(#267), PyAutoCTI and PyAutoReduce (#269). The shared cause is that
`repo_aliases` is HAND-MAINTAINED while the known-target set is DERIVED from the
body map, so the two drift silently and the gap only ever surfaces as a
wrong-but-plausible conductor message ("strengthen tests first" for a
well-tested repo).

Guard 2 added in #271 — a witness-map key must be what its repo normalises to —
closes the witness-map instance only. An alias gap in a map with no coverage
guard is still invisible. Consider deriving `repo_aliases` from the body map so
the class closes rather than its fourth instance.

## Notes on this prompt's header

`pyauto-brain intake classify` scored this `bug` at high confidence (kept), but
proposed `Target: autocti` — it read the prior-instance history above as the
subject — and `Difficulty: too-large` (score 10), inflated by the repo names and
the design-decision keywords. Corrected to `pyautobrain` / `large` on review.
An alternative classification is `refactor`: the fix is behaviour-preserving for
every spelling that resolves today. `bug` was kept because the Bug Agent's
investigate-first strategy matches the "decide before fixing" requirement above.

Acceptance: every spelling of every body-map repo that `_target_sets` registers
as a known target resolves to a key the policy maps are actually filed under, or
is deliberately not registered; a guard makes a future alias gap fail loudly
rather than degrade a conductor's advice.
