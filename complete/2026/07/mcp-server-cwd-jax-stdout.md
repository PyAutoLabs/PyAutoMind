# results-inspector MCP server: run from any launcher (CWD-config + JAX stdout)

**Shipped + MERGED 2026-07-21.** Issue: PyAutoLabs/autofit_assistant#18 (closed).
PRs: autofit_assistant#19 (merge 417bb1a5) + autolens_assistant#85 (merge
0233f482). Surfaced by the Desktop acceptance walkthrough (#17).

## What shipped
Hardened the read-only results-inspector MCP server so it runs from any
launcher / working directory with no env babysitting. In `server.py` (both
assistants, core byte-identical), **before** importing the autofit-backed tool
modules:
- `os.environ.setdefault("JAX_PLATFORMS", "cpu")` — skips jax's xla_bridge
  backend probe, which otherwise logs to stdout during `import autofit`.
- `_pin_config()` — `conf.instance = conf.Config(Path(__file__).resolve().parents[2]
  / "config", ...)`, so autonerves no longer derives its config dir from
  `os.getcwd()` (conf.py:290) and cannot crash on a foreign CWD's `desktop.ini`.
- `with contextlib.redirect_stdout(sys.stderr): from ...import (lens_tools,) tools`
  — swallows any residual import-time stdout. `_route_logging_to_stderr()` still
  runs after for handlers attached during import.

Also added a Windows/WSL launch note to both skills (`{af,al}_inspect_results_mcp.md`)
showing the now-clean `wsl.exe` config (PYTHONPATH only) + the MS-Store config/log
path.

## Verification
Real MCP stdio handshake from `/tmp` with a **minimal env** (PATH+HOME+PYTHONPATH
only — no cd, no JAX/cache/skip vars): both servers (autofit 7 tools, autolens 10)
initialize, `list_searches` ranks gaussian first, zero stdout noise.
`test_mcp_tools.py` passes 10/10 in each repo. Post-merge, re-verified the plain
config against the updated main checkout (10 tools, gaussian first, clean).

## Post-merge cleanup done
- Live packaged + staged FromWSL Claude Desktop configs reverted to the plain
  `PYTHONPATH=… python -m autoassistant.mcp` launch line (the `cd` prefix + JAX/
  NUMBA/MPL/SKIP env from the acceptance workaround are no longer needed).
- Main checkouts of both assistants synced to the merged commits.

## Traps
- `--check-version` in the `wiki-currency` CI is an environmental baseline-vs-
  installed-stack version drift (baseline pinned 2026.7.19.1, installed 2026.7.9.1);
  it fails on clean `main` too and is unrelated to code changes — `--scope all`
  (the real symbol audit) is the one that must pass. main is unprotected → the
  non-required check is override-able (`gh pr merge --admin`).

## Original prompt

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
