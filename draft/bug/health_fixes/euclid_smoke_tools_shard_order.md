# Euclid smoke: `scripts/tools` shard runs without the fits it replays

Type: bug
Target: health_fixes
Themes:
- ci
- smoke
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-10-21

## Context

Heart board finding `test_run:euclid` / `ci_status:PyAutoHeart/workflows/Workspace Smoke`
(red; release-readiness YELLOW reason "workspace validation not passing (1 failed,
cloud#39224774724: euclid scripts/tools/diagnose_latent.py)").

PyAutoHeart#309 (merged 2026-10-17, commit 4891a53) added the Euclid pipeline to
`workspace-validation.yml` smoke mode. The matrix is built by
`PyAutoHands/autohands/script_matrix.py`, which shards a project by directory, so
job `run_scripts (3.12, euclid, tools)` runs `scripts/tools/diagnose_latent.py`
alone in a fresh runner. It fails in 4.9s:

    ERROR: no such search directory: .../workspace/output/test_mode/q1_walsmley/
    102018665_NEG570040238507752998/initial_lens_model/vis_lp

`euclid_strong_lens_modeling_pipeline/smoke_tests.txt` documents that the order is
load-bearing (one output dir; diagnose_latent replays fits run above it), and
`config/build/profile_smoke.yaml` assumes `start_here.py` already ran. Workspace
Smoke passed on 10-16, before euclid was added.

Primary repository: @PyAutoHands (script_matrix sharding) or @PyAutoHeart
(workspace-validation wiring). Do not edit the pipeline script to mask it.

## Ask

Make order-dependent projects (an ordered `smoke_tests.txt`) run as one shard, or
otherwise guarantee the producer scripts run in the same job. Verify with a
Workspace Smoke dispatch that the euclid legs pass.
