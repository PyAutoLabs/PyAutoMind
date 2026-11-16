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
