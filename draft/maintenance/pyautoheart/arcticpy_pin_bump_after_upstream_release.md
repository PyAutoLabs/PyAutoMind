# Heart/DNA: bump the arcticpy pin after the upstream release, re-pin CTI values

Type: maintenance
Target: PyAutoHeart
Repos:
- @PyAutoHeart
- @PyAutoDNA
- @PyAutoCTI
- @autocti_workspace_test
Themes:
- cti
- install
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
Lane: any
Epic: cti-upkeep
Phase: 2b
Blocked-by: a new arcticpy release on PyPI (draft/release/arcticpy/upstream_packaging_pr.md)

> **2026-11-26 — stopgap shipped** (`complete/2026/11/arcticpy-27-git-source.md`): the installer already
> builds 2.7 from `jkeger/arctic@6f5153582aca00b7b0cc11ab04b2c58a7502400d` via `ARCTICPY_SOURCE`, and the
> CTI pins were verified UNCHANGED under 2.7 (the re-pin trap below did not fire). Remaining scope: once the
> PyPI login works, publish 2.7 from that same commit, set `ARCTICPY_VERSION` default to `2.7` (git source
> then unused), switch PyAutoCTI's pyproject note / `.readthedocs.yaml` / AGENTS.md back to `arcticpy==2.7`,
> add arcticpy to DNA, and consider adding rhayes777 as a PyPI maintainer so Hands can release it.

## Scope

- In PyAutoHeart `install_arcticpy.sh`, which holds the single pin, bump
  `ARCTICPY_VERSION`. If upstream has fixed its metadata, drop `--no-deps` and the
  `pip check` exception.
- Add arcticpy to DNA `PUBLIC_PACKAGES` with a stack spec and a short support
  rationale.
- Re-run `arcticpy_smoke.py`.
- **Trap:** the DR2 well-filling model changes clocked values. Expect the
  `test_autocti` fixtures and the 10 pinned literals in autocti_workspace_test
  `scripts/{dataset_1d,imaging_ci}/likelihood/pins.py` (0b, arcticpy 2.6) to move.
  Re-pin them all in one PR with the before and after values recorded. Never
  loosen a tolerance silently.
- Check the pyproject comment in PyAutoCTI that names `arcticpy==2.6`.
