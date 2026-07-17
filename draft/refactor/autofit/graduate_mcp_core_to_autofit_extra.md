# Graduate the mirrored MCP core into an autofit[mcp] extra

Type: refactor
Target: autofit
Repos:
- PyAutoFit
- autofit_assistant
- autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Graduate the mirrored results-inspector MCP core into PyAutoFit as an optional
`autofit[mcp]` extra, removing the byte-identical duplication between
autofit_assistant:autoassistant/mcp/ (tools.py, __main__.py) and
autolens_assistant:autoassistant/mcp/ (same files, mirrored verbatim).

Today the core tool functions live in autofit_assistant and are copied byte-for-byte into
autolens_assistant (server.py header + __init__ docstring say "mirror; diff them when
syncing"). The recorded de-dup path is to promote the core to PyAutoFit:autofit/mcp/ (or
similar) behind a `pip install autofit[mcp]` extra so both assistants import it instead of
copying it; the autolens_assistant lens layer (lens_tools.py: al.agg enum resolution +
AggregateImages/AggregateFITS wrappers) stays in the assistant.

Constraints:
- Import direction: PyAutoFit depends on autoconf only — the mcp extra must NOT pull
  autoarray/autogalaxy/autolens; the `mcp` package is an OPTIONAL extra, never a core
  requirement. (The intake classifier wrongly pulled those repos + typed this "docs" —
  ignore that; this is a PyAutoFit refactor.)
- Preserve the read-only, glue-not-code discipline and the stdout-is-the-JSON-RPC-channel
  protections (tools._stdout_to_stderr + server._route_logging_to_stderr).
- Update both assistants' af_/al_inspect_results_mcp skills, audit_skill_apis wiring, and
  fixture tests to import the library core instead of the mirrored copy.

Only worthwhile once the server has proven its value (Desktop acceptance passed
[[desktop_acceptance_results_inspector_mcp]], real usage) — a refactor to pay down
duplication debt, filed so it is not forgotten. Prefer the lean lever: do NOT graduate
prematurely if the mirror stays a two-file diff-checked copy that hygiene can manage.
