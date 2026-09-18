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
Status: formalised
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
