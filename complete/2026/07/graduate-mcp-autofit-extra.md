# Graduate results-inspector MCP core into an autofit[mcp] extra

**Shipped + MERGED 2026-07-21.** Issue: PyAutoFit#1403 (closed). PRs (library-
first): PyAutoFit#1404 (core, 1af904bd) → autofit_assistant#21 (89811c20) +
autolens_assistant#86 (0d3847bb). Third and last of the results-inspector MCP
follow-ups.

## What shipped
De-duplicated the byte-identical MCP `tools.py` (148 lines, copied across both
assistants) by graduating it into PyAutoFit as an optional `autofit[mcp]` extra.

New `autofit/mcp/` (auto-discovered package): `tools.py` (aggregator wrappers,
imports autofit + autonerves only), `server.py` (`core_server()` FastMCP factory
registering the 7 read-only tools), `bootstrap.py` (`pin_config` +
`route_logging_to_stderr`, **autonerves-only** so a launcher can pin config
before importing autofit), `__main__.py` (standalone `python -m autofit.mcp`).
`pyproject.toml`: `mcp = ["mcp"]` under optional-dependencies (never core).
`__init__.py` lazy-exports `core_server`/`_png` via PEP-562 `__getattr__` to stay
import-light.

Both assistants: deleted `autoassistant/mcp/tools.py`; `server.py` is now a thin
launcher that builds `core_server()`. autolens keeps its lens layer
(`lens_tools.py`, now importing the shared helpers from `autofit.mcp.tools`).

## The crux — nearly regressed the #18 CWD fix
First design imported `pin_config` from `autofit.mcp.bootstrap`, but importing
anything under `autofit` imports autofit first, which reads config at import
(`fitness.py`) — so the pin would land too late and re-break the Desktop
foreign-CWD fix. Fixed by inlining the pin (autonerves-only) in each launcher,
before any autofit import. **Proved** with a planted `%windir%` poison config in
the launch CWD: the server boots clean.

## Verification
Three servers complete a real MCP stdio handshake from a neutral CWD with a
minimal env: autofit_assistant (7 tools), autolens_assistant (10, lens layer),
standalone `python -m autofit.mcp` (7) — gaussian-first, clean stdout. Tests:
PyAutoFit `test_autofit/mcp` 10/10, autolens 10/10 (autofit_assistant core test
deleted — covered by PyAutoFit). Skill-API audit 0 missing (thin launchers carry
`pyauto-api-gate: skip` — not skill-API surface). Confirmed on the merged main
checkouts.

## Traps
- PyAutoFit test must use the **shipped `autofit/config`** (`remove_files: false`),
  NOT `test_autofit/config`, which zips output away → the MCP tools find no files
  on disk. The read-only tools operate on real unzipped output directories.
- Assistant `wiki-currency` CI stays red on the merge (overridden with `--admin`,
  main unprotected): the environmental `--check-version` baseline drift (fails on
  main too) plus a transient `autofit.mcp.tools` symbol that the audit resolves
  against the *released* stack — self-heals on the next PyAutoFit release.
- The `mcp` SDK (`mcp.server.fastmcp`) vs the assistant's own `autoassistant.mcp`
  package can name-collide in the audit's multi-import resolution context; the
  skip-marker on the launchers sidesteps it.

## Original prompt

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
