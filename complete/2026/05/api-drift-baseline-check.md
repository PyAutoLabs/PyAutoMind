## api-drift-baseline-check
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/9
- completed: 2026-05-28
- library-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/10
- repos: autolens_assistant
- notes: Diagnosed stale `al.Kernel2D` AttributeError — symbol renamed to `al.Convolver` ~6mo ago; repo + PyAutoLens/PyAutoArray/PyAutoGalaxy all clean, so the crash is stale generated/collaborator code predating the rename. Added an API version pin + drift-check to work/audit_skill_apis.py: --write-baseline (wiki/core/api_audit_baseline.json = versions + public-dir() hash), --check-version (cheap session-start drift-check), --scope scripts (audits generated scripts/+work/ .py, excludes own tooling), and hardened resolve() against crashes. CLAUDE.md First-interaction drift-check + current-API-only wiki policy (version pin replaces migration tables). Queued follow-ups: wiki_current_api_only.md (remove api_deltas + 10 linkers), pyautobuild_api_baseline_release.md (auto-refresh baseline from release pipeline). Note: --scope all surfaces 23 pre-existing skill/wiki drift rows for a later audit pass.
