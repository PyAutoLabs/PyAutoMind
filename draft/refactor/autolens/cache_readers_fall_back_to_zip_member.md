# Post-completion cache readers should read the preserved zip member instead of recomputing

Type: refactor
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoFit
Themes:
- aggregator
- paths
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: with `remove_files=True` and a completed zip containing `files/multiple_image_positions.json`, re-reading the cached multiple-image positions returns the archived values without re-running the point solver, and the same holds for the adapt-image SNR cache; a regression test asserts the solver/SNR computation is not re-entered.
Review-minutes: 10
Unattended: ready
Filed: 2026-09-10

Follow-up to the aggregator/`preserve_in_zip` fix
(`bug/autofit/aggregator_sibling_dir_shadows_completed_zip.md`). Once
`preserve_in_zip` deletes the loose copy under `remove_files=True`, the two
post-completion cache readers no longer find a file on disk and fall through to
recomputing the cached artifact:

- PyAutoLens `Result._cached_multiple_image_positions_from`
  (@PyAutoLens/autolens/analysis/result.py:299-323) — one point solve.
- the PyAutoGalaxy adapt-image SNR cache
  (@PyAutoGalaxy/autogalaxy/analysis/adapt_images/adapt_images.py:14-27,134-135)
  — one SNR-image set.

That is one of each per stage boundary. Both should first look for the
preserved member inside the search's zip (a small read helper on
`AbstractPaths` in PyAutoFit, beside `preserve_in_zip`, is the natural home)
and only recompute when the member is absent too. Behaviour-preserving: the
archived member is by construction the value that was previously computed.
