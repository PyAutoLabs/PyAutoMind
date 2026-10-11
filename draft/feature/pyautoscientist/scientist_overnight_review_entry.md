# Move overnight review entry to Scientist

Type: feature
Epic: scientist-adoption-pilot
Consequence: judge
Target: PyAutoScientist
Repos: PyAutoBrain, PyAutoScientist
Prerequisite: scientist-local-discovery merged (Brain#518)

## Original request

I also dont know whwy Brain has "Review oernight work" that is a Scientist task, it could be a brain agent I guess but put it there

## Plan

Move the Review overnight work user-facing board section/navigation from Brain to Scientist; retain Brain agent execution and authoritative source evidence. Read board/_board.py and Scientist organism_board.py contracts before selecting feed integration. Preserve exceptions, pending/missing runs and evidence dates; do not copy a competing ledger. Validate both boards. Current start-workspace conflict guard refuses Brain because scientist-local-discovery still claims it; resume after PR#518 and its close-out.
