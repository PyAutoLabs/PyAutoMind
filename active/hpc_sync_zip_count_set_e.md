# hpc/sync pull exits 1 after the first extracted archive: `(( zip_count++ ))` under `set -e`

Type: bug
Target: autolens_assistant
Repos:
- autolens_assistant
- autogalaxy_assistant
- autofit_assistant
Themes:
- hpc
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: A new offline test in `autoassistant/tests/test_hpc_sync.py` runs `hpc/sync pull` over two result roots holding three unextracted zips, and `hpc/sync pull-full`, and asserts exit 0, every archive extracted and the "extracted N archive(s)" line; it fails on current `main` and passes on the branch.
Review-minutes: 3
Filed: 2026-11-25
Updated: 2026-11-25
Issued: 2026-11-25

## Request (verbatim)

Bug in the autolens_assistant HPC sync script: `/home/jammy/Code/PyAutoLabs/lens/autolens_assistant/hpc/sync` runs under `set -euo pipefail` (line 56) and, in `pull()` (about line 355) and in `pull-full` (about line 391), does

    unzip -q -o "$zipfile" -d "$target" && (( zip_count++ ))

`(( zip_count++ ))` evaluates to 0 on the first increment (post-increment from 0), so it returns exit status 1 and `set -e` kills the script right after the first archive is extracted. Symptoms seen on 2026-11-25 in the science project `/mnt/c/Users/Jammy/Workspace/Science/development/stars_dm_slope` (which carries a copy of this script as `hpc/sync`): `hpc/sync pull results` transfers everything with rsync, extracts exactly one zip, then exits 1 without printing "extracted N archive(s)" or "Done." Each rerun extracts one more zip and exits 1 again. With more than one result root in PULL_DIRS (e.g. `output results`), the failure in the first root stops later roots from being pulled at all.

Fix: make the increment safe under `set -e`, e.g. `zip_count=$((zip_count + 1))` (or `(( ++zip_count ))` / `|| true`), in both places, and check the script for any other `(( var++ ))` used as a statement. Add a small regression test if the repo has a test harness for hpc/sync. This is PyAutoLabs library/assistant code: follow `/home/jammy/Code/PyAutoLabs/AGENTS.md` and `/home/jammy/SAFETY.md` (plan first, work through the dev workflow / start_dev, in a worktree, no direct edits on a shared checkout, human merges). Do not edit the project copy in stars_dm_slope; science projects pick up the fixed script from the assistant. Project copies of the script in other science projects under `/mnt/c/Users/Jammy/Workspace/Science/{active,development}/*/hpc/sync` may carry the same line; list which do, but do not change them without the human's OK.

## Findings at filing (2026-11-25)

- `autolens_assistant/hpc/sync` lines 355 (`pull`) and 391 (`pull_full`) carry the line. No other
  `(( var++ ))` / `(( var-- ))` statement exists in the script; the remaining `(( … ))` uses are
  `if` conditions or already guarded with `||`.
- The same two lines are in `autogalaxy_assistant/hpc/sync` and `autofit_assistant/hpc/sync`
  (lines 260 and 296 in each). Neither repo has a `test_hpc_sync.py`.
- `autolens_profiling`, `autolens_inference`, `autofit_profiling` and `autofit_inference` already
  fixed it (autolens_profiling `0dcc528f`, "hpc/sync: branch explicitly on unzip instead of
  `&& (( n++ ))`"): `if unzip …; then zip_count=$(( zip_count + 1 )); else <report>; fi`. Use the
  same form here, so a failed unzip is reported and does not abort the pull either.
- `autolens_assistant/autoassistant/tests/test_hpc_sync.py` is the harness (fake `ssh`/`rsync` on
  `PATH`); it has no test that reaches the unzip loop.
- Science project copies carrying the line (not to be edited under this task):
  `development/{analytic_gaussian, dm_sightlines, ep_gnfw_slope, ep_toy_gaussian,
  erc_angular_structure, ic50_workspace, slope_hierarchy_scale, stars_dm_slope}`.
  Older copies without an unzip step, unaffected: `active/euclid_detailed`,
  `active/sdssj0946_subhalo`, `development/adapt_snr_cap`.
