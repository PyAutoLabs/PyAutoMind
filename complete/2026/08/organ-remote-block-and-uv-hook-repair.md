Two halves of the 2026-08-27 mobile-workflow pass that shipped only partly
rolled-out, because the session that shipped them could attach only PyAutoMind
and PyAutoBrain. Closed with all four organs attached.

## What shipped

**1. Heart and Hands opt into the generated remote-session block.**
`PyAutoMind/policy/remote_sessions.md` is written into each repo's `AGENTS.md`
between `<!-- repos_sync:remote:begin/end -->` by `repos_sync.py --write`, with a
drift check. Mind and Brain carried the markers; Heart and Hands carried
hand-written text that was a pass behind — it named `No module named pytest` as
the symptom of skipping the bootstrap, which the canonical text explicitly
records as a symptom that stopped appearing when the container image moved to
Python 3.12. 23 hand-written lines went in Heart, 28 in Hands. The block now
covers four organs.

The per-repo halves went deliberately: no test counts, no timings, no declared
deps. `test_the_canonical_text_carries_no_per_repo_numbers` pins that. Hands'
`.claude/session-python.txt` bullet went with them; that file carries the same
explanation in its own header and the hook reads it at run time.

**2. `repair_uv_tools` moved from the bootstrap into the hook** as leg 3b,
called right after `retool_uv_tools`. The bootstrap is what a MULTI-repo session
runs — that session registers no SessionStart hook, so it has no other door. A
SINGLE-repo session is the mirror image: the hook fires, nothing calls the
bootstrap. It got leg 2's breakage (the `/usr/local/bin/python3` wrapper every
uv tool env symlinks to) and none of the repair, so mypy, flake8, black, poetry
and pyright all died with `ModuleNotFoundError` naming themselves, in the
ordinary case.

Two paths reach that breakage, not one — leg 3 rebuilds a 3.11 tool and hands
the new env the hijacked path, and leg 2 separately breaks every pre-existing
tool env that already pointed there and that leg 3 skips. Running after leg 3
covers both, because leg 2 runs before it.

## The `set -e` gap the move opened

The hook runs `set -euo pipefail`; the bootstrap ran `set -u`. Three things
would have aborted the whole session start, in a script whose contract is that
every leg "degrades to a logged warning rather than failing the session start":
a failing command substitution in `base="$(…)"`, the same in the post-repair
`prefix="$(…)"`, and `ln -sfn` itself on an unwritable tools dir. All three are
now non-fatal. A function lifted out of a laxer script is exactly where that
kind of contract breaks silently.

The bootstrap keeps both call sites, forwarding to the hook as SUBPROCESSES
rather than sourcing it, so the hook's `set -e` never leaks back into a script
that is a bootstrap and never a gate. Its `--check` leg is unchanged.

## Tests

Four new. The section-7 tests keep driving the bootstrap seam, which is now a
forward — that is what proves the forward works. The substantive addition is
`test_a_single_repo_session_start_repairs_the_tool_env_it_just_broke`: it runs
the canonical hook the way the harness runs it, against a hijacked tool env, and
checks the env afterwards. Not a call-order assertion. Verified to fail on
exactly the bug when the flow call is removed. The first version of it SKIPPED
rather than ran — its guard checked for `"reusing"` in stderr, a proxy for the
wrong thing; replaced with one that skips only when the hook reports it could
not produce a 3.12 interpreter at all.

Suites: PyAutoMind 271, PyAutoBrain 584, PyAutoHeart 656, PyAutoHands 430.

## Findings that outlived the task

**The hook is generated into 34 repos, not four.** `write_session_hooks` walks
the whole manifest. Thirty copies are a pass behind and two (`admin_jammy`,
`euclid_assistant`) carry none at all — a state that predates this task and that
NO CI gate sees, because `firewall_gate.yml` checks out exactly the four organs
and skips absent repos. Heart sees it and says so
(`manifest drift: session-start hooks (generated) — 34 mismatch(es)`); CI cannot.
This task regenerated the four organs — the set CI gates — and left the count
where it found it. Filed as
`draft/maintenance/organs/session_hook_reaches_only_four_of_thirty_four_repos.md`.

**`repos_sync.py --write --root <task worktree>` is not a scoping mechanism —
it is the opposite.** `worktree_create` symlinks every unclaimed repo back to
the canonical checkout, and `Path.is_dir()` follows symlinks, so `--root` on a
worktree resolves 30 names to the live main workspace and regenerates hooks
there, on `main`, outside any branch, in repos other sessions may be working in.
The plan said to do this; it was caught before running and corrected on the
issue. Scope with a scratch root of symlinks to only the claimed worktree repos
and point `--root` at that; absent repos are skipped by design. All 34 canonical
checkouts were walked afterwards to confirm nothing leaked.

## Process notes

- **PyAutoBrain was not in the prompt's `Repos:` list and had to be claimed.**
  It carries a generated hook copy that goes stale the instant the canonical
  changes, and `firewall_gate.yml` checks it out.
- **Shipped under an explicit human override of Heart RED.** The RED reason was
  `release validation FAILED (stage integrate)` — PyAutoHeart run 33073386315,
  a workspace-script failure unrelated to this change. `ship_library`'s
  corrective-PR exception covers only a fix scoped to the RED reason, which this
  was not, so the override is recorded on the issue rather than left implicit.
- **A concurrent session's `prompt_sync_push` (`git add -A`) swept this task's
  prompt move and backlog draft into its own commit** (`fc8aa955`, filing #361).
  Nothing was lost; the remaining registry work was committed by explicit
  pathspec thereafter. The same session co-claimed PyAutoMind — disjoint file
  sets, so the two ran in parallel worktrees rather than serialising.

Issue: PyAutoMind#360. PRs: PyAutoMind#363, PyAutoBrain#308, PyAutoHeart#190,
PyAutoHands#270.

## Original prompt

# Two organs are missing this session's fixes, and the hook still ships the uv bug

Type: maintenance
Target: organs
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

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
