# Heart's manifest_drift parser silently drops any check leg with a suffix after its status

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a unit test feeds `heart/checks/manifest_drift.py`'s parser the real `repos_sync.py --check` stdout and asserts every `^check ` line is accounted for; today 16 of 17 parse and `generated hooks (session-start + end-at-deliverable)` is dropped, so the test is red before the fix and green after.
Review-minutes: 5
Unattended: ready

## The defect

`PyAutoHeart/heart/checks/manifest_drift.py:45`:

```python
_CHECK_LINE = re.compile(r"^check (?P<label>.+?): (?P<status>OK|\d+ mismatch\(es\))$")
```

The status group is anchored to end-of-line, so a leg that prints anything after its
status is not matched at all — it is not counted, not reported, and cannot turn Heart
red. It is invisible rather than green.

One leg does this today. Measured 2026-09-18 against the real workspace by running
`repos_sync.py --check` and matching each `^check ` line with Heart's own regex:

```
  UNPARSED -> check generated hooks (session-start + end-at-deliverable): OK (37 of 37 checked out, 2 excluded)

parsed by Heart: 16 | INVISIBLE to Heart: 1
```

So the hook-propagation drift check — the one that verifies the generated
`session-start` and `end-at-deliverable` hooks are in sync across every checked-out
repo — has never reached Heart's verdict. It passes today, which is why nobody noticed.

## Why it matters beyond this one leg

This is a silent-coupling defect, not a typo: the producer (`PyAutoMind/scripts/repos_sync.py`)
and the consumer (Heart) agree on a line format only by convention, and the consumer fails
open. Any future leg that adds a helpful denominator to its status line disappears from
Heart the same way, with no error anywhere.

Found while adding a new `workspace checkouts (manifest <-> disk)` leg for PyAutoBrain#391;
that leg was deliberately formatted to put its denominator on a separate `  • ...` line
specifically to avoid this trap. That workaround is evidence the contract is too implicit.

## Suggested shape

Fix the consumer, and make the coupling explicit rather than conventional:

1. Allow a trailing parenthetical after the status, or parse the status as a prefix rather
   than anchoring it to `$`.
2. Fail LOUD on an unrecognised `^check ` line — an unparseable leg should be a problem
   Heart reports, never a line it skips. That is the actual bug: the parser's failure mode
   is silence.
3. Consider asserting the leg COUNT, so a leg vanishing from the producer is itself drift.

Do not fix this by reformatting the producer's output to suit the regex — that leaves the
next leg free to trip the same wire.
