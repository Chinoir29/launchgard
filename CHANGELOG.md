# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-18

### Added

- **ARCHI-Ω v1.2 Framework**: Comprehensive architectural framework with fail-closed authority, proof-level system (S0-S4), and risk classification (R0-R3)
- **Deterministic quality gate**: Enforces claim tagging ([USER]/[HYP]/[DED]/[UNKNOWN]) with mandatory origin tracking
- **Execution pipeline**: Complete COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT workflow
- **Validation suite**: Three-level validation with fail-closed linting, unit tests, and framework verification
- **Templates**: User input, ADR, claim ledger, and output format templates
- **CI/CD integration**: GitHub Actions workflow with Python 3.8-3.11 test matrix
- **Security features**: Secrets detection, PII protection, and data hygiene enforcement
- **Risk management**: Risk-based proof budgets and testability requirements (T0-T3)
- **Documentation**: Complete framework documentation, usage guide, quick reference, and examples
- **Configuration**: Flexible YAML-based configuration with MAXCAP mode support
- **MIT License**: Open-source release under MIT License
- **Security policy**: Responsible disclosure guidelines and supported versions

### Framework Capabilities

- Zero fabrication enforcement
- Mandatory proof levels for all claims
- Testability requirements for strong causality claims
- Auto-governance and auto-tools routing
- Context firewall with anti-injection protection
- Claim ledger for assertion tracking

### Initial Public Release

This is the first public release of launchgard, providing a production-ready framework for deterministic quality gates in product documentation, prompts, and repositories.

[0.1.0]: https://github.com/Chinoir29/launchgard/releases/tag/v0.1.0
