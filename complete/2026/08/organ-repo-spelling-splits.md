- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/287 (closed on ship)
- shipped: 2026-08-26 — PyAutoBrain PR https://github.com/PyAutoLabs/PyAutoBrain/pull/288
  and PyAutoMind PR https://github.com/PyAutoLabs/PyAutoMind/pull/333 (Mind merged first)
- classification: bug (PyAutoBrain + PyAutoMind; organism infrastructure — neither
  library nor workspace)
- summary: The bare and prefixed spellings of seven repos normalised to two different
  keys, so a policy map filed under one was invisible to the other. The keying question
  the prompt demanded be answered first was answered — **organs key PREFIXED** — and
  then the class was closed rather than its fourth instance: the bare/prefixed/package
  alias join now DERIVES from the body map's new `package:` field, and five guards make
  the next gap fail loudly.

## The decision, taken before the edit

Organs key on the prefixed form (`pyautobrain`). Not a new rule — #269's rule made
executable: *the canonical key is the package the repo SHIPS where it ships one, the
repo name where it does not.* Organs ship no package; Nerves is the one that does and
already keyed bare (`autonerves`). Everything downstream was already filed prefixed for
organs — `test_witness`, `target_signals`, `REPO_DISPLAY`, `target_default_wiki`, and
the Mind's own `draft/*/pyautobrain/` target folders — so keying bare would have rekeyed
five maps for no gain.

## Shipped changes

- `PyAutoMind/repos.yaml`: `package:` on the seven repos that ship one (six libraries +
  Nerves), documented in the header as identity — the other name a repo is known by.
- `PyAutoBrain/agents/faculties/sizing/_sizing.py`: `_body_map_specs`, `canonical_key`,
  `spellings_of`, `unreachable_repos`, `_derived_aliases`, `_repo_aliases`; the alias
  table is now derived ∪ hand, with a conflict between them raising rather than one
  quietly winning.
- `PyAutoBrain/config/policy.yaml`: `repo_aliases` trimmed to what a body map cannot
  know, with the canonical-key rule written where the maps live.
  `extra_organism_targets` emptied — `autohands` is derived now.
- `PyAutoBrain/agents/conductors/intake/_intake.py`: `REPO_DISPLAY` derived too.
- `PyAutoBrain/tests/test_policy_seams.py`: five guards (below).

## What the reproduction found beyond the prompt

The prompt named five organs. Sweeping every body-map repo found seven splits — the five
organs, PyAutoHands (joined only by a policy literal), and **PyAutoScientist** — plus one
repo that could never resolve at all.

**`pyautolabs.github.io` was DE-REGISTERED, not joined.** This is a deliberate deviation
from the scope answered at plan time ("join both"). `normalise_repo` truncates at the
first `.`/`/`, so no mention can reach a dotted repo name. The obvious fix — alias the
truncated head — is *worse* than the gap: that head is `pyautolabs`, the ORG name, so
`@PyAutoLabs/PyAutoFit` would have started resolving to the static site instead of
PyAutoFit. The acceptance criterion's other branch ("or is deliberately not registered")
covers it. The exclusion derives from the names themselves (any name carrying a
separator), not a hand-kept list, and a guard pins both halves: the repo is out of the
known targets AND its truncated head still resolves to nothing.

## Guards, each mutation-tested

| Guard | Mutation that proves it |
|---|---|
| no repo splits across two keys | removing the derived join names all seven affected repos |
| no alias points at a key nothing is filed under | — |
| body map `package:` agrees with the witness map | mis-keying one `package:` value raises at import |
| unreachable repos excluded, and their head resolves to nothing | forcing the dotted repo back into the set |
| canonical keys survive a body map with no `package:` | deleting the pre-package fallback rows |

## Traps and findings

- **The cross-repo CI pinning is the trap this task turns on.** `tests.yml` checks the
  sibling Mind out at `main`, pinned, so a Brain half that REQUIRED the Mind half would
  sit red until Mind merged. `canonical_key` falls back to the hand table's library rows
  when no `package:` is declared, giving identical keys either way — and a test pins that
  property so the fallback is not an unexercised path. The corroboration guard did NOT
  have that tolerance on first push and **failed CI for exactly this reason**; the fix
  made it all-or-nothing (a map declaring no package has nothing to corroborate; one
  declaring *some* must declare all), which is a stronger guard than the one it replaced,
  not a weakened one.
- **The tenant firewall rejected two drafts of the prose**, for naming PyAutoCTI,
  PyAutoReduce, PyAutoScientist and PyAutoLabs in comments — the third consecutive task
  where it caught the agent's own drift (cf. #267, #269). The comments read generically
  because of it.
- **Behaviour preservation was measured, not asserted.** An A/B over every spelling in
  the alias table and target sets shows exactly six resolutions changed, all intended
  joins; libraries, short forms, renames, workspaces and org-qualified paths byte-identical.
- **`REPO_DISPLAY` had the beginnings of the same drift** — reachable keys (`pyautohands`,
  the CTI/Reduce libraries, the HowTos) carried no row, so a header rendered
  `Target: pyautohands`. Newly-reachable keys would have inherited it, so it was derived
  in the same pass rather than special-cased.
- **A `git checkout --` during the mutation sweep clobbered the implementation** and it
  had to be reapplied. Worth naming: mutation-testing a file you are also editing needs a
  file backup, not a git restore.

## Gate

Brain tests 515 pass (510 baseline + 5 guards), on both matrix legs in CI, and locally
against BOTH body-map states — the branch's Mind with all seven packages declared, and a
Mind checkout at `origin/main` with none. `repos_sync --check` all 13 legs OK. Smoke n/a
(organism repos). **Heart NOT EVALUATED** — `pyauto-heart` is unreachable from a
web-github session, so leg 4 of the ship gate never ran; recorded that way rather than
claimed clean. Effective autonomy `supervised`; the run took its plan checkpoint (two
scope questions put to the human) and proceeded on the answers.

## Follow-ups

- The seven pre-package library rows in `repo_aliases` are the fallback for a body map
  without `package:`. Now that PyAutoMind#333 has merged they are dead weight and can be
  deleted, which also fully arms the corroboration guard's strict path.
- `normalise_repo` still passes `maxsplit` positionally (a DeprecationWarning on 3.13).
  The copy this task introduced was fixed; the pre-existing one was left alone.

## Original prompt

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
