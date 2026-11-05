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
Epic: cti-upkeep
Phase: 2b
Blocked-by: a new arcticpy release on PyPI (draft/release/arcticpy/upstream_packaging_pr.md)

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
