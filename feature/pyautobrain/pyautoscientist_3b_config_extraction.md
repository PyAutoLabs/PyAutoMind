# PyAutoScientist 3b-4: organ config extraction (shrink the firewall allowlist)

Type: refactor
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBuild
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: low
Status: draft — issue on demand (a concrete adopter or launch commitment)

The original Phase 3 extraction, unchanged in scope (assessment §6-D):
Heart version_skew/readiness tables → config/; Build maps → policy YAML;
Brain constant tables → derived from repos.yaml where identity, policy
file where vocabulary. One PR per organ behind its test suite. Each
extraction MUST shrink `FIREWALL_ALLOWLIST` in repos_sync.py — the
allowlist diff is the acceptance metric. Optionally follow with teaching
`repos_sync --write` to stamp the surfaces from the body map (kills the
live setup's own hand-mirroring; §8-4 "the only real engineering").
