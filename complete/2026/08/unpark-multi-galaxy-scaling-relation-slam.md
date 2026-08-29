- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/514 (CLOSED)
- completed: 2026-08-29
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/516 (merged -> main)
- repos: autolens_workspace
- outcome: GATE FAILED — the park was NOT removed. Scope shipped = the park's reason rewritten (one line in `config/build/no_run.yaml`) to record what is now verified and what actually fails; the un-park itself is re-filed as the bug prompt below.
- summary: Cache-free capped runs (CI-form + evidence form, 4 attempts, all exit 1 in 8–12 s). VERIFIED: autolens_workspace#501/#502's pixel-scale fix — `Standard mask radius: 3.0` / `Enlarged mask radius: 4.70` (= 0.5*16*0.6-0.1), masks populated (80 / 192 px), `lens_light[1]` and `lens_light[2]` both reach `Search complete`, no `zero-size array`. THIRD CAUSE: `luminosity_from` raises `Measured luminosity is 0.0` (slam.py:146) — every linear MGE intensity in the truncated light stages' max-likelihood sample is 0.0. The imaging sibling passes the same smoke profile with anchor 22.47 (#513) and both simulators put galaxies within ~0.35" of the origin, so this is neither the off-frame cause 1 nor a generic test-mode limit; it is specific to this script's two-stage (fixed-pair + tier) light setup.
- re-filed: `draft/bug/autolens_workspace/multi_galaxy_scaling_relation_zero_intensity_under_smoke.md` (diagnose which stage yields the zeros; no test-mode-only luminosity fallback). Once fixed, re-run this exact gate and un-park.
- trap: the script's `path_prefix` is `multi_galaxy/slam/` (slam.py:926), so the tree to clear is `output/test_mode/multi_galaxy/slam/` — the obvious `…/features/scaling_relation` path clears nothing and a stale tree fakes a pass ("Fit Already Completed" x2 on the first run). Now recorded in the park reason itself.
- heart-ack: shipped/merged under human-acknowledged YELLOW (2026-08-29) — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source".

## Original prompt

# Un-park multi_galaxy/features/scaling_relation/slam once a capped run passes

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci-smoke
- notebooks
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Blocked-by: a capped run of the script exiting 0 — see "The gate" below
Issued: 2026-08-29
Filed: 2026-08-24

The sibling of `complete/2026/08/unpark-imaging-scaling-relation-slam.md` (shipped 2026-08-29, autolens_workspace#513),
for the entry at `config/build/no_run.yaml:48` that the sibling prompt explicitly
told us *not* to unpark.

## Why this exists

`autolens_workspace#502` (merged `85027bbb`, 2026-08-24) fixed the latent
literal-vs-dataset pixel-scale bug that this script hit after PyAutoArray#431
cleared the earlier 0.0-luminosity cause. Its `NEEDS_FIX` reason was rewritten to
name the new cause, and the entry was **deliberately left parked**.

## The gate

Un-park only when a capped run of THIS script exits 0:

```bash
PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 python3 scripts/multi_galaxy/features/scaling_relation/slam.py
```

Clear `output/<path>` **and** `output/test_mode/<path>` first. In test mode output
is namespaced under `output/test_mode/`, so clearing only the former leaves a stale
tree that fakes a green run as "Fit Already Completed" (gotcha recorded in
`complete/2026/08/small-datasets-loader-pixel-scales.md`).

Expected on a passing run: the script prints an enlarged mask radius of **~4.7**
(`0.5 * 16 * 0.6 - 0.1`), not the `0.30` of the bug report. If it still prints 0.30,
the fix did not take and this is a bug prompt, not a maintenance one.

## Why the gate is not optional

The #502 fix was shipped WITHOUT that capped run — the authoring session had no
numpy and no autolens, and, less obviously, green CI did not cover it either: none
of the eight scripts #502 touched appear in `smoke_tests.txt`, so the smoke job
never ran them. The fix is well-argued and is provably a no-op in uncapped
operation, but it is unexecuted on the path that actually matters.

`autolens_workspace` PR#312 un-parked `group/slam` as "PriorException fixed"
without re-running it. The failure resurfaced in the next scheduled Workspace
Smoke and cost a full cycle. That is the exact trap this gate exists to avoid, and
it has now been recorded twice. Do not un-park on the strength of a merged PR.

## Scope

One line in `config/build/no_run.yaml` (line 48 at time of filing). If the capped
run reveals a further latent fault, file a bug prompt instead and leave the park
in place with its reason updated.
