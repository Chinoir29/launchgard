# LaunchGuard

[![CI](https://github.com/Chinoir29/launchgard/actions/workflows/ci.yml/badge.svg)](https://github.com/Chinoir29/launchgard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Deterministic quality gate for product docs, prompts, and repos.** Enforces claim tagging, blocks overpromises, flags recency triggers, detects secrets, and generates deterministic PASS/FAIL reports via CLI and GitHub Action.

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

LaunchGuard implements the ARCHI-Ω v1.2 methodology for documentation quality:

### Fail-Closed Philosophy

**By default, quality gates fail unless explicitly passing.** This ensures:

- No false sense of security
- Violations are caught before production
- Teams must address issues, not ignore warnings

### No Overpromises

Absolutist claims damage credibility and create legal/reputation risk. LaunchGuard:

- Blocks superlatives without evidence
- Flags "guaranteed" and "100%" language
- Enforces measured, accurate claims

### Claim Ledger

Every factual claim must be tagged and tracked:

- Creates accountability trail
- Enables audit of documentation accuracy
- Surfaces claims needing sources
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

### Console Output

```
═══════════════════════════════════════════════════════════
  LaunchGuard Scan Results
═══════════════════════════════════════════════════════════

Mode:          LIGHT
Files Scanned: 1
Status:        ❌ FAIL
Errors:        3
Warnings:      0

───────────────────────────────────────────────────────────
 Violations
───────────────────────────────────────────────────────────

❌ examples/sample-readme.md:5:23
   [OVER-001] Detects overpromising language
   ...is **revolutionary** and **guarante...

❌ examples/sample-readme.md:5:43
   [OVER-001] Detects overpromising language
   ...d **guaranteed** to solve all your ...

❌ examples/sample-readme.md:37:16
   [SEC-001] Detects exposed GitHub tokens
   ...ken: ghp_123456789012345678901234567...

═══════════════════════════════════════════════════════════
```

### Report Files

**report.json** - Complete scan results in JSON format
**report.md** - Formatted Markdown report with violations and claim ledger

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
