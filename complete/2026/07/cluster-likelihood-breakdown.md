## cluster-likelihood-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/57 (closed)
- completed: 2026-07-09
- pr: autolens_profiling#58 (merged; + ruff-format fix commit — repo lints with `ruff format --check`, not just `ruff check`)
- notes: likelihood_breakdown/cluster/{source_plane,image_plane}.py in house style; 8-digit LL
  parity with production fits (getting there documented three production-formula facts: chi²
  weights distances by |mu|², name pairing hands the fit the model Point centre, noise norm uses
  sigma/mu). Source-plane 3.1 ms vs image-plane solve 0.32 s/call + 10.5 s compile/plane (the
  ~100x ratio, per-step). simulators/cluster.py synced to the scaling-tier truth.
