# PyAutoGut organ decision

Type: research
Target: PyAutoBrain
Repos:
- PyAutoGut
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: decided

PyAutoGut organ decision. Settle whether the organism should grow a **new peer
organ repo** to own the lifecycle of *condemned self-material* — the stale
branches, `git stash` entries, dead code and retired tests that a hygiene /
`repo_cleanup` sweep is 95%-but-not-100% sure is trash. Deliverable: a written
decision (grow the organ, or keep deletion inline in the hygiene conductor's
`tidy`/`repo_cleanup` path) with the organ identity, the storage model, and the
boundary rules against Immune (`bug`), the hygiene conductor, Heart and Memory.

## The demonstrated need

Surfaced in a remote design conversation with the user (2026-07-12) reflecting on
live hygiene runs across the maintained codebases (PyAutoLens, PyAutoFit,
PyAutoArray, PyAutoGalaxy, the `*_workspace*` repos). Three distinct pains, none
of which the current `tidy` → `repo_cleanup` path resolves:

1. **Decision fatigue at the point of least context.** `repo_cleanup`'s safety
   gates (`yes, force delete <name>`; stash keep/apply/drop) are correct, but
   they fire *synchronously, one item at a time, mid-sweep*, while the user is
   context-poor on each. The human is the bottleneck at the worst moment.
2. **The 95%-confident-but-not-certain items have no home.** They are neither
   "keep" nor "safe to delete now", so today the only way to resolve them is to
   interrupt the user — which is pain (1). There is no *staging state* for
   "probably dead, recoverable if wrong".
3. **The fragile forms have no durable backup.** Recoverability is not uniform.
   Merged branches and committed code deletions live in remote history forever —
   a note is enough. But **local-only unmerged branches** and **`git stash`
   entries** exist only in one machine's reflog and are gc-pruned; a manifest
   that merely *points* at a stash is worthless the moment it is dropped. These
   need their bytes captured somewhere durable *before* deletion — and captured
   as a git object, not as lossy `.md` (which drops binaries, exact history and
   re-appliability).

## Decision (2026-07-12, remote design conversation with user)

**Grow a new peer organ repo, `PyAutoGut`, that owns the full lifecycle of
condemned self-material.** It holds condemned items as **durable git refs**
(not markdown copies), reabsorbs the occasional false-positive during a transit
window, and **voids (deletes) them itself on a sweep**. It is a *body organ* —
a peer to PyAutoHeart, PyAutoMemory and PyAutoHands — **not** a PyAutoBrain
function.

### Why a repo — and why this is consistent with the hygiene decision, not a reversal

`research/pyautobrain/hygiene_agent_decision.md` ruled that *hygiene* earns no
repo because "a repo is earned by a persistent reusable-artifact lifecycle …
hygiene has none: its output is a prioritized worklist that lives in Mind
issues." **PyAutoGut passes that exact test that hygiene failed.** Its artifact
is not a worklist — it is a *persistent, recoverable store of git objects* (the
condemned branch/stash refs) held through a defined transit window and
salvageable until voided. That is precisely a persistent reusable-artifact
lifecycle, the same criterion that earns Heart (check functions + verdict
history) and profiling (timing tables/baselines/pins) their repos. Hygiene holds
only a worklist → no repo; PyAutoGut holds bytes that must survive → a repo.
Same doctrine, applied consistently.

The hygiene conductor stays exactly as decided: an orchestrator with no repo. It
*drives* PyAutoGut; it does not become it.

## Organ identity — the gut (large intestine), not the spleen

The organ is the **gut**. The deciding property is **elimination**: PyAutoGut
performs the final deletion itself, and elimination is a gut function. The spleen
filters and salvages senescent cells but *does not excrete* — it hands waste
downstream to be voided; an organ that owns the deletion is therefore the
intestine, not the spleen. The fit is complete on every axis the user's need
names:

- **"grows, then I clean it now and then"** — the accumulate-then-void rhythm is
  the bowel's, not the spleen's.
- **owns the deletion** — gut (excretion); the spleen never eliminates.
- **"different forms and formats, more care"** — the gut's decomposer microbiome
  breaks down heterogeneous dead matter and reabsorbs what is still useful.
- **recovery of the 5% false-positive** — preserved by the gut's **transit
  time**: matter is reabsorbed right up until elimination. An item sitting in
  PyAutoGut with a `sweep-after` date is still recoverable (reabsorption); only
  the sweep voids it. The holding window *is* the transit, with a clock on it —
  so choosing the gut does not trade away the safety the spleen would have given.

At **ecosystem** scale the same role is the **decomposer**, and the gut is
literally where the organism's decomposer microbiome lives — so the organ-scale
and ecosystem-scale answers converge on one place.

## Storage model

- **Payload = durable git refs, never markdown.** Fragile forms (local unmerged
  branches, stashes) are first materialised as real commits on a remote — pushed
  under an archive namespace into PyAutoGut as the attic remote — *before* the
  local copy is deleted. Recovery is a checkout. A stash becomes a branch/commit
  via `git stash branch` or a tagged stash commit.
  <!-- Implementation revision (2026-07-12, during the repo_skeleton build): the
       namespace is `refs/heads/archive/condemned/<name>` (a branch prefix), NOT
       a custom `refs/archive/condemned/*`. GitHub only accepts pushes to
       refs/heads/* and refs/tags/*, so the custom namespace is unpushable. The
       "out of git branch -a" nicety is relaxed to "filter with
       `git branch --list 'archive/condemned/*'`". Tags (refs/tags/condemned/*)
       were the alternative — hidden + immutable — but rejected: immutability
       blocks re-pointing, and they were unusable in the cloud session's git
       proxy. -->

- **Catalog = a manifest in the Mind** (`condemned.md`, symmetric to
  `parked.md`): one entry per item — `type` (branch/stash/file/test), `locator`,
  `confidence`, `reason`, `merged?`, `condemned` date, `sweep-after` date,
  `breaks-if-wrong`, and the archive ref/SHA to recover from. The `.md` is the
  index; the git refs are the payload.
- **Merged branches skip the pen** — reachable from `main` forever, near-zero
  risk; the conductor recommends them straight to deletion without staging.
- **Committed code/test deletions** need only the pre-delete SHA recorded; the
  remote history holds the old bytes.

## Boundaries (settle in PyAutoGut's / the conductor's AGENTS.md)

- **vs Immune (`bug`)** — Immune fights the *foreign and pathological* (bugs,
  regressions, failing tests: code that is *wrong*). PyAutoGut processes the
  *self and spent* (code that is not wrong, just done). No overlap.
- **vs the hygiene conductor** — mirror the **Heart ↔ vitals** template exactly:
  Heart is the organ that does the health-checking; the vitals faculty only
  *reads* it. Likewise PyAutoGut is the organ that *holds and voids*; the hygiene
  conductor *drives* it (decides what to condemn, triggers a sweep) and owns none
  of the storage. The staging-and-clearance substrate lives in the organ; the
  reasoning stays in the Brain.
- **vs Memory** — the two **storage organs** are mirrors: PyAutoMemory holds what
  the organism *keeps* (durable knowledge); PyAutoGut holds what it *sheds*
  (durable discard, recoverable until voided). Retention vs release.
- **vs Heart / profiling** — PyAutoGut issues no health verdict and measures no
  compute speed; it is upkeep storage, not observation.

## Follow-ups (to file only if the decision is to build — implementation prompts,
not filed here)

- `feature/pyautogut/*` — stand up the PyAutoGut repo skeleton (attic remote +
  archive-ref convention + the `condemned.md` manifest schema).
- `feature/pyautobrain/*` — add the drive seam: a PyAutoGut-aware mode so hygiene
  `tidy` *files candidates into `condemned.md`* (async, no gate) instead of the
  synchronous per-item `repo_cleanup` interrogation, and a `sweep` mode that runs
  the existing safety gates in batch against the manifest at a time the user
  chooses.

<!-- settled 2026-07-12 in a remote design conversation with the user, continuing
     the hygiene thread from research/pyautobrain/hygiene_agent_decision.md. The
     earlier doc's "no repo for hygiene" holds; PyAutoGut is a separate peer organ
     that passes the same persistent-reusable-artifact-lifecycle test hygiene
     failed. Organ settled by elimination: gut (owns voiding), not spleen. -->
