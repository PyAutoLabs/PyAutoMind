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
