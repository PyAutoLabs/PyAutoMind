# `@PyAutoFit` `LogGaussianPrior.with_limits` will crash on first call (and so will `_new_for_base_message`)

Type: bug
Target: priors
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A1).

## Problem

`@PyAutoFit/autofit/mapper/prior/log_gaussian.py:71-114` defines two
helpers that pass kwargs the constructor does not accept:

```python
# log_gaussian.py:95-100  (with_limits)
return cls(
    mean=(lower_limit + upper_limit) / 2,
    sigma=upper_limit - lower_limit,
    lower_limit=lower_limit,    # <-- ctor does not accept this
    upper_limit=upper_limit,    # <-- ctor does not accept this
)

# log_gaussian.py:109-114  (_new_for_base_message)
return LogGaussianPrior(
    *message.parameters,
    lower_limit=self.lower_limit,   # self.lower_limit never set
    upper_limit=self.upper_limit,   # self.upper_limit never set
    id_=self.instance().id,
)
```

`LogGaussianPrior.__init__` signature is `(mean, sigma, id_)` (lines 13-19).
Both helpers will raise `TypeError`. This is the same structural shape
as the original `LogUniformPrior` sign-convention bug — the LogGaussian
branch has clearly never run end-to-end.

## Wider context — how these helpers are called

`with_limits` is the standard prior-passing entry point. It is invoked
indirectly through model-mapper passing flows that look like:

- `Prior.with_limits` is called when re-creating priors centred on the
  posterior of a previous run.
- `_new_for_base_message` is called from message projection / EP code
  paths when the underlying message has been refit and the wrapper
  needs reconstructing.

Both flows are dormant until a user runs a fit that produces a
`LogGaussianPrior` result and then chains a second fit that uses
prior-passing on that parameter. That combination has apparently
never been exercised — which is why the crash is latent.

## Python reproducer

```python
# Reproducer: log_gaussian_with_limits_crash.py
# Run: python log_gaussian_with_limits_crash.py
import traceback

from autofit.mapper.prior.log_gaussian import LogGaussianPrior

print("=== with_limits ===")
try:
    p = LogGaussianPrior.with_limits(lower_limit=0.01, upper_limit=10.0)
    print(f"Unexpected success: got {p!r}")
except TypeError as e:
    print(f"TypeError as expected: {e}")
    traceback.print_exc()

print()
print("=== _new_for_base_message ===")
# Build any LogGaussianPrior, then attempt the helper path
p = LogGaussianPrior(mean=0.0, sigma=1.0)
try:
    new = p._new_for_base_message(p.message.base_message)
    print(f"Unexpected success: got {new!r}")
except (TypeError, AttributeError) as e:
    print(f"Error as expected: {type(e).__name__}: {e}")
    traceback.print_exc()
```

Expected (buggy) output: `TypeError: __init__() got an unexpected keyword
argument 'lower_limit'` for both calls (with an additional `AttributeError:
'LogGaussianPrior' object has no attribute 'lower_limit'` likely surfacing
before the TypeError on the second call).

## Proposed fix

Drop the unused kwargs in both helpers:

```python
@classmethod
def with_limits(cls, lower_limit: float, upper_limit: float) -> "LogGaussianPrior":
    return cls(
        mean=(lower_limit + upper_limit) / 2,
        sigma=upper_limit - lower_limit,
    )

def _new_for_base_message(self, message):
    return LogGaussianPrior(
        *message.parameters,
        id_=self.instance().id,
    )
```

There is no `lower_limit` / `upper_limit` for a true log-Gaussian (its
support is `(0, ∞)`), so this fix is the right semantic answer too —
the kwargs should never have been there.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/mapper/prior/log_gaussian.py` end-to-end
   (not just the lines quoted) to confirm the constructor signature
   has not drifted since this prompt was written.
2. Run the reproducer above as a standalone script. Confirm both
   helpers raise.
3. Sketch the fix in a scratch checkout (no commit) and re-run the
   reproducer. Confirm both calls now succeed.
4. File the GitHub issue via `/create_issue priors/01_log_gaussian_with_limits_crash.md`.
5. **In the issue body, explicitly request that a collaborator with
   probabilistic-programming background verify before any PR opens.**
   The proposed fix is mechanical, but the audit was AI-generated and
   we want a second pair of eyes.
6. **Stop. Do not call `/start_dev` until the issue has at least one
   confirmation ack.**


## Fable verdict (2026-07-08, PyAutoFit main @ 0f26ff2d8; PyAutoFit#1330)

**Verdict: CONFIRMED — fix now (severity: medium-high).**
`with_limits` raises `TypeError: __init__() got an unexpected keyword argument
'lower_limit'` as predicted. `_new_for_base_message` also crashes, but via a
different path than the audit predicted: `self.lower_limit` resolves through
`Prior.__getattr__` to the message, and the call then fails with
`AttributeError: 'TransformedMessage' object has no attribute 'instance'`.
Same conclusion — this branch has never run end-to-end. Note
`NormalMessage.from_mode` on current main now defensively pops
`lower_limit`/`upper_limit` kwargs, a workaround in the same family.
Proposed fix stands (drop the kwargs; a log-Gaussian has support (0, inf)).

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
