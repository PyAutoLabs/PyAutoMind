# Resolve release-profile timeout scripts deliberately

Type: bug
Target: health_fixes
Themes:
- release
- ci-smoke
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-07-06 (backfilled from git)

## 2026-08-09 — 1 of the 5 is resolved via § Required work option 3b

Checked by the draft/ sweep against the two workspaces' `config/build/no_run.yaml` on
main. The prompt's item 3 offers an explicit fork per script — optimize below the cap,
**or** add a documented `SLOW` entry. One script has taken the second branch:

- **`autolens_workspace/scripts/cluster/start_here.py` — PARKED.**
  `- cluster/start_here # SLOW 2026-07-22 - hits the full 1800s mode=release cap in
  workspace-validation (PyAutoHeart run 29912642195). Script-specific…` That is exactly
  the documented-parking outcome this prompt asks for, decided after it was filed.

The other four are **not** in either `no_run.yaml`:

- `autogalaxy_workspace/scripts/ellipse/multipoles.py`
- `autolens_workspace/scripts/cluster/modeling.py`
- `autolens_workspace/scripts/imaging/features/advanced/double_einstein_ring/chaining.py`
- `autolens_workspace/scripts/multi/features/slam/simultaneous.py`

Which means either they were optimized under the cap, or the decision was never taken.
**This sweep cannot tell which** — item 1 requires benchmarking from a clean output tree,
which needs a real run. Do not read "absent from no_run.yaml" as "optimized"; that is the
same unproven inference the prompt's item 4 warns against.

One caution for whoever picks this up: the caps themselves moved. This prompt is written
against a **300s** cap, while the 2026-07-22 parking above cites an **1800s
`mode=release`** cap. Re-establish which cap applies to each script before benchmarking,
or the numbers will not mean what the prompt assumes.

---

## Context

Five scripts exceeded PyAutoHands's 300-second per-script cap in release run
`28784914443`. A timeout is a release-surface policy decision, not automatically a code
bug. Stateful local reruns are not authoritative because completed search output can make
chained scripts resume quickly.

Owners: @autogalaxy_workspace, @autolens_workspace, @PyAutoFit, @PyAutoGalaxy,
@PyAutoLens, and @PyAutoHands where runner evidence is needed.

## Scripts

- `autogalaxy_workspace/scripts/ellipse/multipoles.py`
- `autolens_workspace/scripts/cluster/start_here.py`
- `autolens_workspace/scripts/cluster/modeling.py`
- `autolens_workspace/scripts/imaging/features/advanced/double_einstein_ring/chaining.py`
- `autolens_workspace/scripts/multi/features/slam/simultaneous.py`

## Required work

1. Benchmark each script from a clean output tree with the exact release profile and
   record phase-level timing. Confirm whether it completes correctly beyond 300 seconds.
2. Investigate avoidable repeated compilation, plotting, search, dataset, and chaining
   costs without reducing the scientific/tutorial contract.
3. For each script choose explicitly between:
   - optimize it to fit reliably below the cap; or
   - add a documented `SLOW` entry to that workspace's `config/build/no_run.yaml` because
     it is unsuitable for automated release validation.
4. Do not silently raise the global cap. Do not use cached outputs as pass evidence.
5. Validate optimized scripts from clean state or validate that the runner reports the
   chosen scripts as skipped with their documented reasons.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## 2026-08-21 — REPRODUCTION GATE RUN: **4/4 measured live scripts pass far under the cap**

Method (identical to the gate that closed the sibling `autofit_sampler_database`, PyAutoFit#1508):
every script run from a **cleared** `output/`, under its workspace's
`config/build/profile_release.yaml`, env resolved by `autohands.env_config.build_env_for_script`
at workspace CWD, 1800s `mode=release` cap. Libraries at `main`: PyAutoFit `248ca971f`,
PyAutoArray `b808a9b1`, PyAutoGalaxy `7e3856dd`, PyAutoLens `d8f6bb3df`, PyAutoNerves `f6d6d52`.
Three workspace checkouts were **behind `origin/main`** and were synced first.

| Script (resolved path) | Result | Secs | vs 1800s cap |
|---|---|--:|---|
| `autogalaxy_workspace/scripts/ellipse/multipoles.py` | PASS | 102 | 6% |
| `autolens_workspace` `imaging/features/advanced/double_source_plane_lens/chaining.py` | PASS | 444 | 25% |
| `autolens_workspace` `multi_dataset/features/slam/simultaneous.py` | PASS | 426 | 24% |
| `autolens_workspace/scripts/cluster/modeling.py` | PASS | 90 | 5% |
| `autolens_workspace/scripts/cluster/start_here.py` *(parked)* | **NOT MEASURED** | — | — |

`start_here.py` was **operator-stopped at 754s** (SIGTERM, `rc=-15`) — neither a pass nor a
failure. Left unmeasured deliberately: it is already parked `SLOW 2026-07-22`, and this prompt's
own § "1 of the 5 is resolved via option 3b" records that documented parking as its resolved
outcome, so its runtime changes no conclusion here.

**No timeout policy decision is owed on the other four** — none is close to the cap.

**One latent trap, flagged not acted on:** `chaining.py` (444s) and `simultaneous.py` (426s) clear
the 1800s `mode=release` cap comfortably but would blow a **300s** cap. Neither is parked, so any
runner that applies a 300s budget to them will see timeouts that are budget artifacts, not defects.

### Script-path corrections (three renames, verified on disk 2026-08-21)

The tables in this folder have drifted **again** since the 2026-08-09 sweep. All paths resolve;
a 404 here still means drift, never deletion.

- `scripts/jax_likelihood_functions/<dataset>/X.py` -> `scripts/<dataset>/jax_likelihood/X.py`
- `scripts/<dataset>/modeling_visualization_jit.py` -> `scripts/<dataset>/visualization/modeling_visualization_jit.py`
- `scripts/multi/...` -> `scripts/multi_dataset/...`  (this one bit `slam/simultaneous.py`, still
  listed under `multi/` above)
- `double_einstein_ring` -> `double_source_plane_lens`  (autolens_workspace#394) — so
  `imaging/features/advanced/double_einstein_ring/chaining.py` is now
  `imaging/features/advanced/double_source_plane_lens/chaining.py`
