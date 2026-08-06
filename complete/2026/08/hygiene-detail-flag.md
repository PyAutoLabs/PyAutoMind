Added a `--detail` flag to the hygiene conductor's `config` prescan so its
findings can actually be routed to `/refactor`.

## The problem

`agents/conductors/hygiene/_hygiene_config.py` emitted only a `count|summary`
line and its `main()` accepted only `--root`. The mode therefore reported *how
many* library config keys were absent downstream (and a per-repo tally) but
never *which*. The hygiene skill instructs the operator to route config findings
onward for repair — recovering the actual key paths meant importing the module
and re-running `diff()` internals by hand.

## What shipped

**Two views over one traversal.** Each of the two signals was split into a
detail core plus the existing count wrapper:

- `diff_detail()` → `(workspace repo, config file, sorted missing key paths)`
- `orphan_detail()` → `(repo, sorted orphan relpaths)`
- `diff()` / `orphan_files()` became the count view over those same walks, via a
  shared `_summarise()` / `_counts_by_repo()`.

Because the count is now *derived from* the listing rather than computed
alongside it, a tally can no longer disagree with what it is a tally of.

`render_detail()` groups each drifted key path under the workspace config file
missing it, and each orphan file under its repo. `--detail` prints the summary
sentence without the machine `count|` prefix (it is the human/routing view),
then the groups.

**The default is byte-identical.** `prescan_config()` in `hygiene.sh` parses
`${out%%|*}`, so the conductor's default summary table and the `--json` row are
untouched — locked by a test that fails if a line, prefix, or trailing newline
is ever added.

**One addition beyond the filed prompt:** the `hygiene config` single-mode human
branch in `hygiene.sh` now renders the detail block, mirroring the existing
`refs` / `optdeps` / `extras` branches. Without it the flag would be reachable
only by calling the helper directly — the same "hands over nothing routable"
complaint one level up. The usage line was corrected too: the mode has always
folded in the orphan signal, but only named the key drift.

## API constraint that shaped the design

`diff()` and `orphan_files()` keep their exact `(total, ["repo:N", ...])`
returns. Three existing tests in `tests/test_hygiene_conductor.py`
(`test_config_helper_recursive_key_diff`,
`test_orphan_files_flags_unmirrored_and_suppresses_owned`,
`test_orphan_files_skips_non_mirror_repos`) call them directly, so the detail
cores had to go *underneath* them rather than replace them.

## Verification

`--detail` against the live checkouts resolved the 19 drifted keys to exactly
the expected set — this was the acceptance criterion, checked rather than
assumed:

- autofit_workspace `general.yaml` — `output.search_internal`,
  `test.check_likelihood_function`; `logging.yaml` — `total_files_open`
- autogalaxy_workspace `general.yaml` — `test.exception_override`; plus 14
  `notation.yaml` labels (multipoles, virial mass/overdensity, GRF and
  `InputPotential` superscripts)
- autolens_workspace `general.yaml` — `output.fit_dill`

Full PyAutoBrain suite: 236 passed (re-run on merged `main`). Seven new contract
tests cover the key grouping, the orphan grouping (with `ORPHAN_OWNERS`
suppression intact), the unchanged default line, the clean-tree case, the
`hygiene config` surface, and the unchanged `--json` row. Orphan count is 0 in
the current checkouts, so that path is covered by fixtures, not live data.

## PRs

- PyAutoBrain#204 — MERGED `abacdd3` (head `c05c9e4`, Brain Tests green)
- PyAutoMind#138 — MERGED `4d19947` (Mind state; Lifecycle Drift green)
- Issue PyAutoBrain#203 — closed by the merge

## Traps and findings

- **`active.md` conflicts are the norm, not an incident.** PyAutoMind#138 went
  `dirty` within minutes of opening: `main` moved (#137) and both sides
  prepended a section under `# Active Tasks`. Resolution is always additive —
  keep both — and worth verifying with `git diff origin/main -- active.md`
  showing *only* your own section added, rather than trusting the merge.
- **`prompt_sync_push` pushes `main`, not your branch.** On a harness-mandated
  branch it fails with `HTTP 403` / non-fast-forward after committing. The
  commit lands fine; push the branch explicitly afterwards.
- **Local Mind `main` in this container had ~50 commits not on `origin/main`**,
  whose content had in fact landed upstream via PRs under different SHAs —
  `origin/main` was strictly richer in files. Left untouched rather than reset,
  since the local branch still held 335 lines `origin/main` lacked. Worth a
  deliberate reconciliation pass; do not assume local `main` is authoritative.
- **`_hygiene_config.py::_suppressed()` is dead code** — it predates this change
  (`orphan_files` always inlined `r.split("/")[0] in owners`). Deliberately left
  alone to keep the diff scoped; a candidate for a later tidy.
- Cloud session (`web-github`): no worktree, no `gh` CLI — issue, PRs and merges
  went through the GitHub MCP surface; work happened in the canonical
  `/home/user/PyAutoBrain` checkout on the mandated branch.

## Original prompt

# Add a --detail flag to the hygiene config scan so

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Add a --detail flag to the hygiene config scan so its findings are routable. The config scan in PyAutoBrain agents/conductors/hygiene/_hygiene_config.py emits only a 'count|summary' line naming how many library config keys are absent downstream and a per-target tally. Its main() accepts only --root and prints that one line, so there is no way to see which key paths actually drifted. The hygiene skill tells the operator to route config findings onward for repair, but the mode hands over nothing routable: recovering the key paths currently means importing the module and re-running its diff() internals by hand. Add a --detail flag that prints each drifted key path grouped by the config file it is missing from, keeping the existing single-line output as the default so the conductor's summary table is unchanged. Extend the same treatment to the orphan_files signal the module already computes.

<!-- formalised by the Intake (Conception) Agent on 2026-08-05 from user-intake -->
