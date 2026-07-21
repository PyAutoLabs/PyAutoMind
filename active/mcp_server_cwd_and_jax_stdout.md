# results-inspector MCP server: harden config-path + stdout so it runs from any launcher

Type: bug
Target: autofit_assistant
Repos:
- autofit_assistant
- autolens_assistant
Difficulty: small
Autonomy: human-required
Priority: normal
Status: formalised

Surfaced by the Claude Desktop acceptance walkthrough (autofit_assistant#17,
passed 2026-07-21). The read-only results-inspector MCP server
(`autoassistant/mcp/`, mirrored in both assistants) works from the repo root but
fails from a foreign launcher (Claude Desktop → `wsl.exe`) for two reasons. The
acceptance gate worked around both in the launcher config; this task fixes them
in the server so it needs no env babysitting.

## Bug 1 — config resolution depends on the process CWD
`autonerves.conf` defaults its config directory to `os.getcwd()/config`
(`PyAutoNerves/autonerves/conf.py:290`). `import autofit` reads
`conf.instance["general"]["test"]["lh_timeout_seconds"]` at import time
(`PyAutoFit/autofit/non_linear/fitness.py:32`), so a bad CWD crashes the import.
Claude Desktop spawns `wsl.exe` with a Windows CWD → autonerves recursively
scans a Windows `desktop.ini` and `configparser` raises
`InterpolationSyntaxError: '%' must be followed by '%' or '(', found:
'%windir%\System32\ie4uinit.exe,-731'`.

Fix: `autoassistant/mcp/__main__.py` should push a deterministic config path
(the assistant repo's own `config/`, resolved relative to the package, e.g.
`Path(__file__).parents[2] / "config"`) **before** importing anything that pulls
in autofit — so config never depends on where the server was launched.

## Bug 2 — JAX logs to stdout at import, corrupting JSON-RPC
`jax._src.xla_bridge` emits two records (TPU-backend probe INFO + CUDA-fallback
WARNING) to **stdout** during `import autofit`. stdout is the MCP JSON-RPC
channel, so the client dies with `Unexpected non-whitespace character after
JSON`. The existing `server._route_logging_to_stderr()` /
`tools._stdout_to_stderr()` miss it because JAX installs its logging handler
during import, before the server reroutes.

Fix: clamp stdout / redirect the `jax` (and root) logging handlers to stderr
**before** `import autofit` runs — e.g. in `__main__` set the jax loggers to
stderr / raise their level, or default `JAX_PLATFORMS=cpu` when unset. The goal:
a bare `python -m autoassistant.mcp` from any CWD with a minimal env produces a
clean stdout stream.

## Acceptance
`cd /tmp && env -i PATH=... PYTHONPATH=<stack> python -m autoassistant.mcp` boots
and completes an MCP `initialize` + `list_searches` handshake with zero stdout
noise — no `cd`, no `JAX_PLATFORMS`/`NUMBA_CACHE_DIR`/`MPLCONFIGDIR`/
`PYAUTO_SKIP_WORKSPACE_VERSION_CHECK` needed in the launcher. Apply the same fix
to both assistants' mirrored `mcp/` copies. Once shipped, the Desktop config's
`cd …` prefix and extra env vars (added 2026-07-21) can be dropped.
