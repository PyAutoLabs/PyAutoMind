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
