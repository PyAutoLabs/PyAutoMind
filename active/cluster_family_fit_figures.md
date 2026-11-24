# Render cluster family fit diagnostics in the point visualizer

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/883
Issued: 2026-11-24
Type: feature
Target: @PyAutoLens
Related: @autolens_visualization
Epic: cluster-usability
Consequence: judge

Implement the approved Simple cluster family diagnostic layout from PyAutoMind#605. Wire the normal combined point visualizer to produce the cluster overview, individual zooms in the fitted plane, ranked per-image contributions and an overall source-plane panel. Use the actual plane coordinates and equal angular axes. Offer the shared panel as an option. Paginate more than six images in descending contribution order while preserving their IDs, the overall family ranking and the sky context. Represent the actual fitted statistic, including mixtures and unmatched-model penalties. Verify the normal gallery producer and the six/seven-image boundary.
