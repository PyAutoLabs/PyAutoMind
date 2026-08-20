- library-prs: https://github.com/PyAutoLabs/PyAutoFit/pull/1477
- merge-commits: PyAutoFit `1f4b66a937e0012a99b078b1c8b85c52aaac7f0d` (2026-08-16)
- issue: PyAutoFit#1476 (closed by the PR)
- summary: Shipped `AbstractClipper` / `ClipperNone` / `ClipperPriorBox` in
  `autofit/non_linear/clipper.py`, the search-agnostic prior-support enforcement
  the `mge-lane-death` investigation (autolens_profiling#128) asked for. Phase 1
  of three; phase 2 is `draft/feature/autofit/clipper_validation_campaign.md`.
- validation: 22 tests, CI green on 3.12 / 3.13 / docs, plus the out-of-suite
  verification logged below.
- release: not performed; merged PR remains in the pending-release queue.

> **CONSOLIDATED 2026-08-16.** Two sessions independently wrote a completion
> record for this task. This file is the union. The detailed body below —
> the bound-kind design decision, the eight measured traps, the process lesson,
> the verification log and the phase-2 harness traps — comes from the session
> that actually shipped PyAutoFit#1477 (PyAutoMind#189, closed in favour of this
> file). The "What shipped after" section is from the session that did the
> follow-up work. Nothing was dropped in the merge.

Shipped the search-agnostic `Clipper` — prior-support enforcement for the
gradient searches, as the pluggable sibling of `Initializer`. This is follow-up
(1) owed by the `mge-lane-death` investigation (autolens_profiling#128), which
found the MGE lane deaths are the **prior** term, not the likelihood.

- issue: PyAutoFit#1476
- pr: PyAutoFit#1477, **MERGED** 2026-08-16 as `1f4b66a` (squash), +798/-3 over
  7 files. Full CI green on both runs (`unittest` 3.12, `unittest` 3.13,
  `docs / docs-build`).

## What shipped

`AbstractClipper` / `ClipperNone` / `ClipperPriorBox` in a new
`autofit/non_linear/clipper.py`, wired **opt-in** into the two exposed searches:
`AbstractMultiStartGradient` projects after `optax.apply_updates`; `AbstractBFGS`
hands box bounds to scipy (`L-BFGS-B` supports them natively — they were simply
never passed). `project` returns the clipped **mask** as well as the vector, so a
caller can zero optimiser momentum along clipped directions.

Default is `ClipperNone` and the PR is **bit-identical** with it. Flipping the
default is PR 2 — `draft/feature/autofit/clipper_validation_campaign.md`, now
unblocked.

## The design decision worth remembering: inset by BOUND KIND, never by width

The obvious implementation, one relative `margin * (upper - lower)`, is wrong in
two separate and silent ways. Both stem from computing the width unconditionally.
Three cases instead:

| Bound kind | Example | Inset |
|---|---|---|
| two-sided finite | Uniform, LogUniform, TruncatedGaussian | relative `margin * width` |
| unbounded | Gaussian | **none, and no width arithmetic at all** |
| half-open, exclusive | LogGaussian's `0` | absolute `strict_epsilon` |

And note the two-sided margin is **not** for prior support — measurement showed
those bounds are *inclusive* (`UniformPrior.log_prior(2.0) = 0.0`,
`TruncatedGaussian.log_prior(1.0) = -0.5`), so `margin=0` would be valid. It
exists to avoid parking a lane exactly **on** a prior edge, where the model's own
transforms are singular — the same reason the broad-start band defaults to the
interior `(0.15, 0.85)` rather than `(0, 1)`.

## Traps, all measured against a running install

1. **The naive margin turns every unbounded prior into `NaN`.** `-inf + (inf -
   -inf) * m` is `NaN`, and clipping against `NaN` bounds destroys the coordinate
   and the whole objective (`sum(log_prior) = nan`). This would have made the
   feature **actively harmful** on exactly the models it targets — the MGE
   reference model carries `GaussianPrior`s — with a symptom indistinguishable
   from the bug being fixed. Every bit-identity test still passes against it,
   because `ClipperNone` never computes a margin.
2. **scipy reads `bounds=(lower_array, upper_array)` as a sequence of `(min,
   max)` PAIRS.** At n=2 it returns a silently wrong fit (`[0.,1.]` where the
   answer is `[1.,1.]`), no error, no warning; at every other n it raises
   `ValueError`. So it fails loudly for most models and silently for
   two-parameter ones. Build an explicit `optimize.Bounds`. This was the
   *prompt's own* specified return type.
3. **`LogGaussianPrior` misreports its own support.** Its `TransformedMessage`
   defaults limits to `±inf` and is never passed any, yet `log_prior_from_value`
   is `-inf` for `value <= 0`. Declared in the clipper, prior class untouched.
4. **Plain `BFGS` does not reject bounds — it IGNORES them** behind a
   `UserWarning` and returns the unconstrained optimum. "Guard or warn" is too
   weak; raise.
5. **`prior.lower_limit` resolves for every prior type** via `Prior.__getattr__`
   delegating to the message (`AbstractMessage` defaults `±inf`). No type switch
   needed — except for trap 3.
6. **The NumPy and JAX paths disagree on support.**
   `UniformPrior.log_prior_from_value` is `if xp is np: return 0.0` —
   unconditional, no bound test. Only the JAX branch walls off the box, so LBFGS
   is exposed only in its `analysis._use_jax` branch.
7. **float32 makes the box check asymmetric.** `2.0000001` is not representable
   distinctly from `2.0` and reads as in-box, while `-1e-7` against a lower bound
   of `0.0` is caught. A test asserting "overshoot is detected" must use a bound
   near zero or float64, or it passes vacuously.
8. **The `AbstractMultiStartGradient` class docstring was factually wrong** —
   claimed the rule steps "on the unconstrained (unit-cube) parameterization"
   while `_broad_starts` maps draws to physical. That is the sentence that would
   tell the next reader this class of bug cannot exist. Corrected.

## The process lesson: a green suite is not coverage

The first commit shipped an **undefined `optimize` in `LBFGS._fit`** — any real
`LBFGS.fit()` raised `NameError`. The **full 1790-test suite passed against it**,
because nothing in the library suite ever executes an LBFGS fit. It was caught
only by a randomised end-to-end stress run, after the code was already pushed.
Fixed in the second commit with a smoke test that runs a real `LBFGS.fit()`,
verified to fail with exactly that `NameError` if the import is removed again.

When a change touches a path, check whether anything actually *executes* it
before trusting the suite.

## Verification performed (beyond the committed tests)

- **Bit-identity 10/10 on both searches** across randomly generated models mixing
  every prior type — `no clipper arg` vs explicit `ClipperNone`.
- **Core promise 8/8** — with `ClipperPriorBox`, final `sum(log_prior)` finite
  every time, lane deaths **0 in every case** vs 62–96 without.
- **End-to-end**: Gaussian fit with the truth outside the box, lane deaths
  **249 → 0** with 252 clips; the clipped run pins `centre` at the upper bound,
  which is the correct MAP answer under a prior excluding the truth, and an
  independent reproduction of the momentum pinning.
- **Guards verified by inversion** — patching back to the naive width form makes
  5 tests fail, including both named regression guards.
- **Resume path** — a `search_internal` lacking `n_clipped_lane_steps` resumes
  without `KeyError`.
- **Identifiers unchanged** — real fits produce a single identifier dir shared by
  `no clipper` / `ClipperNone` / `ClipperPriorBox`, so existing on-disk results
  are not orphaned. Flip side: two runs differing only in clipper currently
  COLLIDE on one output dir — matters for PR 2's re-baseline.

## Harness traps that cost time (for whoever writes the PR 2 measurements)

- **`.completed` marker short-circuits `fit()`** — a resumed or re-run search
  returns the cached result without entering `_fit`. Three successive versions of
  a resume test "passed" while testing nothing. Also bites when a script is
  re-run with stale output from its previous execution.
- **`fit()` rebuilds `search.paths`**, so an instance-level monkeypatch on
  `paths.save_search_internal` is silently discarded. Patch at CLASS level.
- **The search_internal folder is deleted on successful completion**, so it
  cannot be read back after the fit — capture it as it is written.
- **Two identically-constructed searches did not resolve to the same identifier
  dir**, so "resume" silently started fresh. The reliable method is patching
  `DirectoryPaths.load_search_internal` at class level.
- **Seed `random` AND `numpy` before every fit** — the initializer draws from
  both, and an unseeded comparison reports a spurious bit-identity mismatch.
  (This produced one false alarm on the bit-identity gate.)
- **A box containing the optimum never exercises the clipper.** The first
  efficacy attempt measured 0 clips for exactly this reason; put the truth
  outside the box.

## Corrections issued

`test_nautilus.py::test__single_core_builds_no_pool` **passes in CI**. It failed
only in the local py3.12 venv used for verification. It was correctly identified
as not caused by this task (verified by stashing), but was wrongly described as
"pre-existing on clean main" in an earlier revision of the PR body and in the
`active.md` notes; both were corrected.

## Follow-ups owed (filed, not fixed)

1. `float32` is not JSON serializable in result output —
   `autofit/non_linear/paths/directory.py:80` `save_json` raises `TypeError` at
   the end of a successful clipped run. Surfaced only because clipping let lanes
   survive onto a code path this cell had never taken.
2. A crashed run poisons the next run of the same name: the half-written output
   from (1) makes the next search with the same `name` fail with
   `JSONDecodeError` while resuming — a 4-second no-op that *looks like* a clean
   result. A new form of the cached-result hazard in
   `complete/2026/08/multistart-nan-step-diagnostics.md`.
3. Declare `LogGaussianPrior`'s `(0, ∞)` support on the prior itself, retiring
   the clipper's special case.
4. Decide whether the clipper should enter the search identifier — relevant to
   PR 2's benchmark re-baseline (see "Identifiers unchanged" above).
5. **NUTS remains out of scope** — HMC entering a `-inf` region diverges rather
   than freezing. Different mechanism, its own task.

## Repos / worktree

- PyAutoFit: `claude/autofit-clipper-prior-support-o3jotv` (merged, deletable).
- No worktree was created — this ran in a cloud session from a direct clone at
  `/workspace/pyautofit`.

## What shipped after this record was first written

Three further PyAutoFit PRs landed the same day, all merged, all **unreleased**.
Anything running against a PyPI wheel has none of them.

| PR | merge | what |
|---|---|---|
| #1478 | `bbceff6` | `Clipper`, `Clipped Lane-Steps`, `Clipped Lane-Step Rate` and `Constrained Lane-Steps` reported in `search.summary` |
| #1479 | `b6e89cd` | `NumpyEncoder` — closes follow-up 1 below (the `float32` `save_json` crash) |
| #1480 | `5c9244b` | atomic writes + corrupt-resume recovery — closes follow-up 2 below |

So **follow-ups 1 and 2 in the list below are now FIXED**; they are left in place
because the reasoning that found them is the record. Their own records are
`complete/2026/08/save-json-numpy-scalar-typeerror.md` and
`complete/2026/08/crashed-run-poisons-resume.md`. Follow-ups 3, 4 and 5 remain
open and 3 and 4 were filed as prompts:
`draft/bug/autofit/loggaussian_prior_declares_own_support.md` and the
identifier question — the latter **shipped 2026-08-18** (PyAutoFit#1493 /
#1494, the clipper now enters the MLE identifiers; record
`complete/2026/08/clipper-in-search-identifier.md`).

Two corrections that came out of doing that follow-up work:

- **Follow-up 2's symptom was misdescribed.** Both records originally said the
  poisoned rerun is "a 4-second no-op that looks like a clean result". That
  **did not reproduce**. What reproduces is a hard `JSONDecodeError` on every
  rerun of the same search name. The no-op variant presumably needs a surviving
  `search_internal` whose restored `total_steps` short-circuits the loop — and
  the crash path deletes that directory first, as noted under the harness traps
  above. Do not cite the no-op as observed.
- **`n_clipped_lane_steps` was already in `search_internal` but nowhere else.**
  #1478 carried it into `samples_info` and `search.summary`, and found that
  `n_constrained_lane_steps` — PyAutoFit#1475's trapped-lane counter — had
  reached `samples_info` when it shipped but was never printed, so it had been
  invisible in `search.summary` all along.

On the `test_nautilus.py::test__single_core_builds_no_pool` question raised under
"Corrections issued" above: it is now confirmed from both sessions. It **passes
in CI** and fails in local venvs on both 3.12 and 3.13, with the failure
reproducing on a stashed clean tree. So "not caused by this work" is right;
"pre-existing on clean `main`" is the wrong gloss, and the PR bodies for #1479
and #1480 use that looser phrasing. Read it as environment-specific.

## Original prompt

# Search-agnostic prior-support enforcement: a Clipper class

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Why

`@PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py` builds
its objective as

```
fom = -2 * (log_likelihood + sum(log_prior_list))
```

A `UniformPrior` returns `log_prior = -inf` outside its box, and the search steps
in **physical** parameter space with nothing constraining it to that box. A lane
that oversteps a hard prior edge reads as non-finite, is marked dead, and with
`resurrect=False` is never redrawn.

Measured on the real `imaging/mge` profiling cell (16 starts x 150 steps, cloud
CPU) — full investigation and evidence in autolens_profiling#128:

| arm | value-NaN lane-steps | lanes dead | alive at end |
|---|---:|---:|---:|
| baseline | 1446 (60.25%) | 14/16 | 2 |
| shear box widened to ±1 | 1422 (59.25%) | 15/16 | 1 |
| prior term neutered (diagnostic) | 215 (8.96%) | 3/16 | 13 |
| **clip to prior box (prototype)** | **425 (17.71%)** | **5/16** | **11** |

**The likelihood never went non-finite** in ~7200 lane-steps. This is entirely a
prior-support problem.

The behaviour is worse than "frozen": the overshoot is tiny (median 3% of box
width, min 0.21%), and because `log_prior = -inf` is *constant* outside the box
its derivative is zero, so the total gradient is the finite **likelihood**
gradient. `optax.apply_if_finite` therefore never fires and the dead lane **keeps
stepping forever** — full likelihood-and-gradient cost every step, output
discarded, wandering far (one parameter went `0.30 -> -1.76`). 0/16 lanes ever
revive.

## The exposure is not MultiStart-only

This is why the fix should not live inside one search:

- **`MultiStartGradient`** (`MultiStartAdam` / `MultiStartADABelief` /
  `MultiStartLion` / `MultiStartProdigy` all share one `_fit`) — measured above.
- **`@PyAutoFit/autofit/non_linear/search/mle/bfgs/search.py`** — same
  `Fitness(fom_is_log_likelihood=False, resample_figure_of_merit=-np.inf,
  convert_to_chi_squared=True)`, steps in physical space, and calls
  `optimize.minimize(fun=..., x0=..., method=self.method, options=..., tol=...)`
  with **no `bounds=` argument**. `L-BFGS-B` supports box bounds natively; they
  are simply not passed. Being single-start, this presents as a failed fit rather
  than a population collapse, so it is easier to misattribute.
- **NUTS** (`@PyAutoFit/autofit/non_linear/search/mcmc/blackjax/nuts/search.py`)
  also targets the log posterior from a physical `initial_position`. HMC entering
  a `-inf` region *diverges* rather than freezing. **Out of scope here** — different
  mechanism, needs its own investigation. See "Deliberately out of scope".

Not exposed, and correctly so: the nested samplers already work in unit-cube
coordinates, and the MCMC samplers reject `-inf` proposals so the walker stays
put. **Rejection is the restoring mechanism that gradient methods lack.**

> **CORRECTION (2026-08-18, PyAutoFit#1489):** the MCMC sentence above was FALSE
> when this record was written. On the NumPy path there was no `-inf` to reject:
> `UniformPrior.log_prior_from_value` returned `0.0` unconditionally after
> release 2025.10.16.1 removed `assert_within_limits`/`PriorLimitException`
> (PyAutoFit#1155), so Emcee/Zeus walkers escaped their declared boxes
> (reproduced: an unconstrained parameter under `UniformPrior(-0.1, 0.1)` ran to
> |offset| ~ 1e14). The sentence was true before 2025.10.16.1 (exception-driven
> resampling) and is true again since PyAutoFit#1489 restored strict NumPy-path
> bounds in the priors themselves. The gradient-search reasoning and the clipper
> scoping this record justifies were unaffected, but this sentence must not be
> cited as evidence the MCMC samplers were safe in the 2025.10.16.1 → #1489 fix
> window. See `active/uniform_prior_bounds_unenforced_on_numpy_path.md`.

## The design

A `Clipper`, modelled on `@PyAutoFit/autofit/non_linear/initializer.py` — a
pluggable, per-search strategy object with a config-resolved default.

**One place the `Initializer` analogy does not carry.** `Initializer` has a single
consumption pattern (`samples_from_model`). `Clipper` has **two structurally
different consumers** and must serve both from one source of truth:

- `MultiStartGradient` enforces the constraint itself, every step → wants an
  imperative `project(...)`.
- `LBFGS` hands bounds to scipy and lets *scipy* enforce → wants a declarative
  `bounds`.

Proposed contract:

```python
class AbstractClipper(ABC):
    @abstractmethod
    def bounds_from_model(self, model) -> tuple[np.ndarray, np.ndarray]:
        """(lower, upper) in PHYSICAL parameter order. Unbounded -> -inf/+inf."""

    @abstractmethod
    def project(self, vector, model, xp=np):
        """Return (projected_vector, clipped_mask). Identity where unbounded."""


class ClipperNone(AbstractClipper):
    """No-op. Bounds are ±inf, project is the identity. THE DEFAULT (see below)."""


class ClipperPriorBox(AbstractClipper):
    """Hard projection onto the prior support, inset by a margin."""
```

`project` **must return which coordinates it clipped**, not just the new vector.
That mask is what lets a caller zero the optimiser momentum along clipped
directions. It is needed: the prototype left 5 of 16 lanes pinned to a bound at
the end of the run because the parameters were projected while Prodigy's
accumulated state kept pushing outward. The `Clipper` cannot fix that itself — it
does not own `opt_state` — so it must expose enough for the search to.

Later strategies (`ClipperReflect`, a soft-wall variant) drop in without touching
callers. A soft wall must be a *Clipper* (search-local), **never** a change to the
`Prior` classes — that would silently alter the objective for the nested samplers,
where the hard box currently works correctly.

## Scope — PR 1 (this task)

1. `AbstractClipper` + `ClipperNone` + `ClipperPriorBox` in a new
   `@PyAutoFit/autofit/non_linear/clipper.py`.
2. Bounds extraction covering **every** prior type. Confirmed present in the
   reference model: `UniformPrior` (finite both sides), `TruncatedGaussianPrior`
   (finite both sides, e.g. `(-1, 1)` for `ell_comps`), `GaussianPrior`
   (`±inf` — must pass through untouched). Audit the rest (`LogUniformPrior`,
   `LogGaussianPrior`, any `Constant`/deterministic entries).
3. Wire into `AbstractMultiStartGradient._fit`, applied after
   `optax.apply_updates`, **opt-in**.
4. Wire into `LBFGS`, passing `bounds=` through to `optimize.minimize`,
   **opt-in**. Only valid for bound-supporting methods (`L-BFGS-B`, `TNC`,
   `SLSQP`) — guard or warn for plain `BFGS`.
5. `clipper: AbstractClipper = None` constructor arg on the searches, resolved
   like `initializer`.

**Default is `ClipperNone`, and PR 1 must be bit-identical with it.** Follow the
precedent set by PyAutoFit#1475, whose models declaring no constraint
short-circuit to bit-identical behaviour. Flipping the default is a real
behaviour change that shifts every stored multi-start benchmark, which is exactly
the comparability argument PyAutoFit#1472 made when it deferred its own policy
change.

## Scope — PR 2 (separate prompt, file after PR 1 lands)

Flip `MultiStartGradient`'s default to `ClipperPriorBox`, **with** the benchmark
re-baseline, plus the momentum-reset-on-clip decision informed by how bad the
pinning actually is at production budget.

## Traps, measured

- **Parameter ordering is load-bearing and silent if wrong.**
  `model.priors_ordered_by_id` was used for the prototype and lined up correctly
  with `model.instance_from_vector`, but a mismatch would clip the *wrong
  parameter* with no error. Assert the correspondence in a test rather than
  trusting it.
- **Boundary semantics.** Decide and document whether `log_prior` at *exactly* the
  limit is finite. The prototype inset by `1e-6` of the box width to stay strictly
  inside; that margin is a guess and should be a justified constant.
- **Pinning is correct behaviour, not a bug.** Where the likelihood genuinely
  prefers a value outside the prior, a clipped lane sitting on the bound is the
  correct MAP answer under the declared prior. It is worth surfacing (it says the
  prior is fighting the data) rather than hiding. In the reference cell the shear
  escapes were mixed-sign (`+0.353`, `-0.341`, `+0.301`, `-0.312`), which reads
  more like a poorly-constrained parameter diffusing out than a true value sitting
  outside.
- **Clipping does not fix every death.** 5/16 lanes still died in the prototype;
  those are the NaN-gradient population (likelihood NaN in the *jitted* path,
  which the `Fitness` guard maps to `-inf` and whose `where` makes the gradient
  NaN). Separate mechanism, do not expect this task to remove it.

## Two incidental bugs found while investigating — do not lose these

Both surfaced only because clipping let lanes *survive*, i.e. on a code path this
cell had apparently never taken:

1. **`float32` is not JSON serializable in result output.**
   `@PyAutoFit/autofit/non_linear/paths/directory.py:80` `save_json` raises
   `TypeError: Object of type float32 is not JSON serializable` at the end of a
   successful clipped run. Did not fire on the baseline runs, where 14/16 lanes
   were dead. File separately if confirmed.
2. **A crashed run poisons the next run of the same name.** The half-written
   output left by (1) caused the next search with the same `name` to fail with
   `JSONDecodeError` while trying to resume — a 4-second no-op run that *looked
   like* a clean result (zero deaths, because zero steps). This is a new form of
   the cached-result hazard already recorded in
   `complete/2026/08/multistart-nan-step-diagnostics.md`.

## Deliberately out of scope

- **NUTS.** Divergence, not lane death; may need a transform or a soft wall rather
  than projection. Its own task.
- **Unit-cube stepping.** The more principled long-term fix — PyAutoFit's prior
  machinery is already unit-cube and the nested samplers work that way, and it
  would also normalise parameter scales (`einstein_radius ∈ [0,8]` alongside
  `ell_comps ∈ [-1,1]`). Rejected *for now* on three grounds: a logit
  reparameterisation sends the optimum to infinity when it genuinely sits on a
  boundary, which this cell demonstrably has; the inverse-CDF transform for
  non-uniform priors has `∂θ/∂u -> ∞` at the cube faces, trading one numerical
  hazard for another; and it invalidates every stored benchmark. If pursued, note
  that reparameterising the *search path* does not move the optimum **provided the
  objective is still the physical-space posterior evaluated at `θ(u)`** — optimise
  the density *of u* instead and the Jacobian makes the MAP non-invariant, which
  fails silently.
- **Changing `resurrect` defaults.** Not the fix: a redrawn lane walks out again.

## Testing

- Bounds extraction per prior type, including `±inf` passthrough for `GaussianPrior`.
- Ordering assertion (see traps).
- `ClipperNone` is bit-identical: same seed, same final parameters, on both
  `MultiStartGradient` and `LBFGS`.
- A lane deliberately stepped across a boundary is projected back inside, and the
  returned mask names exactly the crossed coordinates.
- `LBFGS` passes bounds through and rejects/warns for non-bound-supporting methods.
- Regression: with `ClipperPriorBox` on a model with a tight `UniformPrior`, the
  value-NaN rate falls substantially. The reference numbers above are CPU/float32,
  single seed — assert a direction and a large margin, not an exact figure.
