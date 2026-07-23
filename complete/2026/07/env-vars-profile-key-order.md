One canonical `defaults:` key order now applies to every
`config/build/env_vars*.yaml` in the workspace, so the `smoke` profile
(`env_vars.yaml`, per-PR CI gate) and the release-fidelity profile
(`env_vars_release.yaml`) line up row-for-row and can be diffed side by side.
The trailing comment column is aligned at a single column across all files.

Shipped as 10 PRs, all merged 2026-07-23:
autolens_workspace#322, autogalaxy_workspace#148, autofit_workspace#110,
autolens_workspace_test#202, autogalaxy_workspace_test#84,
autofit_workspace_test#67, HowToLens#49, HowToGalaxy#39, HowToFit#28,
euclid_strong_lens_modeling_pipeline#33. Issue:
https://github.com/PyAutoLabs/autolens_workspace/issues/321

## What changed

17 files across 11 repos. Five release profiles genuinely deviated from the
order (`autolens_workspace`, `autogalaxy_workspace`, `autofit_workspace` had a
7-key permutation; `autolens_workspace_test` / `autogalaxy_workspace_test` had
`FAST_PLOTS`/`DISABLE_JAX` swapped). The remaining twelve got comment-column
alignment only. `autocti_workspace_test` needed no change at all — already
canonical, and it carries no inline comments — so the sweep produced 10 PRs,
not 11.

Canonical order (union of every key in use, smoke-first): `PYAUTO_TEST_MODE`,
`PYAUTO_SKIP_FIT_OUTPUT`, `PYAUTO_SKIP_VISUALIZATION`, `PYAUTO_SKIP_CHECKS`,
`PYAUTO_SMALL_DATASETS`, `PYAUTO_DISABLE_JAX`, `PYAUTO_FAST_PLOTS`,
`PYAUTO_SKIP_WORKSPACE_VERSION_CHECK`, `JAX_ENABLE_X64`, `MPLBACKEND`,
`NUMBA_CACHE_DIR`, `MPLCONFIGDIR`.

No keys added or removed, no values changed, every key kept its own comment
text, and `overrides:` was not touched anywhere.

## Why it is safe

`defaults` is applied by plain dict iteration in
`PyAutoHands/autohands/env_config.py`, so its order cannot affect the resolved
environment. `overrides` is the order-sensitive structure (an ordered list of
pattern rules, later rules winning) and it was deliberately left alone.

## How it was verified

The authoritative check was a **resolved-env diff**, not a build run: for every
script in every repo x both profiles, resolve from an EMPTY base via
`resolve_clean()` in `PyAutoHands/autohands/validate_env_profiles.py`, dump to
JSON before and after, and diff. **Identical in all 11 repos.** For a
config-only change with zero `scripts/` edits this is strictly stronger than a
smoke run — it proves every script's environment is byte-for-byte unchanged
rather than sampling a curated subset. Smoke was therefore not re-run as the
gate, and the PRs say so explicitly rather than implying it passed.

`validate_env_profiles.py` verdicts were byte-identical to `main`: the 5
`env_vars_release.yaml: missing` errors (HowToLens, HowToGalaxy, HowToFit,
euclid, autocti_workspace_test carry only the smoke profile) and the 42
`PYAUTO_DISABLE_JAX` derivation-rule warnings are all pre-existing.

## Notes for next time

- **Brain's Feature Agent over-classified this** as `too-large →
  split-into-4-phases`, scored purely off the 11-repo count, with risks
  "public-API change may ripple downstream". Repo count is a poor difficulty
  proxy for a cosmetic sweep; the classification was overridden by judgment and
  shipped as one task in an afternoon.
- `gh pr create` fails with `/usr/bin/git: exit status 128` when run from the
  PyAutoLabs root (not a git repo) even with `--repo` given — it still wants a
  git cwd. `cd` into the repo first.
- `worktree_create` prints `HEAD is now at ...` per repo but does **not**
  disturb dirty files in the source checkouts (euclid's unrelated modified
  `test_report.md` survived intact).

## Follow-up filed as a finding, not fixed

`autofit_workspace_test/config/build/env_vars_release.yaml` omits
`PYAUTO_SMALL_DATASETS` and `PYAUTO_FAST_PLOTS` entirely. The release-profile
header doctrine (see the `autolens_workspace` release header) requires every var
the profile cares about to carry an EXPLICIT value precisely because the runner
only ever *sets* keys it is given — an absent key silently falls through to
whatever the calling process already had, so a leftover smoke-mode `"1"` from an
earlier step can survive into a release-fidelity run. Invisible while the files
could not be diffed; exposed by this alignment. Deliberately out of scope for a
no-op reordering.

## Heart gate

Shipped under the **corrective-PR exception**, human-authorized against the
verbatim RED reason `release validation FAILED (stage integrate)` (verdict red,
score 40, ts 2026-07-23T14:11:21Z; `integrate:fail` on `v2026.7.22.1.dev67201`
from the 2026-07-22 release-validation run). Unrelated to this diff. The
exception stops at PR-open; the subsequent merge was a separate explicit human
instruction.

## Original prompt

# Align env_vars.yaml / env_vars_release.yaml key order across all build configs

Type: maintenance
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- HowToLens
- HowToGalaxy
- HowToFit
- euclid_strong_lens_modeling_pipeline
- autocti_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Original request (verbatim):

> Make env_vars and env_vars_release same order, e.g. the two configs are hard to
> compare side by isde cause the top entries are in different orders,

## Why

Every buildable workspace carries two env profiles under `config/build/`:
`env_vars.yaml` (the `smoke` profile, per-PR CI gate) and `env_vars_release.yaml`
(the release-fidelity profile). They are meant to be read side by side — the
release file's whole job is to say "same knobs, different values". Today they
cannot be: the `defaults:` blocks list the same keys in different orders.

`autolens_workspace` is the clearest case — smoke runs `TEST_MODE,
SKIP_FIT_OUTPUT, SKIP_VISUALIZATION, SKIP_CHECKS, SMALL_DATASETS, DISABLE_JAX,
FAST_PLOTS`, while release runs `TEST_MODE, SMALL_DATASETS, FAST_PLOTS,
SKIP_FIT_OUTPUT, SKIP_VISUALIZATION, SKIP_CHECKS, DISABLE_JAX,
SKIP_WORKSPACE_VERSION_CHECK`. Working out which knob actually differs between
the profiles means scanning, not diffing. The `*_workspace_test` pairs carry a
smaller version of the same skew (`FAST_PLOTS`/`DISABLE_JAX` swapped), and
comment columns are ragged in places.

## Canonical order

Union of every key currently in use, ordered smoke-first:

```
PYAUTO_TEST_MODE
PYAUTO_SKIP_FIT_OUTPUT
PYAUTO_SKIP_VISUALIZATION
PYAUTO_SKIP_CHECKS
PYAUTO_SMALL_DATASETS
PYAUTO_DISABLE_JAX
PYAUTO_FAST_PLOTS
PYAUTO_SKIP_WORKSPACE_VERSION_CHECK
JAX_ENABLE_X64
MPLBACKEND
NUMBA_CACHE_DIR
MPLCONFIGDIR
```

Contract, per file:

- list only the keys the file already has — **no keys added or removed**;
- **no values changed**, and each key keeps its own existing comment text;
- present keys appear in the canonical relative order;
- align the trailing `#` comment column at column 40 within each `defaults:` block;
- **`overrides:` is not touched.** `defaults` is applied by iterating a plain
  dict (`PyAutoHands/autobuild/env_config.py:68`), so its order is semantically
  irrelevant; `overrides` is an ordered list of pattern rules where order *does*
  matter, so it stays exactly as-is.

## Scope

All 17 `config/build/env_vars*.yaml` across the 11 repos above. Five need real
reordering (`env_vars_release.yaml` in `autolens_workspace`,
`autogalaxy_workspace`, `autofit_workspace`, `autolens_workspace_test`,
`autogalaxy_workspace_test`); the remaining 12 get comment-column alignment only.

## Verify

Decidable from config alone — no script execution, no CI dispatch.

- Before and after, resolve **both** profiles for every script in each repo and
  dump to JSON, reusing `resolve_clean(script, cfg)` from
  `PyAutoHands/autobuild/validate_env_profiles.py` (resolves from an empty base,
  never `os.environ`). The before/after diff must be **empty** for every repo — a
  non-empty diff means a key was dropped, renamed, or a value changed.
- Run `validate_env_profiles.py` against each edited repo (exit-1 tier catches
  unparseable YAML, non-mapping profiles, malformed overrides).
- Sanity check the point of the exercise: `diff` a repo's `env_vars.yaml` against
  its `env_vars_release.yaml` and confirm the surviving hunks are value/comment
  differences only, with keys lining up row-for-row.

Pre-flight `git diff --stat` in each worktree before committing: nothing but
`config/build/env_vars*.yaml` may appear.
