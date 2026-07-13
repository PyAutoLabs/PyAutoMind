## api-baseline-refresh
- issue: none (human-directed same-session quick task, prompt issued/api_baseline_refresh.md)
- completed: 2026-07-10
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/60 (MERGED)
- notes: baseline re-pinned 2026.5.29.4 → released 2026.7.9.1 (clean venv, PYTHONPATH-leak caught); clears wiki-currency version-drift leg + Heart "pinned BEHIND" yellow; release-step path bug already fixed on Build main c09f293

## Original prompt

# Refresh the assistant's pinned API baseline to the released stack

Type: maintenance
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: filed

The assistant's wiki-currency CI fails its "Version drift (--check-version)"
leg on every branch: the pinned API baseline is behind the released stack
(nightlies live since 2026.7.9.1; drift report says "public API surface
changed: autoarray, autofit, autogalaxy, autolens, autolens.plot"). This is
also Heart's "autolens_assistant: pinned BEHIND installed" YELLOW reason.
Pre-existing — confirmed on assistant-benchmarks (#57/#58) where all other
legs (symbol audit, idioms, provenance, citations) passed.

Do the al_update_wiki / refresh_api_docs workflow: audit what actually
changed in the released public API, update any stale wiki/core + skills
content it invalidates, regenerate + re-pin the baseline
(`--write-baseline`), and verify `--check-version` exits 0 against the
released stack. Watch for cascades: an API surface change may mean real doc
edits, not just a re-pin. Consider whether the nightly-release cadence needs
this refresh automated post-release (PyAutoBuild already regenerates the
baseline before wiki-currency at release time — investigate why the pin is
still behind despite that ordering).

<!-- COMPLETED 2026-07-10 same-day, human-directed ("do this if quick"): re-pin shipped as autolens_assistant PR#60 (MERGED). Root cause of staleness: release-step script-path bug, already fixed on PyAutoBuild main c09f293; nightly re-pin now a no-op. No wiki content invalidated (drift additive; symbol audit green on released stack). -->
