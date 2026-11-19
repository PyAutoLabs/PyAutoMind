Shift workers now test like a task done in a chat: the changed repo's unit tests, the witness and a targeted smoke (`pyauto-heart smoke --targeted --changed-files …`: only curated scripts that reference the changed module or a touched public name). The full affected smoke (`pyauto-heart smoke --affected-by <repos> --jobs 3`, chain-selected workspaces in parallel with per-process thread caps) moves to the close-out and runs only before an unattended merge. `notify` workers no longer merge in-turn inside a shift; they end at PR-open and the close-out merges (human ruling "ii", 2026-11-19). A human `/smoke_test` with no flags still runs every workspace serially; Heart's release validation is unchanged.

Motivated by shift 2026-11-19-am: the worker's serial all-workspace smoke took ~35–40 min of a 75-min shift (per-script speed at or below CI medians). Human: "this is over testing and makes things too slow"; approved plan C, then "ii".

Shipped in PyAutoHeart#353 (`--affected-by`, `--jobs`, `--targeted`) and PyAutoBrain#685 (worker/close-out templates, AUTONOMY.md leg 2 and the notify ruling), merged 2026-11-19 by human /prm. Heart 1482 and Brain 2420 tests pass. Known limits on the PRs: order-dependent targeted scripts (euclid), HowToLens has no smoke_tests.txt.

## Original prompt

# Shift workers' smoke leg runs only the affected workspaces, in parallel

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-19
Issued: 2026-11-19
Epic: autonomous-orchestrators
Consequence: judge
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in the cockpit for shift 2026-11-19-am, after asking "Are smoke tests or the things these orchestrator tasks running slower than they have been or they are for normal development?": "yes file it and then implement it, this is over testing and makes things too slow."

## Why

Measured in shift 2026-11-19-am (task `jax_grad_of_sersic_stellar_mass_deflections`, PyAutoGalaxy): the worker's smoke leg ran every workspace one after another — autofit nb 1.2 min, autogalaxy nb 2.5, autolens nb 5.9, autolens_workspace_test 12.8 (CI median 7.2), euclid 1.6, HowToLens ~5.8, autocti ~4.1, autocti_test — about 35–40 min of a 75-min shift, which delayed the next named task on the library. Per-script speed is normal (at or below CI medians, except autolens_workspace_test's cold-cache scripts); the cost is scope and serial order.

Sources: Heart `skills/smoke_test/SKILL.md` ("Default: run ALL six workspaces … Run a subset only when the user explicitly passes workspace names"); Brain `AUTONOMY.md` autonomous-ship gate leg 2 ("all six workspaces by default"); `pyauto-heart smoke` runs the selected workspaces serially. Shift workers are inconsistent: some ran all workspaces (213 scripts, #724), others the affected ones (99 scripts, #726).

## Proposed shape (to be planned)

- **Targeted:** select workspaces whose `chain:` in Heart `config/repos.yaml` `smoke:` contains a repo the branch changed (e.g. a PyAutoGalaxy change skips autofit, autocti, autocti_test). A `pyauto-heart smoke --changed <repos>` (or `--affected-by`) option does the selection.
- **Parallel:** `pyauto-heart smoke --jobs N` runs the selected workspaces concurrently (each already has its own cached env), with a laptop-safe default cap and per-workspace thread caps; wall time ≈ the slowest workspace.
- AUTONOMY.md leg 2 and the Heart skill default for autonomous/shift ships become "affected workspaces, in parallel"; the full serial sweep stays the default for a human `/smoke_test` and for Heart's release validation.

## Answers from the human

2026-11-19, in the cockpit: asked whether 13 or 6 minutes was still slower than a chat task (yes); approved shape C ("approve C"). Full plan on https://github.com/PyAutoLabs/PyAutoHeart/issues/352.

## Plan C (approved by the human 2026-11-19: "approve C")

A shift worker tests like a task done in a chat; the full affected smoke moves to the close-out, and runs only before an unattended merge.

1. **Worker (fast, chat-like):** the changed repo's unit tests, the task's `Witness:`, and a **targeted smoke**: only the curated `smoke_tests.txt` scripts (in workspaces whose `chain:` includes a changed repo) that reference the changed code — matched by the changed modules' import paths and the public names the diff touches. If nothing matches, run the single cheapest script of the changed library's own workspace as an import check. Then open the PR and end. Target: a few minutes.
2. **Close-out (full, parallel, off the critical path):** before an *unattended* merge (glance/notify), the close-out runs `pyauto-heart smoke --affected-by <changed repos> --jobs N` on the PR head (task-worktree-equivalent env), and refuses on any failure → /prm. Since M3.6j the next named task's worker has already started, so this no longer delays the shift.
3. **PRs that go to the human's /prm** (decision-taken, judge, public-name, refused): no automatic full sweep — chat-level checks plus PR CI; the PR body says which smoke ran.
4. **Heart CLI** (`heart/smoke.py`, `pyauto-heart smoke`):
   - `--affected-by REPO[,REPO…]`: select workspaces whose `config/repos.yaml` `smoke: workspaces: *: chain:` contains any of them.
   - `--jobs N` (default 1 = today's serial behaviour; shift close-outs pass a laptop-safe 3): run selected workspaces concurrently, each in its existing cached env, with per-process thread caps (OMP/MKL/OPENBLAS/NUMBA_NUM_THREADS, XLA CPU threads) so N×threads ≤ cores; output and per-workspace result files stay separate; overall exit non-zero if any workspace fails.
   - `--scripts-matching PATTERN…` (or `--targeted --changed-files <list>`): run only the curated scripts whose source matches — the worker's targeted mode. A human `/smoke_test` with no flags keeps the full serial sweep; Heart's release validation is unchanged.
5. **Rules/docs:** Brain `AUTONOMY.md` autonomous-ship gate leg 2 (~line 325) rewritten to this split (worker = targeted; close-out before an unattended merge = affected+parallel; human /prm = chat-level); `agents/conductors/batch/worker_template.md` and `closeout_template.md` updated; Heart `skills/smoke_test/SKILL.md` documents the new flags (default unchanged for humans); `skills/ship_library` reference if it restates leg 2. Keep `skills/batch/batch.md` ≤ 200-line budget.
6. **Tests:** Heart — workspace selection per changed repo (PyAutoGalaxy skips autofit/autocti/autocti_test; PyAutoFit selects all); `--jobs 3` gives the same pass/fail and result files as serial on fake workspaces; one failing workspace fails the run; targeted script selection from a fake `smoke_tests.txt`. Brain — the worker prompt asks for targeted smoke, the close-out prompt for affected+parallel before a merge and none for a /prm-bound PR.

Deploy only after shift 2026-11-19-am's late window closes (12:15Z): canonical PyAutoBrain and PyAutoHeart are read by live workers.
