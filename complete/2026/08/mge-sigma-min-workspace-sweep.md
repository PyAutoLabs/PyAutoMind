# mge-sigma-min-workspace-sweep

- shipped: 2026-08-04 (both phases)
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/466 (closed completed 2026-08-04)
- phase-1-pr: autolens_workspace#467 -> `92019316`
- phase-2-prs: autogalaxy_workspace#203 -> `8a7df7a6` / HowToLens#67 -> `4ff3135c` / HowToGalaxy#61 -> `51eed3d6` / autogalaxy_assistant#10 -> `f6966a64`
- upstream: PyAutoGalaxy#549 -> `13d3023c`

## Outstanding at record time

**DEBT 2 of 2 is NOT discharged.** `markdown/` was never regenerated, so seven
curated pages still show MGE snippets without `sigma_min`. Deferred by explicit
human decision 2026-08-04, and split out so it survives this record:
`draft/docs/autolens_workspace/markdown_regeneration_sigma_min.md`. Do not read
this record as "everything is done".

DEBT 1 (autogalaxy_assistant baseline re-pin) and the RELEASE DEBT were both
discharged — see the entry below.

## Bookkeeping note

Written 2026-08-08 by the registry-integrity follow-up, not by `ship_workspace`
at merge time. The task shipped on 2026-08-04 and its tracking issue closed the
same day, but no `complete/` record was written and the entry sat on in
`active.md` -- the exact drift `lifecycle.py issues` now detects. The entry is
preserved verbatim below rather than summarised: it is dense with traps
(`baseline-repin-TRAP`, `gh-trap`, `smoke-trap`, `classification-trap`) that are
the point of keeping a rich record at all.

## Contemporaneous active.md entry (verbatim)

- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/466
- status: BOTH PHASES MERGED 2026-08-04. Phase 1 autolens_workspace#467 -> 92019316 (issue #466 auto-closed). Phase 2 autogalaxy_workspace#203 -> 8a7df7a6, HowToLens#67 -> 4ff3135c, HowToGalaxy#61 -> 51eed3d6, autogalaxy_assistant#10 -> f6966a64. Upstream PyAutoGalaxy#549 -> 13d3023c. All worktrees removed, all branches deleted local+origin, all five canonical checkouts back on main. Code work COMPLETE; two debts remain (below).
- phase-2-prs: autogalaxy_workspace#203 (28 files, `pending-release`) / HowToLens#67 (2 files, `pending-release`) / HowToGalaxy#61 (2 files, `pending-release`) / autogalaxy_assistant#10 (2 files, NO pending-release label — that repo does not define one, gate stated in the PR body instead). All four on branch feature/mge-sigma-min-workspace-sweep.
- phase-2-ci: THREE GREEN — agw#203, htl#67, htg#61 passed every check incl. both smoke matrix legs. aga#10 was MERGED WITH A RED wiki-currency check on explicit human instruction ("merge all"), failing `Version drift (--check-version)` ONLY — pre-existing, see DEBT 1. That red is now on autogalaxy_assistant main and persists for every future PR to that repo until the baseline is re-pinned.
- DEBT 1 of 2 CLEARED 2026-08-04 — assistant baseline re-pinned to the released 2026.8.4.1 stack via autogalaxy_assistant#11 (MERGED 9343e664). Regenerated in a CLEAN VENV with autogalaxy==2026.8.4.1, PYTHONPATH cleared and every module verified to resolve to venv site-packages — NOT from this workspace's source checkouts, which would have stamped the wrong version. Control-tested: old baseline exits 1 in that same venv (reproducing the CI failure), new one exits 0. All five wiki-currency checks pass on main. The re-pin surfaced a real API addition, `subplot_fit_imaging_list` in autogalaxy.plot (27 -> 28 symbols), which was undocumented — now documented in the same PR, and it corrected three stale claims incl. a pre-existing one about subplot_imaging_dataset_list's leaner signature. Original description follows: autogalaxy_assistant `wiki/core/api_audit_baseline.json` was generated 2026-08-01 pinning autogalaxy 2026.7.29.2; PyPI latest is now 2026.8.4.1 (released 2026-08-04). EVERY PR to that repo fails --check-version until the baseline is re-pinned. Proof it is not ours: the PR touches only 2 .md files, and symbol audit (--scope all) reports 0 missing/broken, provenance shows warnings only (no content_sha256 error), idioms clean.
- baseline-repin-TRAP: do NOT run `--write-baseline` from this workspace. It derives api_surface from the INSTALLED library, and local installs are the SOURCE checkouts (autogalaxy 2026.7.23.1), not the released 2026.8.4.1 that CI grades against — a local re-pin stamps the wrong version and turns the check green on a false premise. The re-pin must run against the released stack, as its own separate change.
- phase-2-result: autogalaxy_workspace 10 helper calls + 8 ladders; HowToLens 3 ladders (2 lens floored, 1 SOURCE -> -4, traced to source_bulge); HowToGalaxy 3 ladders all image-plane; autogalaxy_assistant 2 prose pages. Every autogalaxy_workspace MGE verified to attach to `galaxy = af.Model(ag.Galaxy, ...)` — PyAutoGalaxy has no lensing so no source plane exists to exclude. Validation: pyflakes zero introduced undefined names, 16/16 affected scripts pass smoke, notebooks regenerated 1:1 in all three repos with no orphan churn.
- assistant-provenance: wiki/core/concepts/linear_light_profiles_and_mge.md is provenance-stamped and a content_sha256 mismatch is a CI ERROR. Handled: added autogalaxy/analysis/model_util.py to the cited PyAutoGalaxy paths (where sigma_min lives), re-pinned PyAutoGalaxy 13d3023c + autogalaxy_workspace 1f821ba, bumped last_updated, re-stamped via `python3 autoassistant/audit_skill_apis.py --write-provenance`. Audit exits 0, 0 missing/broken. NOTE wiki-currency CI has paired-PR support — it checks out any cited source repo having a branch matching the PR head, so the paired autogalaxy_workspace branch is the grading ground truth.
- gh-trap: autogalaxy_assistant has an SSH remote, so `gh pr create` fails with "none of the git remotes ... point to a known GitHub host". Create its PRs via `gh api repos/<owner>/<repo>/pulls --method POST --input <json>` instead.
- assistant-false-positive: skills/ag_multi_dataset.md matches a `1e-4` grep but it is an intensity LogUniformPrior bound, NOT a sigma floor — deliberately untouched.
- RELEASE DEBT — DISCHARGED 2026-08-07 by publishing 2026.8.7.1 (all five libraries, PyPI). PROVEN, not inferred: downloaded the released `autogalaxy-2026.8.7.1-py3-none-any.whl` from PyPI and confirmed `sigma_min: float = 1e-4` in `autogalaxy/analysis/model_util.py` `mge_model_from` (+ the >0.0 / <=mask_radius guards). A user on a released install no longer hits TypeError. Original description follows: `sigma_min` existed only on PyAutoGalaxy main, NOT in any released PyAutoGalaxy; autolens_workspace main calls it, so released installs raised TypeError until a release carrying #549 shipped. The `pending-release` gate was overridden on explicit human instruction 2026-08-04 with that consequence stated — same pattern as the 2026-08-03 override recorded under release-drive-2026-08-03. Publishing was the remedy, not a preference.
- phase-1-result: 130 lens call sites take `sigma_min=dataset.pixel_scales[0] / 10.0`; 102 source sites untouched. 27 hand-rolled ladders: 10 image-plane floored, 17 source moved -2 -> -4. Classifier control-tested against the 88 explicitly-named sites first (88/88 agree, 0 disagree) before being trusted on the 143 bare `bulge` sites. Validation: 93 scripts byte-compile, pyflakes zero introduced undefined names across all 93, all 22 affected smoke scripts pass, notebooks regenerated 93-for-93 with no unrelated churn.
- heart-ack (2026-08-04): shipped under human-acknowledged YELLOW (score 70, `red_reasons: []`). Acknowledged reasons: (1) "workspace validation not passing (3 failed, 3 timeout, cloud#30858578587: autofit_test scripts/jax_assertions/multi_start_gradient_auto_convergence.py, autolens_test scripts/imaging/pixelization.py, autolens_test scripts/imaging/regularization.py, +3 more)"; (2) "manifest drift: tenant firewall (organ code) — 2 mismatch(es) vs PyAutoMind/repos.yaml"; (3) "release validation stale: source moved since rehearsal (PyAutoFit, PyAutoGalaxy, PyAutoLens)". None caused by this task; (3) is partly this day's own PyAutoGalaxy#549 merge. The ack covers THIS reason set only.
- OUTSTANDING DEBT 2 of 2 — markdown-DEFERRED (human decision 2026-08-04): markdown/ NOT regenerated. 7 of the 30 curated markdown_examples.yaml entries are among the changed scripts (start_here.py, imaging/start_here.py, imaging/modeling.py, multi_dataset/start_here.py, multi_dataset/modeling.py, group/start_here.py, group/modeling.py). generate_markdown.py refuses to run under PYAUTO_TEST_MODE (it executes scripts for real to render images) and a fresh worktree has no output/ resume cache, so a pass means real fits. Those 7 pages show snippets WITHOUT sigma_min until regenerated — outstanding debt, do not assume it is done.
- smoke-trap: the 3 scripts declaring `ENV: full_datasets` (group/, imaging/, multi_dataset/ start_here.py) FAIL with an unrelated IndexError (dataset capped to 16px vs a 209px mask) if run with PYAUTO_SMALL_DATASETS=1. Reproduced on pristine main, so it is a runner-env artefact, NOT a code bug — honour the in-file ENV declaration when smoke-running these.
- prompt: active/mge_sigma_min_workspace_sweep.md
- worktree: ~/Code/PyAutoLabs-wt/mge-sigma-min-workspace-sweep
- upstream: PyAutoGalaxy#549 MERGED 2026-08-04 (13d3023c) added `sigma_min` to `mge_model_from` (default 1e-4) and `mge_point_model_from` (default 0.01). Library defaults deliberately unchanged so archived runs keep their PyAutoFit identifiers — verified bit-identical across 1440 configs, and locked by a regression test in that PR. Nothing improves for users until the examples pass the argument; this task is that sweep.
- phases: 1 autolens_workspace (234 helper call lines + 23 hand-rolled ladder files — all the judgement) → 2 the mirror (autogalaxy_workspace, HowToLens, HowToGalaxy, autogalaxy_assistant prose). Phase 2 starts only once phase 1 merges.
- source-rule (human decision 2026-08-04): source-plane MGEs are EXCLUDED and keep the -4 default — the source is lensed, so magnification samples the source plane far finer than the image pixel scale and a pixel-scale floor would truncate real source structure. Only image-plane (deflector / galaxy light) MGEs take `sigma_min=dataset.pixel_scales[0] / 10.0`.
- classification-trap: this is NOT a regex sweep. Of 234 call lines: 59 explicitly source-named, 29 `lens_bulge`, 143 bare `bulge` needing per-call-site tracing to `lens=`/`source=af.Model(al.Galaxy...)`. scripts/multi_galaxy/modeling.py reuses the SAME name `bulge` for a lens galaxy (line 451) and the source (line 478) — a blind sweep wrongly ties ~100 source MGEs to the pixel scale.
- RESOLVED 2026-08-04 (was the one open question): hand-rolled SOURCE ladders move from -2 to -4, matching the helper they exist to teach. Human chose option 2. This DOES change behaviour in those ~10-14 tutorial sites — deliberately, since the files are pedagogical mirrors of `mge_model_from` and silently disagreeing with it is the inconsistency the sweep removes. Hand-rolled IMAGE-PLANE ladders still move to `np.log10(dataset.pixel_scales[0] / 10.0)`.
- out-of-scope this pass: autolens_workspace_test, autogalaxy_workspace_test, autolens_workspace_developer, autolens_profiling, euclid_strong_lens_modeling_pipeline — changed ladders change fit results there, needs separate re-baselining decision.
- sizing-note: Brain said too-large (16) and proposed design/core-API/examples/docs phases; NOT taken — score is prose-driven, the API shipped in #549, no design remains. Human-scoped 2-phase split by repo kept (point-source-defaults-campaign precedent).
- claim-released (2026-08-04): autolens_workspace dropped from `repos:` — phase 1 PR #467 MERGED, branch deleted on origin, canonical checkout back on main at 92019316. Phase 2 claims a different repo set and will register its own.
- repos-none-claimed: phase 2 has not started, so this entry claims NO repos — listed on this one line deliberately, NOT as 2-space `  - Repo` bullets, because worktree_check_conflict reads any such bullet as a live claim.

## Original prompt

# MGE examples: floor the smallest Gaussian at a tenth of the pixel scale (`sigma_min`)

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
- HowToLens
- HowToGalaxy
- autogalaxy_assistant
- autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal

## Original request (verbatim)

> Can you review this PR https://github.com/PyAutoLabs/PyAutoGalaxy/pull/549, I think we should
> update workspace exampels to make the input always log10(pixel_scale/10.0) but keep the default
> of -4

Clarified in session: the argument stays **linear** (`sigma_min`, as merged), because linear
arcsec reads better at the call site than a log10 value. "Keep the default of -4" means keep the
library default reproducing the old `1e-4` behaviour exactly — which #549 does, and which is
now locked by a regression test. The examples are what change.

Second clarification (verbatim):

> For sources, use the -4 default (if that was always used) for the lower bound, the source
> should not be tied to the dataset pixel scale due to lensing

Answering the parenthetical: yes, `-4` was always what source MGEs got. Every `mge_model_from`
call inherited the hardcoded `np.linspace(-4, ...)`, lens and source alike — no call site has
ever passed anything else, because until #549 there was no argument to pass. So leaving source
call sites untouched preserves exactly their current behaviour. (The 31 hand-rolled teaching
ladders are the exception: those were written at `-2`, so a source ladder among them is at `-2`
today and moving it to `-4` would be a change — flagged below.)

## Background

PyAutoGalaxy#549 merged 2026-08-04. It added `sigma_min` to `ag.model_util.mge_model_from`
(default `1e-4`) and, in the follow-up commit, to `mge_point_model_from` (default `0.01`).

The original bug: `mge_model_from` hardcoded `np.linspace(-4, np.log10(mask_radius), N)` while
its comment claimed the ladder spanned `0.01"`. So the basis always spent Gaussians ~2 dex below
the resolution of any real dataset.

**The library defaults are deliberately unchanged**, so that the fixed `sigma` values — and
therefore the PyAutoFit identifier of every archived run — stay bit-identical. Verified during
review: `np.log10(1e-4)` is exactly `-4.0` and `np.log10(0.01)` exactly `-2.0`, and a
model-by-model diff against the pre-PR code across 1440 configurations showed zero sigma
differences and zero identifier differences.

The consequence is that **nothing improves for users until the examples pass the argument**.
That is this task.

## Scope

In (user-facing surfaces):

- `autolens_workspace`, `autogalaxy_workspace`, `HowToLens`, `HowToGalaxy`
- ~116 `.py` files call `mge_model_from` / `mge_point_model_from`
- a further 31 files hand-roll the ladder inline for teaching purposes rather than calling the
  helper, currently `np.linspace(-2, ...)`. The upper bound cleanly separates plane:
  - `np.log10(mask_radius)` (43 occurrences) — image-plane lens/galaxy light → lower bound
    becomes `np.log10(dataset.pixel_scales[0] / 10.0)`
  - `np.log10(2.0 * pixel_scales)` (2) — the hand-rolled point-source MGE, image-plane → same
  - `np.log10(0.5)` (10) — **source plane**; these sit next to `source_bulge` and use a compact
    0.5" upper bound. Leave the lower bound alone per the source rule — but see the open
    question below, because they are at `-2` today, not `-4`
  - `np.log10(1.0)` (4) and `np.log10(-3, ...)` variants — resolve per file
- regenerate `notebooks/` and `markdown/` from `scripts/` afterwards
- assistant prose documenting the old floor: `autogalaxy_assistant/skills/ag_basis_profiles.md`
  states the ladder spans `0.01"`; sweep siblings in
  `autogalaxy_assistant/wiki/core/concepts/linear_light_profiles_and_mge.md` and the
  `autolens_assistant` equivalents

Out (this pass):

- `autolens_workspace_test`, `autogalaxy_workspace_test`, `autolens_workspace_developer`,
  `autolens_profiling`, `euclid_strong_lens_modeling_pipeline` — a changed sigma ladder changes
  fit results there, so those need re-baselining as a separate, deliberate decision.

## Preferred idiom

**Image-plane (deflector / galaxy light) MGEs only:**

```python
sigma_min=dataset.pixel_scales[0] / 10.0
```

Not a literal. `dataset` is in scope at every call site — including inside the SLaM pipeline
functions, which take it as an argument — and a literal pixel scale silently drifts from the
dataset it is supposed to describe. Note `pixel_scales` is a `(y, x)` tuple, hence the `[0]`.

Only ~17 of the caller files define a real `pixel_scale = <value>` variable; the overwhelming
majority pass `pixel_scales=0.1` as a keyword argument to `from_fits`, so a variable-based idiom
would not generalise.

## Source-plane MGEs keep the `-4` default (human decision)

**Source galaxies are NOT tied to the pixel scale.** The source is lensed, so magnification means
the source plane is sampled far more finely than the image-plane pixel scale — flooring a source
basis at a tenth of the image pixel scale would truncate real small-scale source structure that
the lensing actually resolves. Source MGEs therefore keep the existing `1e-4` default: **do not
pass `sigma_min` at a source call site at all.**

This makes the sweep a classification job, not a regex. The split in `autolens_workspace`
(234 call lines):

- 59 explicitly named source calls (`source_bulge`, `source_0_bulge`, `source_1_bulge`,
  `source_bulge_1`) — leave alone
- 29 explicitly named `lens_bulge` — take `pixel_scales[0] / 10.0`
- 143 bare `bulge = ...` — **ambiguous, must be classified per call site** by tracing which
  galaxy the variable is passed to (`lens=af.Model(al.Galaxy, ..., bulge=bulge)` vs
  `source=af.Model(...)`). Sampling the files that contain a bare `bulge`: 41 are source-only,
  2 lens-only, 16 contain BOTH, 12 match neither pattern.

The same file can reuse the name for both. `scripts/multi_galaxy/modeling.py` assigns
`bulge = al.model_util.mge_model_from(...)` at line 451 for a lens galaxy and again at line 478
for `source = af.Model(al.Galaxy, redshift=1.0, bulge=bulge)`. Any blind sweep gets this wrong.

`autogalaxy_workspace` and `HowToGalaxy` have no source plane at all — every MGE there is
image-plane light, so all of them take the pixel-scale floor.

`mge_point_model_from` stays pixel-scale-tied by construction: its upper bound is already
`2 * pixel_scales`, i.e. it exists to model something at the resolution limit.

## RESOLVED — hand-rolled source ladders move to `-4` (human decision 2026-08-04)

Option 2 below was chosen. The ~10-14 hand-rolled source ladders move from `-2` to `-4`, so a
hand-written source basis behaves identically to one built by `mge_model_from`. This is a
deliberate behaviour change in those tutorial files.

The original framing is kept below for the record.

## (was) OPEN QUESTION — hand-rolled source ladders sit at `-2`, not `-4`

The source rule says "keep the `-4` default, because that is what was always used". That is true
of every **helper** call site — none has ever passed anything but the hardcoded `-4`. It is NOT
true of the ~10-14 **hand-rolled** source ladders, which were written at `-2`.

So for those the instruction's own conditional does not resolve, and there are two defensible
answers:

1. **Leave them at `-2`** — preserves current behaviour exactly, changes nothing for anyone
   re-running a tutorial.
2. **Move them to `-4`** — makes a hand-written source basis behave identically to one built by
   `mge_model_from`. These files exist to teach what the helper does under the hood, so having
   them silently disagree with it is the inconsistency the sweep is meant to remove.

Recommendation: **(2)**, since these are pedagogical mirrors of the helper and the whole point of
the task is to stop the two surfaces disagreeing. Cheap to reverse either way. Needs a human
answer before phase 1 touches these specific files; everything else in phase 1 is unblocked.

## Notes / risks

- This **does** change fit results in the examples — that is the point of the task, but it means
  any script whose expected output is pinned needs checking.
- `mask_radius` is a local float in most scripts (often `3.0`); `sigma_min` must stay below it or
  `mge_model_from` raises. At a tenth of a typical `0.1"` pixel scale (`0.01"`) that is never
  close, but the group/cluster scripts with small mask radii are worth a glance.
- Verify the smoke-test surface still passes; several of these scripts are in the CI smoke set.
