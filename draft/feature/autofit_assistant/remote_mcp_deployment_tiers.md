# Remote-MCP deployment tiers (2 + 3) for the results-inspector server

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
- autolens_assistant
Difficulty: large
Autonomy: human-required
Priority: normal
Status: formalised

Build the remote-MCP deployment tiers (2 and 3) for the read-only results-inspector MCP
server, which shipped 2026-07-17 (autofit_assistant#12) with only tier 1 (local stdio for
Claude Desktop / Claude Code) built and tiers 2/3 documented-not-built in the
af_/al_inspect_results_mcp skills.

Tier 2 — remote for claude.ai web/mobile custom connectors and ChatGPT developer mode,
which speak MCP but only to servers reachable over the public internet (no stdio): expose
the same FastMCP server via mcp.run(transport="streamable-http") behind an
ngrok/cloudflared tunnel.

Tier 3 — a hosted deployment next to shared collaboration outputs (Euclid sample-scale
triage; a natural home for an aggregator-agent-style classifier consumer). Hosting, auth,
and scale are the substance here.

SECURITY (why Autonomy: human-required, never --auto safe): the tools read arbitrary
output directories on the host. A tunneled/hosted server is an unauthenticated
file-reading surface unless auth is designed in first. This task MUST go through the
security-review skill and MUST NOT be auto-shipped — the intake classifier initially
mis-sized it small/safe; that is wrong for a network-facing surface.

Scope this as transport + deployment + auth, NOT new tools — the local-stdio server and
the tool set are unchanged. Coordinate with Richard (rhayes777/PyAutoMCP prior art). Only
pursue once demonstrated demand exists (this is "if it earns it" future capability) and
after the Desktop acceptance walkthrough passes
([[desktop_acceptance_results_inspector_mcp]]).
