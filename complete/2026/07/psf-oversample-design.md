## psf-oversample-design
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/353
- completed: 2026-07-08
- notes: |
    Phase 1/4 of oversampled PSF convolution (parent oversampling.md, split
    2026-07-08). Deliverables in PyAutoMind/feature/autoarray/:
    oversampling_design.md + oversampling_ground_truth.py (s=1 parity vs
    Convolver 5.6e-17; s=2 reference numbers for phases 2-3). Design approved
    unchanged by human after supervised --auto park (calibration: parked ->
    approved-unchanged). No library source edits; no PR needed. Worktree
    removed (zero commits). Key corrections recorded: inversion PSF hook is
    AbstractInversionImaging.operated_mapping_matrix_list, not mapping.py;
    mapper needs sub-resolution mapping matrix (x s^2 memory risk).
