## dr1-sed-after-vis-lp
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/134
- completed: 2026-11-16
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/135

- Human ruling on risk 3 of #133: the Euclid DR1 campaign's `sed` stage now chains `after: {vis_lp: aftercorr}` instead of `{vis_pix: aftercorr}` (`hpc/campaign/dr1.yaml`). `vis_pix` and `sed` both start per lens once that lens's `vis_lp` succeeds, so a failed `vis_pix` no longer loses the lens its SED fit and SED no longer waits behind the 24 h pixelized stage.
- `hpc/README.md` stage table and chaining paragraph updated; `tests/test_hpc_campaign.py` sed dependency assertions updated plus new `test_failed_vis_pix_does_not_block_sed`. `sed_seed.sh` unchanged: it already needs exactly one `vis_lp` zip and reads nothing from `vis_pix`.
- Last commit 34babd3 also updated the `aftercorr` notes in `hpc/README.md` and `dr1.yaml` after a RAL test (SLURM 22.05.11, 2026-11-16): `aftercorr` fires within seconds, still fires after the upstream record is purged (MinJobAge 300 s), and a late fill against a purged array runs too. A purged dependency counts as met even if `vis_lp` failed, so the seed guards (`missing_seed`) are what stop a lens with no `vis_lp` result. Replaces the old "aftercorr never fires on RAL (22.05.9)" warning.
- Tests: `pytest -m "not slow" tests -x` 498 passed; campaign+sync tests 72 passed; control (sed line reverted) fails 4. Merged at b649a30 on human-commanded /prm, CI green (7 success, smoke skipped). Tier judge — no shadow row.

## Original prompt

# dr1-sed-after-vis-lp: DR1 campaign's sed stage depends on vis_lp only

Type: feature
Target: euclid_strong_lens_modeling_pipeline
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- hpc
- campaign
Difficulty: small
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-11-16
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/134
Consequence: judge

## Human decision (verbatim)

Human decision (chat, 2026-11-16, ruling on risk 3 of PyAutoLabs/euclid_strong_lens_modeling_pipeline#133, merged today): the Euclid DR1 campaign's `sed` stage must depend on `vis_lp` only, not on `vis_pix`. Rationale: SED's only data input is the vis_lp result; chaining after vis_pix made a lens whose vis_pix failed lose its SED fit and delayed SED.

## Approved plan

1. `hpc/campaign/dr1.yaml` ~line 100: sed stage `after: {vis_pix: aftercorr}` → `after: {vis_lp: aftercorr}`, with a comment saying why.
2. Update any text that describes the chain as vis_lp → vis_pix → sed (yaml header, README/hpc docs, tests that assert the chain or the plan output, `python -m autofit.campaign validate` expected output in docs). Grep for `vis_pix` near `sed`.
3. Seed guards: sed must still refuse to start without exactly one vis_lp zip — confirm it does not depend on any vis_pix output; if it does, stop and report rather than redesign.
4. Run `pytest -m "not slow" tests -x` and the hpc campaign tests (`tests/test_hpc_campaign.py`, `tests/test_hpc_sync.py`); validate the yaml with `python -m autofit.campaign validate` on a temp copy as #133's Witness did.
