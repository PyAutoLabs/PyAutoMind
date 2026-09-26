# bump_colab_urls.sh: cover autolens_assistant Colab links

Type: feature
Target: pyautohands
Repos:
- PyAutoHands
Themes:
- release
- colab
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 5
Unattended: safe
Blocked-by: PyAutoMind/active/cosmos_web_ring_greeting.md (autolens_assistant#136)
Filed: 2026-09-26

## Why

`autohands/bump_colab_urls.sh` (run from `release.yml`) rewrites the `blob/<tag>/` part of
Colab links only for `autofit/autogalaxy/autolens_workspace`, `HowToGalaxy`, `HowToLens`
and `HowToFit`. The COSMOS-Web Ring greeting (#136) adds a Colab notebook to
`autolens_assistant` (`docs/colab/cosmos_web_ring_colab.ipynb`) linked from its README and
from jamesnightingale.net, so its links would stay on `main` or go stale at each release.

## Plan

Add `autolens_assistant` (and its sibling `*_assistant` repos that gain notebooks) to the
script's repo pattern; add the assistant README to whatever file list it rewrites; test
with the release dry-run.
