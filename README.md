# LaunchGuard

[![CI](https://github.com/Chinoir29/launchgard/actions/workflows/ci.yml/badge.svg)](https://github.com/Chinoir29/launchgard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ARCHI-Ω v1.2](https://img.shields.io/badge/ARCHI--Ω-v1.2-blue.svg)](./ARCHI-OMEGA-v1.2.md)

**Deterministic quality gate for product docs, prompts, and repos.** Implements ARCHI-Ω v1.2 methodology with proof levels (S0-S4), risk classification (R0-R3), claim ledger, and sensitivity analysis. Enforces claim tagging, blocks overpromises, flags recency triggers, detects secrets, and generates deterministic PASS/FAIL reports via CLI and GitHub Action.

## Quick Start

### Installation

```bash
npm install -g launchgard
```

### Basic Usage

```bash
# Scan a single file
launchgard README.md

# Scan all markdown files
launchgard "**/*.md"

# Use max mode (all rules)
launchgard --mode max "**/*.md"

# Create a baseline to ignore existing violations
launchgard --create-baseline .launchgard-baseline.json "**/*.md"

# Scan with baseline
launchgard --baseline .launchgard-baseline.json "**/*.md"
```

### GitHub Action

```yaml
name: LaunchGuard

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Chinoir29/launchgard@v0.1.0
        with:
          mode: 'light'
          files: '**/*.md **/*.yml'
```

## Features

### 🏷️ Claim Tagging

Enforces that factual claims are tagged with one of:

- **[USER]** - User-reported claim (testimonial, feedback)
- **[DED]** - Deduced claim (logically derived from facts)
- **[HYP]** - Hypothesis claim (believed but not proven)
- **[UNKNOWN]** - Claim with unknown veracity

### 🚫 Overpromise Detection

Blocks absolutist language that overpromises:

- "guaranteed", "unique in the world", "revolutionary"
- "100% secure", "never fails", "always works"
- "perfectly", "best in class", "game-changing"

### ⚠️ Recency/Instability Triggers

Flags content that may become outdated:

- Years (2024, 2025, 2026, 2027)
- Temporal words (latest, current, recent, newest)
- Volatile data (price, cost, law, legal, regulation)

### 🔒 Secret Detection

Detects exposed credentials:

- GitHub tokens (ghp*, gho*, ghu*, ghs*, ghr\_)
- OpenAI API keys (sk-, sk-proj-)
- AWS access keys (AKIA...)
- Generic API keys and passwords

### 📊 Deterministic Reports

Generates consistent, sortable output:

- **report.json** - Machine-readable JSON report
- **report.md** - Human-readable Markdown report
- Claim ledger tracking all tagged claims

### 🎯 Scan Modes

**Light Mode** (default)

- Checks: Secrets + Overpromises
- Fast, focused on critical violations
- Exit code 1 only for errors

**Max Mode**

- Checks: Secrets + Overpromises + Recency + Claim Tagging
- Comprehensive scanning
- Warnings for missing sources and claim tags

### 🛡️ Baseline Support

Create a baseline to grandfather in existing violations:

```bash
# Create baseline
launchgard --create-baseline .launchgard-baseline.json "**/*.md"

# Scan with baseline (only new violations fail)
launchgard --baseline .launchgard-baseline.json "**/*.md"
```

## Methodology: ARCHI-Ω v1.2

LaunchGuard implements the ARCHI-Ω v1.2 methodology for documentation quality. See [ARCHI-OMEGA-v1.2.md](./ARCHI-OMEGA-v1.2.md) for complete specification.

### Key Enhancements in v1.2

#### 📊 Proof Levels (S0-S4)

Every claim tracked with epistemic foundation:

- **S0**: User data (testimonials, feedback)
- **S1**: Reasoning/calculation (deductions)
- **S2**: External sources (tool verification)
- **S3**: Reproducible tests (PASS/FAIL criteria)
- **S4**: Cross-checked (≥2 independent sources)

#### ⚠️ Risk Classification (R0-R3)

Violations categorized by impact:

- **R0**: Low (informational, style)
- **R1**: Operational (overpromises, recency)
- **R2**: High impact (security, finance, legal)
- **R3**: Critical (requires STOP)

#### 🧪 Testability Levels (T0-T3)

Claims assessed for verifiability:

- **T0**: Untestable (avoid)
- **T1**: Implicit test
- **T2**: Explicit PASS/FAIL (minimum for causality)
- **T3**: Reproducible with metrics (preferred for R2)

#### 📈 Sensitivity Map

Top 5 factors that would change recommendations:

1. Scan mode changes
2. Baseline usage
3. Exposed secrets count
4. Unverified claims
5. High-risk violations

Each factor includes impact, threshold, and PASS/FAIL test.

### Core Principles

#### Fail-Closed Philosophy

**By default, quality gates fail unless explicitly passing.** This ensures:

- No false sense of security
- Violations are caught before production
- Teams must address issues, not ignore warnings

#### No Overpromises

Absolutist claims damage credibility and create legal/reputation risk. LaunchGuard:

- Blocks superlatives without evidence
- Flags "guaranteed" and "100%" language
- Enforces measured, accurate claims

#### Enhanced Claim Ledger

Every factual claim must be tagged and tracked with full metadata:

- Creates accountability trail with proof levels
- Enables audit of documentation accuracy
- Surfaces claims needing sources
- Distinguishes user feedback from deduced facts
- Tracks dependencies and testability
- Distinguishes user feedback from deduced facts

### PASS/FAIL Tests (R-SUITE)

Each rule has deterministic pass/fail criteria:

- **R-SUITE** = Rules Suite for Uniform Integrity Testing & Enforcement
- Binary outcomes (no subjective "code smells")
- Fixture tests prove rule behavior
- Regression protection

### No Web Fact-Checking

LaunchGuard intentionally avoids web lookups:

- No API dependencies or rate limits
- Deterministic, repeatable results
- Fast local execution
- Teams provide sources manually

Recency triggers (e.g., "2026", "price") become **[UNKNOWN]** warnings, prompting teams to add citations.

## Exit Codes

- **0** - Pass (no errors)
- **1** - Fail (errors found)
- **2** - Error (exception/crash)

## CLI Options

```
Usage: launchgard [options] <files...>

Options:
  -m, --mode <mode>              Scan mode: light or max (default: "light")
  -b, --baseline <file>          Path to baseline file
  --create-baseline <file>       Create baseline file from current violations
  -o, --output <dir>             Output directory for reports (default: ".")
  -v, --verbose                  Verbose output
  -h, --help                     Display help
  -V, --version                  Display version

Examples:
  launchgard README.md
  launchgard --mode max "**/*.md"
  launchgard --baseline .baseline.json "**/*.md"
  launchgard --create-baseline .baseline.json "**/*.md"
```

## Example Output

### Console Output (ARCHI-Ω v1.2)

```
═══════════════════════════════════════════════════════════
  LaunchGuard Scan Results (ARCHI-Ω v1.2)
═══════════════════════════════════════════════════════════

Mode:          LIGHT
Files Scanned: 1
Status:        ❌ FAIL
Errors:        8
Warnings:      0

Risk Distribution:
  🔴 R2 (High Impact):  2
  🟡 R1 (Operational):  6

───────────────────────────────────────────────────────────
 Violations
───────────────────────────────────────────────────────────

❌ examples/sample-readme.md:5:19
   [OVER-001] Detects overpromising language
   This product is **revolutionary** and **guaranteed**...

❌ examples/sample-readme.md:33:15
   [SEC-001] Detects exposed GitHub tokens
   GitHub Token: ghp_1234567890...

───────────────────────────────────────────────────────────
 Claim Ledger (ARCHI-Ω v1.2)
───────────────────────────────────────────────────────────

❓ [DED] S1 (T2) examples/sample-readme.md:18
  - [DED] This product uses AES-256 encryption.
  Dependencies: AES-256

❓ [USER] S0 (T1) examples/sample-readme.md:19
  - [USER] Users report 50% faster processing.

───────────────────────────────────────────────────────────
 Sensitivity Map (ARCHI-Ω v1.2)
───────────────────────────────────────────────────────────

📊 Exposed Secrets
   Impact: 2 secret(s) detected - high security risk
   Test: FAIL if any secrets; PASS if all removed

📊 High-Risk Violations (R2)
   Impact: 2 high-impact violation(s) detected
   Test: FAIL while R2 exists; PASS when resolved

═══════════════════════════════════════════════════════════
```

### Report Files

**report.json** - Complete scan results including:
- All violations with risk classification
- Full claim ledger with proof levels, dependencies, testability
- Sensitivity map with top 5 factors
- Risk distribution summary

**report.md** - Formatted Markdown report with:
- Violations grouped by file
- Enhanced claim ledger table (Claim-ID, S-Level, Dependencies, Testability, Status)
- Sensitivity map section

## Documentation

- **[ARCHI-OMEGA-v1.2.md](./ARCHI-OMEGA-v1.2.md)** - Complete ARCHI-Ω v1.2 specification
- **[RUNBOOK.md](./RUNBOOK.md)** - Operational guide and termination states
- **[METHODOLOGY.md](./METHODOLOGY.md)** - Core principles and rationale
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Development guidelines

## Examples

See [examples/sample-readme.md](examples/sample-readme.md) for a demo file with intentional violations.

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Run tests
npm test

# Run linter
npm run lint

# Format code
npm run format
```

## License

MIT

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure CI passes
5. Submit a pull request

---

**Built with ARCHI-Ω v1.2 principles** | **Deterministic quality gates** | **Fail-closed by design**
