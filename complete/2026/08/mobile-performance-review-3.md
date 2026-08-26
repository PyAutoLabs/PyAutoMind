- completed: 2026-08-26
- issue: none — the third in a series that began as an environment review in a
  mobile session rather than a filed prompt, so it carries no `active/` entry to
  fold. Recorded because the work shipped.
- prs:
  - PyAutoMind — hook, bootstrap, tests
  - PyAutoBrain — regenerated hook copy
  - PyAutoHeart — regenerated hook copy, remote-session block
  - PyAutoHands — regenerated hook copy, declared session deps, drift test,
    remote-session block
- classification-note: four repos, no gate order. `firewall_gate.yml` is
  path-filtered to `scripts/repos_sync.py`, which nothing here touches.
- classification: bug (organism infrastructure; all four organ repos)
- summary: |
    A third pass over the two mobile-performance reviews of the same day. The
    named follow-up from pass 2 — PyAutoHeart and PyAutoHands carrying stale
    generated hooks — turned out not to be dormant drift: those copies carry the
    PRE-pass-2 logic, so the bug pass 2 fixed is still live in half the organs.
    Underneath it, four more defects, every one of them the same shape the
    series keeps finding: **a mechanism that exists, reports success, and is not
    reachable by the thing it was built for.**

## What was still true

1. **Two of four organs carry the bug pass 2 fixed.** Verified by content, not
   by checksum. `PyAutoHeart` and `PyAutoHands` hold the pre-pass-2
   `point_system_default`: `ln -sfn "$(readlink -f "$VENV/bin/python")"` — a
   symlink (which CPython resolves before reading `pyvenv.cfg`, losing the venv)
   pointed at the base interpreter (which loses it again by the other route).
   Their `BASE_DEPS` has no `pytest-xdist`, so a session scoped to those two
   organs also runs its suites on one of four cores.

   In this session it did not bite, and the reason is luck: the hooks fan out in
   alphabetical order, Mind's current copy ran last, and the stale copies'
   `is_py312` guard made them skip a write against a destination that was
   already 3.12. A session holding Heart and Hands *without* Mind gets the
   pre-pass-2 behaviour end to end.

   The lesson the previous two records both logged — **a drift check over N
   repos is only as strong as the number of them your session can see** — has
   now cost a full cycle twice. All four organs were attached this time, so
   `repos_sync.py --write` regenerated all four.

2. **The per-repo dependency mechanism had zero users.** The hook reads
   `.claude/session-python.txt` for deps beyond `pytest`/`PyYAML`/`pytest-xdist`.
   No repo had ever written one. PyAutoHands needs two — its own `tests.yml`
   names them — and without them a fresh remote session runs its suite **14
   failed / 383 passed**, on `ModuleNotFoundError: PIL` and
   `FileNotFoundError: ipynb-py-convert`, in a repo whose CI is green on the
   same commit. A missing dependency reads exactly like a broken test.

3. **Installing the deps fixed nine of the fourteen.** The other five kept
   failing on `FileNotFoundError: ipynb-py-convert` with the package installed —
   the binary sitting in `$VENV/bin`, unreachable, because the venv reaches PATH
   only through the env file that Claude Code writes around a hook a multi-repo
   session never registers. `python3` and `pytest` each have their own shim and
   survive that; nothing else in the venv did. The hook now shims every console
   script the venv owns, under the same claim policy as `pytest`: a name that is
   unresolvable or resolves inside uv's shim dir is ours; a name the image owns
   elsewhere is not.

4. **The bootstrap installed one repo's deps.** `session_bootstrap.sh` ran the
   canonical hook, which derives its repo from its own path — PyAutoMind. So the
   per-repo mechanism, in the multi-repo session that is the only reason the
   bootstrap exists, could only ever serve PyAutoMind. It now runs every sibling
   repo's own copy afterwards: idempotent, ~0.2s each, and it does not depend on
   the workspace-root fan-out having been installed.

5. **`--check` could not read the hook's own shim.** It resolved each tool's
   shebang to find the interpreter — but the shims are `#!/bin/sh` + `exec`
   wrappers, deliberately, because pass 2 proved a symlink loses the venv. So
   the probe got `/bin/sh`, gave up with `interpreter undetermined`, and
   **skipped the import check** — the check pass 2 added precisely because a
   3.12 pytest that cannot import PyYAML fails collection in a way that reads
   like broken source. The two halves of one pass's fix cancelled each other,
   and the session reported healthy either way. It now follows the exec target,
   and names a compiled tool (`ruff`) as a native binary instead of leaving a
   blank that reads like a fault.

| Command | Before | After |
|---|---|---|
| PyAutoHands `pytest -q` | 14 failed, 383 passed | 399 passed, 9 skipped |
| PyAutoHands, four cores | 27s | 13s |
| PyAutoHeart, four cores | 7.6s | 2.7s |
| `--check` on `pytest` | `interpreter undetermined` | `3.12 OK` (import probe runs) |

## The one that cannot be fixed in code

**The workspace-root fan-out cannot help a fresh container, which is the normal
mobile case.** Pass 2 made the seed installable from any session; it is still
written *into a container*, at `/home/user/.claude/settings.json`, and the
workspace root is not a repo — so nothing checks it out and every first session
in a fresh container is one the fan-out has never run in. This session proved
it: `~/.claude/session-env/<session-id>/` was empty and `python3` was 3.11.15,
with the fix from pass 2 merged and present in the checkout.

The seed still earns its place — a second session in the same container gets it
free — but the mechanism that actually survives a container boundary is the
documented instruction to knock on the door in the first turn, because AGENTS.md
is repo content and is loaded. That block existed in PyAutoMind and PyAutoBrain
only; a session scoped to Heart and Hands had no way to learn the door exists.
It is now in all four.

Making that block *generated* by `repos_sync.py`, like the organism-map and
never-rewrite-history blocks, is the obvious next step and was deliberately not
taken here: the per-repo halves differ (each names its own test count and its
own declared deps), and the change would have put this work behind the
Brain-before-Mind gate order for no gain this pass could measure.

## Key traps

- **The stale copy was not inert.** "Two repos carry an old generated file" reads
  like cosmetic drift, and it was the pass-2 bug still shipping. Regenerating a
  copy is not a formality when the copy is executable.

- **A markdown insertion landed inside a generated block.** The remote-session
  section was first written immediately before `## Never rewrite history` — which
  is inside `<!-- repos_sync:history:begin -->`, so the next `--write` would have
  eaten it. Caught by looking at the markers rather than at the heading. The same
  trap as pass 1's dashboard conflict: in this repo, a heading is not evidence
  that the text around it is hand-owned.

- **Nine of fourteen is the dangerous number.** Installing the missing packages
  turned most of the failures green, which is exactly the point at which a fix
  looks finished. The five survivors named the same binary as before and had a
  completely different cause.

## Validation

240 PyAutoMind, 554 PyAutoBrain, 641 PyAutoHeart, 399 PyAutoHands (+9 skipped) —
all green. `ruff` clean, `bash -n` clean, `lifecycle.py check` and
`repos_sync.py --check` clean with all four organs attached. 10 new tests (8 in
PyAutoMind, 2 in PyAutoHands); every one was confirmed to FAIL against the
pre-fix tree before being trusted — the PyAutoMind eight by stashing the two
changed scripts and re-running, the PyAutoHands two by removing the declared
deps file.

Timings for the record: bootstrap 18.8s cold (unshallowing four clones, building
the venv, rebuilding seven uv tools), 2.3s warm with the new fan-out, 0.68s warm
without it.

## Follow-up

- **Generate the remote-session block** from `repos_sync.py` so a fifth organ
  cannot be born without it (see above for why it was not done here).
- `draft/feature/pyautobrain/board_without_gh.md` — unchanged and still open;
  `gh` is absent in this session too.
- The durable fix for the fresh-container case is environment configuration on
  claude.ai (a setup command that runs at container start), not repo code — the
  same class as pass 1's network-allowlist finding, and recorded here for the
  same reason: so the next pass does not spend a cycle looking for it in code.
