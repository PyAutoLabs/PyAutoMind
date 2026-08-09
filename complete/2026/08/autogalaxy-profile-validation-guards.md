Phase 2 (PyAutoGalaxy half) of the @rhayes777 API audit. Four findings on
[PyAutoGalaxy#440](https://github.com/PyAutoLabs/PyAutoGalaxy/issues/440) — B9, B10,
B11, B12 — plus the negative-redshift half of PyAutoLens#532, which turned out to
live in this repo.

**Shipped:** PyAutoGalaxy#566, squash-merged `a366f77` 2026-08-09. #440 closed.
Epic PyAutoArray#415 stays open for phase 4.

## Delivered

| Finding | Guard site | Reach beyond the report |
|---|---|---|
| B9 `scale_radius` ≤ 0 | 5 assignment sites (`AbstractgNFW`, `cNFW` ×2, `KaplinghatCoredNFWSph`, `YangSIDMSph`) | 29 dark profile classes, not just `NFW` |
| B11 `sersic_index` ≤ 0 | both `AbstractSersic` bases (light + stellar mass) | the mass Sersic too, not just the light one |
| B12 `ell_comps` outside unit circle | **one** call at `EllProfile` | every elliptical light *and* mass profile — `ell_comps` has exactly one assignment site in the codebase |
| B10 Ell/Sph agreement | tolerance regression tests | deflections, convergence **and** potential |
| #532 negative redshift | `Galaxy.__init__` | see the ownership note below |

## The #532 ownership call

The negative-redshift finding was filed on **PyAutoLens**#532 because the reporter
reached it via `al.Galaxy`. But `al.Galaxy` **is** `ag.Galaxy` — the class and its
`redshift` assignment live at `autogalaxy/galaxy/galaxy.py:52`. A `Tracer`-level check
would have missed a bare `al.Galaxy(redshift=-0.5)`, which is the reported
reproduction. So the guard landed here and the `Tracer(galaxies=...)` half stayed in
PyAutoLens (#696). Both PRs cross-reference the split.

**Lesson for the remaining audit work:** the repo an issue is *filed on* is where the
user hit it, not necessarily where the attribute is set. Check the assignment site
before scoping.

## Found beyond the audit — Ell/Sph potential disagreement

B10 asked for a tolerance pin on the `Isothermal(ell_comps=(0,0))` vs `IsothermalSph`
deflection difference (`2.357e-06`). While pinning it I measured the other two
quantities, which the report never did:

| Quantity | max abs diff | relative |
|---|---|---|
| deflections | 2.357e-06 | 2.36e-06 |
| convergence | 1.207e-05 | 1.45e-06 |
| **potential** | **5.375e-03** | **1.95e-03** |

**The potential agrees three orders of magnitude worse.** These two are analytically
identical, so that is a real discrepancy, not just numerical noise.

It is **not fixed** — out of scope for B10 as filed. Its tolerance is pinned at the
observed level as an explicit *ratchet*, with a docstring saying exactly that, rather
than folded into a loose bound that would hide it. Flagged in the PR body.

Possibly the same class as `draft/bug/autogalaxy/nfw_truncated_potential_accuracy.md`
(MGE-based potential accuracy) — worth checking together.

## Validation

- Full suite **1080 passed / 1 skipped**, **+36 new tests**
  (`test_autogalaxy/profiles/test_validate.py`). CI green on 3.12, 3.13 and docs.
- **Zero regressions.** No existing test relied on a degenerate profile construction —
  the same surprise as the #333 task.
- Guards delegate to `autoarray.validate` and are tracer-safe by the same gate.

## Phase-4 guard-rail added deliberately

`z_lens > z_source` stays HELD pending the reporter's answer. Rather than leaving that
implicit, a control test now pins today's permissive behaviour at `Galaxy` level (and
another at `Tracer` level in PyAutoLens#696), so phase 4 cannot quietly turn it into an
error.

## Process note

`black` (newer than the repo's formatting) reflowed unrelated code in two files on
first run. Reverted and re-applied the guards by hand so the diff stayed purely
additive. Worth pinning a black version if formatting is ever automated here.

## Original prompt

# PyAutoGalaxy#440: light & mass profile validation guards (+ the B10 tolerance test)

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Why this exists

[PyAutoGalaxy#440](https://github.com/PyAutoLabs/PyAutoGalaxy/issues/440), filed
2026-05-23 by @rhayes777 auditing released `2026.5.21.1`. Four findings — B9,
B10, B11, B12 — re-verified against `main` on 2026-07-28, **all four still
reproduce**. Answered on the issue 2026-07-28 (`#issuecomment-5105855357`);
tracking epic is
[PyAutoArray#415](https://github.com/PyAutoLabs/PyAutoArray/issues/415).

## Depends on the PyAutoArray helper

Three of the four findings (B9, B11, B12) are constructor guards and **must use
the shared `_validate_*` helper defined by
`draft/bug/autoarray/rhayes_333_input_validation_guards.md`**. Start that prompt
first, or reimplement the same rule here with a different message and hand users
inconsistent errors for the same mistake. B10 is independent and can proceed
either way.

## Scope — four findings

| ID | Surface | Today | Wanted |
|---|---|---|---|
| B9 | `mp.NFW(scale_radius=0.0)` | accepted; `deflections_yx_2d_from` returns all-NaN (3200 of 3200 on a 40x40 grid) | `ValueError` — `scale_radius` must be `> 0` |
| B11 | `lp.Sersic(sersic_index=0.0)` | `ZeroDivisionError` from deep inside the profile on `image_2d_from` | `ValueError("sersic_index must be > 0")` from the constructor |
| B12 | `lp.Sersic(ell_comps=(2.0, 0.0))` | accepted; returns a finite non-physical image (sum `1296.0498`) | `ValueError` — `e1**2 + e2**2 < 1` is the definition of a valid axis ratio; outside it `q` is undefined |
| B10 | `mp.Isothermal(ell_comps=(0, 0))` vs `mp.IsothermalSph` | `max|diff| = 2.357e-06` — analytically identical, numerically not | a regression test pinning an **explicit tolerance** |

B12's `ell_comps` guard is the one with the widest blast radius: it belongs on
every elliptical profile, not just `Sersic`. Prefer a single shared
`_validate_ell_comps()` called from the elliptical base, or a slot-level
validator if the profiles are already `attrs`/`pydantic` dataclasses — not a
copy per subclass.

## B10 is a test, not a fix

**Do not chase bit-identity** between the elliptical and spherical evaluation
paths. The `Ell` form goes through a slightly different evaluation route even at
the degenerate point; `2.357e-06` is not load-bearing for science. Pin it at an
explicit tolerance so a future refactor that makes it materially worse is caught.
The epic files B10 under phase 3 rather than phase 2 — it rides here because it
lives on this issue and in this repo, and it needs no helper.

## Binding constraint — JAX

Profile constructors sit on **JAX-traced** paths. Guards must stay correct under
tracing and cost nothing when traced: no Python `if` on a value that may be a
tracer. Use the tracer-safe form settled in the PyAutoArray prompt.

## Verification

- Regression test per finding, built from the reporter's own snippets (the issue
  body is self-contained).
- Assert the message names the offending parameter.
- Controls that must keep passing: `NFW` with a positive `scale_radius`, `Sersic`
  at a normal `sersic_index`, and `ell_comps` inside the unit circle.
- Library unit tests stay **numpy-only** (no JAX).

Repro gotchas: run from a workspace root with
`PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`, `NUMBA_CACHE_DIR=/tmp/numba_cache`,
`MPLCONFIGDIR=/tmp/matplotlib`, `PYAUTO_DISABLE_JAX=1`.

## Out of scope

Everything not on #440 — the PyAutoArray guards, the `adapt_images` precondition,
and the `Tracer` guards each have their own prompt.

## Do not route to `start_dev_for_user`

The reporter's PR offer was declined warmly on 2026-07-28 (JAX-traced hot paths).
We implement in-house.

## Provenance

- Epic: PyAutoArray#415 (open — phases 2-4)
- Campaign prompt: `draft/bug/autoarray/rhayes_audit_validation_and_crashes.md`
- Registry: `planned.md` § `rhayes-audit-validation-phases-2-4`
- Note in `planned.md`: PyAutoGalaxy was **not yet claimed** by this campaign as
  of 2026-07-28 — this prompt is the claim.
