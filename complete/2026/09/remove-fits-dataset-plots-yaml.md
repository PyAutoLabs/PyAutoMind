## remove-fits-dataset-plots-yaml
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/62 (closed completed 2026-09-10; close-out record written 2026-09-13)
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/63 (merged `515716dc2`, head `70d761c2e`, 1 commit)
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/124 (merged `2b600dd0e`, head `e76aa77ce`, 1 commit)
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/24 (merged `255da0138`, head `624be24d6`, 1 commit)
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/80 (merged `c2b26a607`, head `52c85e316`, 1 commit)
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/74 (merged `7b6c54e52`, head `988fb4942`, 1 commit)
- summary: |
    Config-only parity hygiene, following PyAutoGalaxy#608 (`dataset-fits-image-only`):
    the library stopped reading `visualize/plots.yaml` `dataset.fits_dataset` when
    `save_attributes` began writing `dataset.fits` once, unconditionally, to each
    search's `image/` folder. That task removed the key from the packaged configs and
    from autolens_workspace, autogalaxy_workspace and the two workspace_test repos;
    five `config/visualize/plots.yaml` copies still carried it. This task removed it
    from all five, one PR per repo sharing the one issue.

    The identical two-hunk patch in every repo (`1 file changed, 5 insertions(+),
    4 deletions(-)`): hunk 1 rewrote the header block — "two settings which are
    important" and the `fits_dataset` bullet became the autolens_workspace wording
    ("One setting is important…", the `fits_adapt_images` bullet alone) plus two new
    lines stating that the dataset is always output as `dataset.fits` to the `image`
    folder of every fit and is not controlled by any setting there; hunk 2 deleted the
    `fits_dataset: true` line from the `dataset:` block, leaving `subplot_dataset: true`
    alone, as in autolens_workspace.

    No behaviour change, no notebook regeneration, no library work — nothing had read
    the key since PyAutoGalaxy#608 / PyAutoLens#731.
- verification: |
    27 checks across the five PRs, all `completed / success`; every PR
    `mergeable_state: clean`. Post-merge, `config/visualize/plots.yaml` on each `main`
    holds zero occurrences of `fits_dataset` and carries the new "not controlled by any
    setting here" header lines. Each patched file was checked to parse under
    `yaml.safe_load`, and `search_code` confirmed `fits_dataset` occurred exactly once
    per repo, only in that file — no second config copies, no script or docs references.
    Re-proved at close-out 2026-09-13: all five PRs read `MERGED` and every merge commit
    is an ancestor of its repo's `origin/main`.
- notes: |
    Shipped from a Claude Code remote web session (no local worktree; branches pushed
    via the GitHub API). That session merged all five PRs and closed the issue at
    ~02:11-02:12Z on 2026-09-10 but never reached the Mind close-out, so the `active.md`
    row survived. The close-out was run by hand on 2026-09-13 because the row's stale
    HowToLens claim was blocking model-figures phase 6b.

    No pending-release: every repo touched is a workspace/tutorial/pipeline repo, so
    there is no library release to wait on.

    The `worktree_check_conflict` waiver recorded on the row (euclid_strong_lens_modeling_pipeline
    claimed by `euclid-catalogue-rebuild-prep`, PR #61) is moot — that task closed out on
    2026-09-10 and released the claim.

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
