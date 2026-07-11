# Normalize CRLF in executable scripts + add .gitattributes eol=lf guards

Type: refactor
Target: libraries
Repos:
- PyAutoConf
- PyAutoFit
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

The right-sized version of the CRLF fix (the hygiene `crlf` check surfaced it,
severity-split 2026-07-11, PyAutoBrain#98/#99). **Scope is the ~6 executable
scripts that actually break on Linux/HPC — NOT the ~710 cosmetic library `.py`.**
A CRLF shebang (`#!/bin/bash\r`) makes the kernel look for interpreter
`/bin/bash\r` → "bad interpreter" — exactly the "bash scripts don't work on HPC"
pain. Library `.py` CRLF is harmless (Python universal newlines) and mass-
normalising it churns `git blame` across the codebase for zero functional gain.

**Do:**
1. **Normalize the executable scripts with CRLF → LF.** Live count (2026-07-11):
   6 — PyAutoConf 4, PyAutoFit 1, PyAutoLens 1. Find them with
   `hygiene crlf` (the ranked count) or per repo:
   `git grep -Il $'\r$' -- '*.sh'` + executable `.py`
   (`git ls-files --stage -- '*.py' | awk '$1 ~ /755$/'`, then grep those for CRLF).
   Fix: `sed -i 's/\r$//' <file>` / `dos2unix`.
2. **Add a `.gitattributes` to each repo** (none exist today) to keep scripts LF
   forever regardless of a Windows contributor:
   ```
   *.sh    text eol=lf
   *.bash  text eol=lf
   ```
   (and, for any directly-executed `.py`, an explicit `<path> text eol=lf`).
3. **Leave the ~710 library `.py` CRLF alone** for now. If eventual whole-repo
   consistency is wanted, that is a SEPARATE decision and the mechanism is
   `* text=auto` in `.gitattributes` — it normalises files **as they are next
   touched**, avoiding a single ~710-file retroactive diff. Do NOT bundle a mass
   `.py` normalization into this task without an explicit go.

**Boundary/why supervised:** the *fix* is behaviour-preserving (line endings on
scripts), but the *policy* (which repos get `.gitattributes`, whether to adopt
`* text=auto`) is a judgement — confirm the scope before the mass-normalise step.
Extend to the other repos (Array/Galaxy/Build/Brain/Reduce + workspaces) if they
gain script CRLF later; today the 6 are in Conf/Fit/Lens.

**Done when:** the executable scripts are LF, each affected repo has a
`.gitattributes` with `*.sh text eol=lf`, `hygiene crlf` reports 0 scripts, and
the ~710 cosmetic `.py` are untouched (unless the user opts into `* text=auto`).

<!-- filed 2026-07-11 from the "is dos2unix important to enforce?" discussion:
     enforce for scripts (break on HPC), NOT all code. See hygiene crlf severity
     split PyAutoBrain#98/#99 + feedback_crlf_files_in_pyautoarray.md. -->
