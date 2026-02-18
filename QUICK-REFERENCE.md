# ARCHI-Ω v1.2.1 - Quick Reference

A one-page cheat sheet for the ARCHI-Ω framework.

## Priority Order

**SAFETY > TRUTH > ROBUSTNESS > OPS > STYLE**

## Proof Levels (S0-S4)

| Level | Name | Description |
|-------|------|-------------|
| S0 | données user | User-provided data |
| S1 | raisonnement/calcul | Reasoning/calculation |
| S2 | outils/sources | Tools/external sources |
| S3 | tests reproductibles | Reproducible tests |
| S4 | recoupement indépendant | Independent cross-check (≥2 sources) |

## Risk Classes (R0-R3)

| Risk | Type | Proof Budget |
|------|------|--------------|
| R0 | faible | S1 |
| R1 | opérationnel faible | S0/S1 + S2 if unstable |
| R2 | fort impact | ≥2 pillars (S2/S4) + alternatives |
| R3 | illégal/dangereux | STOP |

## Origin Tags

| Tag | Meaning | Use When |
|-----|---------|----------|
| [USER] | User-provided | Direct from user input |
| [DED] | Deduced | Derived from reasoning |
| [HYP] | Hypothesis | Assumption needing test |
| [GAP] | Information Gap | Requires: DECISION + TEST + TERM |

## Testability Levels (T0-T3)

| Level | Name | Required For |
|-------|------|--------------|
| T0 | non testable | Avoid |
| T1 | test implicite | Observation |
| T2 | test explicite PASS/FAIL | Strong causality (minimum) |
| T3 | test reproductible | R2 projects (preferred) |

## Pipeline Stages

```
COMPILER  → Risk, proof budget, modules, triggers
EXPAND    → Facts, constraints, unknowns, claims
BRANCH    → 2-3 alternative options
LINT      → Verify invariants, tags, testability
STRESS    → Test contradictions, proofs, security
SELECT    → Choose robust option + fallback
COMMIT    → Deliverable + termination code
```

## Termination Codes

| Code | Meaning |
|------|---------|
| TERM-LIVRÉ | Complete deliverable |
| TERM-PARTIEL | Partial - missing critical constraint |
| TERM-PROTOCOLE | P0 questions + minimal assumptions |
| TERM-REFUS | Refused - illegal/dangerous |

## Invariants (Must Follow)

1. ❌ Zero fabrication
2. ❌ Zero ghost tools
3. ❌ Zero overpromise ("guarantee", "100%")
4. ✅ Mandatory origin tags
5. ✅ Fail-closed (doubt → degrade/test/ask)
6. ✅ Strong causality needs ≥T2
7. ✅ No secrets/PII in code

## Configuration Defaults

```yaml
mode: MAXCAP
evidence: mid
auto_gov: ON
auto_tools: ON
pcx: ON
nest: ON
```

## CLI Commands

```bash
# Basic usage
archi-omega input.yaml

# With config
archi-omega input.yaml -c config.yaml

# Save to file
archi-omega input.yaml -o output.md

# Different formats
archi-omega input.yaml --format yaml
archi-omega input.yaml --format json
```

## Python Quick Start

```python
from archi_omega import Pipeline, ProjectContext
from archi_omega.epistemic.foundation import Claim, OriginTag, ProofLevel

# Create context
context = ProjectContext()
context.goal = "Your goal"
context.constraints = {"budget": "$500/month"}

# Add claim
claim = Claim(
    claim_id="C001",
    text="System handles 200 QPS",
    origin_tag=OriginTag.USER,
    proof_level=ProofLevel.S0,
    dependencies=[],
    test_description="Load test",
    status="À-CLÔTURER"
)
context.claim_ledger.add_claim(claim)

# Run pipeline
pipeline = Pipeline()
result = pipeline.execute(context)
```

## Output Structure (12 Sections)

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

## Score Matrix (0-5)

- Robustesse
- Sécurité/Conformité
- Simplicité
- Coût
- Performance
- Time-to-ship
- Opérabilité
- Évolutivité
- Risque IA

## Sensitivity Map (Mandatory)

5 items that would change recommendation:
- Information item
- Current assumption
- Threshold (PASS if X)
- Test method
- Impact if different

## Claim Validation Rules

- ✅ [USER] claims: must have source
- ✅ [HYP] claims: must have test
- ✅ [GAP] claims: must have DECISION + TEST + TERM
- ✅ [GAP] + critical → TERM-PROTOCOLE
- ✅ Strong causality → TRACE ≥ T2
- ✅ R2 claims → proof ≥ S2

## Auto-Tools Triggers

- **T-RECENCY**: "latest", prices, laws, versions → use S2 tool or [GAP] + TERM-PROTOCOLE
- **T-NICHE**: ≥10% error risk → use S2 tool or [GAP] + TERM-PROTOCOLE
- **T-R2**: High impact → aim for S2/S3

## Common Patterns

### Create Claim Ledger

```python
ledger = ClaimLedger()
ledger.add_claim(claim)
validation = ledger.validate_all(RiskClass.R2)
stats = ledger.get_statistics()
markdown = ledger.to_markdown_table()
```

### Classify Risk

```python
risk = RiskClassifier.classify(
    has_financial_impact=True,
    has_legal_impact=True,
    has_security_impact=True
)
# Returns: RiskClass.R2
```

### Check Proof Budget

```python
pb = ProofBudget.for_risk_class(RiskClass.R2)
# pb.minimum_pillars = 2
# pb.requires_alternatives = True
```

## Files & Templates

- **Framework**: `ARCHI-OMEGA-v1.2.md`
- **Config**: `archi-omega-config.yaml`
- **User Input**: `templates/user-input-template.md`
- **ADR**: `templates/adr-template.md`
- **Claim Ledger**: `templates/claim-ledger-template.md`
- **Output Format**: `templates/output-format-template.md`
- **Usage Guide**: `USAGE.md`

## Testing

```bash
# Run tests
python tests/test_epistemic.py

# With pytest
pytest tests/
```

---

**Version**: ARCHI-Ω v1.2.1  
**Repository**: https://github.com/Chinoir29/launchgard
