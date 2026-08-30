# Human review: the scaling_relation slam parks (imaging un-parked, multi_galaxy kept)

Type: human review
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci-smoke
Priority: normal
Status: awaiting human review
Consequence: judge
Review-minutes: 25
Unattended: never
Filed: 2026-08-29

Shipped by an agent session on 2026-08-29 in two PRs; the human asked to read the outcome
before it counts as done. This is a sign-off, not a bug — the open bug is filed separately.

## What shipped

- **autolens_workspace#513** (merged `b59229be`) — removed the `no_run.yaml` park for
  `imaging/features/scaling_relation/slam` after a cache-free capped run: exit 0, 6 searches,
  anchor luminosity 22.47. Record: `complete/2026/08/unpark-imaging-scaling-relation-slam.md`.
- **autolens_workspace#516** (merged `148d1eee`) — the gated un-park of
  `multi_galaxy/features/scaling_relation/slam` FAILED; its park reason was rewritten to record
  the verified #502 mask fix (radius 4.70) and the new third cause (all-zero MGE intensities in
  the truncated light stages → `Measured luminosity is 0.0`). Record:
  `complete/2026/08/unpark-multi-galaxy-scaling-relation-slam.md`. Follow-up bug:
  `complete/2026/08/multi-galaxy-scaling-zero-intensity.md` (fixed and un-parked 2026-08-29, autolens_workspace#519)
.

## What to check (read-and-report)

1. **Is the imaging un-park sound?** The script is now in scope for the discovery-based
   Workspace Smoke leg but is NOT in the curated `smoke_tests.txt` (only its `modeling.py`
   sibling is). Decide whether `slam.py` should be added to the curated list.
2. **Is the multi_galaxy diagnosis heading the right way?** The agent's reading: the imaging
   sibling passes the same smoke profile with a non-zero anchor, so the zero intensities are
   specific to this script's two-stage (fixed-pair + tier) light setup, not a test-mode limit.
   A human who knows the SLaM light stages should confirm that framing before the fix lands.
3. **The rewritten park reason** (`config/build/no_run.yaml`, the `multi_galaxy/...` line) is
   long — three causes, a path trap, and a rule. Is that the right place for that history, or
   should it point at the record and stay short?
4. **Runner trap** worth knowing: `run_python.py --report-dir` hides script stdout on success,
   so evidence runs need a second invocation without it (now in memory + the record).

Sign off by retiring this prompt (`scripts/lifecycle.py record …`); anything that does not pass
goes back through `/intake` as an ordinary task.
