Shipped inside `howto-stale-self-location` (HowToGalaxy#76, HowToLens#82, merged
2026-09-14) rather than as its own task, on the human's instruction to fold the
follow-ups in.

**The prompt overstated the work.** It was filed as authoring a `__Paths__`
orientation block for parity with HowToFit. On reading the files, both repos
already had a `__Directories__` block doing most of that job — working-directory
assumption, the folders, the commented `%cd`. What was actually missing was the
**clone URL**: neither repo told a reader who did not have it where to get it,
which is the same defect that opened HowToGalaxy#75 in HowToFit's spelling.
HowToLens was also missing the `config/` mention the other two carry.

So this was a one-sentence addition to an existing block, not new authorship —
which is why it belonged in the fix PRs rather than a separate task.

Shipped: HowToGalaxy `5844d9a`, HowToLens `2d791bc`.

See `complete/2026/09/howto-stale-self-location.md`.
