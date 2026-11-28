# Frozen Nautilus geometry as a high-weight 30D predictor — merged

Merged 2026-11-25 under the human's `/prm`: [autofit_profiling#39](https://github.com/PyAutoLabs/autofit_profiling/pull/39), CI green, head an ancestor of origin/main.

## Delivered

- Replayed frozen bounds from the three independent 30D fits over 60 shells and 1,953,350 held-out rows (`experiments/nautilus_shell_geometry_signal/`).
- The ellipsoid score selected about a tenth of points and captured 84.06%, 83.41% and 64.32% of squared posterior weight, beating the registered 2× enrichment threshold on every seed; the neural margin missed on every seed.
- This identifies a candidate for a support-preserving proposal experiment; time savings and evidence accuracy under a modified proposal remain open.

## Original prompt

# Do frozen Nautilus bounds predict the high-weight draws inside a shell?

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Autonomy: supervised
Lane: local-dev

## Original request

> continue

## Registered phase 0b diagnostic

Use the three independently explored 30D matched-ESS archives from PR #35 and their checkpoint identities from PR #37. Use only fresh rows after the original exploration cutoffs. For every shell, score native unit-cube points using (1) negative squared distance in the frozen neural-bound enclosing ellipsoid's coordinates (best across components), and (2) the highest native ensemble margin above its stored threshold among component ellipsoids containing the point. A shell without a usable score contributes neutral ties. The frozen models learned only during the original exploration. Keep networks and all native defaults.

Use the first temporal half of each shell to set its top-decile cutoff for each score; apply it unchanged to the second half. Resolve boundary ties fractionally so constant scores are neutral. Report selected fraction, recall of held-out top-1%-likelihood points within shell, and fraction of held-out global squared posterior weight captured. Compare both capture metrics against random selection matched to the actual selection rate in each shell. Count every shell and held-out row. No training on held-out labels or tuning against the three outcomes.

Advance a score to a bounded support-preserving proposal experiment only if it achieves at least twice matched-random capture on both metrics in every seed. Two scores are evaluated separately. This screening rule concerns predictive signal only. It is not an adoption, accuracy or speedup gate. No point is discarded from inference, no new fit is run, and the full-support weighting and cost of a real change would need validation. [Predecessor](https://github.com/PyAutoLabs/autofit_profiling/pull/37) · [Canonical profiling producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md). Ship a draft PR and update the epic.

Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/38

## Outcome

[Draft PR #39](https://github.com/PyAutoLabs/autofit_profiling/pull/39). On the three independent seeds, ellipsoid distance captured 64.32–84.06% of held-out squared weight at about 10% selection. Only ellipsoid distance qualified for the support-preserving proposal experiment. [Results and validation](https://github.com/PyAutoLabs/autofit_profiling/blob/406a436acbf78e701644f6d82349a4cbb597996c/experiments/nautilus_shell_geometry_signal/README.md). Awaiting human review.
