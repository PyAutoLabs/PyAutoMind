# Add the hygiene → PyAutoGut drive seam

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoGut
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Add the drive seam that lets the hygiene conductor use **@PyAutoGut** — the
second build follow-up from `research/pyautobrain/pyautogut_organ_decision.md`.
Depends on the repo skeleton (`feature/pyautogut/repo_skeleton.md`) existing
first.

The seam mirrors the **Heart ↔ vitals** template exactly: the organ *holds and
voids*; the @PyAutoBrain hygiene conductor *drives* it (decides what to condemn,
triggers a sweep) and owns none of the storage.

- **PyAutoGut-aware `tidy` mode.** Instead of the synchronous, one-item-at-a-time
  `repo_cleanup` interrogation (the decision doc's pain #1 — decision fatigue at
  the point of least context), `tidy` *files candidates into `condemned.md`*
  asynchronously, with no per-item gate. This gives the 95%-confident-but-not-
  certain items a home (pain #2) and captures the fragile forms' bytes as durable
  archive refs before deletion (pain #3).
- **Batch `sweep` mode.** Runs the *existing* `repo_cleanup` safety gates
  (`yes, force delete <name>`; stash keep/apply/drop) in batch against the
  manifest, at a time the user chooses — the transit-window clock: items with a
  past `sweep-after` date are voided; anything still wanted is reabsorbed
  (recovered) before then.

No second gate implementation — reuse `repo_cleanup`'s gates. The conductor
reasons and delegates; @PyAutoGut performs the actual deletion (elimination is a
gut function).

<!-- formalised 2026-07-12 from ideas.md by intake review; provenance:
     research pyautogut-organ-decision · research/pyautobrain/pyautogut_organ_decision.md.
     Work-type corrected to feature/ per the decision doc's named follow-up
     (the deterministic classifier guessed refactor from surface keywords). -->
