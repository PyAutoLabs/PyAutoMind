# pre_build root-level git add stages nothing when a glob does not match

Type: bug
Target: PyAutoBuild
Repos:
- PyAutoBuild
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

pre_build root-level git add stages nothing when a glob does not match. In pre_build.sh the root-level staging line runs 'git add -- *.py *.md *.txt *.cfg *.ini *.toml *.yml *.yaml LICENSE* requirements* setup* 2>/dev/null || true'. Bash leaves unmatched globs literal, so in any workspace lacking one of those extensions git rejects the ENTIRE pathspec list with 'fatal: pathspec *.cfg did not match any files' (exit 128) and the '|| true' silently swallows it - nothing from that line is staged at all. Measured in autofit_workspace, which has no .cfg/.ini/.toml: exit=128, so its README version bump and llms-full.txt regeneration are never committed by pre_build despite the log printing 'Bumping README version'. The effect is currently MASKED because release.yml's release_workspaces job regenerates and commits the same artifacts on the runner, so main ends up correct - this is latent, not a live breakage. Fix by making the glob tolerant (shopt -s nullglob, or add each pathspec only if it matches) so the line does what its log claims. Found during the 2026.7.15.1 manual release, alongside PyAutoBuild#154 which was the same class of bug: a git add failing under set -e or being swallowed by || true.

<!-- formalised by the Intake (Conception) Agent on 2026-07-15 from user-intake -->
