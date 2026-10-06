"""Green-path tests for metricslite.counters."""

from metricslite import Counter


class TestCounter:
    def test_inc_and_get_same_case(self):
        c = Counter()
        c.inc("requests")
        c.inc("requests", by=4)
        assert c.get("requests") == 5

    def test_unknown_key_is_zero(self):
        assert Counter().get("nope") == 0

    def test_total_sums_all_buckets(self):
        c = Counter()
        c.inc("a", by=2)
        c.inc("b", by=3)
        assert c.total() == 5

    def test_keys_sorted(self):
        c = Counter()
        c.inc("gamma")
        c.inc("alpha", by=2)
        c.inc("alpha")
        assert c.keys() == ["alpha", "gamma"]
        assert c.get("alpha") == 3

    def test_default_increment_is_one(self):
        c = Counter()
        c.inc("hits")
        assert c.get("hits") == 1

    def test_merge_and_as_dict(self):
        a = Counter()
        a.inc("alpha", by=2)
        b = Counter()
        b.inc("beta", by=3)
        a.merge(b)
        assert a.get("alpha") == 2
        assert a.get("beta") == 3
        assert a.total() == 5
        assert a.as_dict() == {"alpha": 2, "beta": 3}
