# The reconstruction noise map describes a different estimator than the default solver

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
- @autolens_workspace
Difficulty: medium
Autonomy: human-required
Priority: medium
Status: in-progress
Filed: 2026-08-22 (backfilled from git)
Issued: 2026-08-27

## Why this exists

Found 2026-08-22 while researching
`draft/bug/autoarray/reconstruction_noise_map_covariance_sqrt.md` (the numerics
and semantics half). The question that started it: *why has the noise map on
source reconstructions not always been reliable?*

The answer is not the elementwise-sqrt bug — that only touches off-diagonals and
provably cannot reach the 1D noise map. It is this: **the noise map is computed
from a formula that describes an estimator PyAutoArray no longer uses by
default.** `Autonomy: human-required` because the primary fix is a statistical
decision about what the reported uncertainty *means*, not a code repair.

## DECISION MADE 2026-08-22 — posterior, not diagnostic

The human was asked whether this noise map is a **posterior** (a calibrated uncertainty on the
reconstructed flux, used for error bars and S/N) or a **diagnostic** (a relative readout of how
well-constrained each pixel is). Answer: **posterior.**

That settles the direction and closes the diagnostic-only escape hatch offered under Defect 1
("rewrite the docstring rather than the maths"). Defects 1 and 2 are real defects, not documentation
drift. What remains open is the *design* of the fix, not whether one is needed.

## Defect 1 — the covariance formula assumes an unconstrained solve; the default is NNLS

`abstract.py:859` computes `C = inv(curvature_reg_matrix)` = `[F + λH]^-1`. That
is the posterior covariance of the **classical semi-linear inversion** — the
unconstrained linear-Gaussian solution of Warren & Dye (2003) eq. 12, which is
what `reconstruction_positive_negative_from` computes.

But `config/general.yaml` ships:

```yaml
use_positive_only_solver: true      # DEFAULT
```

So the default reconstruction is `fnnls_cholesky` — a **non-negative least
squares** solve, minimising `||Zs - x||²` subject to `s >= 0`. That is a
*constrained* estimator with an active set: `fnnls` maintains a passive set `P`
and solves `slg.solve(ZTZ[P][:,P], ..., assume_a="pos")` on the free pixels only,
pinning the rest at exactly zero.

Imposing `s >= 0` is equivalent to truncating the Gaussian prior to the
non-negative orthant. The posterior is then a **truncated** multivariate Gaussian,
whose covariance is *not* `[F + λH]^-1`:

- For pixels well inside the positive region, the constraint is inactive and
  `[F + λH]^-1` is a good approximation.
- For pixels near the boundary, truncation **reduces** the variance, so the
  reported noise is systematically **overstated**.
- For pixels pinned at exactly zero, the marginal posterior is not Gaussian at
  all — it piles up at the boundary. The reported number is meaningless.

**Why this bites source reconstructions hardest.** A lensed source is compact; most
of the mesh is empty sky. So NNLS pins a *large fraction* of pixels at zero, the
active set is large, and the unconstrained formula is worst exactly where it is
most used. That matches the reported symptom precisely.

The docstring makes an uncertainty claim, not a diagnostic one — "the RMS standard
deviation of the noise in every pixel ... should be used for any scientific
analysis (e.g. source reconstructions of strong lenses)" — so this matters.

**The honest counter-argument, which a human should weigh:** if the noise map is
meant only as a *diagnostic* of how well each pixel is constrained by data plus
regularization, `[F + λH]^-1` is defensible for any solver, and the fix is to
rewrite the docstring rather than the maths. Decide which of the two it is before
writing code. That decision is the point of this prompt.

## Defect 2 — the noise map ignores edge-zeroed pixels the reconstruction excluded

`config/general.yaml` also ships `use_edge_zeroed_pixels: true`. Under it, the
reconstruction (`abstract.py:511-539`) subsets the system:

```python
curvature_reg_matrix = self.curvature_reg_matrix[self.zeroed_ids_to_keep][:, self.zeroed_ids_to_keep]
```

solves the reduced problem, then scatters back with **exact zeros** at the zeroed
pixels. `reconstruction_noise_map_with_covariance` inverts `self.curvature_reg_matrix`
— the **full** matrix, respecting neither this reduction nor the separate
`mapper_indices` reduction that `curvature_reg_matrix_reduced` applies for the
log-det.

Those excluded rows are, by the Delaunay mesh's own docstring, the
"poorly constrained boundary vertices" whose zeroing exists to "stabilize the
linear inversion" and "prevent poorly constrained boundary vertices from absorbing
flux". **The noise map re-admits into an explicit inverse precisely the degenerate
rows the reconstruction deliberately dropped to stay stable.**

The user-visible result: a pixel whose reconstruction reads exactly `0` (meaning
"not solved for") gets a noise value computed as though it had been solved.
Reconstruction and noise map disagree about what those pixels mean.

Scope: only bites when `zeroed_pixels > 0`. `Delaunay.__init__` defaults it to `0`,
so this is opt-in per mesh — check `rectangular_rtu_adapt_density` and any
workspace configs before sizing the blast radius.

## Defect 3 — `use_edge_zeroed_pixels` is silently ignored unless the positive-only solver is on

This is the "does the edge-pixel handling make sense next to positive-only?"
question, and the answer is no. The control flow (`abstract.py:509-554`):

```python
if self.settings.use_positive_only_solver:          # default True
    if self.settings.use_edge_zeroed_pixels and self.has(cls=Mapper):
        ...subset, fnnls, scatter back...
    else:
        return reconstruction_positive_only_from(FULL matrix)
return reconstruction_positive_negative_from(FULL matrix)   # edge-zeroing never consulted
```

`use_edge_zeroed_pixels` is nested **inside** the positive-only branch. Setting
`use_positive_only_solver: false` — a reasonable thing to do, for speed or to
permit negative values — **silently disables edge-zeroing too**, with no warning.
The poorly-constrained boundary vertices come straight back into the solve and
results change for a reason the config does not express.

These are orthogonal concerns. Which parameters are *solvable* (edge-zeroing) is a
statement about the mesh; which solver walks them is a separate choice. Edge-zeroing
should apply to both branches, or the coupling should be made explicit and
documented.

## Suggested direction (interpretation now settled; design still open)

If the noise map is to describe the estimator actually used, the covariance should
be formed on the **same index set the reconstruction solved**, and scattered back:

1. Determine the kept set exactly as `reconstruction` does — `zeroed_ids_to_keep`
   under edge-zeroing, and, for the NNLS answer to Defect 1, further restricted to
   the free set (pixels with `reconstruction > 0`).
2. Cholesky-invert that submatrix (per the sibling prompt's `cho_factor` /
   `cho_solve` fix).
3. Scatter back into full shape. **Decide what the excluded pixels report** — `0`
   matches the reconstruction's own convention and keeps plots working; `NaN` is
   more honest ("never estimated") but breaks colourbars and the CSV. Recommend
   `0` with an explicit docstring statement, since the reconstruction already
   reports `0` there and consumers handle it.

Restricting to the NNLS free set gives the covariance *conditional on the active
set* — standard practice for constrained least squares, and a defensible,
documentable choice. It is still an approximation: it ignores the uncertainty in
the active set itself. Say so in the docstring rather than implying exactness.

## Downstream evidence for why this matters (added 2026-08-22)

`autolens_workspace` uses the 1D noise map directly in user-facing science scripts —
`scripts/{imaging,interferometer,group,multi_galaxy}/features/pixelization/source_science.py`
compute:

```python
reconstruction_noise_map = inversion.reconstruction_noise_map
signal_to_noise_map = reconstruction / reconstruction_noise_map
```

So the quantity this prompt argues is computed for the wrong estimator is divided into the
reconstruction to produce a **signal-to-noise map on a source reconstruction** — the number
that ends up in papers. If the NNLS/unconstrained mismatch is real, it propagates straight
into published S/N. That raises the stakes on the Defect 1 decision and is the concrete
reason to instrument a real fit rather than reason about it further.

## SUPERSEDED — synthetic proxy, badly underestimated the effect (kept as a caution)

This prompt's load-bearing claim was that NNLS pins a large fraction of a compact source's mesh,
flagged as reasoned-not-measured. Now measured with PyAutoArray's **real solver**
(`autoarray.util.fnnls.fnnls_cholesky`) on a problem shaped like a source-plane inversion — compact
Gaussian source, 4-neighbour gradient regularization, mesh mostly covering empty sky.

**CONFIRMED — the pinned fraction is large, and scales with source compactness:**

| mesh | pixels | source area | pinned at 0 |
|---|--:|--:|--:|
| 20x20 | 400 | 2% | **46.0%** |
| 20x20 | 400 | 5% | **24.8%** |
| 20x20 | 400 | 15% | 1.2% |
| 30x30 | 900 | 2% | **47.8%** |
| 30x30 | 900 | 5% | **26.4%** |
| 30x30 | 900 | 15% | 0.4% |
| 40x40 | 1600 | 2% | **50.0%** |
| 40x40 | 1600 | 5% | **26.8%** |
| 40x40 | 1600 | 15% | 0.5% |

A quarter to a half of the mesh is pinned for a genuinely compact source; the effect vanishes for an
extended one. The premise holds.

**But the numerical consequence is far smaller than this prompt implied.** Shipped full-matrix noise
map vs the active-set-conditional one (covariance restricted to the free set), on the 900-pixel /
5%-source case (226 pinned):

| quantity | value |
|---|---|
| median noise, shipped (full matrix) | 0.002226 |
| median noise, active-set-conditional | 0.002159 |
| ratio shipped / conditional, free pixels | **median 1.025, min 1.002, max 1.123** |

The shipped map **overstates** uncertainty on the free pixels by ~2.5% median, up to ~12% worst case.
The bias is systematic and one-directional (`min 1.002` — it never understates), exactly as the
truncation argument predicts. But it is a few percent, **not** the order-of-magnitude error the
`Priority: high` grading assumed.

The pinned pixels are less alarming than feared: their reconstruction is exactly `0.0`, so
`signal_to_noise_map = reconstruction / reconstruction_noise_map` yields `0 / 0.00228 = 0`. Zero S/N
for an unlit pixel is defensible — though the reported noise value itself is still meaningless, the
posterior there being a spike at the boundary rather than a Gaussian.

**Re-graded `Priority: high` -> `medium`.** A systematic, always-one-direction ~2.5% (up to 12%)
overstatement of source-plane error bars is worth correcting for a quantity now confirmed to be a
**posterior** and which feeds published S/N maps. It is not an emergency.

**Caveat, and a real one.** This is a *structural proxy*, not a lens fit: the mapping matrix is random
rather than produced by ray tracing, so neighbouring image pixels do not map to neighbouring source
pixels as they do in reality. That structure affects conditioning and could move the magnitude either
way. The pinned *fraction* is robust to it (it follows from source compactness, not mapping
structure); the *2.5% / 12%* figures are indicative only. **Re-measure on a real Delaunay fit before
quoting them anywhere.**

Defect 3 (the config coupling) is untouched by all of this — it is an unambiguous bug at any priority,
but it sits on the reconstruction path and so changes fit results. It needs its own sign-off.

## MEASURED ON A REAL LENS FIT 2026-08-22 — the proxy was wrong; re-graded back to high

The synthetic measurement above was re-run on a **real ray-traced fit**, reproducing
`autolens_workspace/scripts/imaging/features/pixelization/source_science.py`: Isothermal
`einstein_radius=1.6` + shear, `RectangularBilinearAdaptDensity(28, 28)`, `Constant` regularization,
`r=3.0"` mask, `over_sample_size_pixelization=4`, compact Sersic source, PSF and Poisson noise.
Defaults confirmed live: `use_positive_only_solver=True`, `use_edge_zeroed_pixels=True`,
`mesh.zeroed_pixels = 108` of 784.

**The proxy understated the effect by an order of magnitude, and its caveat was the reason.** A random
mapping matrix spreads data support across the whole mesh; real ray tracing concentrates it in the
arc, so far more of the mesh is unconstrained.

Sensitivity sweep (`noise x med` = median shipped/active-set-conditional on free pixels; `flux %` =
change in source flux passing the workspace's `S/N >= 5` cut):

| r_eff | reg coeff | mesh | params | pinned % | noise x med | max | flux % |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 0.05 | 1.0 | 28 | 784 | **97.1%** | **2.837** | 9.34 | **-24.1%** |
| 0.10 | 1.0 | 28 | 784 | **88.6%** | **1.692** | 10.60 | -11.1% |
| 0.30 | 1.0 | 28 | 784 | 53.2% | 1.208 | 8.02 | -3.9% |
| 0.60 | 1.0 | 28 | 784 | 21.0% | 1.025 | 4.06 | -1.1% |
| 0.10 | 0.1 | 28 | 784 | 87.1% | 1.713 | 10.39 | **-29.8%** |
| 0.10 | 10.0 | 28 | 784 | 82.3% | 1.117 | 1.90 | -2.4% |
| 0.10 | 100.0 | 28 | 784 | 83.2% | 1.009 | 1.57 | -0.2% |
| 0.10 | 1.0 | 20 | 400 | 91.0% | 1.481 | 4.93 | 0.0% |
| 0.10 | 1.0 | 40 | 1600 | 90.4% | 1.421 | 10.36 | **-48.9%** |

Two clean trends: the gap **grows with source compactness** and **shrinks with regularization
strength**. At `coeff=100` it essentially vanishes (1.009); at realistic `coeff~1` with a compact
source it is a factor of **1.7-2.8**, with individual pixels up to **10x**.

### The framing that matters — these are two bounds, not right-vs-wrong

Do not read "1.8x" as "the shipped noise map is wrong by 1.8x". The two quantities **bracket** the
truth:

- **Shipped (full-matrix)** ignores the `s >= 0` constraint entirely, so it **overstates** — an upper
  bound.
- **Active-set-conditional** treats the active set as *known*, ignoring uncertainty about which
  pixels are pinned, so it **understates** — a lower bound.
- The true truncated-Gaussian posterior lies between them.

So the finding is: **the source-plane noise map is ambiguous at the factor-of-2 level for compact
sources**, and the shipped value sits at the pessimistic end of that range. That is still a serious
problem for a published error bar — but "switch to the conditional covariance" is **not** the
correct fix, it just swaps one bound for the other. Designing the real fix means either computing the
truncated posterior properly, or documenting the bracket honestly.

### Downstream consequence is a threshold effect, which amplifies it

`source_science.py` does not merely display the noise map:

```python
signal_to_noise_map = reconstruction / reconstruction_noise_map
mesh_pixel_mask = signal_to_noise_map < 5.0
reconstruction_masked[mesh_pixel_mask] = 0.0
```

Source flux and magnification are computed from the surviving pixels. A hard cut turns a smooth noise
bias into a discrete one: pixels near `S/N = 5` flip in or out. Measured flux shifts of **-24%**,
**-30%** and **-49%** in the table above come from a handful of pixels crossing that line.

**Re-graded `Priority: medium` -> `high`.** The earlier downgrade was made on the synthetic proxy and
was wrong.

### What is still not established

- One lens configuration, one mass model, one noise realization per row. No error bars on these numbers.
- `reg coeff` was fixed by hand. In a real model-fit λ is a **free parameter the sampler optimises**,
  and the `coeff=100` row shows the effect nearly vanishes when λ is large. Where fitted λ actually
  lands for these datasets decides whether this bites in practice — **measure that before acting**.
- `RectangularBilinearAdaptDensity`, not Delaunay. Delaunay is the other common source mesh and was
  not tested.

Scripts: `scratchpad/real_fit_measure.py`, `scratchpad/sensitivity.py` (session artefacts).

## SETTLED 2026-08-22 — at the FITTED lambda the effect nearly vanishes. Re-graded to low.

The open question from the sweep above was: those numbers used a hand-set regularization
coefficient, but in a real fit `Constant.coefficient` is a free parameter under
`LogUniform(1e-6, 1e6)` (workspace `config/priors/regularization/constant.yaml`), and the figure of
merit for a pixelized fit is the **Bayesian log evidence**. So `argmax_lambda log_evidence` is what
the sampler converges on — computed deterministically over a 17-point grid rather than by running
Nautilus.

| r_eff | lambda* | log evidence | pinned % | noise x med | max | S/N>=5 ship | cond | flux % |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0.05 | **10** | 27605.4 | 96.6% | **1.263** | 1.91 | 12 | 12 | **0.0%** |
| 0.10 | **10** | 26932.8 | 87.1% | **1.055** | 2.45 | 29 | 30 | **-1.3%** |
| 0.30 | **10** | 24635.2 | 42.3% | **1.007** | 2.10 | 138 | 138 | **0.0%** |

`lambda* = 10` in all three cases, comfortably inside the scanned grid (`1e-3 .. 1e5`) — not an edge
artefact.

**The Bayesian evidence self-selects away from the problematic regime.** The factor-of-2.8 gap found
above occurs at `lambda ~ 0.1-1`, i.e. under-regularized solutions the evidence *penalises*. At the
lambda a real fit chooses, the median gap is **1.007-1.263** and the downstream science outputs —
source flux and magnification through the `S/N >= 5` cut — move by **0.0%, -1.3%, 0.0%**. The pixel
counts either side of the cut are all but identical (12/12, 29/30, 138/138).

The pinned fraction stays large (42-97%), so the *mechanism* in Defect 1 is real and confirmed. It
simply does not have a large numerical consequence at the operating point.

**Re-graded `Priority: high` -> `low`.** Honest accounting: this prompt has been graded high ->
medium -> high -> low across three measurements. The swings came from measuring progressively less
wrong things — synthetic proxy, then a real fit at hand-set lambda, then a real fit at *fitted*
lambda. Only the last is the operating point, and it is the one that governs.

### What remains true and worth doing

- For a **very compact source** (`r_eff = 0.05`) the shipped noise map still overstates by **~26%
  median**, up to ~2x on individual pixels. That is a real bias on a published error bar even though
  it moves no flux. Anyone quoting per-pixel source uncertainties on a compact source should know.
- The **bracket framing stands**: full-matrix overstates, active-set-conditional understates, and the
  truncated-Gaussian posterior lies between. A fix that simply swaps to the conditional covariance
  would be wrong at any lambda.
- **Recommended immediate action is documentation, not code**: state in
  `reconstruction_noise_map`'s docstring that the covariance is that of the unconstrained solve,
  that the default solver is NNLS, and that for compact sources this overstates per-pixel noise by a
  few tens of percent at most. Cheap, honest, no API change.
- A proper truncated-posterior implementation is only worth it if someone needs calibrated per-pixel
  error bars on very compact sources. Not now.

### Caveats on this result

- **The lens mass was fixed at truth.** In a real model-fit the mass is free too, and a poor mass
  model may need a lower lambda to absorb residuals — which is the regime where the gap opens. This
  is the most likely way the conclusion could be wrong.
- One noise realization per row; no error bars on lambda*.
- `RectangularBilinearAdaptDensity` only; Delaunay untested.
- Evidence was maximised on a grid, not sampled — Nautilus explores a posterior over lambda, so some
  posterior mass sits at lower lambda where the gap is larger.

Script: `scratchpad/fitted_lambda.py` (session artefact).

## PARTIALLY ADDRESSED 2026-08-22 — the docstring caveat shipped

The recommended immediate action was taken: **[PyAutoArray#472](https://github.com/PyAutoLabs/PyAutoArray/pull/472)**
documents on `reconstruction_noise_map` that the covariance is that of the *unconstrained* solve
while the default solver is NNLS, quantifies the overstatement at the evidence-optimal coefficient
(x1.01 to x1.26 median, up to ~2x per pixel) and below it (~2.8x median, ~10x per pixel), and records
that restricting to the free set is **not** the correction because the two bracket the truth.

Documentation only — no behaviour change, no API change.

### What this prompt still owns

1. **Defect 1's actual maths.** Computing the truncated-Gaussian posterior properly. Graded `low`:
   worth it only if someone needs calibrated per-pixel error bars on a very compact source.
2. **Defect 2** — the covariance ignores `zeroed_ids_to_keep` while the reconstruction subsets by it.
   Never measured in isolation; the real fits here had 108 zeroed pixels of 784 and they are folded
   into the "pinned" counts throughout, so its separate contribution is unknown.
3. **Defect 3** — `use_edge_zeroed_pixels` nested inside the `use_positive_only_solver` branch, so
   turning the positive-only solver off silently disables edge-zeroing. **Untouched by any of the
   measurement above and unambiguous at any priority.** It sits on the reconstruction path, so it
   changes fit results and needs its own sign-off. This is the most likely next piece of real work
   here.
4. **The open measurement**: re-run the evidence-optimal lambda with the lens mass **free** rather
   than fixed at truth. That is the single result most likely to overturn the `low` grading.

## SCOPED FOR DEV 2026-08-27 — Defect 2 only; Defect 3 is closed

`/start_dev` re-read this prompt against PyAutoArray `main` @ `da5ec9a0`. Three of the four open
items are **not** live code work, so this prompt now owns exactly one:

| Item | State on `main` @ `da5ec9a0` |
|---|---|
| Defect 1 — unconstrained covariance vs NNLS | Docstring caveat **shipped** ([#472](https://github.com/PyAutoLabs/PyAutoArray/pull/472)). The truncated-posterior maths stays deferred at `low` — "worth it only if someone needs calibrated per-pixel error bars on a very compact source". |
| **Defect 2 — covariance ignores `zeroed_ids_to_keep`** | **LIVE. This prompt's task.** `reconstruction_covariance_matrix` (`abstract.py:844`) inverts the full `curvature_reg_matrix`; `reconstruction` (`abstract.py:516-544`) solves the `zeroed_ids_to_keep` submatrix and scatters back exact zeros. |
| Defect 3 — `use_edge_zeroed_pixels` nested inside the positive-only branch | **CLOSED — deliberate, not a bug.** [`84b9ed4`](https://github.com/PyAutoLabs/PyAutoArray/commit/84b9ed42b583dd1473aeda259b8e9d7a3f153c10) (2026-08-22): "the author confirmed the scoping is deliberate". Documented in three places — `config/general.yaml:6`, `Settings.use_edge_zeroed_pixels`, and a comment at the nesting site itself saying explicitly not to hoist the check. The text above calling this "the most likely next piece of real work" is **stale — do not act on it**. |
| The open measurement — evidence-optimal lambda with the lens **mass free** | Deferred. Not code work; belongs in its own `research/` prompt when someone wants it. |

### Blast radius is wider than this prompt assumed

The scope note above says Defect 2 "only bites when `zeroed_pixels > 0`" and that
`Delaunay.__init__` defaults it to `0`, "so this is opt-in per mesh". That understates it.
`RectangularRTUAdaptDensity.zeroed_pixels` (`rectangular_rtu_adapt_density.py:161`) returns the
**entire edge ring unconditionally** — there is no opt-in and no count to set. For the
`Rectangular*AdaptDensity` family it is always on. That is the mesh family every real-fit
measurement in this prompt used: 108 zeroed of 784 on a 28x28 is exactly the edge ring, `4*28 - 4`.

### The three index sets are not three inconsistencies — two of them are unrelated

The Verification section below asks whether `curvature_reg_matrix_reduced`'s `mapper_indices`
reduction should apply to the noise map too, and calls the inconsistency between all three "itself a
finding". It is not. `mapper_indices` drops **linear objects that carry no regularization** (light
profiles and the like) from the reduced matrices; it has nothing to do with edge zeroing. The
comment `# ids of values which are on edge so zero-d and not solved for` at `abstract.py:349`,
`:387` and `:574` is simply **wrong**, and is what makes the two look like the same concern. Correct
the comment as part of this task. Only `zeroed_ids_to_keep` vs the noise map was ever a defect.

### DECISION 2026-08-27 — excluded pixels report `NaN`

The prompt recommended `0` ("matches the reconstruction's own convention and keeps plots
working"). The human chose **`NaN`**, and the two consumer paths were checked before deciding —
neither breaks, and `NaN` is the safer of the two:

- **Plots.** `norm_from` (`plot/utils.py:270`) is the single colour-scale implementation behind
  `plot_array` and `plot_inversion_reconstruction`. It derives `vmax` with `np.nanmax` and its
  docstring already names "an all-`NaN` array" as a handled fallback; the linear branch returns
  `None` and lets matplotlib autoscale, which ignores `NaN`. Unsolved pixels render blank, which is
  what they are.
- **CSV.** `save_reconstruction_csv` (`inversion_plots.py:395`) already writes `nan` into the
  `noise_map` column when the covariance raises. `NaN` extends an established convention rather
  than inventing one.
- **`0` was the worse option, not the safer one.** `source_science.py` computes
  `reconstruction / reconstruction_noise_map`, and the reconstruction at these pixels is exactly
  `0.0`. Under `0` that is `0/0` -> `NaN` **plus a `RuntimeWarning` on every call**; under `NaN` the
  `NaN` propagates silently. Both give `NaN < 5.0 == False`, so the pixels survive the `S/N >= 5`
  cut carrying a reconstruction of `0.0` and measured flux is unchanged either way.

Document the convention in the `reconstruction_noise_map` docstring **and** in the workspace
scripts that consume it — which is why `@autolens_workspace` is now on this prompt.

### This is a value change on the pixels that ARE solved

Restricting the inverse is not a re-scaling of the excluded rows. For an SPD matrix
`[A^-1]_keep >= (A_keep)^-1` in the positive-semidefinite ordering, so **every kept pixel's noise
drops**, on every `Rectangular*AdaptDensity` fit. Needs a measured before/after on a real fit and a
release note.

**The Defect 1 bracket framing does not apply here.** These pixels are fixed at zero *by
construction*, deterministically, before the solver runs — not selected by the data the way the NNLS
active set is. Conditioning on them is exactly right, and there is no upper/lower bracket to
straddle. Do not let the "restricting to the free set is not the correction" caveat in
`reconstruction_noise_map`'s shipped docstring be read as applying to this change; it is about the
NNLS active set only.

### Structural fix, not a local patch

The reason this defect exists is that the predicate deciding whether the solve subsets the system
lives inline in `reconstruction` and nowhere else, so the covariance could never have known about
it. Give the inversion **one** property for "which indices did the solve actually solve", have both
`reconstruction` and `reconstruction_covariance_matrix` read it, and the two cannot drift apart
again.

## Verification

- **Reproduce the symptom first.** Take a real Delaunay source fit, compute the
  noise map under the current code and under the free-set-restricted covariance,
  and compare. Quantify how many mesh pixels are pinned at zero by NNLS — the
  claim that this fraction is large for compact sources is **reasoned, not
  measured**, and the whole prompt rests on it. If the fraction turns out small,
  Defect 1 is a much smaller problem than stated here and should be re-graded.
- Confirm reconstruction and noise map agree on which pixels were solved: every
  pixel the reconstruction reports as an exact structural zero should be
  identifiable in the noise map by the documented convention.
- With `zeroed_pixels > 0`, assert the covariance is formed on the reduced matrix
  — regression-test the shape and the scatter-back, not just values.
- For Defect 3, assert `use_edge_zeroed_pixels: true` + `use_positive_only_solver:
  false` either applies edge-zeroing or raises/warns. It must not silently ignore
  the setting.
- Check whether `curvature_reg_matrix_reduced`'s `mapper_indices` reduction should
  apply to the noise map too. The log-det uses it; the noise map does not. Decide
  deliberately — this is a third, separate index set and the inconsistency between
  all three is itself a finding.

## Prior art — read before starting

- `complete/2026/08/numerical-inversion-failures.md` — this cluster's refutation.
- `complete/2026/07/pix-inversion-not-positive-definite.md` — an earlier
  non-positive-definite hypothesis, also refuted; documents the `GaussianKernel`
  PD-guarantee `f1817af0`.
- `autoarray/util/cholesky_funcs.py:50-80` — near-coincident mesh vertices make the
  Schur pivot's sign depend on BLAS thread count. The degeneracy is real and
  documented; this prompt is about not feeding it into an explicit inverse.
- `abstract.py:805` — the repo already documents `~1e-6` evidence round-off from
  "factorizing the explicitly formed inverse" at `cond(C) ~ 1e9` on clustered
  traced mesh vertices.

## Provenance

- Found during: research for the sibling prompt, 2026-08-22.
- Do the sibling first — it is small, needs no science decision, and its Cholesky
  covariance helper is the building block this prompt reuses.
