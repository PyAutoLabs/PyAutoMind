# Migrate the six user-filed feature threads to the Discussions hub

Type: maintenance
Target: community
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoArray
Themes:
- community
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: glance
Witness: each of the six issues in the manifest is locked with a "converted to discussion" redirect, PyAutoArray#551 sits in the hub's (`PyAutoLabs/.github`) Proposals category and the five shipped threads in Ideas with original authors and comments intact, and `pyauto-brain community` lists #551's discussion as awaiting our response.
Review-minutes: 5
Filed: 2026-09-17

Spawned by `policy/community_surface.md` (PyAutoMind#403). The button is
UI-only: the REST Discussions API is read-only, `createDiscussion` is GraphQL
(refused for remote sessions) and would lose the author anyway. So this is a
human's ten minutes at github.com, in this order:

Live check, 2026-09-19: the org hub already resolves, but its category is
currently **Proposal** (singular, slug `proposal`) and **not answerable**.
Configure **Proposals** (slug `proposals`) as answerable and open to anyone
before merging the seven support-link PRs, whose implementation contact link
targets that category. Check the category's actual settings: GitHub returns
HTTP 200 even for an unknown category URL. **Scientific Analysis** is also
currently not answerable; make it answerable as the policy specifies.
Skip promotion steps already completed, and verify the remaining settings.

1. **Promote the hub.** On `PyAutoLabs/.github` → Settings → Features →
   enable Discussions. Organization settings → Discussions → enable, source
   repository `.github`. Then on the hub's categories: confirm Announcements,
   Q&A (answerable), Ideas, Show and tell, General exist and add
   **Scientific analysis** (answerable, "lens modelling, inference,
   is-this-result-right") and **Proposals** (answerable, open to anyone,
   "a concrete design, API sketch or reference implementation the author
   means to build"). Transfer PyAutoLens's one thread
   (https://github.com/PyAutoLabs/PyAutoLens/discussions/603 → sidebar →
   *Transfer discussion* → `.github`, Announcements), then switch
   PyAutoLens's Discussions off. Pin one Q&A thread titled "How to get help"
   whose body is the two sentences from the policy page.
2. **Convert, then transfer.** *Convert to discussion* creates the thread in
   the issue's **own** repo, so per repo (PyAutoArray, PyAutoGalaxy, then
   PyAutoLens): enable Discussions there (Settings → Features), convert
   each issue, open the new discussion → sidebar → *Transfer discussion* →
   `.github`, then turn that repo's Discussions off again. Category
   **Proposals** for the open design; **Ideas** for the five shipped requests:
   - https://github.com/PyAutoLabs/PyAutoArray/issues/551 (@HRSAstro, open) → **Proposals**
   - https://github.com/PyAutoLabs/PyAutoArray/issues/499 (@HRSAstro, shipped)
   - https://github.com/PyAutoLabs/PyAutoLens/issues/631 (@mwiet, shipped)
   - https://github.com/PyAutoLabs/PyAutoLens/issues/564 (@mwiet, shipped)
   - https://github.com/PyAutoLabs/PyAutoLens/issues/542 (@mwiet, shipped)
   - https://github.com/PyAutoLabs/PyAutoGalaxy/issues/419 (@Sketos, shipped)
   Leave PyAutoArray#535 (@ClarkGuilty) as the issue it is — an open bug with
   a full reproducer is dev work; route it with `/community triage`.
3. **Verify with the Ears:** `bin/pyauto-brain community` lists the #551
   discussion in Proposals under awaiting-response (its last word is @HRSAstro's), and
   nothing else from the manifest (the shipped ones end on our comment).
   Retire this prompt with `scripts/lifecycle.py record`.

The Ears then owe @HRSAstro a reply on the converted #551 thread — draft it in
`/community`, as always.
