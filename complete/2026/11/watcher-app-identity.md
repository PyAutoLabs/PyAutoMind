Pre-M3 identity (epic `autonomous-orchestrators`). Shipped as PyAutoBrain#631 (1be4ba0cd), merged 2026-11-14. Issue PyAutoBrain#630.

**Human decision, 2026-11-14:** the watcher posts as its own minimal GitHub App, `pyautolabs-watcher` (Issues read/write and metadata read, on PyAutoMind only), not `pyautolabs-bot`. The human created and installed it, stored its key in Bitwarden, and added the three variables to `orchestrator.env`.

**Built:**
- The installation token is minted in memory for one tick, with no token on disk.
- Fail-closed: a mint failure holds every watcher write and the steering read, and never uses the human's auth. The two read-only PR reads (`gh_pr_state`, `pr_health`) use the human's auth, as documented.
- `worker_env` strips the App settings and token.
- The poster is `pyautolabs-watcher[bot]`.
- AUTONOMY's network-surface paragraph is reworded to the App identity, with no rule change.
- CI now installs PyJWT and cryptography.

**Witness:**
- 11 offline tests. Brain suite: 1984 passed.
- Live read-only checks: token minted, `pyautolabs-watcher[bot]`, issues:write + metadata:read, PyAutoMind#561 read.
- `ci-verdict` GREEN; merged with `--match-head-commit`.

**Review:** FINDINGS (a doc overclaim, a token cache workers could read, a temp-file race, a None-token path), then fixed, then CLEAN.
