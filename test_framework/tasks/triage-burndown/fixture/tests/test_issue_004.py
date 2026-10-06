"""Documented-red test for issue-004 (Counter keys case-sensitive, not insensitive).

Red on the pristine fixture BY DESIGN. Green once issue-004 is fixed.
Repro: /usr/bin/python3 -m pytest tests/test_issue_004.py -q
"""

from metricslite import Counter


def test_counter_keys_are_case_insensitive():
    counter = Counter()
    counter.inc("Error")
    assert counter.get("error") == 1
    counter.inc("ERROR", by=2)
    assert counter.get("Error") == 3
    assert counter.total() == 3
    assert counter.keys() == ["error"]
