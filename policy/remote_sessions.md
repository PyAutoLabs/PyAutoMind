## Remote sessions (Claude Code on web and mobile)

Three facts, all measured in a web/mobile container, where this file is loaded
and little else is. They ride in every organ because a session may hold any
subset of them — and the session that needs this most is the one holding
several, which is exactly the session no hook fires in.

- **Bootstrap in the first turn, unconditionally** — before the first test
  command, not as a remedy once something looks wrong:

  ```
  bash PyAutoMind/scripts/session_bootstrap.sh          # ~10s cold, ~1s warm
  bash PyAutoMind/scripts/session_bootstrap.sh --check  # report only
  ```

  A session holding several organs registers no SessionStart hook — Claude Code
  reads project hooks from the project directory, which in that layout is the
  repos' *parent*, not a repo — so nothing has set this session up. It was once
  phrased as a remedy keyed to `No module named pytest` or collection
  `ImportError`s naming `yaml`; that symptom stopped appearing when the
  container image moved to Python 3.12, while the environment is still wrong in
  ways that read like a bad command rather than a stale session (`pytest -n
  auto` → `unrecognized arguments: -n`). The bootstrap also **unshallows the
  clones**: a remote session clones shallow, and `git merge-base --is-ancestor`
  then answers "not an ancestor" for a commit whose ancestry is merely absent —
  the answer the ship and close-out procedures act on when proving a branch
  merged.

- **Then run the suite in parallel.** 4 cores, subprocess-heavy suites, no
  single slow test: about 3.5x. `python3 -m pytest -q -n auto`, with
  `pytest-xdist` supplied by the bootstrap above.

- **There is no `gh`, and installing one does not help.** A remote session
  reaches GitHub through the `mcp__github__*` tools, already scoped to the
  session's repos. `gh` installs in two seconds and is a trap: it authenticates,
  then 403s every repo-scoped call, because the egress proxy serves neither the
  REST repo paths nor GraphQL beyond a pinned set of PR-review operations — a
  binary that looks healthy and fails everything that matters. It also defeats
  the surface probe, which keys off `gh auth status`. Read
  `PyAutoBrain/skills/GITHUB_ACCESS.md` at the top of any run that touches
  GitHub; it maps each `gh` operation onto its MCP tool. Spell that path from
  the workspace root, as written: a multi-organ session is cwd'd at the repos'
  *parent*, so a bare `skills/…` reads as a missing file rather than a missing
  repo prefix.
