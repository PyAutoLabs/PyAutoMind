## Outcome

**Resolved on arrival — no code change required.** The task was a stale `NEEDS_FIX` marker whose underlying bug had been fixed three months earlier and whose marker had been removed the previous night by a concurrent session. Issue [autolens_workspace_test#193](https://github.com/PyAutoLabs/autolens_workspace_test/issues/193) filed and closed with the evidence.

The prompt asked for three things — fix `__hash__`, add a unit test, remove the marker. All three were already done:

1. **The fix.** PyAutoGalaxy `0dcea475` (PR #374, 2026-04-28) — *"fix(light/linear): mark pytree_token as ephemeral via `__getstate__`/`__setstate__`"* — landed **one day after** the marker was filed on 2026-04-27. `LightProfileLinear.__hash__` returns `self.pytree_token`; the deserialization path could leave that field non-int, which CPython's `slot_tp_hash` rejects with exactly the reported `TypeError`.
2. **The tests.** The same commit shipped 5 regression tests in `test_autogalaxy/profiles/light/linear/test_abstract.py` (`test__pytree_token_is_int_and_unique`, `test__getstate__omits_pytree_token`, `test__setstate__assigns_fresh_pytree_token_when_missing`, `test__setstate__preserves_pytree_token_when_present`, `test__pickle_roundtrip_preserves_int_hash`). 11 passed on current main.
3. **The marker.** PR #192 (`3c14bf4`, 2026-07-21 21:06, concurrent session) deleted the `NEEDS_FIX` entry from `config/build/no_run.yaml`.

## Verification

A clean from-scratch reproduction of `scripts/database/scrape/general.py` (fresh Nautilus fit → scrape → aggregator → `aplt.subplot_fit_imaging`) exits **0** with all three aggregator checks passing.

**Trap hit and avoided:** the first reproduction attempt silently resumed a stale output dir (`Fit Already Completed: skipping non-linear search`, `Failed to load samples`, `parameter_lists[0]` printed `[]`) — a vacuous pass. Moving the output aside and re-running produced a real search and a trustworthy verdict.

## Findings worth carrying forward

**1. The 60s timeout cap is a myth — and it caused a bad triage call.**

The `no_run.yaml` header comment and `PyAutoHands/autobuild/slow_skip_check.py` both state a *"60s per-script timeout cap"*. The enforced default is **300s** (`PyAutoHands/autobuild/build_util.py:12` → `TIMEOUT_SECS = int(os.environ.get("BUILD_SCRIPT_TIMEOUT", "300"))`; `run_all.py:49` `DEFAULT_TIMEOUT_SECS = 300`), and 1800s in release mode. The wrong figure appears in 7 workspaces' `no_run.yaml` headers and in the slow-skip intro of **every mega-run report**.

Reading the header as authoritative, this session initially recommended retagging `scrape/general` as `SLOW` on a measured 214s runtime — wrong by a 5× error in the documented cap. Follow-up prompt filed; may also mean some of the four `database/scrape/*` siblings still tagged *"exceeds 60s timeout"* from 2026-04-10 are now un-parkable.

**2. `PYAUTO_TEST_MODE=2` is not the harness mode for `database/scrape/`.**

PR #192 verified the un-park under `PYAUTO_TEST_MODE=2`, but `config/build/env_vars.yaml:42-46` explicitly **unsets** `PYAUTO_TEST_MODE`, `PYAUTO_SMALL_DATASETS` and `PYAUTO_DISABLE_JAX` for the `database/scrape/` pattern — so that repro skipped the sampler the harness actually runs. The un-park is nonetheless correct: measured under the harness's real configuration the script takes **214s** (~45s viz warm-up + 83s Nautilus fit + scrape/aggregator/plotting) against the 300s cap, with `PYAUTO_FAST_PLOTS=1` (set by the harness, unset in this run) giving further margin.

**3. A NEEDS_FIX marker is a claim with a timestamp, not a fact.** This is the second census-parked marker to evaporate on reproduction. The fix landed 24 hours after the park; nobody re-checked for three months.

## Process note

`prompt_sync_push` runs `git add -A`, so the Mind push for this task also swept up a concurrent session's staged rename of `ell_comps_kwargs_keyerror_imaging_modeling.md` from `draft/` into `active/`. Not destructive, but it committed another session's in-progress move — commit explicit paths when parallel chats are live.

## Original prompt

# `__hash__ method should return an integer` in linear_light_profile_intensity_dict (parked NEEDS_FIX)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Parked 2026-04-27; still parked after the 2026-07-21 census.

`autolens_workspace_test/scripts/database/scrape/general` fails: PyAutoGalaxy
`abstract_fit.linear_light_profile_intensity_dict` raises `TypeError: __hash__ method should return
an integer` during `subplot_fit_imaging` after the search completes — a light-profile object's
`__hash__` returns a non-int. Surfaced once the `dataset_label="build"` path fix let the script
progress past `Imaging.from_fits`.

Fix the offending `__hash__` in the light-profile class (must return int), add a unit test that hashes
the profile, then remove the NEEDS_FIX marker from autolens_workspace_test/config/build/no_run.yaml.
