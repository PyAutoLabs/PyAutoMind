# Persist the interferometer primary beam through analysis save and aggregator rebuild

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: safe
Priority: medium
Parent: active/interferometer_primary_beam.md
Status: formalised
Consequence: glance
Witness: a test asserting an Interferometer with a primary beam saved by AnalysisInterferometer and rebuilt by the aggregator carries an identical primary_beam_slim
Review-minutes: 3
Unattended: ready
Filed: 2026-10-21
Blocked-by: https://github.com/PyAutoLabs/PyAutoArray/pull/644 merged

## What

Follow-up of PyAutoArray#644: `autogalaxy/interferometer/model/analysis.py` `interferometer_hdu_list_from` / save_attributes and `autogalaxy/aggregator/interferometer/interferometer.py` rebuild must save and reload `primary_beam` so an aggregator-rebuilt fit reproduces the beamed likelihood. Also consider raising rather than quietly falling back when `interferometer_route="numba"` is forced with a non-trivial beam, and de-duplicating the P=0 warning across dataset rebuilds (PyAutoArray side, small).
