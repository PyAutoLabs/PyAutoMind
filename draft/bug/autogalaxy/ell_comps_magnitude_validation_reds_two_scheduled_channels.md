# `ell_comps` magnitude validation REDs the workspace-smoke and python-matrix channels

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Two scheduled channels that the 2026-08-16 wake-up digest reported as three separate red jobs are
in fact **one bug**. Both went red on the same night (2026-08-10) with the same exception:

```
ValueError: ell_comps must satisfy ell_comps[0]**2 + ell_comps[1]**2 < 1;
got (-0.5678625545794941, -0.8616414011084582), whose magnitude is 1.0319369094075934.
```

Affected runs:

| Channel | Repo | Run | Failing script |
|---|---|---|---|
| `python_matrix.yml` | PyAutoHands | 31356134172 | `multi_galaxy/features/pixelization/adaptive.py` (autolens_workspace, py3.13 **and** 3.14) |
| `workspace-smoke.yml` | PyAutoHeart | 31356506626 | `autogalaxy/guides/results/*` (see cascade below) |

The workspace-smoke leg shows the shape of the failure clearly — three primary raises plus a
downstream cascade once the fits produce no result:

```
scripts/guides/results/database/start_here.py      FAIL  ValueError: ell_comps ...
scripts/guides/results/_quick_fit.py               FAIL  ValueError: ell_comps ...
scripts/guides/results/aggregator/samples.py       FAIL  ValueError: ell_comps ...
scripts/guides/results/start_here.py               FAIL  CalledProcessError (_quick_fit.py above)
scripts/guides/results/aggregator/data_fitting.py  FAIL  AttributeError: 'NoneType' has no 'galaxies'
scripts/guides/results/aggregator/models.py        FAIL  AttributeError: 'NoneType' has no 'galaxies'
scripts/guides/results/aggregator/samples_via_aggregator.py  FAIL  AttributeError: 'NoneType' ...
```

The `NoneType` failures are **secondary** — the aggregator scripts have no fit to read because the
fits above them raised. Fixing the `ell_comps` raise should clear all seven.

## What to decide

The magnitudes are only marginally over 1 (1.03 in the case above), and the values differ run to
run, so this is a **sampler draw landing outside the valid geometry**, not a fixed bad literal in a
script. The real question is what should happen when a search proposes such a point:

1. the prior/parametrisation should make an invalid `ell_comps` undrawable in the first place; or
2. an invalid geometry should be rejected as a zero-likelihood sample rather than raising, so the
   search walks away from it; or
3. the validation is correct and the workspace scripts' priors are too wide.

That is a scientific-correctness call, not a mechanical fix — hence `Autonomy: supervised`. Start by
finding where the message is raised (grep the literal `ell_comps must satisfy` in PyAutoGalaxy) and
when it was introduced; the channels were green on 2026-08-03 and red on 2026-08-10, so the
regression window is that week.

**Read the adjacent work first — this boundary is already under active study.**
`draft/research/autolens_profiling/ell_comps_trapping_unmasked.md` characterises searches getting
*stuck against this same `ell_comps` support boundary* (667 of 2400 lane-steps constrained, 27.79%,
once prior-exit deaths were removed), and `complete/2026/08/prior-support-clipper.md` shipped
PyAutoFit#1477 on 2026-08-16 for prior support handling. Options (1) and (2) above may already have
a mechanism there rather than needing a new one. Note the clipper shipped *after* the 2026-08-10
red, so it is not the cause — but it is very likely part of the answer, and the two tasks should not
be worked in ignorance of each other.

## Not part of this task

The third red job in the same digest — `wiki-currency.yml` on autolens_assistant — is **unrelated
and is not a code failure**. Run 31125208913 died in `actions/checkout` with
`fatal: couldn't find remote ref refs/pull/110/merge`; the workflow is `pull_request`-triggered
(not scheduled) and PR #110's merge ref no longer resolves. Nothing to fix in the repo; it clears
on the next PR run.
