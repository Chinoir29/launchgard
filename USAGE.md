# ARCHI-Ω v1.2 - Usage Guide

This guide explains how to use the ARCHI-Ω v1.2 framework.

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/Chinoir29/launchgard.git
cd launchgard

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Using pip (when published)

```bash
pip install archi-omega
```

## Quick Start

### 1. Using the CLI

The simplest way to use ARCHI-Ω is through the command-line interface:

```bash
# Run with a YAML input file
archi-omega examples/sample-input.yaml

# Specify a custom config file
archi-omega input.yaml -c my-config.yaml

# Save output to file
archi-omega input.yaml -o output.md

# Output in different formats
archi-omega input.yaml --format yaml
archi-omega input.yaml --format json
```

### 2. Using the Python API

```python
from archi_omega import Pipeline, ProjectContext
from archi_omega.epistemic.foundation import OriginTag, ProofLevel, Claim

# Create a project context
context = ProjectContext()
context.goal = "Build a REST API for task management"
context.deliverable = "Architecture document"
context.users_load = {
    "users": 1000,
    "qps_average": 50,
    "qps_peak": 200
}
context.constraints = {
    "budget": "$500/month",
    "timeline": "3 months"
}

# Add claims to the ledger
claim = Claim(
    claim_id="C001",
    text="System will handle 200 QPS at peak",
    origin_tag=OriginTag.USER,
    proof_level=ProofLevel.S0,
    dependencies=[],
    test_description="Load test: 200 QPS for 5 minutes",
    status="UNKNOWN"
)
context.claim_ledger.add_claim(claim)

# Execute the pipeline
pipeline = Pipeline()
deliverable = pipeline.execute(context)

# Access results
print(f"Risk Class: {context.risk_class}")
print(f"Termination: {deliverable['termination']}")
print(f"Recommendation: {deliverable['recommendation']}")
```

## Input Format

Create a YAML file with your project requirements:

```yaml
GOAL: "Your business objective and expected value"

DELIVERABLE: "What you need (architecture doc, implementation plan, etc.)"

USERS_LOAD:
  users: 1000
  qps_average: 50
  qps_peak: 200
  latency: "<200ms p95"

SLA_SLO:
  availability: "99.5%"
  latency: "p95 < 200ms"

DATA:
  types: "User data, transactions, etc."
  sensitivity: "Internal/Confidential/Restricted"
  retention: "2 years"

CONSTRAINTS:
  budget: "$500/month"
  timeline: "3 months"
  stack: "Preferred tech stack"
  cloud: "AWS/Azure/GCP"

INTEGRATIONS:
  - "SSO"
  - "Payment gateway"

OPS:
  ci_cd: "GitHub Actions"
  monitoring: "CloudWatch"

SECURITY:
  threats: "List of security concerns"
  requirements: "Compliance requirements"

DONE:
  pass:
    - "Criterion 1: measurable pass condition"
    - "Criterion 2: measurable pass condition"
  fail:
    - "Criterion 1: measurable fail condition"
```

See [examples/sample-input.yaml](examples/sample-input.yaml) for a complete example.

## Configuration

Customize the framework behavior with a config file:

```yaml
# archi-omega-config.yaml
mode: MAXCAP          # MAXCAP | MAX | LIGHT | PROJET
budget: long          # court | moyen | long
evidence: mid         # low | mid | high
divergence: mid       # low (1-2 options) | mid (2-3) | high (3+)
auto_gov: ON          # ON | OFF
auto_tools: ON        # ON | OFF
pcx: ON               # Proof cross-check ON | OFF
nest: ON              # Nested verification ON | OFF
```

## Core Concepts

### Proof Levels (S0-S4)

- **S0**: User-provided data
- **S1**: Reasoning/calculation
- **S2**: Tools/external sources
- **S3**: Reproducible tests
- **S4**: Independent cross-checking (≥2 sources)

### Risk Classes (R0-R3)

- **R0**: Low risk
- **R1**: Operational, low impact
- **R2**: High impact (finance/legal/security/health)
- **R3**: Illegal/dangerous → STOP

### Origin Tags

Every claim must be tagged:
- **[USER]**: User-provided information
- **[DED]**: Deduced from available information
- **[HYP]**: Hypothesis - needs testing
- **[UNKNOWN]**: Unknown - requires verification

### Testability Levels (T0-T3)

- **T0**: Not testable (avoid)
- **T1**: Implicit test / vague observation
- **T2**: Explicit PASS/FAIL (minimum for strong causality)
- **T3**: Reproducible + metric + threshold + procedure

## Pipeline Stages

The framework executes these stages in order:

1. **COMPILER**: Determine risk class, proof budget, active modules
2. **EXPAND**: Extract facts, constraints, unknowns, claims
3. **BRANCH**: Generate 2-3 alternative options
4. **LINT**: Verify invariants, origin tags, testability
5. **STRESS**: Test for contradictions, missing proofs, security risks
6. **SELECT**: Choose most robust option + fallback
7. **COMMIT**: Produce final deliverable with termination code

## Working with Claims

### Creating Claims

```python
from archi_omega.epistemic.foundation import (
    Claim, OriginTag, ProofLevel, TestabilityLevel
)

claim = Claim(
    claim_id="C001",
    text="Using Redis cache will reduce DB load by 70%",
    origin_tag=OriginTag.HYP,  # Hypothesis
    proof_level=ProofLevel.S1,  # Reasoning
    dependencies=["C002"],  # Depends on other claims
    test_description="A/B test: measure DB load with/without cache",
    status="UNKNOWN",
    testability=TestabilityLevel.T3  # Reproducible test
)

# Validate strong causality
if not claim.validate_strong_causality():
    print("Warning: Strong causality claim needs T2+ testability")
```

### Managing Claim Ledgers

```python
from archi_omega.epistemic.foundation import ClaimLedger, RiskClass

ledger = ClaimLedger()
ledger.add_claim(claim)

# Validate all claims
validation = ledger.validate_all(RiskClass.R2)
if not validation["valid"]:
    print("Issues:", validation["issues"])

# Get statistics
stats = ledger.get_statistics()
print(f"Total claims: {stats['total_claims']}")
print(f"By status: {stats['by_status']}")

# Export to markdown
markdown = ledger.to_markdown_table()
print(markdown)
```

## Risk Classification

```python
from archi_omega.epistemic.foundation import RiskClassifier, RiskClass

risk = RiskClassifier.classify(
    has_financial_impact=True,
    has_legal_impact=True,
    has_security_impact=True,
    has_health_impact=False,
    has_pii=True,
    is_illegal=False,
    is_dangerous=False
)

print(f"Risk Class: {risk}")  # R2 (high impact)
```

## Proof Budget

```python
from archi_omega.epistemic.foundation import ProofBudget, RiskClass

# Get proof budget for risk class
pb = ProofBudget.for_risk_class(RiskClass.R2)

print(f"Required levels: {pb.required_levels}")
print(f"Minimum pillars: {pb.minimum_pillars}")
print(f"Requires alternatives: {pb.requires_alternatives}")
```

## Examples

See the [examples](examples/) directory for:

- [simple-web-api-example.md](examples/simple-web-api-example.md) - Complete walkthrough
- [sample-input.yaml](examples/sample-input.yaml) - Sample input file

## Templates

Use the templates to structure your work:

- [User Input Template](templates/user-input-template.md)
- [ADR Template](templates/adr-template.md)
- [Claim Ledger Template](templates/claim-ledger-template.md)
- [Output Format Template](templates/output-format-template.md)

## Testing

Run the test suite:

```bash
# Run all tests
python tests/test_epistemic.py

# Run with pytest (if installed)
pytest tests/
```

## Invariants (Global Rules)

The framework enforces these invariants:

1. **Zero fabrication**: No invention of facts or sources
2. **Zero ghost tools**: Don't claim verification without capability
3. **Zero overpromise**: No guarantees or "100%" claims
4. **Mandatory origin**: Every claim must be tagged
5. **Fail-closed**: When in doubt, degrade or ask, don't guess
6. **Testability**: Strong causality requires ≥T2 tests
7. **Data hygiene**: No secrets or PII in code/docs

## Termination Codes

Every deliverable ends with a termination code:

- **TERM-LIVRÉ**: Complete deliverable provided
- **TERM-PARTIEL**: Partial - critical constraint missing
- **TERM-PROTOCOLE**: P0 questions + minimal assumptions needed
- **TERM-REFUS**: Refused - illegal/dangerous (R3)

## Best Practices

### 1. Start with Complete Input

Fill out all sections of the user input template. Missing critical info triggers TERM-PROTOCOLE.

### 2. Tag All Claims

Always tag claims with origin:
- `[USER]` for user-provided facts
- `[DED]` for deduced information
- `[HYP]` for assumptions that need testing
- `[UNKNOWN]` when information is not available

### 3. Define Tests

For every important claim, define:
- What metric to measure
- What threshold = PASS
- How to reproduce the test

### 4. Validate Strong Causality

If claiming "X will cause Y", ensure:
- Testability level ≥ T2 (explicit PASS/FAIL)
- Proof level appropriate for risk (S2+ for R2)
- Test is defined and reproducible

### 5. Use Claim Ledger

Maintain a claim ledger for:
- Tracking all important assertions
- Managing dependencies between claims
- Validating proof adequacy
- Reporting test status

### 6. Sensitivity Analysis

Always include a sensitivity map showing:
- What information could change recommendation
- Threshold values for change
- Tests to verify sensitivity

## Troubleshooting

### "No module named 'archi_omega'"

Set PYTHONPATH or install the package:
```bash
export PYTHONPATH=/path/to/launchgard/src
# or
pip install -e .
```

### "Risk classification R3 (TERM-REFUS)"

Your project involves illegal or dangerous activities. Framework refuses to proceed. Review your requirements.

### "TERM-PROTOCOLE termination"

Critical information is missing. Check the output for:
- Open questions (P0)
- What information to provide
- What to verify
- What decisions to make

### "Proof level inadequate for risk"

For R2 (high-impact) projects:
- Use proof levels ≥ S2 (tools/sources)
- Provide ≥2 independent sources (S4)
- Define reproducible tests (T3)

## Support

- **Documentation**: See [ARCHI-OMEGA-v1.2.md](ARCHI-OMEGA-v1.2.md) for complete framework
- **Issues**: Report bugs or request features on GitHub
- **Examples**: Check [examples/](examples/) directory

## License

[To be determined]

---

**Version**: ARCHI-Ω v1.2  
**Last Updated**: 2026-02-18
