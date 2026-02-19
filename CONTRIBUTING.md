# Contributing to ARCHI-Ω

Thank you for your interest in contributing to ARCHI-Ω! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

This project adheres to a code of conduct (see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/launchgard.git
   cd launchgard
   ```
3. **Set up the development environment** (see below)
4. **Create a feature branch**: `git checkout -b feature/your-feature-name`

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages
- Code samples (if applicable)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear, descriptive title
- Provide detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include examples of how it would work

### Pull Requests

Good pull requests (patches, improvements, new features) are welcome. Please:

1. Follow the coding standards
2. Update documentation as needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Keep changes focused and atomic

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### Verify Installation

```bash
# Run all validation checks
python scripts/archi_omega_lint.py
python tests/test_epistemic.py
python verify.py
```

## Testing

### Running Tests

```bash
# Run unit tests
python tests/test_epistemic.py

# Run verification checks
python verify.py

# Run fail-closed validation
python scripts/archi_omega_lint.py

# Run all checks
python scripts/archi_omega_lint.py && \
python tests/test_epistemic.py && \
python verify.py
```

### Writing Tests

- Place new tests in the `tests/` directory
- Follow existing test structure and naming conventions
- Aim for high coverage of new code
- Include both positive and negative test cases
- Test edge cases and error conditions

### Test Requirements

All pull requests must:
- Pass all existing tests
- Include tests for new functionality
- Maintain or improve code coverage

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters (flexible for readability)

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/ --select=E9,F63,F7,F82
```

### Type Hints

- Use type hints for function parameters and return values
- Use `typing` module for complex types
- Optional: Run mypy for type checking

### Documentation Strings

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining behavior,
    edge cases, and important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When and why this is raised
    """
    pass
```

## Documentation

### When to Update Documentation

Update documentation when you:
- Add new features
- Change existing behavior
- Fix bugs that affect documented behavior
- Add new configuration options

### Documentation Files

- `ARCHI-OMEGA-v1.2.md`: Framework specification (critical - discuss before changing)
- `README.md`: Project overview and quick start
- `USAGE.md`: Detailed usage instructions
- `VALIDATION.md`: Testing and validation guide
- Docstrings in Python code

### Documentation Standards

- Write in clear, concise English or French (match existing style)
- Include code examples where helpful
- Keep examples up-to-date
- Use consistent terminology (see glossary in ARCHI-OMEGA-v1.2.md)

## Submitting Changes

### Before Submitting

1. **Run all tests**: Ensure all validation checks pass
2. **Update documentation**: Include any necessary doc updates
3. **Add CHANGELOG entry**: Document your changes
4. **Commit messages**: Write clear, descriptive commit messages

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintain build, dependencies, etc.

**Example:**
```
feat: Add support for JSON output format

- Implement JSON serializer for deliverable
- Add --format json CLI option
- Update tests and documentation

Closes #123
```

### Pull Request Process

1. **Push to your fork**: `git push origin feature/your-feature-name`
2. **Open a pull request** on GitHub
3. **Fill out the PR template** completely
4. **Link related issues** using "Closes #123" or "Fixes #456"
5. **Wait for review**: Maintainers will review your changes
6. **Address feedback**: Make requested changes
7. **Squash commits** if requested
8. **Merge**: Maintainer will merge when approved

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] CHANGELOG updated
- [ ] No merge conflicts with main branch

## Review Process

### What We Look For

- **Correctness**: Does the code work as intended?
- **Tests**: Are there adequate tests?
- **Documentation**: Is it documented?
- **Style**: Does it follow our coding standards?
- **ARCHI-Ω principles**: Does it respect fail-closed, origin tagging, etc.?
- **Security**: Are there security implications?

### Review Timeline

- Initial review: Within 7 days
- Follow-up reviews: Within 3-5 days after updates
- Merge: After approval from maintainer(s)

### Addressing Review Comments

- Respond to all review comments
- Make requested changes in new commits
- Mark conversations as resolved when addressed
- Ask for clarification if feedback is unclear

## Framework-Specific Guidelines

### ARCHI-Ω Principles

When contributing, respect these core principles:

1. **Fail-closed**: When in doubt, fail safely
2. **Origin tagging**: All claims must have [USER]/[DED]/[HYP]/[UNKNOWN]
3. **Proof validation**: Risk-based evidence requirements
4. **Zero fabrication**: Never invent facts or sources
5. **Testability**: Strong causality requires ≥T2
6. **Security**: PII/secrets hygiene, input validation

### Adding New Features

When adding features to the framework:

1. **Discuss first**: Open an issue to discuss major changes
2. **Update spec**: May require updating ARCHI-OMEGA-v1.2.md
3. **Maintain compatibility**: Avoid breaking existing functionality
4. **Add examples**: Include usage examples
5. **Update templates**: Modify templates if needed

### Modifying the Pipeline

Changes to pipeline stages require:

- Clear justification and discussion
- Comprehensive tests
- Documentation updates
- Validation that all existing tests still pass

## Questions?

- **General questions**: Open a discussion on GitHub
- **Bug reports**: Create an issue
- **Security concerns**: See [SECURITY.md](SECURITY.md)
- **Feature requests**: Open an issue with [Feature Request] tag

## Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Acknowledged in release notes
- Added to contributors list (coming soon)

Thank you for contributing to ARCHI-Ω! 🚀

---

**Last Updated**: 2026-02-19  
**Framework Version**: v1.2.0
