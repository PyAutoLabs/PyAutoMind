## verify-install-release-checks
- issue: https://github.com/Jammy2211/admin_jammy/issues/11
- completed: 2026-04-29
- tooling-pr: https://github.com/Jammy2211/admin_jammy/pull/12
- repos: admin_jammy
- notes: Split `/verify_install` into a standalone `verify_install.sh` (source of truth, aliased into ~/.bashrc) and a thin `verify_install.md` skill wrapper. Replaced the single pip+start_here.py probe with five independent checks A–E in throwaway envs: A=pip+welcome, B=3.9/3.11 rejection, C=conda flow, D=[optional] extra, E=yanked-pin (autolens==2025.10.6.1). Per-check PASS/FAIL/SKIP table; missing interpreter/conda → SKIP, never FAIL, so the suite is portable. CLI: `verify_install [A|B|C|D|E|all] [--version <v>] [--keep] [--help]`. Lightweight workflow (no worktree) since admin_jammy carries unrelated dirty state and the change is pure tooling — no test suite. Smoke-tested locally: --help, bad-arg paths exit 2, `verify_install B` on host without 3.9/3.11 → SKIP/SKIP/PASS. Real install paths (A/C/D/E) intentionally not exercised in this session — left as unchecked items in PR test plan; user runs them post-release.
