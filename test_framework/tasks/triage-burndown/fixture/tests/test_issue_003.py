"""Documented-red test for issue-003 (summarize([]) raises the wrong error type).

Red on the pristine fixture BY DESIGN. Green once issue-003 is fixed.
Repro: /usr/bin/python3 -m pytest tests/test_issue_003.py -q
"""

import pytest

from metricslite import summarize


def test_summarize_empty_raises_value_error():
    with pytest.raises(ValueError):
        summarize([])
