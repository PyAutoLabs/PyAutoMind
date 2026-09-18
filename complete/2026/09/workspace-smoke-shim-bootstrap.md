# Workspace smoke bootstrap — phase 2c complete

Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/416
Mechanism: https://github.com/PyAutoLabs/PyAutoMind/pull/417 (merged 2e3c5482)
Rollout: https://github.com/PyAutoLabs/PyAutoMind/pull/418 (merged f188ed8e)
Propagation: https://github.com/PyAutoLabs/PyAutoMind/actions/runs/35402643923 (SUCCESS)

## What shipped

A single generated bootstrap block replaces the flat-layout assumption in all
twelve smoke shims. Mind owns the canonical block, manifest-selected generation,
drift checking and event-driven propagation. The five runner variants remain
unchanged outside that block; CI's existing build_util import wins. Local runs
use marker/shared-resolver discovery, reject an inferred foreign bundle root,
and give a useful missing-Hands error. The mechanism's design and review findings
are in `workspace-smoke-bootstrap-mechanism.md` beside this record.

The human approved a bootstrap-only overlap waiver after inspection found no
smoke-shim overlap with the active lens workspace and Euclid tasks. Their task
branches were not changed. This rollout does not depend on tonight's library
release and changes no library API or release-install logic.

## Evidence

- Mechanism full suite: 565 passed; rollout focused suite: 53 passed.
- Independent Sol review CLEAN for both mechanism and enablement.
- All applicable CI workflows/jobs passed on both PR heads before merging;
  template publication was intentionally skipped on pull requests.
- PR #418 had a task-ledger-only merge conflict after another session updated
  main. Retained the current main ledger, reran CI, and merged exact head
  dfafe9b7 after both applicable workflows passed. Final diff was only the flag
  and its comments; no implementation changed during conflict resolution.
- Propagation run logged twelve successful pushes, no failures.
- Every deployed main bootstrap is byte-identical to canonical. Clean local main
  checkouts were fast-forwarded; each deployed shim was then copied into a nested
  fixture and imported build_util successfully: 12/12.
- `repos_sync.py --check --only 'generated smoke bootstraps'`: OK, 12 of 12.
- The legacy `parent / "PyAutoHands"` join is absent from all twelve installed
  run_smoke.py files. The one-source-edit/twelve-updates witness was demonstrated
  by the generator tests and fresh remote-clone dry runs, with exterior bytes
  unchanged.

Verified deployed heads (later unrelated commits may advance them):

| Consumer | Verified main |
|---|---|
| autofit_workspace | `aa6d37383b89` |
| autogalaxy_workspace | `3ca2b75681d7` |
| autolens_workspace | `3b12fbb15cc7` |
| autocti_workspace | `4a602184e1ee` |
| autofit_workspace_test | `14ccf6fb1479` |
| autogalaxy_workspace_test | `7ac0ce6c9230` |
| autolens_workspace_test | `e2bd284d3c88` |
| autocti_workspace_test | `c23d118c5092` |
| HowToFit | `394639b79464` |
| HowToGalaxy | `595fc7bd6df1` |
| HowToLens | `143f4035855d` |
| euclid_strong_lens_modeling_pipeline | `b3c6e75f3986` |

## Boundaries and remaining work

Phase 2c is complete. Phase 3 — physical directory regrouping — remains deferred
until the release and pending workspace merges clear. No directories, Python
paths, IDE settings, task branches, or Heart install-chain code were changed.
The canonical Mind checkout's pre-existing staged draft deletion was preserved.

Scoped reconciliation found one resemblance-only suspect,
`draft/maintenance/pyautobrain/unregistered_worktrees_invisible_to_conflict_guard.md`;
it is outside this bootstrap change and remains filed. Revisit through
`/intake reconcile draft/maintenance/pyautobrain`.

## Original prompt

# The smoke shim's PyAutoHands bootstrap: 12 divergent copies of one flat-layout assumption

Type: maintenance
Target: PyAutoBrain
Repos:
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- autocti_workspace_test
- autocti_workspace
- HowToFit
- HowToGalaxy
- HowToLens
- euclid_strong_lens_modeling_pipeline
Difficulty: large
Autonomy: supervised
Priority: normal
Status: issued
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/416
Consequence: judge
Witness: a local `run_smoke.py` run from a NESTED workspace fixture imports build_util successfully in every one of the 12 repos; `grep -rl 'parent / "PyAutoHands"'` returns 0 across the workspace; and whatever consolidation is chosen, a single edit to the bootstrap reaches all 12 without a hand sweep (demonstrated, not asserted).
Review-minutes: 25
Unattended: needs-slicing

Phase 2c of the workspace regroup. Changes NO directory layout. Split out of
`workspace_resolver_fanout.md` (phase 2, SHIPPED 2026-09-18 — PyAutoMind#415,
PyAutoReduce#75, PyAutoArray#561; record complete/2026/09/workspace-resolver-fanout.md)
because it is a different KIND of
problem from the rest of that task.

## The defect

Every workspace's `.github/scripts/run_smoke.py` bootstraps PyAutoHands like this:

    WORKSPACE = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(WORKSPACE.parent / "PyAutoHands" / "autohands"))

guarded by `try: import build_util / except ImportError:`. `WORKSPACE.parent` assumes the
workspace root is the repo's parent. Under any regroup it becomes the family directory,
PyAutoHands is not there, and the import fails — **loudly, but mis-diagnosed** as
`No module named build_util` rather than "PyAutoHands not found".

It is dead in CI: PyAutoHeart's reusable smoke workflow puts `autohands` on PYTHONPATH, so
the `try` branch succeeds and the fallback never runs. This is a LOCAL-run defect only.

## The prior question — do not skip it

There are 12 of these files and **they are not copies**. Measured 2026-09-18: 12 distinct
checksums, clustering into 5 shape-classes.

| shape | repos |
|---|---|
| 119 lines, join at :63 | autolens_workspace, autogalaxy_workspace, autofit_workspace |
| 77 lines, join at :50 | the four `*_workspace_test` |
| 75 lines, join at :45 | HowToFit, HowToGalaxy, HowToLens |
| 72 lines, join at :45 | autocti_workspace |
| 97 lines, join at :52 | euclid_strong_lens_modeling_pipeline |

There is no propagation mechanism. The file's own header records that past fixes — the
PyAutoHands entry point, the per-script timeout and process-group kill (PyAutoHands#185,
#226/#227), the jupyter guard — "had to be swept across every copy by hand".

So patching the bootstrap twelve times fixes this instance and re-affirms the structure that
produced it. Decide the shape BEFORE editing:

- **Sweep** — 12 near-identical edits, 12 PRs. Cheapest now, same position next time.
- **Propagate** — make the bootstrap a generated block like the session-start hook, which
  `PyAutoMind/.github/workflows/session_hook_propagate.yml` bot-pushes to every manifest repo
  precisely because "thirty PRs per hook edit is a review queue nobody would read". The hook is
  the proof this pattern already works here.
- **Thin the shim** — have PyAutoHands ship the bootstrap (it already owns `build_util`), so
  each `run_smoke.py` carries one import and nothing to drift. Note the workspaces legitimately
  differ (5 shapes), so this must separate the common bootstrap from the per-workspace part
  rather than flattening them.

The witness deliberately requires that a single edit reach all 12 without a hand sweep, so
"sweep" only satisfies it if paired with a mechanism.

## Constraints

- CI must keep working unchanged: the reusable workflow supplies PyAutoHands on PYTHONPATH and
  the `try` branch must keep winning there. Verify against `PyAutoHeart/.github/workflows/smoke-tests.yml`.
- Phase 2 shipped the pattern to copy: the hook resolves by marker, PREFERS the shared
  resolver but never depends on it (read in a subshell that drops `set -euo pipefail`, so an
  absent or broken resolver costs nothing), and REFUSES a resolver answer that does not
  contain its own checkout — without that guard a bundle resolves to the canonical workspace.
  Copy that shape rather than re-deriving it.
- The marker walk introduced in phase 1a is the resolution rule to adopt
  (`.pyauto-root`, with the sibling-organ probe as the fallback) — do not invent a second one.
- Do NOT touch `PyAutoHeart/heart/smoke.py`'s flat `pip install ./PyAutoFit ./PyAutoArray ...`
  chain: Heart runs that script LOCALLY (`smoke.py:313`, `cwd=organism_root`), and it needs the
  flat layout. That is phase 3.
