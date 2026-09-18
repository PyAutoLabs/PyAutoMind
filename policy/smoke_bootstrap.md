# Smoke bootstrap ownership and rollout

`policy/smoke_bootstrap.py` is the canonical bootstrap embedded between
`pyauto:smoke-bootstrap` markers in each opted-in `.github/scripts/run_smoke.py`.
The surrounding runner belongs to its repository. Discovery only runs when
`build_util` is absent from Python's import path; CI keeps its existing import.
A missing dependency inside an installed Hands checkout remains an import error.

The local fallback uses explicit `PYAUTO_ROOT`, otherwise the nearest ancestor
marker (flat parent fallback for unmarked CI/local checkouts). It prefers the
Brain resolver when available, rejects an inferred root outside the consumer's
ancestry, and tolerates an absent or broken resolver. The marker identifies a
workspace, including a task bundle; it never means "canonical checkout".

## Generate and inspect

Run from Mind. Always name the destination tree explicitly for the narrow CLI:

```sh
python3 scripts/smoke_bootstrap_sync.py --root <tree> --dry-run --require-all
python3 scripts/smoke_bootstrap_sync.py --root <tree> --check --require-all
python3 scripts/propagate_smoke_bootstrap.py --dry-run
```

The last command clones all selected repositories into a temporary directory,
actually generates there, verifies the result, and reports would-push/current.
It never pushes in dry-run mode. The first command leaves even its named tree
unchanged. `--check` grades installed bytes even while rollout is held.

Targets come from `smoke_bootstrap: true` entries in `repos.yaml`. The generator
resolves identities in a flat tree or one family level, refusing ambiguity.
First adoption recognizes the exact legacy block, refusing unknown variants.
Subsequent updates replace only the marked block. It preflights all targets
before writing and refuses symlinks in any changed destination path, so running
inside a task bundle cannot rewrite its symlinked canonical siblings.

## Rollout hold

`smoke_bootstrap_rollout: false` holds installation and automated pushes while
consumer repositories are claimed by other tasks. During the hold, the ordinary
`repos_sync.py` report explicitly says installations are **not graded**, rather
than printing a misleading `check ...: OK`. Tests and disposable-clone dry runs
still prove the proposed changes. Phase 2c is not complete until delivery lands
and all target installations pass the drift check.

After coordinating the claims, review a change setting the flag to `true`.
The merge triggers `smoke_bootstrap_propagate.yml`; future source/generator or
manifest changes trigger the same workflow. It pushes only the generated shim
change into each repository's default branch using `PAT_PYAUTOLABS`. Failed
clones, generation, commits or pushes fail the job. Partial delivery is reported
per target and is safe to retry. No force push is used.

Enabled local writes use either the narrow CLI's `--write`, or:

```sh
python3 scripts/repos_sync.py --root <tree> --write --only 'generated smoke bootstraps'
```

This bounded invocation must not regenerate unrelated hooks or documentation.
The ordinary drift check reports the installed target count separately from the
verdict, preserving Heart's status parser. A partial CI checkout is not evidence
that the complete deployment is current; the propagation job requires all targets.

PR correctness is tested against fixtures and disposable clones. Downstream
main copies cannot match a proposed source until it merges and propagates;
never require that impossible precondition as the source PR's acceptance test.
