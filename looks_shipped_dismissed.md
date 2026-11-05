# Looks shipped — dismissed

<!-- The close-out guard (PyAutoBrain `intake looks-shipped`, run daily by
     .github/workflows/looks_shipped.yml) flags open drafts with strong evidence
     their work already shipped. It never retires anything: a human answers each
     flag on the dashboard's "Looks shipped — confirm" section.

     Confirm  = close the draft: `python3 scripts/lifecycle.py close <slug>
                --date <YYYY-MM-DD> --from-file <record-body.md>
                --prompt <draft path> --apply`.
     Dismiss  = add one bullet below — the draft path first, then the date and
                why it is NOT shipped. A dismissed draft is no longer flagged and
                the batch planner may propose it again. Delete the bullet to let
                the guard look at it afresh.

     Format: `- draft/<work-type>/<target>/<name>.md — YYYY-MM-DD — <why>` -->
