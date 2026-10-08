# Samples adapter and Checkpointer/resume split (epic search-extensibility, phase A3)

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Themes:
- searches
- persistence
Difficulty: large
Autonomy: safe
Consequence: judge
Witness: constructing `af.Emcee()`, `af.BlackJAXNUTS()` and `af.SMC()` leaves `conf.instance` unchanged (the three `CONFIG_MUTATION_XFAIL` strict xfails are deleted and pass); golden `samples.csv` fixtures for emcee, dynesty, nautilus, NUTS and SMC are byte-identical through the adapter; a pre-A3 output folder (Emcee HDF included) still loads in the aggregator; the two Dynesty A0a(ii) xfails (restored folder falls back to samples.csv) are deleted and pass
Unattended: ready
Priority: high
Epic: search-extensibility
Status: planned
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1677
Filed: 2026-10-08

Human launch 2026-10-08: `--auto` for A2, A3, A3b and B3. Plan `draft/research/autofit/search_extensibility_epic_report.md` §4 (phase text quoted verbatim below), architecture §3.3–§3.5, decisions in §8. A0, A0c, A1 and B2 are merged (A1: capability attributes, `Analysis.is_jax`, REQUIRED gate, registry/manifest, `docs/design/run_ctx.md` frozen). Golden identifiers (A0a(i)) are frozen by human ruling: any identifier change stops the item and is flagged. The nine A0 strict xfails are witnesses: flip only the ones a phase names, never add silent ones. Parallel with A2: this phase does not touch `Fitness`, `parallel/` or the `run(ctx)` bridge. Implemented on its own branch from main; the main session merges A2 and A3 independently and reconciles any overlap.

## Original request (verbatim from the epic plan)

"A3 — Samples adapter, Checkpointer/resume split (depends on A1; parallel with A2, no Fitness touch; surveys/01 P3; D5, D8, D13). Repo: PyAutoFit. Scope: golden `samples.csv` tests on pickled emcee, dynesty, nautilus, NUTS and SMC fixtures, merged before the adapter; `samples/adapter.py` (`RawSamples`, `samples_from_raw`, one log-prior helper, sentinel unification; D13); `ChainPosterior.thin`, which gives Emcee the empty-chain fallback; base `samples_via_internal_from` implemented once; the three archive `Checkpointer` strategies and the separate `resume_state`; `resumable` declared honestly; delete the NUTS/SMC duplicate pickle, the Emcee no-op and the three `conf.instance` mutations; injected internal-result loading with format-aware legacy detection, and the design note on atomic writes, corruption and retention (D5). Risk: medium. Numerical equivalence of samples must hold byte-for-byte against the goldens. Verify: the A0a `conf.instance` xfails flip to pass; `test_emcee/zeus/blackjax_nuts/blackjax_smc.py`, `nss/test_checkpoint.py`; kill-and-resume via `MultiStartResurrect.py` and a Nautilus kill-and-resume; directory, database, null, zipped and summary-only outputs load; the aggregator loads a pre-A3 folder (Emcee HDF included). Witness: constructing `af.Emcee()` leaves `conf.instance` unchanged, the goldens are byte-identical, and a pre-A3 output folder still loads in the aggregator."

## Pins (main 2026-10-08)

`conf.instance["output"]["search_internal"] = True` at `emcee/search.py:131`, `nuts/search.py:265`, `smc/search.py:315`. Architecture §3.4: `DillCheckpointer` default, `PickleCheckpointer` (NUTS, SMC), `NativeFileCheckpointer(filename, loader)` (emcee HDF, dynesty savestate, nautilus hdf5, NSS pkl); each offers `save/load/exists/finalize` + `retain_after_completion`; `result_internal` (archive) is separate from `resume_state` (Dynesty, Nautilus, NSS, MultiStart only). The A0a(ii) Dynesty xfails exist because `output_search_internal` deletes `savestate.save` after a completed fit: the retention policy fixes that. The A1 `checkpointer` capability attribute (deferred from §3.1) lands here. Goldens: generate the pickled fixtures + `samples.csv` from main FIRST (own commit), then the adapter must reproduce them byte-for-byte. Samples weights/representations preserved, no renormalisation (D13). The legacy HDF detection at `paths/directory.py:238-246` moves, it is not replaced by a dill-only fallback.

## Verification

Full `pytest test_autofit` (expect 9 → 4 strict xfails: the three CONFIG_MUTATION and the two Dynesty backend xfails deleted; the four Emcee/Zeus/NUTS/SMC import-time-settings xfails are A4 and stay); nojax emulation; afT `searches/{Emcee,Zeus,DynestyStatic,Nautilus,BlackJAXNUTS,SMC,MultiStartResurrect}.py` under test mode; a Nautilus kill-and-resume script; aggregator load of a pre-A3 folder produced from main.

## Shape

One PyAutoFit PR (`pending-release`), commits: goldens → adapter → thin/empty-chain → Checkpointers + resume_state + retention → conf.instance deletions + xfail flips → legacy loading + design note. Refactor cap safe → ends at PR-open; tier judge.
