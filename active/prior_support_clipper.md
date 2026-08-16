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
