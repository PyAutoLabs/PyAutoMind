## frame-registration
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/19 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/20 (merged bff3d2d, squash)
- summary: inter-exposure registration quantified + extracted — frames/manifest.json per-frame registration block (WCS solution identity + absolute-fit quality, flagged as NOT the modeling number, + MEASURED relative residual via WCS-resample + whitened phase correlation); slacs0008 relative registration <=0.1 native px (<=5 mas), measurement floor 0.1-0.3 px from CR holes (3-estimator cross-check); max_registration_residual_px in reduction.json; loud runtime notice (user-requested, test-pinned); phase_offset(whiten=) kwarg; modeling stance documented: default shifts-known, precision frees per-frame (dy,dx) with recorded-width priors — user approved recommendation, human-directed merge in-conversation
- followups: feature/pyautoreduce/per_frame_psf.md is next (user ordering); retire the loud print deliberately once the fact is internalized
