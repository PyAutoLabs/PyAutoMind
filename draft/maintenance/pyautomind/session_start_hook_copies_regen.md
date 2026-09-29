# Regenerate the 28 drifted `.claude/hooks/session-start.sh` copies after the organ-order change

Type: maintenance
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Status: draft
Consequence: glance
Witness: `python3 scripts/repos_sync.py --check` reports 0 mismatches on its hooks leg.
Filed: 2026-09-29

## The finding

`repos_sync.py --check` reports 28 `.claude/hooks/session-start.sh`
mismatches across the organism. They differ only in the `holds_an_organ`
check order and are left over from the organ-order change (Mind#439,
`4cde3d30`), which updated the canonical hook without re-propagating every
copy. Surfaced while shipping PyAutoEyes phase 3 (PyAutoMind#452).

## Fix

One sweep PR set regenerating the hook copies from the canonical source via
`repos_sync.py --write` (one PR per affected repo). The
`.github/profile/README.md` row is human-only — hand that patch to the human.

Sweep opened 2026-09-29 (27 PRs, unmerged; `.github/profile/README.md` patch left for the human): https://github.com/PyAutoLabs/HowToFit/pull/69 https://github.com/PyAutoLabs/HowToGalaxy/pull/83 https://github.com/PyAutoLabs/HowToLens/pull/94 https://github.com/PyAutoLabs/PyAutoArray/pull/587 https://github.com/PyAutoLabs/PyAutoCTI/pull/111 https://github.com/PyAutoLabs/PyAutoFit/pull/1650 https://github.com/PyAutoLabs/PyAutoGalaxy/pull/636 https://github.com/PyAutoLabs/PyAutoLens/pull/755 https://github.com/PyAutoLabs/PyAutoMemory/pull/106 https://github.com/PyAutoLabs/PyAutoReduce/pull/79 https://github.com/PyAutoLabs/autocti_assistant/pull/33 https://github.com/PyAutoLabs/autocti_workspace/pull/35 https://github.com/PyAutoLabs/autocti_workspace_test/pull/22 https://github.com/PyAutoLabs/autofit_assistant/pull/52 https://github.com/PyAutoLabs/autofit_workspace/pull/165 https://github.com/PyAutoLabs/autofit_workspace_developer/pull/27 https://github.com/PyAutoLabs/autofit_workspace_test/pull/104 https://github.com/PyAutoLabs/autogalaxy_assistant/pull/31 https://github.com/PyAutoLabs/autogalaxy_workspace/pull/252 https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/126 https://github.com/PyAutoLabs/autolens_assistant/pull/140 https://github.com/PyAutoLabs/autolens_inference/pull/16 https://github.com/PyAutoLabs/autolens_workspace/pull/580 https://github.com/PyAutoLabs/autolens_workspace_developer/pull/145 https://github.com/PyAutoLabs/autolens_workspace_test/pull/326 https://github.com/PyAutoLabs/autoreduce_workspace/pull/3 https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/107
