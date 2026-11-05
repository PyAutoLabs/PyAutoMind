- summary: shipped in PyAutoMind#539 (commit dc471e1d6), narrowed scope: option (a) of the 2026-11-05 re-size, chosen by the human. A single `OptInBlock` dataclass (`noun`, `begin`, `end`, `organs_only`) drives both the drift check and `--write` for the three opt-in AGENTS.md blocks: map, history and remote. `check_map_blocks` / `check_history_blocks` / `check_remote_blocks` stay as thin wrappers. The deliverable, filing and standards blocks, the hooks and the mode-gated writers stay explicit, because their contracts differ.
- witness: byte-identical before/after for `--check` on the live workspace, `--write` on a scratch copy of the workspace, the follow-up `--check`, and the files `--write` produced. New `tests/test_repos_sync_opt_in_blocks.py` pins the shared contract per block. Mind suite 725 passed; 1 failure that also fails without this change (`test_the_hook_survives_an_unwritable_tools_dir`, root in the container).
- not done: the full one-declaration-per-surface collapse (option b). Re-file it only if a new generated surface makes it worth it.

## Original prompt

# Deduplicate repos_sync.py's check/write pairs

Type: refactor
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- mind-workflow
- hygiene
Difficulty: large
Autonomy: supervised
Priority: low
Status: formalised
Consequence: notify
Witness: `repos_sync.py` has one declaration per generated surface driving both `check` and `--write`; every CLI flag's output is byte-identical before and after (captured in a test); `tests/test_repos_sync_hygiene_coverage.py` and the firewall_gate.yml legs pass.
Review-minutes: 0
Unattended: never
Filed: 2026-08-19 (backfilled from git)

Found by the 2026-08-19 readability-pass census (#248). Behaviour-preserving
refactor of @PyAutoMind/scripts/repos_sync.py (940 lines, no dead functions):

- Eleven `check_*` functions share the same shape — walk repos, compare a
  generated block against the on-disk block, return `list[str]` of problems.
- The `--write` leg has 4 near-identical `write_block(...)` call sites.

Collapse each check/write pair into one declaration per generated surface —
e.g. a small `Check` dataclass (name, target file, block renderer) driving both
the lazy `checks` dict in `main()` and the `--write` leg, so adding a generated
surface means one new declaration instead of a new function plus a new call
site. All existing CLI flags and outputs stay byte-identical;
`tests/test_repos_sync_hygiene_coverage.py` and the firewall_gate.yml legs are
the safety net.

## Re-sized 2026-11-05 (queue check-in) — needs a human design call before start

The premise has moved: `scripts/repos_sync.py` is now 3204 lines (was 940), with
23 check legs. The `--write` leg is no longer a set of uniform `write_block`
pairs: it carries mode gates (`codex_only_write`, `smoke_only_write`,
`standards_only_write`, the held smoke rollout), self-installing marker
insertion (`insert_deliverable_markers`, `write_filing_blocks`) whose ordering
matters, and standards pre-validation that must run before any writer. A
one-`Check`-dataclass collapse therefore has to model write ordering and
mode-exclusive writers — a design fork, not a mechanical dedup.

Options for the human: (a) narrow to the uniform subset only — the five
`AGENTS.md` marker blocks (map/history/remote/deliverable/filing) plus public
tables — as one declaration table, leaving special writers explicit; (b) keep
the full refactor, re-sized large, phased; (c) park it. Recommendation: (a).
