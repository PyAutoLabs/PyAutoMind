# Add a read-only "results-inspector" MCP server to the AI assistants

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
- autolens_assistant
- PyAutoFit
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Add a read-only "results-inspector" MCP server to the AI assistants so chat harnesses
without code execution (Claude Desktop first; claude.ai web / ChatGPT via remote MCP later)
can inspect PyAutoFit/PyAutoLens fit results: list and filter searches in an output
directory, get model composition and posterior summaries (model.result, log evidence,
samples summaries), and fetch/combine result images and FITS, with figures returned
inline via the MCP Image type.

Scope and design constraints (agreed in research discussion 2026-07-17):

- READ-ONLY. No optimise/fit-running tools, no compute tools. Model composition and fit
  execution stay script-first through the existing skills; the trap of flattening the
  compositional API into JSON schemas (demonstrated by rhayes777/PyAutoMCP's `optimise`
  tool, which hardcodes pixel_scales/Imaging/LBFGS) is explicitly out of scope.
- Glue, not code: ~8-10 tools, each a thin wrapper over an existing public PyAutoFit
  aggregator API (Aggregator, SearchOutput, AggregateImages, AggregateFITS) or existing
  aplt subplot functions. Rule: any logic beyond argument-parsing + calling an existing
  public API belongs in PyAutoFit itself, not the server. If a tool needs new logic,
  add the method to PyAutoFit first.
- Shared core + thin lens layer: the aggregator tool core is autofit-level and shared by
  autofit_assistant and autolens_assistant; autolens_assistant adds a thin layer of
  lens-specific visualization tools (fit subplots, source reconstruction) reusing
  existing aplt functions. No duplicated code between the two assistants.
- Delivery inside the assistants (e.g. autoassistant/mcp/ + a .mcp.json registration),
  documented by a symmetric af_/al_ skill file in each assistant's skills/. Graduate the
  core into PyAutoFit proper only if it earns it.
- Anti-drift: the server's cited PyAuto* symbols are added to the existing
  audit_skill_apis sweep so the tool surface cannot drift silently against the stack.
- Acceptance test: a Claude Desktop session with the server configured (local stdio)
  can list fits in an output directory ranked by log evidence, show a model.result
  summary, and display a fit subplot inline in chat.
- Tiers 2/3 (claude.ai web / ChatGPT via ngrok-cloudflared tunnel; hosted
  collaboration/Euclid deployment next to shared outputs) are DOCUMENTED in the skill
  file but not built in this task.
- Prior art to review: rhayes777/PyAutoMCP (FastMCP prototype, Sept 2025 — aggregate.py
  and visualise.py are the good parts to mature; drop optimisation.py/compute.py) and
  rhayes777/aggregator-agent (pydantic-ai vision triage over fit subplots — a future
  consumer of this tool surface, not part of this task). Coordinate with Richard, who
  built both prototypes.

Repos: autofit_assistant (primary), autolens_assistant (lens layer), PyAutoFit (only if
a wrapper needs a missing public method).

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/62cb3586-fee3-4e7e-9ad4-2f57084e840f/scratchpad/mcp_results_inspector_raw.md -->
