# Nerves board flags library config keys no library code reads

PyAutoNerves#175 → `eb27da24` (closing PyAutoNerves#174), merged 2026-09-27 with `--merge`.
Member of bundle `cockpit-followups` (with gut-void-sibling-reach, start-dev-heart-gate);
epic organ-cockpit. Fable-planned, Opus-executed; Heart YELLOW acked by the human 2026-09-27.

- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/174
- completed: 2026-09-27
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/175
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/175

## What shipped
- `scripts/board.py`: a `conf.instance` lookup scan classifies every library config key as
  used / section-read / unused; unused keys render as info items on the Nerves board.
- `nerves_board.yml`, tests (206 passed), README and AGENTS.md updated; board re-dispatched
  after merge.
- Follow-up filed: workspace config cleanup (79 orphan workspace keys across 14 files, the
  `fit_imaging {}:` typo, and a human-review-gated library-side unused-key list).

## Original prompt

# Organ cockpit: Nerves board flags config keys not in use anymore

Type: feature
Target: PyAutoNerves
Repos:
- PyAutoNerves
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: the board's index lists at least one unused key with its library and file link, and a deliberately referenced key in the fixture is not listed; the scan's false-positive rate on PyAutoFit general.yaml is reviewed by the human on the PR.
Review-minutes: 3
Unattended: ready
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/174
Filed: 2026-09-26
Epic: organ-cockpit

The human, on shipping the Nerves board (PyAutoNerves#172, 2026-09-26): 'build into the board a flag that a config is drifted or not in use anymore?'. The drift flag exists (workspace keys no library defines → orphan rows + yellow feed items). This prompt adds the other direction: library YAML keys that no library code reads.

1. In PyAutoNerves scripts/board.py collect: scan each library's Python source (the sparse clone must therefore also fetch the package's .py files, or a second sparse pattern) for config lookups — conf.instance["a"]["b"]..., conf.instance.dict[...], prior_config / visualize_config helpers and the autoconf-era get_config patterns — and build the set of key paths the code reads, including partial reads where the code indexes a whole section. Mark each library YAML key path as used / possibly-used (section read wholesale) / unused (never referenced). Prior files are exempt (looked up dynamically by class name).
2. Render: an 'unused' chip on the key, a per-file count, an index section 'possibly unused config keys' grouped by library with the GitHub link, and a state.json info item per library summarising the count (never yellow — a false positive must not colour the feed until the scan is trusted).
3. Tests: hermetic fake library with three lookup styles and one unreferenced key.

Out of scope: deleting anything; workspace files (covered by the drift flag).

Witness: the board's index lists at least one unused key with its library and file link, and a deliberately referenced key in the fixture is not listed; the scan's false-positive rate on PyAutoFit general.yaml is reviewed by the human on the PR.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
