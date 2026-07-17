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
