# Deduplicate repos_sync.py's check/write pairs

Type: refactor
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- mind-workflow
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
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
