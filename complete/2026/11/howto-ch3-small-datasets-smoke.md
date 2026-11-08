# howto-ch3-small-datasets-smoke

Shipped 2026-11-08: HowToLens#131 and HowToGalaxy#105, both merged after green CI on every leg
(smoke 3.12/3.13, navigator, tutorials-complete).

The chapter-3 fit-problems and adaptive-reconstruction tutorials (HowToLens t5/t6, HowToGalaxy
t3/t4) no longer raise `ValueError` on non-finite or edge-of-range evidence scans. The human ruled
on 2026-11-08: "I don't think a user needs to see them". The fit-problems refinement clamps its
neighbours so a peak at the grid edge refines inward. The `__Env__ / ENV: full_datasets` sections
were removed, so the smoke gate runs these tutorials on small datasets like the rest of the
chapter. Users still run them at full size.

Measured locally (py3.12, smoke env, small vs full size):
- HowToLens: t5 12.2s vs 98.0s; t6 18.6s vs 76.8s.
- HowToGalaxy: t3 7.2s vs 81.9s; t4 11.4s vs 68.0s.

Caveat: HowTo repos are outside release validation, so nothing in CI runs these tutorials at full
size any more.

Follow-up: notebooks regenerate at the next pre-build (scripts only were edited).
