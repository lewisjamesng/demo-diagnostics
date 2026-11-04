import pytest

from diagnostics import load_rules, parse_code, parse_report


@pytest.fixture(scope="module")
def rules():
    return load_rules()


def test_load_rules_reads_yaml(rules):
    assert rules["systems"]["P"] == "powertrain"
    assert len(rules["rules"]) == 4


def test_parse_code_matches_rule(rules):
    code = parse_code(" p0a80 ", rules)
    assert code.code == "P0A80"
    assert code.system == "powertrain"
    assert code.subsystem == "high-voltage battery"
    assert code.severity == "critical"


def test_parse_code_falls_back_to_default(rules):
    code = parse_code("B1234", rules)
    assert code.subsystem == "unclassified"
    assert code.severity == "medium"


def test_parse_code_rejects_garbage(rules):
    with pytest.raises(ValueError):
        parse_code("XYZ", rules)


def test_parse_report_sorts_and_dedupes(rules):
    report = parse_report("P0505, C0110\nP0A80 P0505", rules)
    assert [c.code for c in report] == ["P0A80", "C0110", "P0505"]


def test_load_rules_rejects_invalid_file(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("just: a mapping\n")
    with pytest.raises(ValueError):
        load_rules(bad)
