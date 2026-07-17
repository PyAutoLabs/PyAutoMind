## api-gate-clause-scope
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/130 (Phase 5 F5 item)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/77 (merged; boundary+wiki-currency green)
- summary: fixed the F5 API-gate false positive (docs/agent_failure_modes.md). The PreToolUse gate latched saw_python for the rest of a compound command, so a .py argument to a LATER non-python clause (python3 -c '...' ; grep x foo.py) was scanned and blocked on a stale symbol in the grepped source file — bit this session twice. _collect_sources now splits into per-clause token lists at ; && || | (quotes respected, unparseable -> fail open) and scopes saw_python per clause; each source carries its own interpreter. 3 regression tests + full 28-test suite green against the real stack. Fix is live in the local hook (self-session).
