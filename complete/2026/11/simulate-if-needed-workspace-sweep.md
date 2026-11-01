## simulate-if-needed-workspace-sweep
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/268
- completed: 2026-11-01
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/612
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/269
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/353
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/39
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/132
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/120
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/99
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/118
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/549

- Phase 3 of `one-line-auto-simulate-helper` (`complete/2026/11/one-line-auto-simulate-helper.md`). Merged after the PyAutoArray 2026.11.1.1 release, which carries #670; the wheel was checked to contain `simulate_if_needed`.
- 536 standard blocks rewritten across 7 repos with an AST matcher that only accepts the exact block. A redundant `str(...)` is dropped. Every inserted call is black-exact. Notebooks were regenerated with `generate.py <project> --assistant-root <assistant>`.
- Witness met: `check_dataset_allowlist` finds the same guarded call-site count before and after in every swept repo (256/85/67/43/42/30/18).
- Detectors kept in step: the euclid repo-invariant simulation tokens (#118) and the PyAutoBrain hygiene `simulates` lever (#549) now match `simulate_if_needed`.
- Deliberately left: autolens_workspace_developer (22) and autolens_profiling (1) use extra argv or `cwd=`, which the helper doesn't support; autofit_workspace has intentional raw guards; plus 4 scripts with inline simulation or prints. autogalaxy_workspace `markdown/` renders refresh at release.
- Trap: `generate.py` without `--assistant-root` (or `PYAUTO_ASSISTANT_ROOT`) silently strips the Colab assistant context from every notebook. The assistant's current contexts.yaml also differs from the committed notebooks, so a full regen refreshes contexts in about 30 notebooks; those were reverted here to keep diffs scoped.
- Trap: autocti_workspace scripts are CRLF. Read and write bytes and preserve the EOL, or every line diffs.
- Trap: the HowToLens generator emitted `\uXXXX` escapes and a trailing-newline change versus the committed notebooks; reverted line-by-line.
- Note: autocti on PyPI is still 2024.11.13.2, so autocti_workspace already runs on library `main`.
- Note: autolens_workspace, the HowTos and euclid were swept on explicit human instruction despite other active claims (`magnification-errors-source-science`, `howto-chapter2-format`, `sky-orientation-p2`). Neither of the first two had a remote branch at the time.

## Original prompt

# Sweep workspaces onto al.util.dataset.simulate_if_needed (one PR per repo)

Type: feature
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- HowToLens
- HowToGalaxy
- assistants
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: after the sweep, `grep -rn "subprocess.run" --include=*.py` next to `should_simulate` returns zero hits in every workspace, and `check_dataset_allowlist` reports the same number of guarded call sites before and after.
Review-minutes: 3
Unattended: needs-slicing
Blocked-by: PyAutoArray release carrying https://github.com/PyAutoLabs/PyAutoArray/pull/670 (pending-release)
Filed: 2026-11-01
Issued: 2026-11-01
Issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/268

- Status: split out of `one-line-auto-simulate-helper` at close-out. Phases 1–2 shipped in `complete/2026/11/one-line-auto-simulate-helper.md` (PyAutoArray#670, PyAutoHands#329); this is phase 3, what remains.

Replace the 8-line auto-simulate block in every workspace script:

```python
if al.util.dataset.should_simulate(str(dataset_path)):
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "scripts/simulator/lens_x2.py"],
        check=True,
    )
```

with the one-liner shipped in PyAutoArray#670:

```python
al.util.dataset.simulate_if_needed(dataset_path, simulator="scripts/simulator/lens_x2.py")
```

- Start only after the PyAutoArray release that carries #670 has published; workspaces pin released libraries.
- First confirm `al.util.dataset.simulate_if_needed` and `ag.util.dataset.simulate_if_needed` resolve. The re-export was assumed at close-out, not verified.
- Do one PR per repo (autolens/autogalaxy/autofit workspaces, *_workspace_test, HowToLens/HowToGalaxy, assistants). This is a mechanical rewrite: keep the dataset_path and simulator path exactly as in each script.
- Regenerate notebooks where the repo generates them. Smoke-test a sample per repo.
- Watch for variants (extra argv, different indentation, `aa.`/`ag.` prefixes). Leave any non-standard block untouched and list it in the PR.
- Run `check_dataset_allowlist` before and after in each repo: the guarded call-site count must not drop. PyAutoHands#329 already makes the guard recognise `simulate_if_needed`.
