# ARCHI-Ω v1.2 Methodology

This document explains the methodological principles behind LaunchGuard.

## Overview

ARCHI-Ω v1.2 is a documentation quality framework that emphasizes:

- Deterministic, repeatable quality gates
- Claim accountability and traceability
- Fail-closed approach to violations
- Evidence-based documentation

## Core Principles

### 1. Fail-Closed by Design

**Traditional "warnings" are often ignored.** LaunchGuard fails fast:

- Quality gates **block** violations by default
- Exit code 1 (fail) when errors detected
- Teams must fix issues, not accumulate tech debt
- Baseline support allows controlled migration

**Why fail-closed?**

- Prevents gradual quality degradation
- Makes quality non-negotiable
- Catches issues before production
- Creates accountability

### 2. No Overpromises

Absolutist claims create legal risk and damage credibility:

❌ **Bad:**

- "guaranteed to work"
- "unique in the world"
- "100% secure"
- "never fails"

✅ **Good:**

- "designed to provide..." [DED]
- "users report..." [USER]
- "we believe this may..." [HYP]

**Why avoid overpromises?**

- Reduces legal exposure
- Builds realistic expectations
- Improves credibility
- Prevents customer disappointment

### 3. Claim Ledger

Every factual claim must be:

- **Tagged** with [USER]/[DED]/[HYP]/[UNKNOWN]
- **Tracked** in the claim ledger
- **Sourced** if it contains recency/instability triggers

**Tag meanings:**

**[USER]** - User-reported claim

- Testimonials, feedback, survey results
- Example: "[USER] 85% of users report faster load times"

**[DED]** - Deduced claim

- Logically derived from technical facts
- Example: "[DED] Uses AES-256 encryption for data at rest"

**[HYP]** - Hypothesis claim

- Belief or theory, not yet proven
- Example: "[HYP] This approach may reduce latency by 30%"

**[UNKNOWN]** - Unknown veracity

- Claim source/status unclear
- Requires investigation
- Example: "[UNKNOWN] Industry standard practice"

**Why tag claims?**

- Creates accountability trail
- Enables claim audits
- Distinguishes facts from opinions
- Surfaces unsourced assertions

### 4. PASS/FAIL Tests (R-SUITE)

**R-SUITE** = Rules Suite for Uniform Integrity Testing & Enforcement

Each rule has:

- Binary pass/fail outcome
- No subjective interpretation
- Deterministic behavior
- Fixture-based tests

**Example rule structure:**

```yaml
- id: 'OVER-001'
  name: 'Absolute claims'
  description: 'Detects overpromising language'
  severity: 'error'
  patterns:
    - 'guaranteed'
    - 'unique in the world'
    - '100% secure'
```

**Why PASS/FAIL?**

- No ambiguity
- Automatable
- Regression-proof
- CI/CD friendly

### 5. No Web Fact-Checking

LaunchGuard **intentionally avoids** external APIs:

❌ Does not:

- Look up facts on Wikipedia
- Verify claims via APIs
- Check prices/dates externally

✅ Instead:

- Flags recency triggers as needing sources
- Requires teams to provide citations
- Remains deterministic and fast
- Avoids API dependencies

**Why no web checking?**

- Deterministic results (no API failures)
- Fast local execution
- No rate limits
- Offline-friendly
- Team retains responsibility

### 6. Recency/Instability Triggers

Certain content becomes outdated quickly:

**Recency triggers:**

- Years: 2024, 2025, 2026, 2027
- Temporal: latest, current, recent, newest

**Instability triggers:**

- Pricing: price, cost, $X
- Legal: law, regulation, compliance

**What happens?**

- In **max mode**: Flagged as warnings
- Team must either:
  - Add a [TAG] with source
  - Remove the claim
  - Baseline the violation

**Why flag recency?**

- Docs rot over time
- Prevents outdated claims
- Encourages maintenance
- Highlights volatile content

## Baseline Support

Baselines allow **controlled migration** to LaunchGuard:

### Creating a Baseline

```bash
# Scan and capture current violations
launchgard --create-baseline .launchgard-baseline.json "**/*.md"
```

This creates a JSON file with violation fingerprints.

### Using a Baseline

```bash
# Only NEW violations fail
launchgard --baseline .launchgard-baseline.json "**/*.md"
```

Baselined violations are **ignored**, allowing teams to:

- Adopt LaunchGuard incrementally
- Fix issues over time
- Prevent new violations
- Track progress

### Baseline Philosophy

Baselines are **temporary migration tools**:

- Not a permanent ignore list
- Should be reduced over time
- New code must be clean
- Legacy code gets fixed iteratively

## Implementation Patterns

### Pattern 1: Pre-commit Hook

```yaml
# .husky/pre-commit
launchgard --mode light $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|yml|yaml)$')
```

Blocks commits with new violations.

### Pattern 2: PR Check

```yaml
# .github/workflows/pr-check.yml
- uses: Chinoir29/launchgard@v0.1.0
  with:
    mode: 'max'
    files: '**/*.md'
```

Blocks PR merges with violations.

### Pattern 3: Nightly Audit

```yaml
# .github/workflows/nightly.yml
# Runs in max mode, reports to Slack
- run: launchgard --mode max "**/*.md" || true
- uses: slack-notify-action
  with:
    report: report.md
```

Monitors documentation health.

## Rationale: Why These Rules?

### Why block "guaranteed"?

- Creates legal liability
- Sets unrealistic expectations
- Damages trust when things fail
- Alternative: "designed to provide"

### Why flag years like "2026"?

- Content becomes outdated
- Requires maintenance
- May mislead users
- Alternative: Add "as of [date]" with source

### Why detect secrets?

- Prevents credential leaks
- Protects security
- Compliance requirement
- No false sense of security

### Why require claim tags?

- Creates audit trail
- Distinguishes fact from opinion
- Surfaces unsourced claims
- Improves documentation rigor

## Comparison to Other Tools

| Feature               | LaunchGuard | Linters | Vale    | Grammarly |
| --------------------- | ----------- | ------- | ------- | --------- |
| Claim tagging         | ✅          | ❌      | ❌      | ❌        |
| Overpromise detection | ✅          | ❌      | Partial | ❌        |
| Secret detection      | ✅          | ❌      | ❌      | ❌        |
| Deterministic output  | ✅          | ✅      | ✅      | ❌        |
| Fail-closed design    | ✅          | Partial | Partial | ❌        |
| Claim ledger          | ✅          | ❌      | ❌      | ❌        |
| Baseline support      | ✅          | Rare    | ❌      | ❌        |

## Limitations

LaunchGuard **does not**:

- Verify factual accuracy (no web lookups)
- Check grammar/spelling
- Analyze code quality
- Replace human review

LaunchGuard **does**:

- Enforce structural quality
- Detect patterns of risk
- Create accountability
- Provide deterministic gates

## Future Enhancements

Potential v2.0 features:

- Custom rule definitions
- Source citation validation
- Claim confidence scoring
- Integration with fact databases (opt-in)
- Multi-language support

## Conclusion

ARCHI-Ω v1.2 creates **accountable, measurable, fail-closed** documentation quality. LaunchGuard is a reference implementation demonstrating these principles in practice.

**Key takeaway:** Quality should be enforced, not suggested.

---

_For questions or feedback, open an issue on GitHub._
