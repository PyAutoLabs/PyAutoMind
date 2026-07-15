# Audit pre_build.sh for the silent/fatal git-add failure class — and ask what its local commit is even for

Type: research
Target: PyAutoBuild
Repos:
- PyAutoBuild
- autofit_workspace
- autolens_workspace
- autogalaxy_workspace
- HowToFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Model: Fable

## What this is

An **audit** task with a design question attached. On 2026-07-15 the first manual live release
since 2026-07-09 hit **two bugs in `pre_build.sh`, both the same shape**, one after the other.
Each was ~5 lines to fix. Neither was hard. The point of this task is not to fix them — one is
already merged and the other is already filed — it is to find out **how many more of that shape
are in this file**, and whether the file's design is what keeps producing them.

The shape: **a `git add` whose failure is handled wrongly in one of two opposite directions.**

1. **Fatal.** `[ -d dataset ] && git add dataset/` under `set -e`. `git add` exits non-zero when
   every path it matches is ignored, so this killed the entire release on the first workspace
   processed. Merged as **PyAutoBuild#154**.
2. **Swallowed.** `git add -- *.py *.md *.txt *.cfg … 2>/dev/null || true`. Bash leaves unmatched
   globs literal, git rejects the **whole pathspec list** (`fatal: pathspec '*.cfg' did not match
   any files`, exit 128), and `|| true` eats it — so **nothing from that line is ever staged** in
   any repo missing one of those extensions. Filed as
   `draft/bug/pyautobuild/root_level_git_add_stages_nothing_on_unmatched_glob.md`, **unfixed**.

One over-fails, one under-fails. Both come from the same underlying assumption: that `git add`
either works or is worth dying over, when in this script it is routinely and *correctly* a no-op.

**There is already a confirmed third instance, and I found it while writing this prompt** — which
is the whole argument for the audit. `pre_build.sh` has exactly three `|| true` / `2>/dev/null`
sites (**:55, :79, :88**), and :55 is the README version bump:

```bash
echo "  Bumping README version → $readme_pkg v$VERSION..."   # prints unconditionally
sed -i "s/…/…/g" README.rst README.md 2>/dev/null || true
```

**No workspace has a `README.rst`** (checked autofit_workspace, autolens_workspace, HowToFit).
So this sed exits **2, every time, in every repo** — the `|| true` is not a safety net for a rare
case, it is **permanently load-bearing**, and a genuine sed failure is indistinguishable from the
expected missing-file one. The banner prints either way. Three sites, three instances of the class.
Assume there are more; that is the job.

**Take the time this needs.** This file commits and pushes to ~14 repos and then dispatches a live
PyPI release. It is the least-exercised, highest-consequence code in the organism.

## Why this went undetected (this is the interesting part)

Both bugs were **latent for days in a file that runs constantly** — because the *live* path barely
runs:

- The `2026.7.9.1` release (2026-07-09) **predates** PyAutoBuild#150 (merged 2026-07-13), which
  introduced bug 1 by dropping a `git add -f` (correctly — the `-f` was force-committing simulated
  datasets, #126).
- Every night since, `nightly-release` died at **Stage 4** (validation) on an unrelated bug, so it
  never reached **step 6** (the live release) where `pre_build` runs.
- So between 07-13 and 07-15, `pre_build`'s staging path executed **zero times**. **Merged is not
  the same as ever ran.**

And bug 2 is *still* invisible in production, because **`release.yml`'s `release_workspaces` job
regenerates and commits the same artifacts on the runner**. Verified 2026-07-15: origin/main's
READMEs correctly pin `2026.7.15.1` and `llms-full.txt`/`workspace_index.json` match freshly
generated local output — even though `pre_build` staged **none** of it locally. The runner covers
for the script.

## The design question worth more than the audit

If `release.yml` regenerates and commits these artifacts on the runner anyway, **what is
`pre_build`'s local commit actually for?**

Bug 2 has been silently no-op'ing the root-level staging for an unknown length of time and
**nobody noticed, because the outcome was correct anyway**. That is either:

- evidence the local staging is **redundant** and should be deleted (the lean-lever, delete-the-trap
  outcome — cf. PyAutoBuild#47's shape: it deleted 31 lines of config and a whole bug class by
  noticing the dangerous setting bought nothing); or
- evidence it is **load-bearing in a case not exercised on 2026-07-15**, and got lucky.

**Find out which.** Do not assume the first because it is tidier. If it is redundant, the audit's
best deliverable is a smaller file, not a more defensive one. If it is load-bearing, say exactly
where and why.

## Measured facts (2026-07-15 — re-measure; do not inherit)

- `pre_build.sh:13` — `set -e`. This is what makes bug 1 fatal.
- `pre_build.sh` processes **13 `run_workspace` calls**, then commits/pushes **PyAutoBuild itself**
  with `git add -A` **on whatever branch is checked out**, then dispatches `release.yml` with **no
  `rehearsal` field — which defaults to `false`, i.e. a real PyPI release.**
- `run_workspace` stages only: `dataset/`, `config/`, `notebooks/`, `scripts/`, optional
  `slam_pipeline/`, and the root-level glob line. **Anything else black touches is never staged.**
- **Two `.gitignore` dialects**, different git behaviour — measured with `git add -n dataset/`:

  | pattern | repos | `git add dataset/` |
  |---|---|---|
  | `dataset/` (whole dir) | autofit_workspace, autofit/autogalaxy/autolens_workspace_test, HowToFit/Galaxy/Lens = **7 of 11** | **exit 1** |
  | `dataset/**` + `!` allowlist | autolens_workspace (13 entries), autogalaxy_workspace (5) | exit 0, stages real data |

- `autofit_workspace` has no `.cfg`/`.ini`/`.toml` → the root glob line (`:88`) exits **128** there.
- The **only** three failure-tolerant sites in the file are `:55`, `:79`, `:88` — and on
  2026-07-15, **two of the three were masking a bug** (`:88`) or were themselves the bug (`:79`,
  pre-#154). `:55` masks unconditionally (no repo has `README.rst`; sed exits 2 every run). That
  is a 3-for-3 hit rate on a very small sample — treat the idiom itself as the suspect.
- **Observed collateral, unexamined:** black reformats files that `run_workspace` never stages and
  therefore never commits — e.g. `.github/scripts/check_tutorials_complete.py` in all three HowTo
  repos, and ~11 `autoassistant/*.py` files in `autolens_assistant`. These are reformatted on every
  release and left dirty locally, forever. **Is that a third instance of this class, or intended?**
  I did not determine this. It is a good place to start.

## What to sweep

Not just the two known lines. The whole file, and what it calls:

- `pre_build.sh` end to end — every command whose failure is either unhandled under `set -e` or
  swallowed by `|| true` / `2>/dev/null`. Both directions are bugs; enumerate both.
- The interaction between `set -e` and `&&` lists. Note `[ -d x ] && cmd` under `set -e` is subtle:
  a failing `[ -d x ]` is *ignored* (non-final in an `&&` list) but a failing `cmd` is *fatal*.
  The idiom appears more than once. Is it right anywhere?
- Bash glob behaviour: unmatched globs stay literal without `nullglob`. Where else does this bite?
- `check_dataset_allowlist.py`, `generate.py` — same lens: what do they do on failure, and does
  `pre_build` notice?
- The **`pre_build` vs `release.yml` division of labour** — who is responsible for producing which
  artifact, where they overlap, and where the overlap is masking a defect.
- Anything that **prints a claim it did not do.** `"Bumping README version → …"` prints before a
  sed that always exits non-zero into a `|| true`, and the result is then not staged by `:88`. Log
  lines that lie are how this stayed hidden — the 2026-07-15 log printed that banner for all 14
  repos and I believed it. (Precisely *which* half fails is unresolved: the sed does still edit
  `README.md` despite erroring on the absent `README.rst`, so the bump likely happens and merely
  goes uncommitted. **I did not confirm this** — a version-like grep of the local README returned
  a pre-release string, but that grep matched other version references in the file and proves
  nothing. Settle it properly; do not inherit either reading.)

## Trust nothing here

This document was written by the agent that made the mistakes on 2026-07-15. Two of its
conclusions were wrong *that day* and were caught only by re-checking:

- **"I reproduced bug 1."** — **false.** The first repro used a synthetic repo with `dataset/**`
  and **exited 0**; it did not reproduce the bug at all. The real `.gitignore` is `dataset/`, which
  git treats differently. I was one step from "verifying" a fix against a bug I had never
  triggered. Reproduce in the **real** repo.
- **"The tags are missing on PyAutoFit and PyAutoLens."** — **false.** `gh api repos/X/tags
  --jq '.[0].name'` is **not** date-sorted; it returned `pull` and `v1.15.2`. All five tags
  existed. Use `git/ref/tags/<version>`.

Both had the same shape as the day's other errors: **checking the path already assumed and calling
it proof.** Treat this document as a lead sheet, not a source of truth.

## What to produce

1. **A complete enumeration** of the failure class in `pre_build.sh` and its callees — each with
   the concrete repo/condition that triggers it, measured, not reasoned. A per-repo exit-code
   matrix (`git add -n` is safe and does this without staging) beats prose.
2. **An answer to the design question** above: is the local staging redundant, load-bearing, or
   partly each? With evidence.
3. **A target design** for error handling in this file. Hypotheses to argue with, not requirements:
   - a no-op and a failure should not be the same event;
   - anything that *may legitimately match nothing* should say so explicitly, not rely on `|| true`;
   - a log line should not be able to claim work that did not happen;
   - if the runner is the real producer, the local script should stop pretending to be.
4. **What you rejected and why.** Including: is `shopt -s nullglob` the right fix for bug 2, or does
   it just make a redundant line silently succeed?
5. **Open decisions for the human** — separated from what you're confident about. Specifically: the
   unstaged-black-reformat question, and whether `pre_build`'s local commits should exist at all.

## Method

- **Run things.** `git add -n` per repo per pattern; `bash -n`; `bash -x pre_build.sh` against
  throwaway clones. Nothing here is expensive; being wrong is.
- **Reproduce in the real repo**, never a synthetic one you built from your own mental model of the
  `.gitignore`. See "Trust nothing here" — this exact shortcut failed on 2026-07-15.
- **Exercise both dialect groups.** Any claim about `dataset/` staging must be tested against a
  `dataset/`-ignored repo *and* a `dataset/**`+allowlist repo. The allowlist group is the one that
  agrees with you.
- **Prove no-ops empirically.** "Provably inert" preceded being wrong that day.
- **Adversarial pass before concluding:** for each load-bearing claim, *what would have to be true
  for this to be false, and have I looked?*
- **Prefer deleting the trap to hardening it.** If the answer is "add defensive error handling to
  every line", ask first whether the line should exist.

## Constraints

- **This script dispatches live PyPI releases.** `release.yml`'s `rehearsal` input defaults to
  `false`. Never test by running `pre_build.sh`; test the primitives against throwaway clones.
  To exercise the pipeline, dispatch `release.yml` with `rehearsal=true` explicitly.
- **Never** reintroduce `git add -f` for `dataset/` — that was the simulated-dataset leak (#126),
  and #150 removed it deliberately. Bug 1 is the *consequence* of that correct fix, not an argument
  against it.
- `pre_build` commits with `git add -A` **on the current branch** — any fix lands on `main` before a
  release runs, or the release commits onto your feature branch.
- Behaviour-preserving where the behaviour is correct: main ends up right today, and it must still
  end up right after.
- Design first. Plan approval before implementation, per the usual workflow.
