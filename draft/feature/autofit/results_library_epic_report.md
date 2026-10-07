# Results library epic — lessons from building the Euclid DR1 catalogue

Type: feature
Target: autofit
Repos:
- PyAutoFit
Themes:
- results
- euclid
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: evidence record for the results-library epic — never issued; read it from the epic ledger
Consequence: glance
Review-minutes: 0
Unattended: never
Epic: results-library
Filed: 2026-10-07

Written 2026-10-07 by the Fable architect session, with five read-only Opus
workers reviewing the Claude Code session logs (JSONL) for Sept 9 – Oct 7,
2026, plus one survey of PyAutoFit and the DR1 science-clone tooling. No code
was edited. Companion to `results_library_epic.md` (the campaign map), which
cites this file as "report Pn".

Citation form: `<session id, first 8 chars> <UTC time>` from the JSONL
`timestamp` field. The local clock was BST (UTC+1), so a time quoted inside
assistant prose can be one hour ahead. PyAutoFit line references are `main` @
`710f4b343`, relative to `fit/PyAutoFit/autofit/`. DR1 script references are
to the science clone `euclid_dr1/` (not pipeline main).

## 0. Summary

- **The catalogue was slow because of how results are read.** Every producer re-walked and re-extracted every zip: 9 producers, about 16 min per 100 lenses, about 27 h serial (w5 A3; 1b29d67b 14:28).
- **The final build took about 26 h** from launch (10-06 11:21) to verified zips (10-07 13:32), against a 4-5 h estimate. It needed 2 chunk attempts and 2 merge attempts. All 12 chunks hit TIMEOUT at 7h07 (b5bbd7b8 06:10).
- **Silent omissions were the costliest failure.** 5 of 10 rows were dropped by stray sibling dirs (fixed in PyAutoFit#1602). The 3σ latent columns held the 1σ values on all 2,990 rows of the published June catalogue (1f278c25 16:09). 695 lenses lack `model.fits`, and 20 of them were flagged complete by QA (b5bbd7b8 13:34).
- **Identity was the folder name and nothing else.** The released catalogue had 5 grade-A wrong-cutout fits and 34 duplicates (9d3eda96 16:50). 941 A+B lenses were missing because their sample folder had been archived (b5bbd7b8 15:45).
- **Status was reverse-engineered** from SLURM logs, zip globs and h5py probes. Two different completeness rules existed in two scripts (w5 C9).
- **About 4.2k lines of hand-written Python** (plus about 290 lines of submit shell) rebuilt index, status, dedup, completeness, chunk/merge, packaging and parity outside PyAutoFit (w5 B).
- **Size:** a result zip is about 95% `image/` (w5 A1). The distribution is about 100 GB as 10 parts of about 10 GB, mostly copies of media already inside the zips.
- **Half the pain was not library-shaped** (HPC sync, spec agreement, agent hand-offs). §6 routes it as separate prompts.

## 1. Timeline (Sept 9 – Oct 7)

| Date (UTC) | Session | Work | Outcome |
|---|---|---|---|
| 09-09 17:16 | 862ded5b | Ran catalogue producers on an ordered run plus a control | 15/42 blank columns wrongly called "structural" (17:21); bundle crashed on "aggregator is empty" |
| 09-09 18:40 | 99cc7b63 | Disk audit and low-disk config | 501 MB = 130 MB zips + 371 MB extracted copies; pipeline #61 `unzip_temporary`, `samples: false` |
| 09-09 19:35 | 99cc7b63 | 3 failed tasks of 342301 | PyAutoFit pulled on RAL mid-array changed the identifier hash |
| 09-10 15:26 | 1f278c25 | Local catalogue build plus parity | `lens_mass.csv` had 5/10 rows: stale sibling dirs shadowed zips |
| 09-10 15:52-16:09 | 1f278c25 | Column audit after the user asked | Retired `latent.` prefix gave silent None; 3σ = 1σ; max_lh = median; vis_lp wrote no latents |
| 09-10 19:30-22:54 | 94cfb571 | Source fixes | PyAutoFit #1598, #1600, #1602; PyAutoLens #734; `compare_catalogues.py` (pipeline #68) |
| 09-11 12:47 | 521de454 | Parity rerun | Parity FAIL by construction: two identical runs differ by median z 15.4 |
| 09-12 18:41-19:53 | 819c5936 | Magnitude parity | Median abs(dmag) 0.024; comparator gave false FAILs (duplicate keys) |
| 09-13 12:17 | c004e808 | Resimulate from results | Linear profiles rebuilt from `model.json` gave zero flux |
| 09-16 21:45-23:22 | 67a9f465 | Mass-map stage | `tracer.json` shadowed `tracer.fits` in the aggregator (PyAutoFit#1633) |
| 09-16 22:56-23:07 | aca5ba12 | COOLEST into finished results | Global `force_pickle_overwrite` toggle plus SLURM reload pass |
| 09-17 08:54 | 58f73591 | "Is it really in the catalogue?" | 33 min and 82k subagent tokens for a yes/no: no manifest |
| 09-17 13:16 | c8cde173 | DR1 bundle rebuild | Sersic products read from the wrong tree: "silently true since the prelim run" |
| 09-23 08:50-12:53 | f184b313 | Status of 4,922 fits | Status parsed from SLURM logs, wrong twice; 741-tile extraction truncated at 566 |
| 09-23 13:31-14:12 | 1b29d67b | Full bundle 350581 | 4,912 not 4,922 (phantom "Finished"); aggregator walked the tree 4×; subagent submitted on a relayed "continue" |
| 09-24 07:11 | 59955182 | Check 350581 | 10 stages OK, job FAILED: `tar: command not found` |
| 09-28 07:55 | 57c19491 | Image catalogue | vis_pix rewrites the vis_lp zip on start: mtime is not fit time |
| 09-28 15:37-21:04 | 74ceb5b1 | Image catalogue delivered | 5,215 lenses, 6.8 GB; magnitudes 4h54m; OneDrive setup about 70 min |
| 09-29 19:58 | c7d2ad66 | Referee tables | Three RAL jobs of 1-2 h each; copy back of 5,199 folders took 68 min |
| 09-30 08:23-11:33 | 07040b99 | Grow to 6,948 lenses | Whole 9.4 GB tar rewritten; 183 lenses with no Einstein radius, unexplained; empty `wcs.csv` shipped |
| 10-05 10:20 | ef45156a | Readiness on 100 lenses | "Not ready as-is": Sersic read from `output/` again ("same as the 09-26 test") |
| 10-05 19:50 | ef45156a | Chunked build prepared | CRLF in `tiles.csv` faked missing zips; 714 lenses with no SED |
| 10-06 08:01-11:22 | 1a1ec986 | Launch | Overnight claims false; SSH lockout; fixes ran on RAL uncommitted; 12 chunks launched at 7h07 |
| 10-07 06:07-13:34 | b5bbd7b8 | Rerun, merge, ship | All 12 chunks TIMEOUT; CSV steps rebuild every row (4h00-4h32); merge crashed on truncated HDF5; DONE: 14,905 lenses |
| 10-07 15:22-16:24 | b5bbd7b8 | Post-release | Datasets and segmentation not in the parts; A+B funnel: 941 missing |
| 10-07 16:50 | 9d3eda96 | Collaborator reconciliation | 5 wrong-cutout grade-A, 34 duplicates, 35 unaccounted; v1.1 needed |

## 2. Pain points by owner layer

### 2.1 PyAutoFit library (fit outputs)

**P1. Result zips are not atomic and resume deletes the zip.** `zip_directory` writes in place with DEFLATE for every member (`tools/util.py:76-84`). `restore()` rmtree's the folder, extracts and deletes the zip at every rerun start (`non_linear/paths/abstract.py:484-506`). Cost: truncated-artefact risk on every walltime kill, and PNG/FITS compression wasted. Root cause shared with hpc-campaign phase 0 (w5 A2).

**P2. Checkpoints are resumed blindly.** A Nautilus `LinAlgError` poisoned `search_internal`, and every retry resumed it and crashed in about 25 s: 24 of 50 tasks in the 10-03 probe; about 440 SED tasks failed before 10-05 (1a1ec986 08:30). Cancelling the SED fill left a truncated `checkpoint.hdf5`. The merge's own h5py probe caught OSError but not RuntimeError, so merge 397451 died after 2 min (b5bbd7b8 12:17). The fix ran on RAL only. Resume is triggered by file existence (`nautilus/search.py:315-318`).

**P3. Completion is binary.** `.completed` means "ended", not "converged" (`non_linear/paths/directory.py:202-207`). The convergence audit parsed SLURM logs: block-buffering read as a "hard stall" (f184b313 08:50, retracted 09:44), `f_live` is None on success (10:14), log Z is truncated to 9 characters (11:58). "Finished" was echoed when Python died, so the count was 4,912 not 4,922 (1b29d67b 13:31). Cost: about 2 h and two public corrections; the usable sample fell 25% from what was reported. Run-time half belongs to hpc-campaign.

**P4. No policy for which sibling hash is current.** A library pull mid-array changed the identifier, so 3 of 10 tiles could not find their prior stage (99cc7b63 19:39). Changed config writes a new `<hash>` folder (`abstract.py:333-353`). DR1 picks the newest by zip mtime in two places, and mtime lies: vis_pix rewrites the vis_lp zip when it starts (57c19491 07:41, 07:55).

**P5. No dataset identity or provenance.** A lens is `<sample>/<tile>` and nothing else. Result: 5 grade-A objects fitted on the old off-centre cutout, 34 objects twice in the master, 35 unaccounted (9d3eda96 16:50-16:52); 941 A+B lenses silently absent because their sample folder had been archived (b5bbd7b8 15:45). User: "dr1_sep1_top1000 is definitely NOT the missing lenses, double checkl" (b5bbd7b8, between 15:45 and 16:24). Co-owned by the project data model.

**P6. Output JSONs carry no schema version.** All 10 DR1 `wcs.json` were the old 4-key form, so the producer needed a recompute fallback and a `source_rule` column (29f963ca 10:43).

**P7. Adding a product to finished results needs a global flag.** For `coolest.json` and `wcs.json`: toggle `force_pickle_overwrite: true`, commit, push, run a SLURM reload array, toggle back, push, back up 108 MB, pull, rebuild (aca5ba12 22:56-23:07). A live job reading the config mid-toggle would inherit the flag.

**P8. Media dominate and are duplicated.** `image/` is about 95% of a result zip (w5 A1). The default aggregator extracted every zip beside itself, so 501 MB of output was 74% redundant (99cc7b63 18:50). The catalogue copies the same PNG/FITS again: about 6.7 MB per lens, about 100 GB (w5 B). `hpc_mode` also silently re-enabled quick updates the user wanted off (99cc7b63 18:50).

**P9. Instances rebuilt from samples lose linear-profile fluxes.** `model.json` plus the max-LH vector gives `intensity = 1.0` placeholders and zero flux; the mocks were pure noise (c004e808 12:17-12:36). Fixed in the project by reading `files/tracer.json`.

**P10. Latent output was all-or-nothing.** One non-finite latent made the global NaN mask drop all 12; an assertion inside the latent jit was swallowed into NaN rows (1f278c25 16:09; 94cfb571 19:56). Partly fixed (PyAutoFit#1600, PyAutoLens#734).

### 2.2 Aggregator and export

**P11. Unresolvable columns became silent blanks, and wrong values were published.** `latent.effective_einstein_radius` resolved to None. The agent called 15 blank columns "structural" (862ded5b 17:21); the cause was found 22.5 h later after the user asked: "is it just effecrtive_einstein_radius that is blank, or other things?" (1f278c25 15:52). `row.py` read the 1σ values for 3σ on all 2,990 published rows and seeded max_lh from the median (1f278c25 16:09). The tests asserted `x == "a" or "b"`. Fixed in PyAutoFit#1598, but `strict` is still opt-in and the header still comes from the first row (`aggregator/summary/aggregate_csv/__init__.py:19, 113-123`; c8cde173 09:11).

**P12. An empty or mis-pointed aggregator is quiet.** Producers pointed at `output/` while the Sersic fits live in `output_sed/` produced empty products (c8cde173 13:16; 7bff8610 14:10) and the same bug came back at release ("same as the 09-26 test", ef45156a 10:20). Empty queries raise `ValueError` in one place, skip in another, and `StopIteration` in a third, which aborted the bundle under `set -e` (29f963ca 11:25).

**P13. Every scan extracts everything, and one bad zip kills it.** `from_directory` extracts every zip before any query (`aggregator/aggregator.py:254-295`); a single `BadZipFile` aborts the walk (`:280-285`). Each of about 9 producers re-walks (`scripts/build_inspection_bundle.sh:125-201`). Measured: about 16 min per 100 lenses, 16 GB RAM per 2,500 lenses, TMPDIR on `/mnt/ral` at about 20 MB per lens (w5 A3). Einstein radius scrape about 1 h, magnitudes 4h54m, Sersic 2h07, offsets 2h13 (c7d2ad66 16:01-18:49).

**P14. Exports are not incremental.** "The CSV steps rebuild every row from scratch" (b5bbd7b8 07:54). The rerun took 4h00-4h32 against a 1-2 h estimate. The submitter refuses an existing catalogue name, so every rerun rebuilds all 15k (`submit_catalogue_chunked.sh:~84-87`). User, polling: "check" at 07:53, 11:34 and 12:16.

**P15. Bare-name lookup is ambiguous.** `SearchOutput.value(name)` resolves JSON before FITS, so `files/tracer.json` hid `image/tracer.fits` (67a9f465 22:18). Fixed for AggregateFITS only (PyAutoFit#1633); about 50 min of a 1h37m session.

**P16. No query, dedup or label primitives.** No path-existence predicate; per-producer newest-result dedup (`latest_result_per_lens_band`, `catalogue_util.py:276-339`) (c8cde173 09:11, 09:46). Labels pair by row index. The user wanted grade folders, but "the folder layout drives resume, seeding and discovery", so grades became a join table after 87 min of subagent time (74ceb5b1 17:42, 19:11).

**P17. Coverage gaps had no reasons.** 183 lenses with images but no Einstein radius, never explained (07040b99 11:33). 695 lenses lack `model.fits`, and 20 have `fully_complete=True` but no VIS magnitude row, because QA counted a zip as complete (b5bbd7b8 13:34; the Tile102015606 pattern). `source_clumps: []` on every real tile (85d0d0a2 12:13). Each delivery needed a hand-written caveat list.

**P18. Column semantics were implicit.** `magnitudes.csv` holds µJy fluxes (b38ed821 11:56); `einstein_radius` in `lens_mass.csv` is the SIE parameter, not the effective value; 1σ columns are bounds, not ±errors; 1,035 offsets at the prior edge are lower limits (07040b99 08:23, 09:37).

**P19. Parity had no tool and the wrong statistic.** "Matches the euclid folder" was read as "within 3σ". Two Nautilus runs with the same code and data differed by median z 15.4 (521de454 12:47); latent 1σ collapsed to zero width at 100 PDF draws. The comparator dropped 16 duplicate reference keys and failed on 1-16 mas astrometry (819c5936 18:51, 19:53). User: "just showing a few lenses have really good consistency would give me confidence there's no code bug" (819c5936 19:17).

### 2.3 Project scripts

**P20. About 4.2k lines of hand-built results tooling** (w5 B): `merge_catalogue.py` 842, `compare_catalogues.py` 1094, `build_wcs_package.py` 613, `build_inspect.py` 489, plus 10 smaller scripts. They carry two inconsistent completeness rules (`merge_catalogue.py:298` zip-only vs `sed_completeness.py:51` zip-or-`.completed`), mtime-based "latest zip" in two places, and a status table from a hand snapshot (`grade_manifest.py:259`). About 50 commits are unpushed in the science clone (ee9e30af 06:18).

**P21. Implicit stage gates silently emptied products.** `build_inspect.py:182` skipped a lens unless both vis_lp and vis_pix existed: no products for 100/100 lenses in job 350452 (f184b313 08:31; 1b29d67b 12:56). A default `DATASET_NAMES_PATH` would have shrunk 4,912 to 100 (1b29d67b 13:32).

**P22. Flat vs nested output layout.** RAL has `output/dr1_sep1/<Tile>/`, the laptop `output/<Tile>/`. Every local build needed a scratch symlink, hit in 4 of 5 sessions in week 2 (aca5ba12 23:07; 58f73591 09:06; c8cde173 13:16).

**P23. Shell fragility.** `tar: command not found` failed job 350581 after 10 good stages (59955182 07:11). CRLF broke parsing twice: a third of spot checks looked like missing zips (ef45156a 19:50), and KNOWN_ISSUES told recipients "0 lenses" instead of 20 (b5bbd7b8 15:27). An ad-hoc fix-up zipped `wcs.csv` before closing it and shipped it empty (07040b99 11:33).

**P24. Packaging rewrote everything and the contents were not agreed.** The image catalogue tar was rewritten whole at 7.2 then 9.4 GB with `/mnt/ral` 94% full (07040b99 08:23). After 107 GB had started downloading, the user asked: "are the dataset and segementation map .zip files in th results zips?" No (b5bbd7b8 15:22). Rebuilding all parts adds about 11 GB.

### 2.4 HPC sync and transfer

**P25. Custom output roots were invisible.** `hpc/sync` hard-codes `PULL_DIRS=(output output_sed inspect)`; rsync without `--delete` re-created deleted sibling dirs (862ded5b 14:28; 99cc7b63 21:16). User: "it will become common place for me to split results using custom output folders, so we should fix that in Cortex or wherever it is appropriate" (862ded5b 16:06).

**P26. Many small files over NFS and SSH.** 741-tile extraction at 160 KB/s cut at 566 (f184b313 12:53); copy back of 5,199 folders 68 min (c7d2ad66 19:58); `du`/counts timed out at 25 min (07040b99 08:23); 107 GB download at about 5.5 MB/s, about 5.5 h (b5bbd7b8 14:14). User: "is this thing sitll running seeems very slow?" (f184b313 12:51).

**P27. Fixes lived only on RAL.** The retry wrapper, `DEPENDENCY=`, the post-build check and the RuntimeError fix ran uncommitted (1a1ec986 08:14; b5bbd7b8 13:34); the README records the git revision as "unknown" (ef45156a 12:17).

**P28. Walltime scaled linearly from a 110-lens test.** 16-32 min per 100 lenses at test scale; about 34 min per 100 at full scale under NFS contention. All 12 chunks TIMEOUT at 7h07, still on sample 1 of 2 (b5bbd7b8 06:10). The merge never ran at full size before production (b5bbd7b8 12:20).

**P29. SSH lockouts amplified by retries.** 8 minutes of subagent retries closed the host for about 2.5 h (1a1ec986 ~08:26); "Too many authentication failures" for about 40 min (b5bbd7b8 11:34).

### 2.5 Agent workflow

**P30. Explaining blanks away and designing witnesses wrongly.** The blank-column rationalisation (P11) and the 3σ parity witness (P19).

**P31. Hand-offs and approvals.** A survey subagent submitted 350581 on a relayed "continue" (1b29d67b 13:34-14:12). A 21:09 hand-off said the README and test tasks were in flight; next morning: "Nothing ran overnight, and last night's summary got two things wrong" (1a1ec986 08:01).

**P32. The funnel was reconciled after release, not before.** The agent advised not merging samples (ef45156a 16:41, user: "Are we safe to merge these all into one dr1_sep1_rest folder?"); the merge came back on 10-07 with duplicates (9d3eda96). The A+B count check (15,070 vs 14,028) ran only after shipping (b5bbd7b8 15:45).

**P33. Spec interpretation.** "Oh also .fits galaxy images and whatnot" (ef45156a 08:42) was read as model FITS only (P24). "5 examples" became zips (f184b313 12:34). "How quick … for the 100 lenses?" became an unrequested 25-lens build (9b4783b6 16:59).

**P34. Workflow overhead on a project repo.** The Heart-RED gate needed acknowledgement for non-release pipeline PRs four times (67a9f465 22:27 and others; 29f963ca 11:51 never answered). A plan-mode subagent spent 30 min and 93k tokens to park a plan (470a7dd6 17:26-17:32). Dirty shared Cortex/Mind checkouts blocked commits (b38ed821 11:54; 1a1ec986 08:14).

## 3. What worked and must be kept

- **Controls and red tests.** An ordered vs unordered control cleared assertions in 5 min (862ded5b 17:18); the sibling-dir fix was tested on the broken tree (20/20 vs 5) (94cfb571 ~21:00); every new test shown failing on unfixed source (67a9f465 22:41).
- **Measure before acting.** The per-type disk audit killed the `search.log` red herring (99cc7b63 18:50); the convergence audit saved about 25,000 core-hours of SED on bad inputs (f184b313 10:27).
- **Reading zip members in place.** A 14.8 GB nested STORED delivery read without unpacking (f69e5858); `build_inspect.extract_zip_member` and the slim image catalogue byte-identical to zip members (57c19491 08:16).
- **Manifests from disk, not logs** (f184b313 12:39), and include/exclude manifests with reasons instead of moving folders (74ceb5b1 19:11).
- **Chunk + merge + `parts_manifest.csv` + SHA256SUMS + per-zip re-open**, with `PARTS=k` unit-tested (28 tests) and idempotent per-lens file steps (`already_present`) (b5bbd7b8 06:29, 12:17).
- **sha256 end to end** and atomic replacement of delivered tars (07040b99 12:12-12:17); detached downloads ending in a checksum gate (`=== ALL OK`) (b5bbd7b8 14:14).
- **Read-only witnesses**: sha256 of source zips before and after, `find -newer` empty (67a9f465 22:11).
- **Provenance columns for fallbacks** (`source_clump_rule`, `source_rule`) and **post-build checks as afterok jobs**.
- **Test at small scale before production**, which caught the wrong-tree bug the second time (ef45156a 10:20).
- **Hand-off prompts with a "Traps (all hit before)" section** (9d3eda96 16:21) and memory notes at each milestone.

## 4. What PyAutoFit offers today, and the gaps

**Today** (w5 A1-A5):
- Layout `<output>/<path_prefix>/<unique_tag>/<name>/<identifier>` (`non_linear/paths/abstract.py:333-353`); `files/*.json`, `samples_summary.json`, `latent/latent_summary.json`, `image/`, `.completed` (`directory.py:264-268`).
- A zip is always written; `remove_files`/`hpc_mode` only decide whether the folder is deleted (`abstract.py:181-187, 363-381`; `abstract_search.py:1119-1144`). `preserve_in_zip` lets post-completion writers replace members (`abstract.py:383-445`).
- `Aggregator.from_directory(completed_only, unzip_temporary)`: one `os.walk`, sentinel `files/search.json`, eager extraction, sibling arbitration (fixed by #1602), path-sorted output (`aggregator/aggregator.py:177-393`). Lazy `SearchOutput` properties (`search_output.py:128-380`). Predicate queries are O(N) file reads (`aggregator.py:482-587`).
- The SQLite scraper builds a classic aggregator first and duplicates rows on re-add (`database/aggregator/scrape.py:40-45`; `database/aggregator/aggregator.py:398-401`). Not used by DR1.
- `AggregateCSV` (strict opt-in, first-row header, non-atomic save, labels by row index), `AggregateFITS`, `AggregateImages`. No manifest, checksum or packaging.
- `search_internal.dill` is atomic (`directory.py:209-223`); checkpoints are resumed on existence without validation (`nautilus/search.py:315-318`).

**The 17 gaps** (w5 C, numbering kept):
1. No results index or manifest; only `.completed`.
2. Status is binary (no running / interrupted / corrupt ckpt / corrupt zip / superseded / never-started).
3. No "which sibling hash is current" policy.
4. Eager full extraction on every scan.
5. No caching across scans; the SQLite scraper is not incremental.
6. One bad zip aborts the whole scan.
7. Non-atomic result zips and non-atomic CSV export.
8. No checkpoint validity check before resume.
9. No completeness over a declared grid.
10. AggregateCSV is all-or-nothing and non-incremental; labels by row index.
11. No chunk/merge support for exports.
12. No packaging/distribution helper (and PyAutoFit DEFLATEs PNG/FITS).
13. No plain-JSON view of typed outputs.
14. No library-level diff/parity tool.
15. Rerun means rebuild everything.
16. Image payload dominates and is duplicated; no library-oriented product policy.
17. Minor: `print` reporting; inverted `post_fit_output` docstring; `restore()` deletes the zip at every rerun start.

## 5. Gap → phase mapping

| Gap | Phase | Notes |
|---|---|---|
| 1 index | 1 | `.autofit_index.*` + CLI |
| 2 status classes | 1 | reads hpc-campaign `status.json` when present |
| 3 sibling policy | 1 | `agg.latest_per` on `completed_at` |
| 4 eager extraction | 1 | lazy member reads, `from_index` |
| 5 scan cache | 1, 3 | index (1), cached rows (3) |
| 6 bad zip abort | 0 | `on_error`, `agg.errors` |
| 7 non-atomic | 0, 3 | zip (0), CSV (3) |
| 8 checkpoint validity | 0 | probe + quarantine |
| 9 completeness | 2 | declared grid, per-product |
| 10 AggregateCSV | 0, 3 | strict default + union header (0), incremental (3) |
| 11 chunk/merge | 3 | scheduler-agnostic |
| 12 packaging | 0, 4 | STORED media (0), `af.export.package` (4) |
| 13 plain JSON | 3 | `search_output.plain` |
| 14 diff/parity | 4 | plus scatter helper |
| 15 rebuild all | 3 | refresh in place |
| 16 media payload | 4 + open question 5 | render on demand needs a ruling |
| 17 minor | 0, 1 | docstring, `restore` (0); logging (1) |

Pain points not mapped to a phase: P9 (linear-profile instances, a PyAutoFit/PyAutoGalaxy bug prompt), P10 residual (per-latent NaN masking, fit-time: hpc-campaign or a bug prompt), P3 run-time half (hpc-campaign phase 1), and P25-P34 (§6).

## 6. Non-library lessons as candidate prompts

Proposed paths only; none of these files were created.

- `draft/feature/autolens_assistant/hpc_sync_custom_output_roots_and_index_pull.md` — `PULL_DIRS` from config, `--delete` on result legs, pull index/inspect only (P25, P26).
- `draft/feature/autolens_assistant/hpc_sync_ssh_retry_cap_backoff.md` — hard 2-attempt cap with backoff on every ssh wrapper (P29).
- `draft/feature/autolens_assistant/hpc_sync_push_refuses_newer_remote_and_stamps_revision.md` — refuse to push over newer RAL files; write a git-revision stamp on push (P27).
- `draft/feature/autolens_assistant/results_library_release_checklist.md` — agree distribution contents, reconcile the object funnel, 1% test plus a full-size merge dry run, walltime from p95 not linear scaling, before any build (P24, P28, P32, P33).
- `draft/feature/euclid/catalogue_scripts_shell_hygiene.md` — `set -euo pipefail`, Python archiving instead of `tar`, CRLF-safe readers, never run a producer against an empty tree silently (P21, P23). Fold into the upstream-tooling prompt if still open.
- `draft/feature/pyautobrain/subagent_never_submits_on_relayed_continue.md` — a relayed "continue" is never approval to submit or spend compute (P31).
- `draft/feature/pyautobrain/handoff_claims_require_durable_state.md` — record state on disk before a hand-off claims it (P31).
- `draft/feature/pyautobrain/blank_column_is_lookup_miss_until_proven.md` — agent rule: a blank column is a lookup miss until the summary JSON proves otherwise; parity witnesses use run-to-run scatter (P30).
- `draft/maintenance/pyautobrain/heart_red_gate_exempt_non_release_project_repos.md` — exempt project pipeline repos from the Heart-RED PR-open gate (P34).
- `draft/bug/autofit/linear_profile_instance_from_samples_zero_flux.md` — warn or raise when a max-LH instance has unsolved linear profiles (P9).
