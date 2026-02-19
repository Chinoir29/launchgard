# Changelog

All notable changes to ARCHI-Ω will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-02-19

### Added

#### Framework Core
- Complete ARCHI-Ω v1.2 specification with 12 sections
- Fail-closed authority system with context firewall
- Anti-injection protection for external content
- Mandatory origin tagging system: [USER], [DED], [HYP], [UNKNOWN]

#### Epistemic Foundation
- Proof levels (S0-S4): user data → independent cross-checking
- Risk classes (R0-R3): low risk → illegal/dangerous
- Testability levels (T0-T3): non-testable → reproducible
- Proof budget system with risk-based requirements
- Claim validation and strong causality checking
- Comprehensive claim ledger functionality

#### Pipeline
- 7-stage execution pipeline: COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT
- Risk classification and proof budget determination
- Option generation (2-3 alternatives with scoring)
- Invariant verification and stress testing
- Robust option selection with fallback strategies
- Deliverable generation with termination codes

#### CLI & API
- Command-line interface (`archi-omega` command)
- Python API for programmatic use
- YAML/JSON input support
- Multiple output formats (Markdown, YAML, JSON)
- Configuration file support

#### Documentation
- Complete framework specification (ARCHI-OMEGA-v1.2.md)
- Comprehensive README with quick start
- Usage guide with examples
- Validation guide for local testing
- Quick reference card
- Status tracking document
- Repository assessment report

#### Templates
- User input template (10 sections)
- Output format template (12 mandatory sections)
- ADR (Architecture Decision Records) template
- Claim ledger template

#### Examples
- Sample REST API input file
- Complete web API example walkthrough

#### Testing & Validation
- 9 unit tests for epistemic foundation
- 6 verification checks for system integrity
- Fail-closed validation with 6 security checks
- CI/CD workflow with GitHub Actions

#### Configuration
- Default configuration (MODE=MAXCAP, AUTO-GOV=ON)
- Support for 10 user-configurable parameters
- AS-CODE YAML format for machine-readable configs

#### Security
- Data hygiene rules and PII protection
- Secrets management guidelines
- Input validation and sanitization
- Security policy and vulnerability reporting process

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Implemented fail-closed by default
- Added context firewall for anti-injection
- Enforced mandatory origin tagging
- Added proof validation system
- Implemented risk-based evidence requirements

## [Unreleased]

### Planned Features
- Extended test coverage beyond core functionality
- Integration with external pricing/verification APIs
- Web UI for framework interaction
- Additional domain-specific examples
- Performance benchmarks
- API documentation generation
- Multi-language support for documentation

---

## Version History

- **1.2.0** (2026-02-19): Initial production release
  - Complete ARCHI-Ω framework implementation
  - All 12 specification sections
  - Production-ready with comprehensive testing

---

**Note**: For security updates, see [SECURITY.md](SECURITY.md)

**Format**: [Major.Minor.Patch]
- **Major**: Breaking changes to API or framework principles
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, documentation updates
