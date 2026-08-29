# Teach repos_sync --write to stamp organ config surfaces

Type: feature
Target: pyautomind
Themes:
- mind-workflow
Difficulty: hard
Autonomy: supervised
Priority: low
Filed: 2026-08-17 (backfilled from git)
Issued: 2026-08-29

The design's own endgame for tenant-firewall drift, specified in
`docs/pyautobrain/pyautoscientist_generalisation_assessment.md` §8-4 and
restated in `docs/pyautobrain/pyautoscientist_phase3_research.md` ("Demand-
gated, later"): teach `scripts/repos_sync.py --write` to *stamp* the organ
config surfaces from the body map + per-organ policy fields, the way it
already stamps doc blocks. Quoting the assessment: "That turns 'edit five
mirrors' into 'edit one file, regenerate' … **This is the only real
engineering in the whole plan**, and it removes his own hand-mirroring burden,
so it pays for itself even with zero adopters."

Filed 2026-08-17 from the tenant-firewall drift-clear
(PyAutoMind#198), whose research pass found this remedy named in the design
but never filed anywhere in Mind. Context there: the allowlist grew 72→109
files in five weeks of reactive patches; #198's PR-time CI gates stop drift
*landing*, this task removes the hand-maintained mirrors that *generate* it.

## Scope sketch (to be refined at start_dev)

- Candidate surfaces to stamp: Heart `config/repos.yaml` blocks
  (`version_skew:`, the `smoke:` block #198 introduces), Hands
  `autohands/config/workspaces.yaml`, and any organ constant table still in
  the allowlist that is identity-derivable.
- Needs per-organ policy fields the body map deliberately does not carry
  (dependency chains, package import names, short keys) — decide where policy
  lives (per-organ policy YAML consumed by the stamper vs schema extension),
  honouring the body map's "identity only" doctrine.
- The stamper must be drift-checked itself (the check legs already exist —
  stamping makes them tautologies for stamped blocks, which is the point).

## Not in scope

- The firewall check semantics (unchanged).
- The comments/docstrings exemption — CONSIDERED AND REJECTED, recorded in
  `complete/2026/08/autohands-firewall-allowlist.md`; do not re-propose.
