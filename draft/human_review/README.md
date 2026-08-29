# human_review/

Work that has already **shipped** and that a human wants to read and sign off
before it counts as done. The prompt describes what to check and points at the
evidence — the merged PR(s), the commits, the `complete/` record.

This is the one work-type nothing infers. `/intake` will never choose it, and no
completed task acquires it by default: file one only by declaring
`Type: human review` (`human-review`/`human_review` read the same) when a human
asks for a review. Review is opt-in, not a lifecycle stage — `/prm` and the ship
skills close a task out exactly as before. An empty folder means nothing has been
flagged, not that nothing shipped.

`dashboard.md` renders these as their own **Human review** section directly under
*In flight*, never as backlog: a review is not work to pick up, it is work
waiting on a person. Its 📋 hands out a read-and-report prompt, not a
`/start_dev` — the work is done; what is outstanding is the reading.

Sign one off by retiring the prompt the usual way (`scripts/lifecycle.py record
<slug> --date <YYYY-MM-DD> --from-file <body> --apply`, then `git rm` the prompt
and regenerate the dashboard). If it does not pass, file the follow-up with
`/intake` as an ordinary task.

See [`../../ROUTING.md`](../../ROUTING.md) and REFERENCE.md "Prompt taxonomy".
