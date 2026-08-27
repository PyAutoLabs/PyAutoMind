## smoke-install-stale-jax-pin
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/266
- completed: 2026-08-23
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/268 (merged a97f052)
- sibling-pr: autogalaxy_workspace_test — companion PR, identical change; its smoke_install.sh on main carries the same JAXCHECK block
- summary: Dropped the vestigial `jax<0.7 jaxlib<0.7` pin from smoke_install.sh. Added in #82 solely to keep tensorflow-probability==0.25.0 importable; #184 removed that dependency for tfp-nightly and left the pin behind. Not inert: jax is a base dep of autonerves (>=0.7.0,<0.12.0), so the pin downgraded a conforming install to 0.6.2 and only the following `[optional]` re-resolution pulled it back to 0.10.2 — CI green by line ordering, not by constraint. Replaced with a #82→#184 trail comment plus a JAXCHECK heredoc asserting the resolved version in [0.7.0, 0.12.0).
- mind-drift: shipped without touching Mind state; retired to complete/ on 2026-08-27 after the still-live dashboard chip caused a re-pick. See the close-out note below.

`autolens_workspace_test/.github/scripts/smoke_install.sh` pinned
`jax<0.7 jaxlib<0.7`. The pin was added in #82 for exactly one reason, stated in
its own commit message: keeping `tensorflow-probability==0.25.0` importable,
since `tfp.substrates.jax` referenced `jax.interpreters.xla.pytype_aval_mappings`,
removed in JAX 0.7.0. #184 then deleted `pip install tensorflow-probability==0.25.0`
when the stack moved to `tfp-nightly` (pinned by `PyAutoArray[optional]`, whose
own comment documents the nightly as the `jax>=0.7`-compatible one). The pin
outlived the dependency it protected.

The framing that made it worth fixing rather than shrugging at: it was **not
inert**. `jax` is a *base* dependency of `autonerves` (`jax>=0.7.0,<0.12.0`,
PyAutoLens#702), so the preceding line already installed a conforming jax; the
pin then downgraded it to 0.6.2 — a configuration the stack does not claim to
support — and only the *following* `[optional]` re-resolution pulled it back to
0.10.2. CI was green by **line ordering, not by constraint**. Reordering those
two lines, or a change in what the extras resolve, would have dropped the whole
smoke suite onto jax 0.6.2 silently, surfacing as unexplained smoke breakage
rather than as an install error.

## PRs

- autolens_workspace_test#268 → `a97f052` (issue autolens_workspace_test#266 closed),
  branch `feature/smoke-install-stale-jax-pin`, merged 2026-08-23. +23/−1, one file.
- `autogalaxy_workspace_test` carried the identical line and was fixed in a
  companion PR; its `smoke_install.sh` on `main` now carries the same `JAXCHECK`
  block.

## The fix

Delete the pin and let `autonerves`' base requirement govern. In its place:

1. A comment recording the #82 → #184 trail, so the pin is not reintroduced by
   someone reading the file cold.
2. A `JAXCHECK` heredoc appended after the final
   `pip install --force-reinstall --no-deps ./PyAutoNerves`, asserting
   `(0, 7) <= (major, minor) < (0, 12)` on the resolved `jax.__version__` and
   printing it to the CI log. With `set -e` at the top, a violation aborts the
   install step.

The `tfp-nightly` NOTE block and the trailing `--force-reinstall --no-deps
./PyAutoNerves` were preserved verbatim — both remain accurate.

Two decisions worth not "simplifying" later:

- **Deleted, not rewritten as an honest `jax>=0.7,<0.12`.** A second copy of the
  constraint drifts, and this one already had: the range was `<0.11` when the
  defect was filed and `<0.12` by the time it was fixed. The assertion checks the
  range without owning it.
- **The guard compares a major/minor tuple, not `packaging.version`.** It runs
  inside the install epilogue, where an undeclared import would fail the install
  rather than fail softly. `import jax` is deliberately unguarded: the workflow
  runs on `ubuntu-latest`, where `autonerves`' platform marker always installs
  jax, so an absent jax is itself worth catching. That would need softening only
  if this workflow ever ran on Intel macOS.

## Verification

The PR's own Smoke Tests run **is** the from-scratch install replay the prompt
asked for; the guard is what turns it from an inference into a check. Before
that: `bash -n` clean; the guard executed as a real bash heredoc against a stub
`jax` (`0.10.2` prints and exits 0; `0.6.2` and `0.12.0` exit 1 with the
explanatory message); boundary cases `0.7.0`/`0.9.0`/`0.10.2`/`0.11.4` pass and
`0.6.2`/`0.12.0`/`1.0.0` fail.

## Sibling sweep (the prompt's scope item 4)

`autocti_workspace_test` and `autofit_workspace_test` were checked at fix time
and carry no jax pin. Re-confirmed at close-out: an org-wide code search for
`jaxlib<0.7` across PyAutoLabs returns **no live script** — only this prompt's
own text in PyAutoMind and one prose mention in
`complete/2026/08/jax-grad-local-vs-ci-assertions.md`.

## Close-out note: this record is late, and why

The task shipped on 2026-08-23 without ever touching Mind state — no `active.md`
entry, no `active/` move, no record. The prompt sat in
`draft/maintenance/ci/` and kept rendering on `dashboard.md` as pickable
backlog with a live `/start_dev` chip, which is how it came to be picked again on
2026-08-27. Nothing downstream could tell the difference: as `AGENTS.md` notes,
a shipped-but-unretired prompt renders faithfully and no workflow detects it.
`lifecycle.py check` did not catch it either — its invariant is that no
`active.md` slug has a record, and this task was in neither place.

The re-pick cost only a verification pass, because the prompt named the file and
the file's current contents were the answer. The generalisable check for the next
one: before opening an issue, read the prompt's own target file on `main`. If the
defect it describes is not there, look for the merged PR before doing anything
else.

## Original prompt

# smoke_install.sh's stale `jax<0.7` pin — CI is on the right jax by accident

Type: maintenance
Target: ci
Repos:
- @autolens_workspace_test
Difficulty: low
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-08-22 (backfilled from git)

Found 2026-08-22 while building a CI-equivalent environment to reproduce
autolens_workspace_test#260. Latent — CI is green today — but it is green for the
wrong reason.

## The defect

`autolens_workspace_test/.github/scripts/smoke_install.sh:9`:

```bash
pip install "jax<0.7" "jaxlib<0.7"
```

Replaying the install script verbatim, that line **downgrades jax to 0.6.2** and
raises a resolver conflict against autonerves' own requirement:

```
autonerves 9999.0.0.dev0 requires jax<0.11.0,>=0.7.0; ... but you have jax 0.6.2
which is incompatible.
Successfully installed jax-0.6.2 jaxlib-0.6.2
```

The install only ends up on the intended **0.10.2** because the *next* line's
`[optional]` extras happen to pull it back up:

```bash
pip install "./PyAutoArray[optional]" "./PyAutoGalaxy[optional]" "./PyAutoLens[optional]"
```

## Why it matters

The pin no longer expresses the intent it was written for, and the correct
outcome now depends on line ordering rather than on the constraint. Any
reordering of those two lines, or a change to what the `[optional]` extras
resolve, would silently drop the entire smoke suite onto jax 0.6.2 — and because
`autonerves` declares `jax>=0.7`, that is a configuration the stack does not
claim to support. The failure would surface as unexplained smoke breakage, not as
an install error.

The comment block immediately below that line (about `tfp-nightly` vs
`tensorflow-probability`) is still accurate and should be preserved.

## Suggested scope

1. Establish what the `jax<0.7` pin was originally protecting against, and whether
   that reason still holds — do not simply delete it because it looks stale.
2. Either remove it (letting `autonerves`' `jax<0.11.0,>=0.7.0` govern) or replace
   it with a pin that states the real intended range.
3. Verify by replaying the install from scratch and asserting the resolved jax
   version, rather than inferring it from a green run.
4. Check whether sibling workspaces' install epilogues carry the same stale pin.

<!-- Sizing: declared low; the sizing faculty derives medium (5). Kept at low — the
     change is one line plus a verification replay; the prompt is long because the
     evidence is, not because the work is. -->

<!-- Not filed as a GitHub issue at discovery time: unrelated to the bug being
     worked (autolens_workspace_test#260), and deliberately not folded into it. -->
