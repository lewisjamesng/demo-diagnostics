# demo-diagnostics

Diagnostic trouble code (DTC) parser. It reads classification rules from `config/dtc_rules.yaml` and turns raw code lists into severity-sorted results. **Synthetic demo repository.** All codes, rules and data are fictional sample material for a security-remediation demo.

**Owner:** `@demo-org/vehicle-diagnostics-team` (see `.github/CODEOWNERS`)

## Develop

Requires Python 3.11.

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## Security scanning

CI runs `pip-audit` (dependencies), `osv-scanner` (SARIF) and `bandit` (code patterns) in the `security-scan` job. Reports are uploaded as artifacts, and the SARIF goes to GitHub code scanning.

## Licence

MIT
