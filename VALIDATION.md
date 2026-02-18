# Local Validation Guide

This guide explains how to validate the ARCHI-Ω v1.2 framework locally before submitting changes.

## Prerequisites

```bash
# Install Python 3.8+
python --version

# Install dependencies
pip install -r requirements.txt
```

## Validation Commands

Run these commands in order. All must pass (exit code 0) before submitting:

### 1. Fail-Closed Validation (REQUIRED)

```bash
python scripts/archi_omega_lint.py
```

**What it checks:**
- No overpromise keywords (guarantee, 100%, etc.)
- Origin tags properly implemented
- Testability enforcement working
- Risk classification correct
- Fail-closed pipeline behavior
- Documentation includes limitations

**Expected output:** `✓ VALIDATION PASSED` with exit code 0

### 2. Unit Tests (REQUIRED)

```bash
python tests/test_epistemic.py
```

**What it checks:**
- Proof levels (S0-S4)
- Risk classification (R0-R3)
- Claim management
- Origin tagging
- Testability validation
- Claim ledger functionality

**Expected output:** `All tests passed! ✓` with exit code 0

### 3. Framework Verification (REQUIRED)

```bash
python verify.py
```

**What it checks:**
- File structure complete
- Python imports working
- Epistemic foundation operational
- Risk classification functional
- Claim ledger operational
- Pipeline execution successful

**Expected output:** `🎉 All checks passed!` with exit code 0

## Quick Validation (All at Once)

Run all validation checks with a single command:

```bash
python scripts/archi_omega_lint.py && \
python tests/test_epistemic.py && \
python verify.py && \
echo "✓ All validation checks passed!"
```

If any check fails, the command stops and reports the failure.

## What to Do If Checks Fail

### Fail-Closed Validation Fails

**Issue:** Overpromise keywords detected
- **Fix:** Remove or rephrase words like "guarantee", "assured", "100%" (unless contextual like "100% test coverage")

**Issue:** Origin tags not working
- **Fix:** Check `src/archi_omega/epistemic/foundation.py` - ensure Claim class requires `origin_tag` parameter

**Issue:** Testability not enforced
- **Fix:** Check `Claim.validate_strong_causality()` method

### Unit Tests Fail

**Issue:** Import errors
- **Fix:** Ensure `PYTHONPATH` includes `src/` directory or run `pip install -e .`

**Issue:** Test assertion failures
- **Fix:** Review the specific test and verify the implementation matches expected behavior

### Framework Verification Fails

**Issue:** Missing files
- **Fix:** Ensure all required files are present (see file list in verification output)

**Issue:** Pipeline execution fails
- **Fix:** Check pipeline stages in `src/archi_omega/pipeline/stages.py`

## CI/CD Validation

These same checks run automatically in CI when you push:

1. GitHub Actions workflow (`.github/workflows/ci.yml`)
2. Runs on Python 3.8, 3.9, 3.10, 3.11
3. All three validation commands must pass

**To see CI status:**
- Check the "Actions" tab in GitHub
- Look for green checkmarks on your PR
- Review logs if any check fails

## Before Submitting PR

Run this checklist:

- [ ] `python scripts/archi_omega_lint.py` → PASS
- [ ] `python tests/test_epistemic.py` → PASS
- [ ] `python verify.py` → PASS
- [ ] Code reviewed for overpromises
- [ ] Documentation includes limitations/scope
- [ ] No secrets or credentials in code
- [ ] Changes are minimal and focused

## Troubleshooting

### "Module not found" errors

```bash
# Option 1: Set PYTHONPATH
export PYTHONPATH=/path/to/launchgard/src

# Option 2: Install in development mode
pip install -e .
```

### "Permission denied" on scripts

```bash
chmod +x scripts/archi_omega_lint.py
chmod +x verify.py
```

### Tests pass locally but fail in CI

- Check Python version (CI uses 3.8-3.11)
- Verify all dependencies in `requirements.txt`
- Check for platform-specific code

## Additional Validation (Optional)

### Code Formatting

```bash
pip install black flake8
black src/ tests/
flake8 src/ tests/ --select=E9,F63,F7,F82
```

### Type Checking

```bash
pip install mypy
mypy src/
```

### Coverage

```bash
pip install pytest pytest-cov
pytest tests/ --cov=src/archi_omega --cov-report=term
```

---

**For more information:**
- Framework spec: [ARCHI-OMEGA-v1.2.md](ARCHI-OMEGA-v1.2.md)
- Usage guide: [USAGE.md](USAGE.md)
- Quick reference: [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
