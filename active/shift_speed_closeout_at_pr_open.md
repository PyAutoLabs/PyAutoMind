# M3.7b Close-out starts at PR-open, merges on green CI, no pre-merge full smoke

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) an orchestrator test: a `glance` or `notify` PR that a worker has just opened, with CI still pending, gets its close-out started on the next tick (on main it waits for CI to land); (2) the rendered close-out prompt has no `pyauto-heart smoke --affected-by` step, and tells the session to run the witness and read the diff first, then wait in-turn for CI and judge it with `ci-verdict` before merging; (3) an orchestrator test: a later PR of the shift whose changed files are disjoint from every PR of the shift merged ahead of it on that library is closed out without a branch-update session; (4) the same test with one shared file, or with GitHub reporting a conflict, still gets the branch update and waits for green CI on the new head; (5) merge order is unchanged: a later PR never merges while an earlier PR of the shift on that library is open; (6) `AUTONOMY.md` records rulings S2, S5 and S6 with their revert conditions; (7) the Brain suite passes
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat: "we still seem to be normalizing 18 minutes of testing plus 10+ minutes to merge. What would a solution which is much closer to the faster turn over look like?" Then: "approved, all rulings yes".

## Why

After PyAutoBrain#684 and #685 a worker's PR waits for: PR CI (Galaxy 4 minutes, Fit 10), about 5 minutes of ticks, a 4 to 5 minute close-out, and a full affected smoke estimated at 10 to 15 minutes on the laptop. Each later PR in a chain on one library also pays a branch update and a second CI run on the new head. A five-PR chain is about two hours of merging. The serial workspace smoke failed no script in 7 of 7 tasks.

## Rulings (human, 2026-11-19)

- **S2, leg 2 before an unattended merge.** The pre-merge smoke is the worker's targeted smoke. The close-out runs no full affected smoke. The full sweep runs in the cloud after merge (M3.7d, M3.7e). *Revert condition:* one red sweep traced to an unattended merge restores the close-out's full affected smoke.
- **S5, close-out timing.** A close-out may start at PR-open. It runs the `Witness:`, reads the diff adversarially and checks labels, public names and Heart while CI runs, then waits in-turn for CI and merges on a green `ci-verdict`. Every other guard of "Unattended `glance` merges — 2026-11-03" applies unchanged, and the merge slot is taken immediately before the merge, as now.
- **S6, M3.6j ruling (a) amended.** The branch update and the CI rerun on the new head are required only when the PR's changed files overlap those of a PR of this shift merged ahead of it on that library, or when GitHub reports the branch as conflicting. Otherwise the PR merges on its own green CI. Merge order (rulings b, c, f) is unchanged. *Revert condition:* one red `main` CI traced to two disjoint shift PRs merged this way restores the unconditional update.

## Shape

- `_orchestrator.py`: `_start_closeouts` starts on PR-open for an eligible tier (not `decision-taken`, not `judge`, no public-name hit) rather than on landed CI; a close-out that is waiting behind an earlier open PR still waits (no session spent on it until it is next in order); the branch-update decision compares changed-file lists (`gh pr view --json files`, within the watcher's existing network surface for shift PRs).
- `closeout_template.md`: remove step 5 (the smoke); reorder so the witness and diff read come before the CI judgment; add the in-turn wait with a stated limit (a CI that has not finished in 30 minutes refuses to `/prm`).
- `AGENTS.md` (batch conductor), "The watcher": describe the new timing and the overlap rule.
- `AUTONOMY.md`: S2, S5, S6 in the "Shift speed — 2026-11-19" section; leg 2's "Before any unattended merge" bullet and the M3.6j paragraph point to them.

## Risks to state in the PR

- Two disjoint PRs that are each green can break `main` together; `main` CI and the shift-end sweep find it after the merge.
- A close-out that starts at PR-open and then sees red CI has spent its tokens; count them in the digest as today.

## Order

After M3.7a. Before M3.7c (same file).
