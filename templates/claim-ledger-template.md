# Claim Ledger Template - ARCHI-Ω v1.3.0

## Purpose

The Claim Ledger tracks all important claims (assertions that change decisions, costs, risks, or architecture) to ensure:
1. Every claim has a clear origin tag ([USER] [DED] [HYP] [GAP])
2. Every claim has appropriate proof level (S0-S4)
3. Every claim has testability level (T0-T3)
4. Every claim's dependencies are tracked
5. Every claim has a test and status
6. **[NEW v1.3.0]** Every [GAP] claim has mandatory closure (DECISION+TEST+IMPACT+TERM)

## Ledger Format

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status | GAP Closure |
|----------|------------|------------|---------|--------------|------|--------|-------------|
| C001 | [Short claim description] | [USER/DED/HYP/GAP] | S0-S4 | [List of dependent claim IDs] | [Test description] | PASS/FAIL/À-CLÔTURER | [If GAP: DECISION+TEST+IMPACT] |

## Example Entries

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status | GAP Closure |
|----------|------------|------------|---------|--------------|------|--------|-------------|
| C001 | System must handle 10K QPS | [USER] | S0 | - | Load test: 10K QPS sustained for 5 min | PASS | - |
| C002 | PostgreSQL can handle required write throughput | [DED] | S1 | C001 | Benchmark: 10K writes/sec on similar hardware | PASS | - |
| C003 | Using Redis for caching will reduce DB load by 70% | [HYP] | S1 | C001, C002 | A/B test: measure DB load reduction | À-CLÔTURER | - |
| C004 | Exact AWS Lambda cost unknown | [GAP] | S1 | C001 | Conservative budget validation | À-CLÔTURER | DECISION: Budget 500$/mo (2x margin); TEST: Verify bill after 1mo; IMPACT: ±200$ depending on traffic |
| C005 | Current market leader for API gateway | [GAP] | S0 | - | Verify with market research | À-CLÔTURER | DECISION: Use AWS API Gateway (stable, well-supported); TEST: Re-evaluate in 6mo; IMPACT: Vendor lock-in risk |

## Claim Origin Tags (v1.3.0)

- **[USER]**: Information explicitly provided by the user in this chat
- **[DED]**: Deduced logically from [USER] information (explicit chain, no jumps)
- **[HYP]**: Hypothesis proposed (not proven) with impact/risk + test defined
- **[GAP]**: Information missing / unstable / not verifiable here and now
  - **MANDATORY**: Every [GAP] must have DECISION + TEST + IMPACT + TERM

### **[GAP] Closure Rule (v1.3.0)**

**A [GAP] can never be "the end"**. Every [GAP] MUST include:

1. **DECISION**: Conservative choice that minimizes impact/risk (without affirming the unstable fact)
2. **TEST**: PASS/FAIL closure test (how to verify/resolve)
3. **IMPACT**: Risk/cost/time impact if GAP not resolved
4. **TERM**: Termination code (usually TERM-PROTOCOLE if critical)

Example GAP Closure:
```
[GAP]: RGPD jurisdiction unclear (US vs EU?)
DECISION: Apply RGPD by default (more strict)
TEST: Ask client to confirm jurisdiction
IMPACT: +2 weeks dev if RGPD; +cost for EU hosting
TERM: TERM-PROTOCOLE (P0 blocker)
```

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

## Claim Status (v1.3.0)

- **PASS**: Test executed successfully, claim verified
- **FAIL**: Test executed, claim disproven or criteria not met
- **À-CLÔTURER**: Not yet closed - requires test execution or GAP resolution

*Note: "UNKNOWN" status removed in v1.3.0 - replaced with "À-CLÔTURER" (to be closed)*

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
3. Tag the origin appropriately (v1.3.0: use [GAP] instead of [UNKNOWN])
4. **If [GAP]**: Define DECISION + TEST + IMPACT + TERM (mandatory closure)
5. Determine proof level based on available evidence
6. List all claim dependencies (other claims it relies on)
7. Define a specific test (PASS/FAIL criteria)
8. Set initial status (usually À-CLÔTURER until tested)

### Updating Claim Status

- **PASS**: Test executed successfully, claim verified
- **FAIL**: Test executed, claim disproven or criteria not met
- **À-CLÔTURER**: Not yet closed - requires test execution or GAP resolution

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

### Validation Rules (v1.3.0)

1. **No [USER] claims without source**: User claims must reference where user provided this
2. **[HYP] requires test**: Every hypothesis must have a defined test
3. **[GAP] requires closure**: Every [GAP] must have DECISION+TEST+IMPACT+TERM (no naked GAPs!)
4. **[GAP] triggers protocol**: [GAP] information triggers TERM-PROTOCOLE if critical
5. **Strong causality needs ≥T2**: If claim states "X causes Y", testability must be ≥T2
6. **R2 claims need ≥S2**: High-impact risk claims require proof level ≥S2
7. **No "UNKNOWN" status**: Use "À-CLÔTURER" instead (v1.3.0)

## Claim Ledger Review Checklist (v1.3.0)

- [ ] All important claims have unique IDs
- [ ] All claims have origin tags
- [ ] All claims have proof levels
- [ ] All dependencies are mapped
- [ ] All claims have defined tests
- [ ] All [HYP] claims have verification plans
- [ ] **All [GAP] claims have complete closure (DECISION+TEST+IMPACT+TERM)**
- [ ] **No naked [GAP] without closure**
- [ ] No [DED] claims without clear reasoning chain
- [ ] Strong causal claims have TRACE ≥ T2
- [ ] No "UNKNOWN" status (use "À-CLÔTURER")

## Template for New Claim Ledger (v1.3.0)

```markdown
# Claim Ledger - [Project Name]

**Date:** YYYY-MM-DD
**Version:** 1.3.0
**Risk Classification:** R0 / R1 / R2 / R3
**Complexity Classification:** C0 / C1 / C2 / C3
**Profile:** P-SIMPLE / P-STANDARD / P-COMPLEX / P-PROJET

## Claims

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status | GAP Closure |
|----------|------------|------------|---------|--------------|------|--------|-------------|
| C001 | | | | | | | |
| C002 | | | | | | | |
| C003 | | | | | | | |

## Summary Statistics

- Total Claims: 
- PASS: 
- FAIL: 
- À-CLÔTURER: 
- By Origin: [USER]: X, [DED]: Y, [HYP]: Z, [GAP]: W
- By S-Level: S0: X, S1: Y, S2: Z, S3: W, S4: V
- GAPs with Closure: X / W
- GAPs without Closure: 0 (MUST BE ZERO!)

## Critical Open Items

[List any critical À-CLÔTURER or FAIL claims that need attention]

## GAP Summary (v1.3.0)

| GAP-ID | GAP Description | DECISION | TEST | IMPACT | TERM |
|--------|-----------------|----------|------|--------|------|
| [List all GAPs with their closures] |

## Next Steps

1. 
2. 
3. 
```

---

**Note**: The Claim Ledger is a mandatory component of Section 11 (RAPPORT DE REVUE + CLAIM LEDGER) in the final deliverable.
