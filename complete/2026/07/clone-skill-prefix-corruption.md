## clone-skill-prefix-corruption
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/150
- completed: 2026-07-23
- prs: PyAutoHands#178, PyAutoBrain#151, autocti_assistant#9 — ALL MERGED
- summary: The Clone Agent's skill-prefix substitution (`al_ -> ac_`, from package initials) was applied by `clone_seed.substitute` as a bare `str.replace` to BOTH paths and file text. Meant to rename `al_fit_model.md`; unanchored it rewrote the `al_` inside every identifier ending in `al`. Fixed by giving a rule an optional third element `"word"`, compiled to `(?<![A-Za-z0-9])<old>` — so the prefix may START a token but never continue one. The rule deliberately still applies to file TEXT (skills cross-reference each other by name in prose; a path-only rule would leave broken links in every newborn). Two-element rules keep plain-replace, so existing plan JSON is unaffected. 16 regression tests. Also repaired the 7 live corruptions in autocti_assistant.
- gotchas:
  - **A short substitution rule applied to free text is a latent corruptor.** `al_` is 3 chars; `total_draws`, `external_shear`, `isothermal_core`, `exponential_core`, `virial_mass`, `radial_minimum` all end in `al_`. The rule had been live since autocti_assistant's birth and NONE of it was caught, because every corruption is silent: a dead yaml key falls back to the library default, and an unreachable prior file falls back to library priors. Both dead keys happened to hold the SAME value as the default, so there was no observable symptom at all.
  - **The bug was found from a one-character typo.** `radiac_minimum` in a config file that was itself dead. Chasing why a dead file had a typo found a live tool bug. [[feedback_sweep_siblings_not_just_the_named_file]] applied at the tool level: the sibling of a corrupted name is every other name the same rule touched.
  - Brain Bug Agent said `investigate-first` + `too-large(11)` + "public-API change may ripple downstream". Root cause was already reproduced (the 7 corruptions ARE the reproduction) and the schema change is backward-compatible. Overridden with human approval.
  - PyAutoBrain `test_skill_install::test_every_public_agent_has_a_skill_wrapper` (missing `sizing` wrapper) fails on CLEAN MAIN at b58070b — verified directly rather than trusting the note in the rename task's active.md entry. Not caused by this work.
  - autocti_assistant `wiki-currency` is RED on main, caused by `cecdb67` which rewrote the checker to gate on API-surface hash and landed without a wiki-currency run.
- follow-ups:
  - `/hygiene config` orphan-config blind spot — the audit diffs library keys vs workspace keys, so a workspace config file with NO library counterpart is structurally invisible. That is how grids.yaml survived ~1yr. A prototype orphan check gave 100+ hits, nearly all legitimate (`build/*` workspace-only by design; `priors/*` for workspace-defined classes), so NOT shipped. Needs a suppression design before it earns its keep.
  - autocti_assistant `wiki-currency` red on main (see gotcha).
  - autolens_assistant `boundary` red on main — 4 `docs/images/*` + `docs/make_readme_figures.py` unclassified; must be recorded in BOTH `modes/maintainer.md` "## Assistant-as-template" and `_clone.py` `REFERENCE_PROFILES['autolens_assistant']`. Blocks every future assistant birth.
  - `rename-autobuild-to-autohands` (parked) now has main moved under it on 2 of these files — merge note added to its active.md entry; the new test file's `from autobuild.clone_seed import substitute` import must be updated by the rename.

## Original prompt

# Clone-agent skill-prefix substitution corrupts every identifier ending in `al_`

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoHands
- autocti_assistant
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> merge and sort hygeine

Filed 2026-07-23 while sorting the hygiene follow-up from the
`defunct-grids-yaml-removal` task (autolens_workspace#317). The intended
follow-up was the `/hygiene config` orphan-file blind spot; probing it surfaced
this instead, which is a live tool bug rather than an audit gap.

## Why

`PyAutoBrain/agents/conductors/clone/_clone.py:413` emits a skill-prefix
substitution built from the package initials:

```python
[f"{ref_pkg[0]}{ref_pkg[4]}_", f"{target_pkg[0]}{target_pkg[4]}_"],   # "al_" -> "ac_"
```

`PyAutoHands/autobuild/clone_seed.py:56` applies it as a raw substring replace
to **both paths and file text**:

```python
def substitute(text, subs):
    for old, new in subs:
        text = text.replace(old, new)
    return text
```

The rule is meant to rename skill files (`al_fit_model.md` → `ac_fit_model.md`).
Because it is unanchored it also fires mid-word, on every identifier ending in
`al` followed by `_`.

### Observed damage (autocti_assistant, born from autolens_assistant)

| Corruption | Should be | Impact |
|---|---|---|
| `config/non_linear/mle.yaml:78` `totac_draws` | `total_draws` | dead key — real PyAutoFit `Drawer` param (`autofit/non_linear/search/mle/drawer/search.py:21`, default 50) |
| `config/visualize/general.yaml:37` `totac_contours` | `total_contours` | dead key — read by `autoarray/plot/utils.py:768` via `_c.get("total_contours", 10)` |
| `config/priors/mass/sheets/externac_shear.yaml` | `external_shear.yaml` | prior file unreachable for `ExternalShear` |
| `config/priors/mass/total/isothermac_core.yaml` | `isothermal_core.yaml` | prior file unreachable |
| `config/priors/light/linear/exponentiac_core.yaml` | `exponential_core.yaml` | prior file unreachable |
| `config/priors/light/standard/exponentiac_core.yaml` | `exponential_core.yaml` | prior file unreachable |
| `config/priors/mass/dark/gnfw_viriac_mass_conc.yaml` | `gnfw_virial_mass_conc.yaml` | prior file unreachable |
| `config/grids.yaml` `radiac_minimum` | `radial_minimum` | already deleted 2026-07-23 (#317) |
| `autoassistant/audit_skill_apis.py:513,542` `totac_symbols` | `total_symbols` | internal local, self-consistent — harmless |

The two dead config keys happen to carry the same value as the library default
(50 and 10), so nothing is observably *wrong* today — but both knobs are inert.
The five prior files are the real damage: they can never be found for their
classes, so those priors silently fall back to library defaults.

The other three assistants (`autolens_assistant`, `autofit_assistant`,
`euclid_assistant`) are clean — this is not historical residue, it is a live
rule that will corrupt the next birth. Any target prefix reproduces it
(`aa_` would give `totaa_draws`).

## Scope

**1. Anchor the rule (the fix).** The rule must keep applying to file *text* —
skill files cross-reference each other by name in prose, so scoping it to paths
only would leave broken links in every newborn. Anchor it instead so the prefix
cannot match mid-word:

```
(?<![A-Za-z0-9])al_   ->   ac_
```

- `PyAutoHands/autobuild/clone_seed.py` — `substitute()` gains support for a
  third rule element marking the rule word-anchored. Two-element rules keep
  today's plain-replace behaviour so any existing plan JSON still works.
- `PyAutoBrain/agents/conductors/clone/_clone.py` — emit the skill-prefix rule
  with the anchored marker. The other three rules
  (`autolens_assistant`→target, `PyAutoLens`→`PyAutoCTI`, `autolens`→`autocti`)
  stay plain: they are long and specific enough not to collide.
- Regression test: `total_draws` / `external_shear` survive; `al_x.md`,
  `skills/al_x.md` and a backticked `` `al_x` `` in prose all rename.

**2. Repair autocti_assistant.** `git mv` the 5 prior files to their correct
names, fix the 2 dead config keys, and fix the matching `PENDING.md` lines.
Leave `totac_symbols` in `audit_skill_apis.py` — renaming a self-consistent
local is churn, not a fix (or rename it for readability, but it is not a defect).

## Out of scope

- The `/hygiene config` orphan-config-file blind spot that started this thread.
  A prototype produced 100+ hits across the workspaces, nearly all legitimate
  (`build/*` is workspace-only by design, as are `priors/*` for
  workspace-defined classes). Not worth shipping as a signal in that form —
  see the "decidable refusals earn their keep" lesson from the build-chain
  campaign.
- `autocti_assistant`'s two red CI checks on main (`wiki-currency`, and
  `boundary` on `autolens_assistant`) — separate pre-existing failures, noted
  on autolens_workspace#317.

## Verify

- New regression test passes; PyAutoBrain and PyAutoHands suites stay green.
- `grep -rE "totac_|radiac_|exponentiac|viriac|externac|isothermac" autocti_assistant`
  returns only the deliberate `audit_skill_apis.py` locals (or nothing).
- The 5 renamed prior files resolve for their classes.
