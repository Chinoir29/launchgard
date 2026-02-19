# launchgard

Deterministic quality gate for product docs, prompts, and repos. Enforces claim tagging ([USER]/[HYP]/[DED]/[UNKNOWN]), blocks overpromises, flags recency, detects secrets, and generates PASS/FAIL reports via CLI + GitHub Action.

## 🟥🟩 ARCHI-Ω v1.2 Framework

This repository now includes **ARCHI-Ω v1.2**, a comprehensive architectural framework with:

- **Fail-closed authority** and context firewall (anti-injection)
- **Proof-level system** (S0-S4) with mandatory origin tagging
- **Risk classification** (R0-R3) with proof budgets
- **Execution pipeline**: COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT
- **Auto-governance** and auto-tools routing
- **Testability levels** (T0-T3) for claim verification
- **Structured deliverables** with mandatory sections

### Key Features

- ✅ **Zero fabrication**: No invention of facts, sources, or recency assumptions
- ✅ **Origin tagging**: Every claim tagged [USER]/[DED]/[HYP]/[UNKNOWN]
- ✅ **Proof budgets**: Risk-based evidence requirements (S0-S4)
- ✅ **Testability**: All strong causality claims require TRACE ≥ T2
- ✅ **Security**: Data hygiene, secrets management, PII protection
- ✅ **Fail-closed**: Unknown critical info triggers TERM-PROTOCOLE
- ✅ **Claim ledger**: Track all important assertions with tests and status

### Quick Start

1. **Use the framework**: See [ARCHI-OMEGA-v1.2.md](./ARCHI-OMEGA-v1.2.md) for complete framework
2. **Fill user input**: Use [templates/user-input-template.md](./templates/user-input-template.md)
3. **Review example**: Check [examples/simple-web-api-example.md](./examples/simple-web-api-example.md)
4. **Generate output**: Follow [templates/output-format-template.md](./templates/output-format-template.md)

### Validation

**Local validation (3 commands):**
```bash
python scripts/archi_omega_lint.py  # Fail-closed validation
python tests/test_epistemic.py       # Unit tests
python verify.py                     # Framework verification
```

See [VALIDATION.md](./VALIDATION.md) for detailed validation guide.

**CI/CD:** GitHub Actions automatically runs all validation checks on push.

### Configuration


Default configuration in [archi-omega-config.yaml](./archi-omega-config.yaml):

```yaml
mode: MAXCAP
evidence: mid
auto_gov: ON
auto_tools: ON
pcx: ON  # Proof cross-check
nest: ON  # Nested verification
```

### Templates

- **User Input**: [templates/user-input-template.md](./templates/user-input-template.md)
- **ADR**: [templates/adr-template.md](./templates/adr-template.md)
- **Claim Ledger**: [templates/claim-ledger-template.md](./templates/claim-ledger-template.md)
- **Output Format**: [templates/output-format-template.md](./templates/output-format-template.md)

### Framework Principles

1. **SAFETY > TRUTH > ROBUSTNESS > OPS > STYLE**
2. **Fail-closed**: When in doubt, don't conclude; degrade, test, or ask
3. **No ghost tools**: Don't claim verification without explicit capability
4. **Mandatory proof**: Claims need appropriate evidence level (S0-S4)
5. **Testability**: Strong causality requires explicit tests (≥T2)

### Risk Classes & Proof Budgets

| Risk | Type | Proof Budget |
|------|------|--------------|
| R0 | Low | S1 (reasoning) |
| R1 | Operational, low impact | S0/S1 + S2 if unstable |
| R2 | High impact (finance/legal/security) | ≥2 independent pillars (S2/S4) |
| R3 | Illegal/dangerous | STOP or strict framework |

### Execution Pipeline

```
COMPILER  → Determine risk, proof budget, active modules
  ↓
EXPAND    → Extract facts, constraints, unknowns, claims
  ↓
BRANCH    → Generate 3 internal + 2-3 external options
  ↓
LINT      → Verify invariants, tags, recency, testability
  ↓
STRESS    → Test for contradictions, missing proofs, security
  ↓
SELECT    → Choose most robust option + fallback
  ↓
COMMIT    → Produce deliverable + TERM status
```

### Output Format

Every deliverable includes (in order):

0. FACTS [USER]
1. OPEN QUESTIONS (P0→P2)
2. ASSUMPTIONS [HYP]
3. OPTIONS + SCORES
4. RECOMMANDATION + SENSITIVITY MAP
5. ARCHITECTURE CIBLE
6. SÉCURITÉ & CONFORMITÉ
7. IA/ML (if applicable)
8. ADR (Decision Records)
9. PLAN DE VÉRIFICATION + R-SUITE
10. RISKS REGISTER
11. RAPPORT DE REVUE + CLAIM LEDGER
12. PROCHAIN PAS + TERM + RUNBOOK

### Examples

- [Simple Web API](./examples/simple-web-api-example.md) - Complete walkthrough

### Limitations & Scope

**What the framework does:**
- Enforces structured reasoning with proof levels and origin tagging
- Validates claims against risk-based proof budgets
- Provides templates and pipelines for architectural analysis
- Prevents fabrication through fail-closed validation

**What the framework does not do:**
- Does not make architectural decisions for you (provides structure for your decisions)
- Does not replace domain expertise or professional judgment
- Does not access external APIs or real-time data automatically
- Does not provide legal, financial, or medical advice
- Cannot verify claims beyond the tools and sources you provide
- Does not eliminate all risks (reduces them through systematic validation)

**Known limitations:**
- Requires manual input of project requirements
- Option scoring requires domain knowledge to calibrate
- External tool integration (pricing APIs, etc.) not included in base implementation
- Pipeline assumes human review of generated options
- Does not enforce ARCHI-Ω principles on external content automatically

### Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Security

For security issues, please see our [Security Policy](SECURITY.md).

### License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2026 launchgard

---

**Version**: ARCHI-Ω v1.2  
**Last Updated**: 2026-02-18
