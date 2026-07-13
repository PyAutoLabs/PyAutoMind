# Stand up the PyAutoGut repo skeleton

Type: feature
Target: PyAutoGut
Repos:
- PyAutoGut
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Stand up **@PyAutoGut**, the new peer organ repo that owns the lifecycle of
*condemned self-material* — decided in
`research/pyautobrain/pyautogut_organ_decision.md`. This is the first of that
decision's two build follow-ups (the Brain-side drive seam is the sibling
`feature/pyautobrain/hygiene_pyautogut_drive_seam.md`).

Scope — the storage substrate only (organ holds + voids; the reasoning stays in
the Brain conductor):

- **Attic remote + archive-ref convention.** Fragile forms (local unmerged
  branches, `git stash` entries) are materialised as real commits and pushed
  under an archive namespace — `refs/archive/condemned/<name>` — which stays out
  of `git branch -a`, into PyAutoGut as the attic remote, *before* the local
  copy is deleted. Recovery is a checkout; a stash becomes a branch/commit via
  `git stash branch` or a tagged stash commit.
- **The `condemned.md` manifest schema** (lands in @PyAutoMind, symmetric to
  `parked.md`): one entry per item — `type` (branch/stash/file/test), `locator`,
  `confidence`, `reason`, `merged?`, `condemned` date, `sweep-after` date,
  `breaks-if-wrong`, and the archive ref/SHA to recover from. The `.md` is the
  index; the git refs are the payload. Merged branches skip the pen (reachable
  from `main` forever); committed code/test deletions need only the pre-delete
  SHA recorded.
- **Register PyAutoGut as a peer organ**: add it to @PyAutoMind `repos.yaml` and
  to @PyAutoBrain `ORGANISM.md` (then `python3 scripts/repos_sync.py --write`),
  as a body organ peer to Heart/Memory/Hands — the storage mirror of Memory
  (Memory keeps; Gut sheds, recoverable until voided).

Boundaries to settle in PyAutoGut's `AGENTS.md` (from the decision doc): vs
Immune/`bug` (self+spent, not foreign+pathological), vs the hygiene conductor
(Heart↔vitals template — the conductor drives, the organ stores/voids), vs
Memory (retention vs release), vs Heart/profiling (no verdict, no compute
measure).

Note: creating the GitHub repo itself is a human-required step; the rest of the
skeleton (conventions, manifest schema, doctrine wiring) is the supervised work.

<!-- formalised 2026-07-12 from ideas.md by intake review; provenance:
     research pyautogut-organ-decision · research/pyautobrain/pyautogut_organ_decision.md.
     Target PyAutoGut is a new repo not yet in repos.yaml, so the deterministic
     classifier could not resolve it — corrected to feature/pyautogut per the
     decision doc's named follow-up. -->
