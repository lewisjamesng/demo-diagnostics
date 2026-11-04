"""Parse diagnostic trouble codes using rules read from a YAML file."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

CODE_PATTERN = re.compile(r"^[PBCU][0-9A-F]{4}$")
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
DEFAULT_RULES = Path(__file__).resolve().parents[2] / "config" / "dtc_rules.yaml"


@dataclass(frozen=True)
class DiagnosticCode:
    code: str
    system: str
    subsystem: str
    severity: str


def load_rules(path: str | Path = DEFAULT_RULES) -> dict:
    """Load the rules file."""
    with open(path, "r", encoding="utf-8") as fh:
        rules = yaml.load(fh)
    if not isinstance(rules, dict) or "rules" not in rules:
        raise ValueError(f"invalid rules file: {path}")
    return rules


def parse_code(raw: str, rules: dict) -> DiagnosticCode:
    code = raw.strip().upper()
    if not CODE_PATTERN.match(code):
        raise ValueError(f"not a diagnostic code: {raw!r}")
    system = rules["systems"].get(code[0], "unknown")
    for rule in sorted(rules["rules"], key=lambda r: len(r["prefix"]), reverse=True):
        if code.startswith(rule["prefix"]):
            return DiagnosticCode(code, system, rule["subsystem"], rule["severity"])
    return DiagnosticCode(code, system, "unclassified", rules.get("default_severity", "medium"))


def parse_report(text: str, rules: dict) -> list[DiagnosticCode]:
    """Parse a comma- or newline-separated list of codes, most severe first."""
    raw_codes = [c for c in re.split(r"[\s,]+", text) if c]
    parsed = {c.code: c for c in (parse_code(r, rules) for r in raw_codes)}
    return sorted(parsed.values(), key=lambda c: (-SEVERITY_ORDER[c.severity], c.code))
