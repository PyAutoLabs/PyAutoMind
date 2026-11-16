Enforces the human's 2026-11-16 public-name narrowing of `glance` (after the seeded audit, row 08, PyAutoGalaxy#656). Shipped as PyAutoBrain#642 (0c534de76), merged 2026-11-16 on `ci-verdict` GREEN with Heart dev-ship GREEN. Issue PyAutoBrain#641.

**Built:** `bin/public_names.py` / `pyauto-brain public-names`, an `ast` comparison of library modules' public names at merge base and head.
- Exit 1: added or renamed. Exit 2: cannot tell, which fails closed.
- Covered repos are case-folded and listed in `config/policy.yaml`; package directories come from Mind `repos.yaml`.
- **The watcher runs it deterministically** in `spawn_closeout`, before any close-out session. A hit or a cannot-tell writes a refused `.closeout`, which reaches the digest.
- It is also a stop in the tiered merge (`/prm`, `ship_*`) and an entry in the ReviewSurface.

**Doctrine (human-approved):**
- the Enforcement paragraph;
- a network-surface amendment allowing read-only `gh api` reads on the library PRs the shift's own workers named: the PR, compare, files, contents, and the package directory.

**Witness:**
- 40 tests. #656 is refused, live too (also when spelled lowercase). Five other library PRs come back clean.
- Brain suite: 2069 passed.

**Review:** independent Opus, FINDINGS ×6 then fixed. Re-review found the amendment missed two calls, fixed in 0df7f54. A star import of a public module no longer over-refuses (2605756).

## Original prompt

# Glance close-out and review: detect added or renamed public library names

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Consequence: glance
Priority: high
Status: draft
Filed: 2026-11-16
Epic: autonomous-orchestrators
Lane: any

Enforces AUTONOMY.md "Public-name narrowing of `glance` — 2026-11-16" (human ruling after the
seeded audit, row 08, PyAutoGalaxy#656): a change that adds or renames a public name in a library
package (PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens, PyAutoCTI) is a human `/prm`. Public
means a module-level function, class or constant without a leading underscore, or anything
exported from a package `__init__`.

Add a deterministic diff check, shared by the watcher close-out, the in-turn ship skills and the
review faculty. Run it over `git diff base..head` of library repos with Python `ast`, comparing the
public names per module before and after. Added or removed-and-added (renamed) names refuse
`glance` with the reason "public name added/renamed: <names> → human /prm", and the digest
lists it. Private names, tests, workspace and organ repos are ignored.

Witness: offline tests. PyAutoGalaxy#656's diff (seven `latent_*_from`) is refused. A private
helper or a body-only change passes. A rename is caught. The close-out refusal reaches the digest.
