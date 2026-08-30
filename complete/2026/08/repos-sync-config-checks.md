## repos-sync-config-checks (Heart version_skew and Hands workspaces.yaml identity checked; the config stamper deferred, demand-gated)
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/370
- completed: 2026-08-29
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/373
- prompt: draft/feature/pyautomind/repos-sync-config-stamper.md (bundle `mind-workflow`; descoped at plan time)
- summary: The prompt asked `repos_sync.py --write` to stamp Heart's `version_skew:`/`smoke:` and Hands' `workspaces.yaml` from the body map. Measured before issuing: those Heart blocks changed ~3 times in six weeks, `workspaces.yaml` twice ever, zero adopters, and the design doc itself files the stamper as "demand-gated, later". The stamper is therefore DEFERRED and what shipped is the cheaper gap it would have closed as a side effect: Heart's `version_skew:` block was entirely unchecked by `--check`, and `PyAutoHands/autohands/config/workspaces.yaml` claimed in its header that the check flags drift while no leg read it. `check_heart` now validates `version_skew:` (keys and `library` are manifest repos; `package` equals the library's manifest `package:`; a library with no manifest package is a problem; absent block tolerated). New leg `PyAutoHands/autohands/config/workspaces.yaml` checks `run_all[*].repo`, `libraries[*].name` + `package`, `slow_skip_default[*]`; absent file skipped; `--only`-selectable.
- validation: 15 tests in `tests/test_repos_sync_config_checks.py` — the first ever for `check_heart` — written to fail on the unmodified script (12 failed / 3 passed), 15 pass after; suite 296 passed; both legs OK on the real Heart/Hands files.

## Decision: stamper deferred
- Revisit trigger: an adopter, or the hand-mirrored fields below drifting more than the membership legs catch. The remaining hand-mirrored surfaces a stamper would take over: `smoke.workspaces[*].chain`, `run_all` short keys and `report` dirs, the `libraries:` release-matrix order (which lists 5 of the 7 packaged repos — no PyAutoReduce/PyAutoCTI — a policy choice that membership checking is indifferent to). Design shape agreed at plan time if it is ever built: policy stays in the organ files as plain name lists, identity comes from the manifest, the stamper does the join through the existing `replace_block`/`extract_block`/`write_block` triad with a `#`-comment YAML marker family; a workspace→library relation would be a manifest `library:` key (identity, not policy).
- The comments/docstrings firewall exemption stays REJECTED (`complete/2026/08/autohands-firewall-allowlist.md`).

## Traps and findings
- A check leg's absent-file skip must use the same soft idiom as its neighbours (`check_pre_build`'s `if not path.exists(): return []`), or a partial checkout goes red on nothing.
- A test that proves a check leg is *registered* should drive the CLI (`--only no-such-check` lists the choices) rather than grep the source: the `checks` dict entry is line-wrapped and a literal source match broke on the first attempt.
- On this branch the full `--check` showed 2 `session-start hooks` mismatches for `euclid_assistant`: the untracked `.claude/` residue that had masked its hookless state was removed under #369, and this branch (cut from `origin/main` independently) lacks #372's `session_hook: false` exclusion. Expected, and it clears when #372 merges.

## Original prompt

# Teach repos_sync --write to stamp organ config surfaces

Type: feature
Target: pyautomind
Themes:
- mind-workflow
Difficulty: hard
Autonomy: supervised
Priority: low
Filed: 2026-08-17 (backfilled from git)
Issued: 2026-08-29

The design's own endgame for tenant-firewall drift, specified in
`docs/pyautobrain/pyautoscientist_generalisation_assessment.md` §8-4 and
restated in `docs/pyautobrain/pyautoscientist_phase3_research.md` ("Demand-
gated, later"): teach `scripts/repos_sync.py --write` to *stamp* the organ
config surfaces from the body map + per-organ policy fields, the way it
already stamps doc blocks. Quoting the assessment: "That turns 'edit five
mirrors' into 'edit one file, regenerate' … **This is the only real
engineering in the whole plan**, and it removes his own hand-mirroring burden,
so it pays for itself even with zero adopters."

Filed 2026-08-17 from the tenant-firewall drift-clear
(PyAutoMind#198), whose research pass found this remedy named in the design
but never filed anywhere in Mind. Context there: the allowlist grew 72→109
files in five weeks of reactive patches; #198's PR-time CI gates stop drift
*landing*, this task removes the hand-maintained mirrors that *generate* it.

## Scope sketch (to be refined at start_dev)

- Candidate surfaces to stamp: Heart `config/repos.yaml` blocks
  (`version_skew:`, the `smoke:` block #198 introduces), Hands
  `autohands/config/workspaces.yaml`, and any organ constant table still in
  the allowlist that is identity-derivable.
- Needs per-organ policy fields the body map deliberately does not carry
  (dependency chains, package import names, short keys) — decide where policy
  lives (per-organ policy YAML consumed by the stamper vs schema extension),
  honouring the body map's "identity only" doctrine.
- The stamper must be drift-checked itself (the check legs already exist —
  stamping makes them tautologies for stamped blocks, which is the point).

## Not in scope

- The firewall check semantics (unchanged).
- The comments/docstrings exemption — CONSIDERED AND REJECTED, recorded in
  `complete/2026/08/autohands-firewall-allowlist.md`; do not re-propose.
