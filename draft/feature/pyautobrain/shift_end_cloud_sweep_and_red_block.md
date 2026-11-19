# M3.7e Shift-end cloud sweep: dispatch, read the verdict, block unattended merges on red

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) an orchestrator test: a shift that merged at least one library or workspace PR dispatches `workspace-smoke.yml` exactly once at its close, and a shift that merged none dispatches nothing; (2) the digest has the line "workspaces verified through `<sha>`" per library from the latest green sweep, or "sweep running: <url>" when the shift's own sweep has not finished; (3) an orchestrator test: when the latest completed sweep is red, no close-out starts for a PR on a repo in the failing workspaces' install chains, the PR is refused for `/prm` with the reason "workspace sweep red: <run url>", and PRs on unaffected repos still close out; (4) the same red run files one bug draft through the one Mind writer, naming the failing scripts and every PR merged on the affected repos between the last green sweep's SHAs and the red one's; a second tick on the same red run files nothing more; (5) nothing in the watcher or a close-out reverts a commit or dispatches a bisect run; (6) `AUTONOMY.md` records ruling S4 and the watcher network-surface amendment; (7) the Brain suite passes
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat, on the cloud verification lane and its rulings: "approved, all rulings yes".

## Why

M3.7b removes the full smoke before an unattended merge. The full sweep then has to run after the merge, without the human asking, and a red result has to stop further unattended merges until someone has looked. The same sweep covers the human's `/prm` merges, which today get no workspace run until Monday.

## Rulings (human, 2026-11-19)

- **S4.** The watcher may dispatch `workspace-smoke.yml` at shift close (`gh workflow run`, one call) and read that workflow's latest runs each tick (`gh run list` / `gh run view`). This is an amendment to "The watcher's network surface — 2026-11-03".
- **Red handling.** A red sweep blocks unattended merges on the affected repos, in this shift and the next, until a later sweep is green or the human clears it. It files one bug draft naming the failing scripts and the suspect PRs. Reverts are draft PRs opened for the human; nothing is reverted unattended.
- **Bisection** is dispatched from a chat session with `commit_shas`, not by the watcher.

## Shape

- `_orchestrator.py`: the dispatch at close (after the last merge, before the digest); the per-tick read of the latest completed sweep; the block in `_start_closeouts`, using Heart `config/repos.yaml` `smoke:` chains to map failing workspaces to repos.
- `_digest.py`: the verified-through line and the blocked PRs.
- `_mind_writer.py`: the bug draft op, idempotent on the run id.
- How the human clears a block: a `/clear-sweep` comment on the shift issue, or a green sweep. State which in the plan and get the human's word if it needs a new steer command.
- `AUTONOMY.md`: S4 and the red-handling rule in "Shift speed — 2026-11-19"; the network-surface section gains the two calls.
- The sweep finishes about 30 minutes after the shift closes. The digest is not held for it; the next shift's first tick, or the nightly run, reads the result.

## Order

Last of M3.7. After M3.7c (same file). M3.7d (the workflow input and the recorded SHAs) merged 2026-11-19 (PyAutoHeart#355, record `complete/2026/11/workspace-smoke-nightly.md`), so its blocked-by header is satisfied and removed; its witness items 2 to 4 still await runs on `main`.
