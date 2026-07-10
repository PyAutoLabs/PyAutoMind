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

## 4a/4b split (recorded 2026-07-10, Heart#53)

4a SHIPPED: Heart (version_skew map + readiness/dashboard library tuples →
config/repos.yaml, strict no-fallback) + Build (run_all matrix + slow_skip
defaults → autobuild/config/workspaces.yaml); allowlist shrunk 42→16 tokens
across five files. **4b remaining (Opus-executable against 4a's pattern):**
Brain constant tables — sizing sets/aliases/MEMORY_WIKIS, intake
TARGET_SIGNALS, feature/refactor maps, release LIBRARIES + nightly TAG_REPO —
derived from repos.yaml where identity, per-organ policy file where
vocabulary; Brain's 12-test suite is thin, so pair each move with a seam
test. Also still open: Heart url_check_live fixup rules → config.

## 4b SHIPPED (2026-07-10, Brain#75)

Brain identity sets derive from the body map at runtime (strict); vocabulary
in PyAutoBrain/config/policy.yaml (aliases, memory_wikis, target_signals,
default wikis, test witness, release policy incl. nightly tag_repo); Heart
url_check_live's 31 fixup rules → config/url_fixups.yaml (byte-identical,
verified). Seam tests: Brain suite 12→22. Feature/intake decisions verified
identical pre/post. Allowlist: sizing 8→1, refactor+activity_gate rows
DELETED, url_check_live 11→3. Config extraction COMPLETE — the remaining
allowlist is docstring examples + test fixtures + the workspace-root default.
