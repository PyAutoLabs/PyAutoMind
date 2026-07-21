# Claude Desktop acceptance walkthrough — results-inspector MCP server

**Shipped 2026-07-21.** Issue: PyAutoLabs/autofit_assistant#17 (closed). No PR —
manual acceptance/validation gate. This was the one unchecked acceptance box from
the results-inspector MCP work (autofit_assistant#12; PRs autofit_assistant#13 +
autolens_assistant#75, shipped 2026-07-17).

## Outcome
Human-driven Claude Desktop chat PASSED against the read-only MCP stdio server:
demo fits listed ranked by evidence (gaussian first), best fit's `model.results`
summary rendered, `data` image displayed inline. Unblocks the two follow-ups it
gated: remote MCP deployment tiers, and `autofit[mcp]` core graduation.

## CLI prep that got it there
- Staged config `C:\Users\Jammy\FromWSL\claude_desktop_config.json` had rotted:
  `PYTHONPATH` listed the deleted `PyAutoConf` (autoconf→autonerves rename; server
  imports `autonerves.dictable`). Swapped to `PyAutoNerves`.
- Gitignored demo dir `autolens_assistant/scripts/scratch/mcp_demo/output` was
  gone — regenerated (generator kept at scratchpad `gen_mcp_demo.py`): 2
  DynestyStatic fits, gaussian logZ −42.55 > exponential −43.50 (~8σ, stable),
  each with `image/data.png` + `image/model_fit.png`.
- Both the live packaged-app config
  (`…/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/claude_desktop_config.json`)
  and the staged FromWSL copy updated with the final working launch line.

## Two real server-robustness bugs surfaced (worked around; clean fix filed as bug/)
The walkthrough is what exposed both — neither was a config typo:

1. **CWD-dependent config.** `autonerves.conf` defaults its config dir to
   `os.getcwd()/config` (`PyAutoNerves/autonerves/conf.py:290`). Claude Desktop
   spawns `wsl.exe` with a Windows CWD → autonerves scanned a Windows
   `desktop.ini` → `configparser.InterpolationSyntaxError` on its
   `%windir%\System32\...` value. Worked around by prepending
   `cd /home/jammy/Code/PyAutoLabs/autolens_assistant` to the launch command
   (also fixes the `python -m` sys.path[0] ambiguity — both assistant repos ship
   an `autoassistant` package; autolens_assistant is first on PYTHONPATH = the
   10-tool lens server, and cd-ing there keeps that consistent).
2. **JAX logs to stdout at import.** `jax._src.xla_bridge` writes two
   INFO/WARNING lines (TPU probe + CUDA fallback) to **stdout** during
   `import autofit`, corrupting JSON-RPC. The server's
   `_route_logging_to_stderr()` misses them because JAX installs its handler
   first. Worked around with `JAX_PLATFORMS=cpu` (+ `NUMBA_CACHE_DIR`,
   `MPLCONFIGDIR`, `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK`) in the launch env.

Clean fix (filed): `draft/bug/autofit_assistant/mcp_server_cwd_and_jax_stdout.md`
— the server's `autoassistant/mcp/__main__` should push a deterministic config
path and clamp stdout/JAX logging to stderr **before** importing autofit, so it
works from any launcher without env babysitting.

## Traps (durable)
- Claude Desktop on Windows may be the **Microsoft Store packaged** build:
  config + logs live under
  `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\`, NOT
  `%APPDATA%\Claude\`. Readable from WSL at
  `/mnt/c/Users/<user>/AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/`.
- Verifying an MCP server via a direct-python stdio handshake from the repo root
  does NOT prove the Desktop launch: it hides (1) the CWD-config dependence and
  (2) JAX device-init stdout, which only bite with a foreign CWD / minimal env.
  Reproduce with `env -i` + a neutral cwd to catch them.

## Original prompt

# Claude Desktop acceptance walkthrough — results-inspector MCP server

Type: test
Target: autofit_assistant
Repos:
- autofit_assistant
- autolens_assistant
Difficulty: small
Autonomy: human-required
Priority: normal
Status: formalised

Complete the Claude Desktop acceptance walkthrough of the read-only results-inspector
MCP server (shipped 2026-07-17, autofit_assistant#12; PRs autofit_assistant#13 +
autolens_assistant#75). This is the one unchecked acceptance box from that task.

Everything is pre-staged and already proven end-to-end via the wsl.exe hop:
- Ready config at C:\Users\Jammy\FromWSL\claude_desktop_config.json (wsl.exe -e bash -c
  launch line with PYTHONPATH for the editable checkouts; validated against a real MCP
  client session).
- Demo output dir: autolens_assistant/scripts/scratch/mcp_demo/output — two DynestyStatic
  fits of the same noisy dataset (gaussian log_evidence -45.2 beats exponential -48.3),
  each with data.png / model_fit.png.

Manual steps (require Claude Desktop, which is NOT installed on the Windows host as of
2026-07-17, hence Autonomy: human-required — only the user can drive a Desktop chat):
install Claude Desktop, copy the staged config to
%APPDATA%\Claude\claude_desktop_config.json, restart, then in a Desktop chat ask it to
list the demo fits ranked by evidence, show the best one's result summary, and fetch its
data image. Correct behaviour: gaussian ranked first, a model.results block, the plot
rendered inline. First tool call after launch is slow (cold WSL import of autolens+JAX);
failure log is %APPDATA%\Claude\logs\mcp-server-pyauto-results-inspector.log.

This is a manual acceptance/validation gate, not a code change — no PR expected unless the
walkthrough surfaces a bug in the server. If it does, that bug is a separate bug/ prompt.
Gates the two follow-ups filed alongside it (remote tiers, autofit[mcp] graduation).
