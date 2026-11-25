# Does CPU placement of posterior derived quantities shorten a GPU Nautilus fit?

Type: research
Target: @autolens_inference
Epic: nautilus-fast-likelihoods
Consequence: judge
Lane: local-dev

> continue...

Continue the [JWST ring feeder pilot](https://github.com/PyAutoLabs/autolens_inference/pull/75). Replay two frozen, reproducible 100-row weighted selections from its two serial-GPU posterior tables. Compare native GPU derived outputs with the same computation in a fresh CPU interpreter. Include serialization, startup, rebuilding the observed fixture, returning native samples and computing the summary. Check ordered keys, rows, weights and every retained value (rtol 1e-6, atol 1e-8). Require 15% and five seconds saved on both seeds before testing whole fits. If this clears, compare two pairs of complete GPU fits, reversing arm order by seed, with matched posterior selections, native serial training and ordinary output. Require the same inference results and at least 5% whole-fit savings on each seed. Publish all outcomes in a draft inference PR for human merge. Local representative conditional JWST F444W fixture, single GPU. Keep library and sampler defaults. The domain follow-up belongs to autolens_inference. No Pulse or Insight production campaign.

[Domain issue #76](https://github.com/PyAutoLabs/autolens_inference/issues/76)
