## prior-config-cache
- issue: https://github.com/PyAutoLabs/PyAutoConf/issues/129
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoConf/pull/130 (MERGED)
- summary: The aggregator arc's "deeper follow-up" — cProfile showed 77% of per-result summary/model load was Model.__init__ default-prior construction, dominated by JSONPriorConfig re-SORTING the whole flattened config per lookup + linear scans of identical repeated queries. Cached sorted tuples + memoized lookups per instance (incl. misses — the class-family probe relies on expected misses; _UNCACHED/_NOT_FOUND sentinels since found-None is legal). Fresh instance per conf push = natural invalidation; returned sub-dicts were already aliased.
- measured: values("model") 8.15→4.60 ms/result (−44%); summaries −25%. Benefits every Model/Collection construction incl. search startup. Remaining floor (~4.6ms/result: sample-json from_dict + prior construction) = diminishing returns, NOT pursuing.
- suites: autoconf 148 + PyAutoFit 1495 green. Shipped+merged through 5-reason pre-existing Heart RED on user ack.

## Original prompt

# Cache prior-config lookups (from_dict model deserialization floor)

Type: feature
Target: PyAutoConf
Repos:
- PyAutoConf
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: issued

Deeper-speed follow-up off the aggregator arc: 77% of per-result summary/model load
is Model.__init__ default-prior construction; JSONPriorConfig re-sorts the whole
flattened config per lookup and linear-scans it, identical queries repeating per
prior per result. Cache sorted tuples + memoize lookups per instance.
Issue: https://github.com/PyAutoLabs/PyAutoConf/issues/129
