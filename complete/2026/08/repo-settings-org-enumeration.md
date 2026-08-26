The repo-settings sweep now enumerates the organisation instead of deriving its
targets from the body map, so a repo inherits "Automatically delete head
branches" without anyone remembering to register it first.

## Why the body map could not work

PyAutoBrain#290 (merged the same day) had already turned the setting into a
weekly sweep and removed `/prm`'s remote-delete step — that step was dying on a
403 in cloud sessions while `git push origin --delete` still printed
`Everything up-to-date` and exited 0, so every web close-out reported a
deletion it had not performed.

What #290 left was a source-of-truth problem rather than a bug: **a repo is
created before anyone registers it in `repos.yaml`**, so the repos most in need
of the setting were exactly the ones a body-map-derived sweep could not see.
Nine live org repos were absent from the body map entirely; ten more registered
ones fell outside `SWEEPABLE_CATEGORIES`. 27 of 44 org repos were swept.

There was no birth-time hook to add instead — verified across all three
candidates: the four assistants' `start-new-project.md` create a *visiting
scientist's own* repo under *their* account; the clone conductor has no create
call (`clone/DESIGN.md:148` still lists repo creation as an open v0 question);
`/spawn` force-syncs template repos that already exist. Org repos are made by
hand on github.com.

## What shipped (PyAutoBrain#292, merge 475d292e0)

- `repo_settings.yml` lists non-archived repos under `${{ github.repository_owner }}`
  from the API, union `--outside-owner` for body-map repos under another account.
- Scope-aware failure policy: an in-org PATCH refusal is an error, an
  out-of-org one a `::warning::`. Previously *every* refusal set `failed=1`,
  which would have reddened the weekly unattended run permanently the first
  time it reached a personal-account repo.
- `ORG` / `MODE` moved into the step `env:` rather than interpolated into the
  shell.
- `--include-self-sweeping` retired — org enumeration removed its only
  consumer, and an unused widening flag on a module whose other modes delete
  refs is a trap. A regression test asserts a stale caller exits 2 rather than
  silently falling back to the narrow set.
- `targets()` and `SWEEPABLE_CATEGORIES` untouched: the branch sweep's boundary
  measured 25 slugs before *and* after. #290's "must not widen" assertion still
  holds — this bypasses the boundary for one consumer rather than moving it.

## Verification

548 tests pass (baseline measured at 542; 542 − 1 removed + 7 new reconciles
exactly). Because the workflow had **never executed**, its `run:` block was
extracted and control-tested against a stubbed `gh` across 7 scenarios,
including that an empty org listing *refuses* rather than reporting a clean
sweep. Live enumeration returns 44 non-archived repos. The tenant-firewall
check was proven non-vacuous by injecting a deliberate instance-fact leak
(went RED naming file and line) and reverting.

**The change validated itself on its own merge:** GitHub auto-deleted
`feature/repo-settings-org-enumeration` when #292 landed, confirmed by
`git ls-remote` returning nothing for the ref.

All 46 live repos (44 org + 2 personal) had already been PATCHed to `true` by
hand while filing, so the sweep's first real run should report all-already-on.

## Shipped over a red Heart

Heart was RED on `release validation FAILED` (`integrate:fail`,
v2026.8.25.1.dev73701), standing since 2026-08-23 and unrelated to this diff.
Shipped on an explicit human override recorded in the PR body — not the
corrective-PR exception. That RED remains open and unowned.

## Follow-up

The workflow still has never run. Dispatch `mode: audit` before `apply`; a
`refused (needs admin)` row is `PAT_PYAUTOLABS` scope, a human decision rather
than a retry.

## Original prompt

# The repo-settings sweep should enumerate the org, not the body map

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-26
Issued: 2026-08-26

## The original request (verbatim)

> I want to make it so that when a branch merges via PR, on all repos, its auto
> deleted. Can we do that here or do I need to manually go to each repo on
> Github.com and do it?

and, once told PyAutoBrain#290 had already shipped most of it:

> make it so new repos do inherit this, we should of also just made it so prm
> doesnt try to delete anymore, I think the mobile chat pushed but chec

## What is already done — do not redo it

PyAutoBrain#290 (merged `5ac5586`, 2026-08-26, from a mobile session) shipped:

- `.github/workflows/repo_settings.yml` — a weekly + dispatchable sweep that
  PATCHes `delete_branch_on_merge=true`, targets derived from the body map.
- `bin/branch_sweep_targets.py --include-self-sweeping` — the widened organ
  boundary that sweep uses, plus `tests/test_branch_sweep_targets.py`.
- **`/prm` deletes no remote branch on any surface** (`skills/prm/prm.md:43`,
  step 5.6). The second half of the request above is therefore **already
  satisfied** — do not reopen it.

Separately, all 46 live repos (44 `PyAutoLabs/*` + `Jammy2211/admin_jammy` +
`Jammy2211/euclid_assistant`) were PATCHed to `true` by hand in the filing
session and verified by re-reading the API. **This task is about durability for
repos the sweep cannot currently see — not about today's state.**

## The hole

The sweep derives its targets from `PyAutoMind/repos.yaml`. Two consequences:

1. **A new repo is invisible until someone registers it.** Org repos are created
   by hand on github.com — there is no `gh repo create` path in the organism for
   them (checked: the four assistants' `start-new-project.md` create a *visiting
   scientist's own* private project repo under *their* account; the clone
   conductor has no create call at all, `clone/DESIGN.md:148` still lists repo
   creation as an open v0 question; `/spawn` force-syncs template repos that
   already exist). So birth-time is not a hook we have, and registration is the
   only thing standing between a new repo and the sweep.
2. **Nine live org repos are absent from the body map** and so are never swept:
   `.github`, `PyAutoLogo`, `PyAutoMemory-template`, `PyAutoMind-template`,
   `PyAutoProject`, `autolens_jax_joss`, `autoproject_workspace`,
   `autoproject_workspace_test`, and the typo repo
   `autolens_workspace_developer-`.

A third, smaller gap: the category boundary excludes `assistant` (5),
`pipeline` (1), `project` (3) and `admin` (1), so 10 of the 37 *registered*
repos are skipped too — 27 of 37 swept. Those exclusions are correct for the
**branch sweep**, whose action is deleting refs, and PR#290 added a test
asserting they must not widen. They do not transfer to flipping a reversible
boolean on repos that demonstrably merge PRs (autolens_assistant#115,
autogalaxy_assistant#19, autocti_assistant#26 all merged this week).

## Decision (human, at filing time)

**Enumerate the org live.** Targets become every non-archived repo under
`${{ github.repository_owner }}` read from the API, union any body-map repo
whose owner is *not* the org. This closes all three gaps at once and needs no
category boundary at all. The owner comes from the GitHub context, so no
instance fact enters organ code and the tenant firewall stays satisfied.

**Do not touch the assistants' `start-new-project.md`.** That repo belongs to
the visiting scientist, under their own account, and the skill presents it as a
backup/collaboration surface that may not use PRs. Imposing our merge policy on
it is our convention leaking into someone else's workspace.

## Notes for the implementer

- `--include-self-sweeping` has exactly **one** consumer, `repo_settings.yml:84`.
  Org enumeration removes that consumer, so the flag becomes dead code on a
  safety-relevant boundary — retire it with its two tests rather than leaving it
  loaded. This reverses part of a PR merged hours earlier; say so in the PR body.
- The **plain** derivation still has two consumers (`branch_sweep_all.yml:98`,
  `branch_archive.yml:110`) and its narrow category boundary must not move.
- Out-of-org repos are the user's own (`Jammy2211/*`); `PAT_PYAUTOLABS` admin
  scope there is unverified. A PATCH refusal on those must **warn**, not fail —
  the job currently sets `failed=1` on any refusal and would go red every week.
- Stale claims to update once the source changes: the workflow's own header
  comment ("27 repos", body-map framing), `skills/repo_cleanup/SKILL.md:133`
  ("body-map-wide"), and the derivation paragraph at
  `skills/repo_cleanup/reference.md:164` if it describes the settings consumer.
- The workflow has never actually run. Dispatching it after merge is the smoke
  test: with every repo already `true`, `apply` should report all-already-on.
