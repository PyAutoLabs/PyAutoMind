# Simplify inference dashboard and match Pulse likelihood navigation

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight
Difficulty: medium
Consequence: glance
Autonomy: safe
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/17

## Plan

Refine the already approved dashboard design using the user's concrete review. Campaign table becomes Campaign / Recent progress / Next steps; omit empty last-checkin text. Keep ledger metadata intact. Make active task cells readable without splitting status/priority tokens. Use one Inference Results section containing PyAutoLens → Imaging → likelihood list, adopting Pulse model-choice CSS and font. Group instruments inside the likelihood page via a select; split record-backed JAX and Numba implementations (unknown separately), preserving exact record binding and old setup URLs. Collapse normal provenance in Evidence details; retain short warnings only on actual failures/staleness. Validate grouping, backend/instrument isolation, old links, campaign fields, desktop/mobile navigation and copy behavior. No producer schema/data changes or scientific execution.

Detailed files: insight/campaigns.py table rendering; insight/board.py section hierarchy/provenance; insight/setup_browser.py grouping/filtered page rendering; CSS/JS instrument route and Pulse style; tests and generated board. Existing v2 stable setup IDs stay unchanged. Display groups derive from recorded backend, never hardware inference. Empty declared instruments remain explicit without fabricated timings.

Witness: live/preview hierarchy has no duplicate repo section, Delaunay and Delaunay (Numba) distinct, instrument change retains chosen implementation and shows only its records; campaign status words not split. Existing failure/unknown qualifications still accessible. Tier: glance — merge mode: human-authorized continuation of approved dashboard work, merge on green with witness.

## Original request

The Active campaigns table has a lot of text wrap around (e.g. active-e), I also think theres too much text and its info overload. Maybe just have Recent Progress and Next Steps? Job Status repeats the same thing and Blockers seems               unecessary.            Remove "Last check-in: not recorded yet.".            Active tasks has some text wraparound work removing where possible.         Is "Inference Eevidence" mean to be separate from "autolens_inference"? Should it be "Inference Results" -> "PyAutoLens" -> "Imaging" like PyAutoPulse? I also thing all the Delaunay and rectangular things should then be a list in exactly the style of Pulse (font size, etc).    I think the instrument, which defines run time, should be a drop down menu when you click on the thing, which again mirrors Pulse to have unique likelihood functions the clickable things.             We therefore also want Delaunay (Numba) to be a separate thing from Delaunay as the run times are different.          Remove this text: "Integrity: ok · Freshness: freshness policy unspecified · evidence time unknown · Scientific qualification: 0/56 accepted by producer; remaining assessments shown below

Captured source branch: main. Revision: de37acfe797465205128d45973af5e853c74a684. Capture time: 2026-10-08T08:44:26Z. Latest attempt: 2026-10-08T08:44:26Z."

## Routing

Brain feature decision direct; organ dashboard source routes through start_workspace/ship_workspace (not published-library release), as in the parent task. No scientific change requires Memory research. Branch survey clean main; no conflicting claims.
