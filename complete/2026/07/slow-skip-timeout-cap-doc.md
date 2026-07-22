## Outcome

**8 PRs merged.** The SLOW-skip convention documented a *"60s per-script timeout cap"* that has never been enforced anywhere. Real values: **300s** smoke/default (`PyAutoHands/autobuild/build_util.py:12`, `TIMEOUT_SECS = int(os.environ.get("BUILD_SCRIPT_TIMEOUT", "300"))`, matching `run_all.py:49` `DEFAULT_TIMEOUT_SECS = 300`) and **1800s** for `mode=release` (`PyAutoHeart/.github/workflows/workspace-validation.yml:308`).

- **PyAutoHands#173** (issue #172, auto-closed) — code. `slow_skip_check.py` now sources the figure from `build_util.TIMEOUT_SECS` across all three stale sites (module docstring, `_BANNER_CONFIG["slow"]["footer"]`, `_REPORT_CONFIG["slow"]["intro"]`) rather than carrying a second hardcoded copy that can drift again. `format_warning_banner` / `format_report_section` take an optional `timeout_secs`; `run_all` passes the value actually in force at both `category="slow"` call sites, so a `--timeout-secs` override is reported accurately.
- **Comment-only, one line each:** autolens_workspace#313, autolens_workspace_test#194, autogalaxy_workspace#144, autofit_workspace#105, autofit_workspace_test#62, HowToLens#43, HowToGalaxy#33.

## Why this was not a cosmetic docs fix

A 5× understatement of the cap biases every *"is this script too slow to un-skip?"* judgement in the same direction — toward parking scripts that would in fact pass. It did exactly that during the triage that spawned this task: `database/scrape/general` measured **214s**, which reads as an obvious SLOW-skip against 60s but has ~86s of *headroom* against the real 300s cap. The recommendation to re-park it was withdrawn only after checking `build_util.py` instead of trusting the header comment.

## Verification on merged main

- `python3 -m pytest tests -q` in PyAutoHands → **132 passed**.
- Banner rendered against a live workspace scan: *"These scripts are skipped because they exceed the **300s** per-script cap"*; with `timeout_secs=1800` the same text correctly reads 1800s. No unformatted `{t}` leaks; the `needs_fix` category is unaffected (its strings carry no `{t}`).
- `grep -rl "60s per-script" --include=no_run.yaml .` → **0 files**.

## Open threads deliberately not closed

1. **Five `60s` strings remain inside individual SLOW entries' own reason text** — the `database/scrape/*` markers dated 2026-04-10 (`multi_analysis`, `slam_general`, `slam_multi_one_by_one`, `slam_pix`), each saying *"exceeds 60s timeout"*. That is data, not template, and rewriting the claim without re-timing the scripts would assert something unverified. **Some may now clear the real 300s cap and be un-parkable entirely** — worth re-timing.
2. **`format_report_section` is imported at `run_all.py:164` but never called**, so the corrected report intro currently has no live call site and the slow-skip section may not be reaching `report.md` at all. Pre-existing, out of scope here.

When re-timing anything under `database/scrape/`, note that `config/build/env_vars.yaml` **unsets** `PYAUTO_TEST_MODE`, `PYAUTO_SMALL_DATASETS` and `PYAUTO_DISABLE_JAX` for that pattern — a `PYAUTO_TEST_MODE=2` measurement skips the sampler entirely and is not the harness mode.

## Provenance

Spun out of the `scrape-general-stale-needs-fix` triage (autolens_workspace_test#193) on the same day, where the wrong cap nearly caused a passing script to be re-parked.

## Original prompt

# SLOW-skip docs claim a 60s per-script timeout cap; the real cap is 300s (1800s release)

Type: bug
Target: pyautobuild
Repos:
- PyAutoHands
- autolens_workspace
- autolens_workspace_test
- autogalaxy_workspace
- autofit_workspace
- autofit_workspace_test
- HowToLens
- HowToGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Found 2026-07-22 while triaging `autolens_workspace_test` #193.

The SLOW-skip convention documents a **"60s per-script timeout cap"**. That number is wrong
and has been for a long time. The enforced values are:

- **300s** — smoke/default. `PyAutoHands/autobuild/build_util.py:12`
  `TIMEOUT_SECS = int(os.environ.get("BUILD_SCRIPT_TIMEOUT", "300"))`, matching
  `PyAutoHands/autobuild/run_all.py:49` `DEFAULT_TIMEOUT_SECS = 300`.
- **1800s** — `mode=release`. `PyAutoHeart/.github/workflows/workspace-validation.yml:308`
  sets `BUILD_SCRIPT_TIMEOUT: "1800"` for the release run.

Nowhere is 60s enforced. The stale figure appears in two kinds of place:

1. **`PyAutoHands/autobuild/slow_skip_check.py`** — the module docstring (line ~18) and
   `_REPORT_CONFIG["slow"]["intro"]` (line ~160). The latter is user-visible: it prints
   *"**{n} script(s)** are being skipped because they exceed the 60s per-script timeout cap"*
   into the slow-skip section of **every mega-run report**.
2. **Seven workspaces' `config/build/no_run.yaml`** headers, all identical at line 9:
   *"skipped because they exceed the 60s per-script timeout cap"* — `autolens_workspace`,
   `autolens_workspace_test`, `autogalaxy_workspace`, `autofit_workspace`,
   `autofit_workspace_test`, `HowToLens`, `HowToGalaxy`.

This is not cosmetic — it caused a wrong triage call. Working #193, a clean run of
`database/scrape/general` was measured at 214s; read against the documented 60s the
recommendation was to SLOW-skip it, when against the real 300s cap it has ~86s of headroom
and is correctly un-skipped (as PR #192 had already done). A 5× understatement of the cap
makes every "is this too slow?" judgement wrong in the same direction — toward parking
scripts that would in fact pass.

## Work

- Correct both sites in `slow_skip_check.py` to state the real cap, ideally sourcing the
  number from `build_util.TIMEOUT_SECS` rather than hardcoding a second copy that can drift
  again, and mention the 1800s release override.
- Correct the line-9 header comment in all seven `no_run.yaml` files.

## Follow-up worth considering (separate task)

The four `database/scrape/*` siblings (`multi_analysis`, `slam_general`,
`slam_multi_one_by_one`, `slam_pix`) are still tagged `# SLOW 2026-04-10 - exceeds 60s
timeout`. Those markers were written against the wrong cap; some may clear the real 300s
cap and be un-parkable. Worth re-timing them once this is fixed.
