# LaunchGuard RUNBOOK

Operational guide for using LaunchGuard and understanding termination states.

## Quick Start

```bash
# Light mode (default): secrets + overpromises only
launchgard README.md

# Max mode: all rules including recency and claim tagging
launchgard --mode max "**/*.md"

# With baseline (incremental adoption)
launchgard --baseline .launchgard-baseline.json "**/*.md"

# Create baseline
launchgard --create-baseline .launchgard-baseline.json "**/*.md"
```

## Exit Codes

| Code | Status | Meaning | Action |
|------|--------|---------|--------|
| **0** | PASS | No errors detected | Proceed with confidence |
| **1** | FAIL | Errors found | Fix violations before proceeding |
| **2** | ERROR | Exception/crash | Check logs, fix configuration |

## Termination States (ARCHI-Ω v1.2)

### TERM-LIVRÉ (Delivered)

**Status**: ✅ Complete

**Meaning**: Scan completed successfully with actionable results.

**Report Includes**:
- Full violation list with risk classification
- Complete claim ledger with proof levels
- Sensitivity map showing critical factors
- Risk distribution summary

**Next Actions**:
1. Review all R2 (high-risk) violations first
2. Address R1 (operational) violations
3. Consider R0 (low-risk) items for cleanup
4. Update documentation based on claim ledger feedback

---

### TERM-PARTIEL (Partial)

**Status**: ⚠️ Partial Delivery

**Meaning**: Scan completed but with limitations (e.g., missing baseline, limited file access).

**Common Causes**:
- Baseline file not found but referenced
- Some files inaccessible
- Incomplete rule configuration

**Next Actions**:
1. **Provide**: Missing resources (baseline file, access to files)
2. **Verify**: Re-run scan with complete inputs
3. **Decide**: Accept partial results or wait for complete scan

**Example**:
```bash
# If baseline missing, create one:
launchgard --create-baseline .launchgard-baseline.json "**/*.md"

# Then re-run with baseline:
launchgard --baseline .launchgard-baseline.json "**/*.md"
```

---

### TERM-PROTOCOLE (Protocol Needed)

**Status**: ❓ Information Required

**Meaning**: Critical information missing; cannot complete assessment without user input.

**Common Scenarios**:
- Custom rules needed for specific domain
- Ambiguous claim tags requiring clarification
- Unknown file formats or structures

**PROTOCOL Actions**:

#### 1. Provide Missing Information
Answer these P0 (critical) questions:
- What file patterns should be scanned?
- Which scan mode is appropriate (light/max)?
- Are there existing violations to baseline?
- What custom rules are needed?

#### 2. Verify Assumptions
Test these minimal hypotheses:
- **H1**: Standard Markdown/YAML files use UTF-8 encoding
- **H2**: Claim tags follow [TAG] format
- **H3**: Secrets are accidental, not intentional examples

#### 3. Execute S3 Tests
Run these reproducible tests:
```bash
# Test 1: Verify file accessibility
find . -name "*.md" -type f | head -5

# Test 2: Check encoding
file -i README.md

# Test 3: Validate claim tag format
grep -E "\[(USER|DED|HYP|UNKNOWN)\]" README.md
```

#### 4. Decide Next Step
- ✅ Accept default configuration and re-run
- 🔄 Provide custom rules and re-run
- ⏸️ Defer scan until information available

---

### TERM-REFUS (Refused)

**Status**: 🛑 Cannot Proceed

**Meaning**: Request violates policy or contains R3 (critical) violations.

**Common Causes**:
- Instruction to disable critical security checks
- Request to ignore R3 violations
- Contradiction with ARCHI-Ω authority

**REFUSAL Reasons**:

#### R3 Violation Examples
- Intentionally leaving secrets exposed
- Bypassing security checks
- Fabricating verification results

#### Policy Conflicts
- Disable fail-closed behavior
- Skip mandatory claim tagging
- Ignore overpromises for marketing

**Resolution Path**:

1. **Review**: Understand the policy conflict
   ```
   Why was this refused?
   - [X] R3 violation (critical security/legal risk)
   - [ ] Policy conflict (contradicts ARCHI-Ω)
   - [ ] Invalid request (nonsensical configuration)
   ```

2. **Mitigate**: Adjust requirements
   - Remove R3 violations from scope
   - Align with policy requirements
   - Use appropriate risk mitigation

3. **Escalate**: If mitigation impossible
   - Document the constraint
   - Escalate decision to stakeholder
   - Consider alternative approaches

**Example Resolution**:
```yaml
# ❌ REFUSED: Disable secret detection
mode: light
disable-rules: [SEC-*]  # REJECTED - R3 violation

# ✅ ACCEPTED: Use baseline for migration
mode: light
baseline: .launchgard-baseline.json  # Grandfathers existing issues
```

---

## Risk-Based Workflow

### R2 Violations (High Priority)

**Immediate Actions Required**

```bash
# 1. Run scan
launchgard --mode light README.md

# 2. Filter R2 violations from report
jq '.violations[] | select(.riskClass == "R2")' report.json

# 3. Address each R2 violation:
# - Secrets: Remove or redact immediately
# - Legal claims: Add sources or remove
# - Security promises: Validate or soften claims

# 4. Verify fixes
launchgard README.md
```

**Test Criteria**:
- FAIL: Any R2 violations remain
- PASS: Zero R2 violations detected

---

### R1 Violations (Medium Priority)

**Address Before Production**

```bash
# 1. Identify R1 violations
jq '.violations[] | select(.riskClass == "R1")' report.json

# 2. Common R1 fixes:
# - Overpromises: Soften language ("designed to" instead of "guaranteed")
# - Recency: Add dates and sources
# - Claim tagging: Add [DED], [HYP], or [USER] tags

# 3. Validate improvements
launchgard --mode max README.md
```

---

### R0 Violations (Low Priority)

**Address During Cleanup**

```bash
# 1. Review R0 items
jq '.violations[] | select(.riskClass == "R0")' report.json

# 2. Common R0 improvements:
# - Add claim tags for consistency
# - Improve documentation clarity
# - Enhance claim ledger completeness

# 3. Optional: Create baseline to defer
launchgard --create-baseline .launchgard-baseline.json "**/*.md"
```

---

## Sensitivity Map Usage

The sensitivity map shows the top 5 factors that would change scan results.

### Interpreting Factors

#### Example: Scan Mode
```
Factor: Scan Mode
Impact: Switching to max mode would check recency triggers and claim tagging
Test: PASS if mode=max detects more violations
```

**Action**: Decide if max mode is appropriate:
- ✅ Use max mode for: New documentation, public-facing content
- ⚠️ Use light mode for: Quick checks, CI/CD pipelines

#### Example: Exposed Secrets
```
Factor: Exposed Secrets
Impact: 2 secret(s) detected - high security risk
Test: FAIL if any secrets detected; PASS if all removed
```

**Action**: Immediate remediation required (R2 violation)

#### Example: Baseline
```
Factor: Baseline File
Impact: Using a baseline would ignore existing violations
Test: PASS if baseline filters out grandfathered violations
```

**Action**: Decide migration strategy:
- Incremental: Create baseline, fix new issues first
- Complete: Fix all issues without baseline

---

## Claim Ledger Interpretation

### Status Indicators

| Icon | Status | Meaning | Action |
|------|--------|---------|--------|
| ✅ | PASS | Claim adequately supported | Verify proof level is appropriate |
| ❌ | FAIL | Claim lacks required support | Add sources or soften claim |
| ❓ | UNKNOWN | Status unclear | Add claim tag and/or sources |

### Proof Level Guide

| Level | Requirements | When to Use |
|-------|--------------|-------------|
| **S0** | User-provided data | User feedback, testimonials |
| **S1** | Logical deduction | Architecture decisions, technical specs |
| **S2** | External source | Third-party tools, references |
| **S3** | Testable | Performance metrics, security features |
| **S4** | Cross-checked | Critical claims, compliance statements |

### Testability Guide

| Level | Requirements | Example |
|-------|--------------|---------|
| **T0** | Avoid - untestable | "Best solution" (subjective) |
| **T1** | Implicit | "Users report faster performance" |
| **T2** | Explicit PASS/FAIL | "Encrypts data at rest" (verifiable) |
| **T3** | Reproducible with metrics | "Reduces latency by 50%" (measurable) |

---

## Baseline Management

### Creating a Baseline

```bash
# Scan and capture current state
launchgard --create-baseline .launchgard-baseline.json "**/*.md"

# Review baseline contents
jq '.violations | length' .launchgard-baseline.json
# Output: 15 (violations captured)
```

### Using a Baseline

```bash
# Only NEW violations will fail
launchgard --baseline .launchgard-baseline.json "**/*.md"

# Expected: PASS (existing issues ignored)
```

### Updating a Baseline

```bash
# 1. Fix some violations
# 2. Regenerate baseline
launchgard --create-baseline .launchgard-baseline.json "**/*.md"

# 3. Verify improvement
jq '.violations | length' .launchgard-baseline.json
# Output: 10 (5 violations fixed)
```

### Baseline Expiry

**Recommendation**: Review baselines quarterly

```bash
# Check baseline age
stat -c %y .launchgard-baseline.json

# If > 3 months old, review and update:
launchgard --create-baseline .launchgard-baseline-new.json "**/*.md"
diff <(jq '.violations | length' .launchgard-baseline.json) \
     <(jq '.violations | length' .launchgard-baseline-new.json)
```

---

## Troubleshooting

### Exit Code 2 (ERROR)

**Symptoms**: Scan crashes or fails to complete

**Common Causes**:
1. Invalid YAML in rules file
2. Corrupted baseline JSON
3. Inaccessible files
4. Memory limit exceeded (too many files)

**Solutions**:
```bash
# 1. Validate rules file
yamllint rules/base.yml

# 2. Validate baseline JSON
jq empty .launchgard-baseline.json

# 3. Check file permissions
ls -la *.md

# 4. Reduce file count
launchgard README.md  # Test single file first
```

### False Positives

**Problem**: Valid content flagged as violation

**Solutions**:

#### Option 1: Use Baseline
```bash
# Grandfather specific violations
launchgard --create-baseline .launchgard-baseline.json file.md
```

#### Option 2: Adjust Content
```markdown
<!-- Before -->
This is guaranteed to work.

<!-- After -->
[DED] This is designed to work based on architectural constraints.
```

#### Option 3: Custom Rules (Advanced)
```yaml
# Disable specific pattern in rules/base.yml
patterns:
  # - 'guaranteed'  # Commented out
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: LaunchGuard Check

on: [pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Chinoir29/launchgard@v0.1.0
        with:
          mode: 'light'
          files: '**/*.md'
          baseline: '.launchgard-baseline.json'
```

### Pre-commit Hook

```bash
# .husky/pre-commit
launchgard --mode light $(git diff --cached --name-only | grep -E '\.(md|yml)$')
```

---

## Support

For questions or issues:
1. Check [ARCHI-OMEGA-v1.2.md](./ARCHI-OMEGA-v1.2.md) for methodology
2. Review [METHODOLOGY.md](./METHODOLOGY.md) for principles
3. See [examples/](./examples/) for usage patterns
4. Open issue on GitHub

---

*LaunchGuard RUNBOOK - ARCHI-Ω v1.2 Compliant*
