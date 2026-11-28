## Summary

The point visualizer now renders the approved Simple cluster family diagnostics: the cluster overview, a zoom per image in the fitted plane, ranked per-image contributions and an overall source-plane panel. Panels use the actual plane coordinates on equal angular axes and are labelled with catalogue image IDs. Families of more than six images are paginated in descending contribution order. The panels are exposed one by one through `autolens.plot`, rendered in the autolens_visualization gallery (nine reviewed MACS J0416 family figures, on the Eyes board) and taught in autolens_workspace using Pandora.

## PRs

- PyAutoLens#884, PyAutoLens#890, PyAutoLens#891 (library; reach users in the next PyAutoLens release)
- autolens_visualization#20, autolens_visualization#22, PyAutoEyes#38
- autolens_workspace#687 (merged 2026-11-26 by human /prm)

## Notes

Closed out from a Claude Code /prm session on the human's command; the implementation ran in a Codex desktop session. Closing frees the PyAutoLens claim that blocked phase 3 of adapt-mesh-weighting.

## Original prompt

# Render cluster family fit diagnostics in the point visualizer

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/883
Issued: 2026-11-24
Type: feature
Target: @PyAutoLens
Related: @autolens_visualization
Epic: cluster-usability
Consequence: judge

Implement the approved Simple cluster family diagnostic layout from PyAutoMind#605. Wire the normal combined point visualizer to produce the cluster overview, individual zooms in the fitted plane, ranked per-image contributions and an overall source-plane panel. Use the actual plane coordinates and equal angular axes. Offer the shared panel as an option. Paginate more than six images in descending contribution order while preserving their IDs, the overall family ranking and the sky context. Represent the actual fitted statistic, including mixtures and unmatched-model penalties. Verify the normal gallery producer and the six/seven-image boundary.
