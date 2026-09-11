# release-integrate: analyze-side foreign-path filter and a workspace-repo lint for tracked result files

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-09-11

The remainder of `complete/2026/09/release-integrate-discard-stale-result-files.md`,
which shipped option 1 of the three guards the original prompt offered
(PyAutoHeart#225: every shard now deletes any result file the workspace checkout
carries before the runner starts, and warns per file). Two defence-in-depth
layers were left open and are re-filed here so the dashboard does not offer the
shipped prompt as backlog:

1. **Analyze-side path filter.** In the analyze/collector path
   (`heart/validate.py` rglob over `*.json`; `heart/checks/test_run.py` and
   `script_timing.py` glob `*__script.json`), drop or flag any result entry whose
   `file` path is not under the runner workspace (does not start with
   `$GITHUB_WORKSPACE`, or starts with a home directory such as `/home/<user>`),
   and log a loud warning naming the shard and the foreign path. This catches a
   leak that arrives by any route the pre-run discard does not see (a result
   written under a different name, or a future runner that changes the layout).
2. **Workspace-repo lint.** A Heart required workflow, or a check in the workspace
   CI, that fails when `test-results/` or any `*__script.json` / `smoke_timings.json`
   is tracked in git — so the leak is refused at the workspace PR rather than
   laundered at the release.

Tests in `PyAutoHeart/tests` for each layer, using a fixture that plants a stale
`*__script.json` carrying a foreign path and asserts it is excluded and warned
about (layer 1), and a planted tracked result file that the lint rejects (layer 2).

Background: nightly Release Integrate runs 34323573912 (2026-09-09) and
34449490363 (2026-09-10) failed at Stage 3 on three stale `jax_likelihood`
failures that autolens_workspace_test#311 had committed by accident; awt#313
removed them and the 2026-09-11 nightly went green. See the record above for
the trap that cost a CI round (the tenant firewall reads test modules).
