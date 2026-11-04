# clean_slate.sh --packaging silently finds nothing on the grouped repo layout

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-11-04 (pre-rehearsal /hygiene sweep)

`pyauto-brain hygiene packaging` reported 10 ignored `*.egg-info/` and `build/` directories (Nerves, Fit, Array, Galaxy, Lens), and recommends `@PyAutoBrain/bin/clean_slate.sh --packaging`. On the dev box, `DRY_RUN=1 clean_slate.sh --packaging` printed only "Dry run only — nothing changed": it enumerates repos with `for dir in */` at `$PYAUTO_ROOT` (line ~155), but `~/Code/PyAutoLabs` groups repos (`fit/PyAutoFit`, `array/PyAutoArray`, `organs/PyAutoNerves`, ...), so no repo matches. The hygiene scan itself handles the grouped layout, so the scan and the remedy disagree.

The 10 directories were removed by hand on 2026-11-04, using the same rule: ignored and no tracked files. Fix: enumerate repos the way the hygiene scanner does (or through the shared repo resolver), and add a test with a grouped-layout fixture. The dataset/output/scratch scopes of `clean_slate.sh` probably share the same blind spot; check them too.
