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
