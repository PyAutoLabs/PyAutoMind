# Two organs are missing this session's fixes, and the hook still ships the uv bug

Type: maintenance
Target: organs
Repos:
- PyAutoMind
- PyAutoHeart
- PyAutoHands
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27

The 2026-08-27 mobile-workflow pass shipped two things that are, by
construction, only half-rolled-out. Both need a session with **all four organs
attached** — this one could not attach PyAutoHeart or PyAutoHands (`add_repo`
was refused), which is the same "a drift check is only as strong as the number
of repos your session can see" the last three passes each paid for once.

## 1. Opt Heart and Hands into the generated remote-session block

`PyAutoMind/policy/remote_sessions.md` is now the single source, written into
each repo's `AGENTS.md` between `<!-- repos_sync:remote:begin/end -->` by
`repos_sync.py --write`, with a drift check. Mind and Brain carry the markers;
Heart and Hands still carry their own hand-written text, which is already a pass
behind (it says "bootstrap if pytest misbehaves", a trigger that no longer
fires).

Add the markers to both, run `--write`, and confirm `--check` reports the block
for four repos rather than two. No gate order: `firewall_gate.yml` is
path-filtered to `scripts/repos_sync.py`, which this does not touch.

## 2. Promote the uv-tool repair from the bootstrap into the hook

`scripts/session_bootstrap.sh` gained `repair_uv_tools`: uv creates each tool
env's `bin/python` as a symlink to `/usr/local/bin/python3`, the hook replaces
that path with a wrapper that `exec`s the session venv, and the exec replaces
argv — so every tool env resolves `sys.prefix` to the venv and mypy, flake8,
black, poetry and pyright all die with `ModuleNotFoundError` naming themselves.
Measured 2026-08-27; `--check` called them all `3.12 OK` until the same commit
taught it to run each tool.

The fix belongs in `policy/session_start_hook.sh`, beside `retool_uv_tools`
which creates the condition — the hook is what a **single-repo** session runs,
and that session never calls the bootstrap. It was left in `scripts/` because
the hook is generated into all four organs and two of them could not be
attached: changing it here would have made `firewall_gate.yml` red on repos this
session could not regenerate.

So: move the function into the hook, regenerate all four copies, keep the
bootstrap's call (it is idempotent, and the bootstrap runs the hook anyway), and
keep the `--check` leg where it is.

## Done when

- `repos_sync.py --check` is clean with all four organs checked out, and the
  remote-session block leg names four repos.
- A fresh remote session that runs only the SessionStart hook — no bootstrap
  call — has a working `mypy`, `flake8` and `black`.
- The existing tests still pass, plus a hook-level version of
  `test_a_tool_env_pointed_at_the_session_venv_is_repaired`.
