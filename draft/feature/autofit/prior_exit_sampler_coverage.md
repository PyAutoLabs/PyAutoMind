# Which other searches need prior-support handling — coverage audit after Prodigy

Type: feature
Target: autofit
Repos:
- PyAutoFit
Themes:
- samplers
- jax-gradient
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-17 (backfilled from git)

## What this is

The **coverage** follow-up to the prior-support work. Everything measured so far
came from **one search** (`MultiStartProdigy`) on **one cell** (`imaging/mge` hst).
This asks which of the other searches share the failure mode, which are already
immune, and which need the fix in a different shape.

Run it **after** the Prodigy step-scaling task
(`draft/feature/autofit/per_parameter_step_scaling.md`), so the audit can measure
both levers rather than only the clipper.

## The mechanism being audited

The MAP objective is `-2 * (log_likelihood + sum(log_prior))`. A `UniformPrior` is
`-inf` outside its box, so a lane whose *likelihood* is finite goes non-finite the
moment any coordinate leaves prior support. The gradient searches step in
**physical** space with nothing holding them inside, and prior box widths on a real
model span **40x** (8.0 for `einstein_radius` down to 0.2 for `bulge.centre`), so a
globally-scaled step is a wall-crossing for the narrow-box parameters.

Two mitigations now exist, and they are complementary, not alternatives:

- **`ClipperPriorBox`** — enforces the invariant; also the only way to express a MAP
  answer that genuinely sits on a bound.
- **per-parameter step scaling** — reduces how often a wall is reached at all.

## Prior art: what is already known to be immune, and why

From `complete/2026/08/prior-support-clipper.md` — **verify rather than assume**,
but do not re-derive from scratch:

- **Nested samplers (Nautilus, Dynesty)** already work in **unit-cube** coordinates,
  so they cannot leave prior support. Nautilus is the campaign's reference bar for
  exactly this reason.
- **MCMC (Emcee, Zeus)** **reject** `-inf` proposals, so the walker stays put.
  *"Rejection is the restoring mechanism that gradient methods lack."*
- **NUTS** targets the log posterior from a physical start and **diverges** rather
  than dying — a different mechanism, explicitly out of scope of the clipper work
  and needing its own investigation.

So the exposed family is the **gradient / MLE** searches. That is the audit's focus.

## What to audit

| search | expected exposure | what to check |
|---|---|---|
| `MultiStartAdam` | **high** | fixed `learning_rate=0.01` in PHYSICAL units, no adaptation at all |
| `MultiStartLion` | **high** | fixed `learning_rate=0.001`, sign-based updates |
| `MultiStartADABelief` | **high** | fixed rate, same exposure as Adam |
| `MultiStartProdigy` | measured | baseline from autolens_profiling#131 |
| `LBFGS` / `AbstractBFGS` | different shape | already takes `clipper` and hands **bounds to scipy**; scipy enforces, so check the enforcement actually happens and that non-bound-supporting methods reject or warn |
| `BlackJAXNUTS` | out of scope | divergence, not lane death — confirm and file separately |

**The load-bearing hypothesis: the fixed-rate optimizers should be affected MORE
than Prodigy, not less.** Prodigy at least estimates its own step scale; Adam, Lion
and ADABelief take a literal constant in physical units, so the 40x box-width
disparity cannot be absorbed anywhere. If that is right, the Prodigy numbers are the
*optimistic* end of the range and the campaign's "clipping is cosmetic" verdict may
not transfer.

## What to produce

1. **A coverage table**: for each search — is prior exit reachable, is it already
   mitigated, by what mechanism, and is that mechanism enforced or assumed.
2. **A cheap empirical check per exposed search** on the characterised cell
   (`imaging/mge` hst), with `ClipperPriorBox` on, recording the **clip rate** and
   the **alive-versus-step curve**. The clip rate is the comparable quantity across
   searches; the raw lane counters are survival integrals and are not comparable
   across different step budgets.
3. **A recommendation per search** on both levers — clipper default and step
   scaling — feeding phase 3 of the prior-support work.

## Grading rules (inherited, all paid for)

- **Grade on the alive-versus-step curve**, not the percentage. `alive_history` is in
  `search_internal`; `alive_fraction` is the budget-independent scalar.
- **At least two seeds.** Identical settings swung the Prodigy result **171,000
  nats** between seeds 0 and 1. Use the search's `seed` argument.
- **A `ClipperPriorBox` arm reporting zero clips has not exercised the clipper** — a
  broken arm, not a null result. Unless it is a genuinely unbounded model, in which
  case zero is the PASS.
- **Name the step budget with every number.** At 105 steps clipping was worth 114
  nats on Prodigy; by 3000 it was worth zero.
- **`search.summary` is `Key = Value`**, not colon-separated.

## Out of scope

- Flipping any default (phase 3).
- NUTS divergence — confirm it is a different mechanism and file it separately.
- The seed-dependence investigation, filed on its own.
