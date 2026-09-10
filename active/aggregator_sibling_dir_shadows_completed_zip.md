# Aggregator prefers an incomplete sibling directory over a `.completed` zip, and `preserve_in_zip` leaves a loose copy under `remove_files`

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- aggregator
- paths
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Witness: an aggregator over `<hash>.zip` (containing `.completed`) plus a sibling `<hash>/files/x.json` with no `.completed` returns 1 output under `completed_only=True` in both in-place and `unzip_temporary=True` modes; after `preserve_in_zip` under `remove_files=True` no file remains outside the zip; `Aggregator.from_directory` over the pulled euclid_dr1_prelim 342398 tree returns 20 outputs (today 5).
Review-minutes: 20
Unattended: ready
Filed: 2026-09-10

## Symptom

Found 2026-09-10 on the `euclid_dr1_prelim` RAL job 342398. `Aggregator.from_directory(root, completed_only=True)`
returned 5 of the 20 searches present in the pulled output tree; the derived
`lens_mass.csv` carried 5 of 10 rows, and `build_inspection_bundle.sh` aborted
with "aggregator is empty". Nothing was printed to warn that fifteen completed
searches had been silently dropped.

Every dropped search had a `<hash>/` directory sitting beside its `<hash>.zip`.
That directory held only two files — `files/galaxy_images_snr.fits` and
`files/multiple_image_positions.json` — whose mtimes matched the zip's, and both
of which were *also* members of the zip. Crucially the directory contained no
`.completed` marker, while the zip did.

## Root cause (verified)

After a search is zipped and its output directory removed under `hpc_mode`
(@PyAutoFit/autofit/non_linear/paths/abstract.py:181-187 forces `remove_files`
whenever `general.hpc.hpc_mode` is set), post-completion caches write back into
`paths._files_path`:

- PyAutoLens `Result._cached_multiple_image_positions_from`
  (@PyAutoLens/autolens/analysis/result.py:299-323)
- the PyAutoGalaxy adapt-image SNR cache
  (@PyAutoGalaxy/autogalaxy/analysis/adapt_images/adapt_images.py:14-27,134-135)

The `_files_path` property mkdirs the directory on access
(@PyAutoFit/autofit/non_linear/paths/abstract.py:352-358), so a `<hash>/files/`
tree is recreated beside the zip. The writers then call
`paths.preserve_in_zip(path)`
(@PyAutoFit/autofit/non_linear/paths/abstract.py:383-423), which adds or
replaces the archive member but leaves the loose file exactly where it was —
correct under `remove_files=False`, wrong under `remove_files=True`, where the
zip is meant to be the only store.

`Aggregator.from_directory`
(@PyAutoFit/autofit/aggregator/aggregator.py:239-266) then skips any zip whose
`<hash>/` sibling already exists (:243-245). That check sits *before* the
`unzip_temporary` branch, so temporary-extraction mode has the same hole. The
walk descends into the sibling, `_is_search_output` accepts it because
`files/search.json` is present (:101-113 — the sentinel is also a preserved
zip member), and `completed_only` then drops it for lacking `.completed`
(:261-262). No warning is printed anywhere along that path.

`test_autofit/aggregator/test_from_directory.py::test_zip_not_re_extracted`
(:42-49) currently locks in the unconditional skip, and
`test_zip_temporary_uses_an_existing_extracted_directory` (:110-116) is its
temporary-mode twin.

## What to do

1. **`aggregator.py:243-245`** — skip the zip only when
   `(extracted / ".completed").exists()`. Otherwise extract the zip: in place,
   `extractall` onto the existing directory (which merges, and the zip's copies
   are authoritative); in temporary mode, to the temporary path as today. Emit a
   `logger.warning` naming the path — a sibling directory without `.completed`
   beside a completed zip, and that the zip was used. Add a count of outputs
   dropped by `completed_only` to the summary print at :320-325 so a silent
   shortfall becomes visible.

2. **`preserve_in_zip`** — after the member is written or replaced, if
   `self.remove_files` is true delete the loose file and prune now-empty parent
   directories up to and including `output_path`. State in the docstring that
   under `remove_files` the zip is the only store, and that post-completion
   caches are recomputed on next access.

3. **Tests** — rewrite `test_zip_not_re_extracted` and its temporary-mode twin
   to the new contract: a sibling *with* `.completed` still wins and the zip is
   not re-extracted; a sibling *without* `.completed` loses to the zip in both
   modes, and `completed_only=True` returns 1. Add a `preserve_in_zip` test
   beside `test__preserve_in_zip__file_survives_restore`
   (@PyAutoFit/test_autofit/non_linear/paths/test_paths.py:120) asserting that
   under `remove_files=True` no loose file and no empty directory remain, and
   that the loose file *does* remain under `remove_files=False`.

4. **Follow-up prompt** — file
   `PyAutoMind/draft/refactor/autolens/cache_readers_fall_back_to_zip_member.md`
   (small, supervised; Repos: PyAutoLens, PyAutoGalaxy, PyAutoFit): the two
   cache readers should read the preserved zip member when the loose file is
   absent rather than recomputing it. Today that costs one SNR-image set plus
   one point solve per stage boundary.
