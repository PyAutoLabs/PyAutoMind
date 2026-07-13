# `@PyAutoFit` `RelativeWidthModifier` produces zero / negative sigma for parameters near 0

Type: bug
Target: priors
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A9
and C7).

> **Prerequisite:** prompt 06 (`NormalMessage` sigma check) should
> land first. With negative sigma rejected by the constructor, this
> bug becomes loud — `RelativeWidthModifier` × negative mean would
> raise immediately. Without that fix, this bug is silent.

## Problem

`@PyAutoFit/autofit/mapper/prior/width_modifier.py:78-81`:

```python
class RelativeWidthModifier(WidthModifier):
    def __call__(self, mean):
        return self.value * mean
```

This is the prior-passing width used when the user has not specified
an absolute floor. For a parameter posterior centred near 0 or
crossing 0:

- `mean = 0` → new prior sigma = 0 → degenerate Gaussian.
- `mean < 0` → new prior sigma < 0 → currently accepted silently by
  `NormalMessage` (see prompt 06), which then produces a Gaussian
  whose `variance = sigma² > 0` but whose `value_for`, gradient and
  `sample` propagate the negative scale (sometimes flipping signs).

## Wider context — how this is reached in practice

Prior passing flow (paraphrased from
`@PyAutoFit/autofit/mapper/prior_model/abstract.py` and the
`GaussianPrior.with_limits` family):

1. A search finishes. Each parameter gets a posterior median `m̂`.
2. For each parameter, look up the `WidthModifier` configured for
   that class+attribute in `conf.instance.prior_config`.
3. If `RelativeWidthModifier(0.5)`, the next prior has
   `sigma = 0.5 · m̂`.
4. If no width-modifier is configured, the system defaults to
   `RelativeWidthModifier(0.5)` (see `width_modifier.py:57-72`).

So this default path is reachable any time:

- A parameter is roughly centred near zero (common: pixel offsets,
  ellipticity components, perturbations).
- A parameter can take negative values (common: shifts, log-residuals).

The default is silently dangerous in either case.

## Python reproducer

```python
# Reproducer: relative_width_modifier_safety.py
import autofit as af

from autofit.mapper.prior.width_modifier import RelativeWidthModifier

mod = RelativeWidthModifier(0.5)

print("=== Various means through RelativeWidthModifier(0.5) ===")
for m in [10.0, 1.0, 0.1, 0.0, -0.1, -1.0]:
    sigma = mod(m)
    print(f"  mean={m:>6.2f}  →  sigma={sigma:>6.3f}", end="  ")
    if sigma <= 0:
        print("← PROBLEMATIC (sigma must be > 0 for Gaussian)")
    else:
        print()

print()
print("=== Downstream: build a GaussianPrior with the bad sigma ===")
sigma_bad = mod(-1.0)
try:
    p = af.GaussianPrior(mean=0.0, sigma=sigma_bad)
    print(f"  GaussianPrior(mean=0, sigma={sigma_bad}) constructed silently: {p!r}")
    print(f"  value_for(0.5) = {p.value_for(0.5)}")
    print(f"  value_for(0.84) = {p.value_for(0.84)}  (should be ~mean+sigma)")
except Exception as e:
    print(f"  raised {type(e).__name__}: {e}  (expected after prompt-06 lands)")

print()
print("=== Zero-sigma degeneracy ===")
try:
    p0 = af.GaussianPrior(mean=0.0, sigma=mod(0.0))
    print(f"  GaussianPrior with sigma=0 constructed: {p0!r}")
    print(f"  value_for(0.1) = {p0.value_for(0.1)}")
    print(f"  value_for(0.9) = {p0.value_for(0.9)}")
    print(f"  (collapsed: every unit value maps to the mean)")
except Exception as e:
    print(f"  raised {type(e).__name__}: {e}")
```

Expected (buggy) output: negative and zero sigmas pass through the
modifier without complaint. With prompt 06 still unfixed, the
downstream `GaussianPrior` also constructs silently.

## Proposed fix — needs a design decision

Three options, in increasing scope:

### Option A: minimal safety floor in `RelativeWidthModifier`

```python
class RelativeWidthModifier(WidthModifier):
    def __init__(self, value, absolute_floor=None):
        super().__init__(value)
        self.absolute_floor = absolute_floor  # optional, defaults None

    def __call__(self, mean):
        sigma = self.value * abs(mean)
        if self.absolute_floor is not None:
            sigma = max(sigma, self.absolute_floor)
        return sigma
```

- Uses `abs(mean)` so sign is preserved as a width.
- Lets users opt into a floor per attribute via YAML config.
- Backwards-compatible default (no floor).

Pro: smallest change. Con: doesn't fix the default-zero-floor case.

### Option B: mandatory floor with sensible default

Always require an `absolute_floor` (e.g. default `1e-8`), so the
modifier *cannot* return zero. Existing YAML configs need a one-time
audit to add explicit floors where needed.

Pro: defensive by default. Con: config migration work.

### Option C: redesign per finding C7 in the audit

Replace `WidthModifier` subclasses with a single
`PriorPassWidth(relative=..., absolute_floor=..., absolute_cap=...)`
that always sigmoids between bounds. YAML schema migrates accordingly.

Pro: cleanest long-term API. Con: largest change, breaks config files.

### Decision criteria

The reviewer should consider:

- How many YAML `prior_config` entries currently use the implicit
  `RelativeWidthModifier(0.5)` default? (Grep workspace configs.)
- Are any of those for parameters that can cross zero?
- Is `abs(mean)` the right thing? Some users may rely on negative
  sigma silently flipping the prior — though no test covers this.

## What the agent picking this up should do

1. **Wait for prompt 06 to be acked and merged first.** This prompt
   leans on `NormalMessage` rejecting negative sigma; otherwise the
   reproducer's "downstream effect" is silent and harder to argue.
2. Read `@PyAutoFit/autofit/mapper/prior/width_modifier.py` and the
   YAML `prior_config` files in `@PyAutoFit/autofit/config/priors/`
   and the workspaces.
3. Grep across `@PyAutoFit`, `@PyAutoArray`, `@PyAutoGalaxy`,
   `@PyAutoLens`, `@autofit_workspace`, `@autogalaxy_workspace`,
   `@autolens_workspace` for `RelativeWidthModifier` and
   `width_modifier:` to list every config that relies on the default.
4. Run the reproducer. Confirm zero / negative sigma escapes the
   modifier.
5. File the GitHub issue via `/create_issue priors/08_relative_width_modifier_safety.md`.
6. **In the issue body, present options A/B/C and ask the reviewer
   which is the right scope.** Include the config audit list so the
   reviewer can judge migration cost.
7. **Stop. Do not implement until the reviewer chooses A, B, or C.**


## Fable verdict (2026-07-08, PyAutoFit main @ 0f26ff2d8; PyAutoFit#1330)

**Verdict: CONFIRMED — fix after prompt 06 (severity: medium).**
`RelativeWidthModifier(0.5)(-1.0) = -0.5` flows into `GaussianPrior`
silently; `value_for(0.84) = -0.497` (scale flipped). Zero mean gives
sigma = 0 degenerate prior. Implicit default `RelativeWidthModifier(0.5)`
still in place. Options A/B/C decision still required; prompt 06 landing
first turns this from silent to loud as designed.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
