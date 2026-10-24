"""Green-path tests for the metricslite CLI."""

import json

import pytest

from metricslite.cli import main


class TestCli:
    def test_summarize_prints_json(self, capsys):
        assert main(["summarize", "--samples", "1,2,3"]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload == {"count": 3, "mean": 2.0, "min": 1.0, "max": 3.0}

    def test_percentile_prints_json(self, capsys):
        assert main(["percentile", "--samples", "10,20,30", "--p", "50"]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload == {"p": 50.0, "value": 20.0}

    def test_unparsable_samples_exit_nonzero(self, capsys):
        assert main(["summarize", "--samples", "abc"]) == 1
        assert "error:" in capsys.readouterr().err

    def test_missing_subcommand_exit_nonzero(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            main([])
        assert excinfo.value.code != 0
