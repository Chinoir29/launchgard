# Claim Ledger Template - ARCHI-Ω v1.2

## Purpose

The Claim Ledger tracks all important claims (assertions that change decisions, costs, risks, or architecture) to ensure:
1. Every claim has a clear origin tag ([USER] [DED] [HYP] [UNKNOWN])
2. Every claim has appropriate proof level (S0-S4)
3. Every claim has testability level (T0-T3)
4. Every claim's dependencies are tracked
5. Every claim has a test and status

## Ledger Format

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status |
|----------|------------|------------|---------|--------------|------|--------|
| C001 | [Short claim description] | [USER/DED/HYP/UNKNOWN] | S0-S4 | [List of dependent claim IDs] | [Test description] | PASS/FAIL/UNKNOWN |

## Example Entries

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status |
|----------|------------|------------|---------|--------------|------|--------|
| C001 | System must handle 10K QPS | [USER] | S0 | - | Load test: 10K QPS sustained for 5 min | PASS |
| C002 | PostgreSQL can handle required write throughput | [DED] | S1 | C001 | Benchmark: 10K writes/sec on similar hardware | PASS |
| C003 | Using Redis for caching will reduce DB load by 70% | [HYP] | S1 | C001, C002 | A/B test: measure DB load reduction | UNKNOWN |
| C004 | Latest version of library X fixes security issue | [UNKNOWN] | S0 | - | Verify: Check CVE database + release notes | UNKNOWN |
| C005 | AWS Lambda costs will be under $500/month | [DED] | S1 | C001 | Calculate: (10K QPS × avg duration × price) × safety margin | PASS |

## Claim Origin Tags

- **[USER]**: Information directly provided by the user
- **[DED]**: Deduced from available information through reasoning
- **[HYP]**: Hypothesis that needs testing/verification
- **[UNKNOWN]**: Information not available, requires external verification

## Proof Levels (S-Levels)

- **S0**: données user (User-provided data)
- **S1**: raisonnement/calcul (Reasoning/calculation)
- **S2**: outils/sources (Tools/external sources)
- **S3**: tests reproductibles (Reproducible tests)
- **S4**: recoupement indépendant (Independent cross-checking, ≥2 sources/methods)

## Testability Levels (TRACE)

- **T0**: Non testable (avoid)
- **T1**: Test implicite / observation vague
- **T2**: Test explicite PASS/FAIL (minimum for strong causality)
- **T3**: Test reproductible + metric + threshold + procedure (preferred for R2)

## Usage Guidelines

### Adding a Claim

1. Assign a unique Claim-ID (sequential: C001, C002, etc.)
2. Write a concise claim text (one sentence)
3. Tag the origin appropriately
4. Determine proof level based on available evidence
5. List all claim dependencies (other claims it relies on)
6. Define a specific test (PASS/FAIL criteria)
7. Set initial status (usually UNKNOWN until tested)

### Updating Claim Status

- **PASS**: Test executed successfully, claim verified
- **FAIL**: Test executed, claim disproven or criteria not met
- **UNKNOWN**: Not yet tested or awaiting verification

### Important Claims Requiring Ledger Entry

Claims that should be tracked:
- Performance requirements and capacity claims
- Security assertions
- Cost estimates
- Technology selection rationale
- Causal relationships ("X will cause Y")
- Compliance requirements
- Data handling claims
- Integration assumptions

### Validation Rules

1. **No [USER] claims without source**: User claims must reference where user provided this
2. **[HYP] requires test**: Every hypothesis must have a defined test
3. **[UNKNOWN] triggers protocol**: Unknown information triggers TERM-PROTOCOLE if critical
4. **Strong causality needs ≥T2**: If claim states "X causes Y", testability must be ≥T2
5. **R2 claims need ≥S2**: High-impact risk claims require proof level ≥S2

## Claim Ledger Review Checklist

- [ ] All important claims have unique IDs
- [ ] All claims have origin tags
- [ ] All claims have proof levels
- [ ] All dependencies are mapped
- [ ] All claims have defined tests
- [ ] All [HYP] claims have verification plans
- [ ] All [UNKNOWN] claims are documented for follow-up
- [ ] No [DED] claims without clear reasoning chain
- [ ] Strong causal claims have TRACE ≥ T2

## Template for New Claim Ledger

```markdown
# Claim Ledger - [Project Name]

**Date:** YYYY-MM-DD
**Version:** 1.0
**Risk Classification:** R0 / R1 / R2 / R3

## Claims

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status |
|----------|------------|------------|---------|--------------|------|--------|
| C001 | | | | | | |
| C002 | | | | | | |
| C003 | | | | | | |

## Summary Statistics

- Total Claims: 
- PASS: 
- FAIL: 
- UNKNOWN: 
- By Origin: [USER]: X, [DED]: Y, [HYP]: Z, [UNKNOWN]: W
- By S-Level: S0: X, S1: Y, S2: Z, S3: W, S4: V

## Critical Open Items

[List any critical UNKNOWN or FAIL claims that need attention]

## Next Steps

1. 
2. 
3. 
```

---

**Note**: The Claim Ledger is a mandatory component of ANNEXE A in the final deliverable (Section 11 of output format).
