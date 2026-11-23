# Fix Codex shift launch and smoke parity

Issued: 2026-11-23
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/714
Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Consequence: judge
Lane: local-dev
Witness: a disposable auto-mode worker writes its marker and reports usage through the production launcher, and the dispatch procedure verifies that the watcher can read the pushed brief locally.

User request verbatim: ok shall we fix those things

Pilot PyAutoMind#600 exposed incompatible auto-mode CLI flags, a smoke test hard-coded to dontAsk, and an omitted watcher-checkout refresh after pushing from a separate worktree.

Additional request verbatim: yeah go also fix cockpit for live codex feedback?
