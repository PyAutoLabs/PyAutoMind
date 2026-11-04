# Optional dependency guard and likelihood LaTeX fixes

Completed: 2026-11-04
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/618
PR: https://github.com/PyAutoLabs/autolens_workspace/pull/619
Merge: 22d2cb56d8f969bfafc3c71795bfea4b7bf46c82

The array-free datacube example now skips cleanly with installation guidance when nufftax is absent, before mask creation or dataset simulation. Raw narrative strings preserve LaTeX in the group and cluster likelihood guides; mixed doubled escapes were normalized within the affected strings. All three notebooks were regenerated (the cluster notebook remained identical), with navigation refreshed. Scientific executable code in both likelihood guides is unchanged.

Validation: all 3 CI runs / 8 jobs passed, including Python 3.12 and 3.13 smoke. Local curated smoke 42 scripts + 2 notebooks, targeted scripts 3/3, pytest 3/3, absent-backend exit 0 before mask/simulation, clean escapes/optdeps scans, notebook executable parity, navigation/size/whitespace checks and independent CLEAN review. Heart at ship was STALE solely for absent current-source release rehearsal.

Human /prm authorized the merge. Every claimed branch is contained in origin/main; issue closed. No remaining scope or release obligations.

Review bundle preserved: /mnt/c/Users/Jammy/Workspace/Science/scratch/alw_optdeps_escapes_2026-11-04/index.html

## Original prompt

# autolens_workspace: nufftax skip guard + raw docstrings for damaged LaTeX

Type: refactor
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: high
Status: awaiting-merge
Issued: 2026-11-04
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/618
Consequence: judge
Filed: 2026-11-04 (pre-rehearsal /hygiene sweep; human: "go with the recommendation")

Two hygiene findings in @autolens_workspace, bundled because they touch the same repo and are each a few lines:

1. **optdeps.** `@autolens_workspace/scripts/interferometer/features/datacube/modeling_array_free.py` is smoke-listed and builds a `TransformerNUFFT` (needs `nufftax`) with no `importlib.util.find_spec("nufftax")` skip guard. A CI or release matrix leg without the optional extras fails on it. Add the standard guard, mirroring `@autolens_workspace/scripts/interferometer/modeling.py` (around line 81: print "Skipping ..." then `sys.exit(0)`).
2. **escapes.** `@autolens_workspace/scripts/cluster/likelihood_function.py` (`\m` near line 554) and `@autolens_workspace/scripts/group/likelihood_function.py` (`\c` near line 36, plus one SILENT `\t`/`\f` corruption that raises no warning) have LaTeX broken by Python string escapes. The fix is an `r` prefix on the enclosing docstring. Do NOT double the backslashes, which would leak into the rendered notebook prose. Get the exact list from `pyauto-brain hygiene escapes`.

Regenerate the affected notebooks; never hand-edit `.ipynb` files.

Validation: `pyauto-brain hygiene optdeps` and `hygiene escapes` report clean for autolens_workspace; the three scripts run under the smoke profile, and the datacube script skips cleanly with `nufftax` hidden.

Unblocked 2026-11-04: the tutorial sweep and autolens_workspace#617 are merged; see `complete/2026/11/tutorial-link-sweep.md`. Start through start_dev, rechecking current claims. The two fixes above remain outstanding.

PR: https://github.com/PyAutoLabs/autolens_workspace/pull/619
Validated 2026-11-04: curated smoke 44/44, targeted scripts 3/3, pytest 3/3, missing-backend guard, notebook parity, hygiene and independent CLEAN review. Heart STALE solely for absent current-source release rehearsal. Awaiting human /prm.
