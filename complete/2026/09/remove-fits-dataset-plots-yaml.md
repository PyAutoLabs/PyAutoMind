- summary: Removed the dead `dataset.fits_dataset` key from the five remaining `config/visualize/plots.yaml` copies and mirrored the `autolens_workspace` header wording. Nothing has read the key since PyAutoGalaxy#608 / PyAutoLens#731 made `save_attributes` write `dataset.fits` once, to `image/`; the packaged configs and the four workspace copies were done in that task. Parity hygiene, not a bug — config only, no behaviour change, no notebook regeneration.
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/62
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/63
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/124
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/24
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/80
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/74
- verification: identical two-hunk patch in all five repos (`1 file changed, 5 insertions(+), 4 deletions(-)`); 27 checks across the five PRs all `completed / success`, every PR `mergeable_state: clean`. Each patched file was applied to a byte-exact copy of its own `main` and checked to parse under `yaml.safe_load`. Post-merge, `config/visualize/plots.yaml` on all five `main`s has zero `fits_dataset` occurrences and carries the new header lines.
- lesson: the whole task ran from a Claude Code web session with no local checkouts — the five target repos were attached mid-session with `add_repo`, branched via the GitHub API, then shallow-cloned one at a time to push a locally-verified file rather than retyping 6 KB of YAML through `create_or_update_file`. Cloning to push is the safer lane whenever exact whitespace matters.
- note: `worktree_check_conflict` flagged euclid_strong_lens_modeling_pipeline as claimed by `euclid-catalogue-rebuild-prep` (PR #61). The human waived it at the plan checkpoint: that guard protects a shared *local* worktree this session never used, and #61 does not touch `config/visualize/plots.yaml`. The claim was left untouched.

## Original prompt

# Remove the dead `fits_dataset` key from the remaining `config/visualize/plots.yaml` copies

Type: maintenance
Target: config
Repos:
- euclid_strong_lens_modeling_pipeline
- autolens_assistant
- autogalaxy_assistant
- HowToLens
- HowToGalaxy
Themes:
- config
- hygiene
Difficulty: trivial
Autonomy: safe
Priority: low
Status: active
Consequence: judge
Review-minutes: 5
Unattended: ready
Filed: 2026-09-08
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/62

Follow-up to PyAutoGalaxy#608 (`dataset-fits-image-only`): the library no longer reads
`visualize/plots.yaml` `dataset.fits_dataset` — `dataset.fits` is always written once, to the
search's `image/` folder, by `save_attributes`. The key was removed from the packaged configs
and from `autolens_workspace`, `autogalaxy_workspace`, `autolens_workspace_test` and
`autogalaxy_workspace_test` in that task. Five more copies still carry the dead key plus its
two comment lines (L8 and L18 of each file):

- `euclid_strong_lens_modeling_pipeline/config/visualize/plots.yaml`
- `autolens_assistant/config/visualize/plots.yaml`
- `autogalaxy_assistant/config/visualize/plots.yaml`
- `HowToLens/config/visualize/plots.yaml`
- `HowToGalaxy/config/visualize/plots.yaml`

A stale key is harmless (nothing reads it), so this is parity hygiene, not a bug. Mirror the
`autolens_workspace/config/visualize/plots.yaml` header wording from that task's PR. One PR
per repo; no notebook regeneration (config only).
