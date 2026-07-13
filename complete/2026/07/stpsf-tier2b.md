## stpsf-tier2b
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/29 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/30 (merged 117a1ec, squash)
- summary: JWST per-frame PSF coverage lifted 3/6 -> 6/6 (F115W validated) — STPSF tier-2b at frame DETECTOR + target position, DET_DIST ext (detector-sampled INCL. distortion = correct native-frame kernel); position clamp for off-detector targets (star-starved edge frames put the target exactly there, recorded); poppy-cupy import-block pin (WSL2 CUDA JIT broken, post-import flags don't rebind); missing-stpsf = recorded outcome; literature caveat on every tier-2b kernel; 197 tests; human-directed ship+merge ("ship it")
- followups: HST TinyTim tier-2 stays roadmap; stpsf now in venv (2.2.0 + data auto-found); duplicate frame-ePSF compute when both flags on still open
