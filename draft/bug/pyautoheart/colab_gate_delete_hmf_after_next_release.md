# Colab gate: delete the hmf accepted-miss once autolens without hmf is on PyPI

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: notify
Witness: `PyAutoHeart/heart/config/colab_gate.yaml` has no `hmf` entry, `tests/test_colab_gate.py` asserts the exemption set {colossus, mcp}, and a continuous check F run (`verify_install.sh F`) against a PyPI autolens newer than 2026.11.19.1 passes with no hmf row.
Review-minutes: 0
Unattended: ready
Lane: any

## Finding

PyAutoHeart#356 kept the `hmf` entry in `heart/config/colab_gate.yaml`: source main imports no hmf
(PyAutoLens PRs 867/868), but the released autolens 2026.11.19.1 still imports it unguarded in
`autolens/lens/los.py`, and the continuous check F audits the PyPI release. Removing the entry
before a release carrying PR 867 is on PyPI turns check F FAIL.

## Ask

reproduce before fixing: `pip download autolens --no-deps` gives a version newer than 2026.11.19.1 whose `autolens/lens/los.py` has no `import hmf`.

1. Delete the `hmf` entry from `heart/config/colab_gate.yaml`.
2. Shrink the asserted set in `test_shipped_config_accepts_exactly_the_three_argued_exemptions` to {colossus, mcp} and rename it.
3. Run check F continuous.

## Provenance

[from: shift 2026-11-19-pm2 worker, PyAutoHeart#356 decide-and-flag]
