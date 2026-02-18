#!/usr/bin/env python3
"""
ARCHI-Ω v1.2 - Verification Script

This script verifies that the framework is correctly installed and functioning.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_imports():
    """Verify all modules can be imported"""
    print("Checking imports...")
    try:
        from archi_omega import (
            ProofLevel, RiskClass, TestabilityLevel, OriginTag,
            Claim, ClaimLedger, RiskClassifier, ProofValidator,
            Pipeline, ProjectContext, TerminationCode
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def check_epistemic():
    """Verify epistemic foundation"""
    print("\nChecking epistemic foundation...")
    try:
        from archi_omega.epistemic.foundation import (
            ProofLevel, RiskClass, Claim, OriginTag, TestabilityLevel
        )
        
        # Create a test claim
        claim = Claim(
            claim_id="TEST",
            text="Test claim",
            origin_tag=OriginTag.USER,
            proof_level=ProofLevel.S0,
            dependencies=[],
            test_description="Test",
            status="PASS"
        )
        
        assert claim.claim_id == "TEST"
        print("✓ Epistemic foundation working")
        return True
    except Exception as e:
        print(f"✗ Epistemic foundation failed: {e}")
        return False


def check_pipeline():
    """Verify pipeline execution"""
    print("\nChecking pipeline...")
    try:
        from archi_omega.pipeline.stages import Pipeline, ProjectContext
        
        # Create minimal context
        context = ProjectContext()
        context.goal = "Test goal"
        context.constraints = {"budget": "$100"}
        
        # Run pipeline
        pipeline = Pipeline()
        result = pipeline.execute(context)
        
        assert "termination" in result
        print(f"✓ Pipeline executed successfully (termination: {result['termination']})")
        return True
    except Exception as e:
        print(f"✗ Pipeline failed: {e}")
        return False


def check_risk_classification():
    """Verify risk classification"""
    print("\nChecking risk classification...")
    try:
        from archi_omega.epistemic.foundation import RiskClassifier, RiskClass
        
        # Test different risk levels
        r0 = RiskClassifier.classify()
        r2 = RiskClassifier.classify(has_financial_impact=True, has_security_impact=True)
        r3 = RiskClassifier.classify(is_illegal=True)
        
        assert r0 in [RiskClass.R0, RiskClass.R1]
        assert r2 == RiskClass.R2
        assert r3 == RiskClass.R3
        
        print("✓ Risk classification working correctly")
        return True
    except Exception as e:
        print(f"✗ Risk classification failed: {e}")
        return False


def check_claim_ledger():
    """Verify claim ledger functionality"""
    print("\nChecking claim ledger...")
    try:
        from archi_omega.epistemic.foundation import (
            ClaimLedger, Claim, OriginTag, ProofLevel, RiskClass
        )
        
        ledger = ClaimLedger()
        
        claim1 = Claim(
            claim_id="C001",
            text="Test claim 1",
            origin_tag=OriginTag.USER,
            proof_level=ProofLevel.S0,
            dependencies=[],
            test_description="Test 1",
            status="PASS"
        )
        
        ledger.add_claim(claim1)
        stats = ledger.get_statistics()
        
        assert stats["total_claims"] == 1
        assert stats["by_status"]["PASS"] == 1
        
        print("✓ Claim ledger working")
        return True
    except Exception as e:
        print(f"✗ Claim ledger failed: {e}")
        return False


def check_files():
    """Verify all required files exist"""
    print("\nChecking required files...")
    required_files = [
        "ARCHI-OMEGA-v1.2.md",
        "README.md",
        "USAGE.md",
        "QUICK-REFERENCE.md",
        "archi-omega-config.yaml",
        "setup.py",
        "requirements.txt",
        ".gitignore",
        "templates/user-input-template.md",
        "templates/adr-template.md",
        "templates/claim-ledger-template.md",
        "templates/output-format-template.md",
        "examples/simple-web-api-example.md",
        "examples/sample-input.yaml",
        "src/archi_omega/__init__.py",
        "src/archi_omega/epistemic/foundation.py",
        "src/archi_omega/pipeline/stages.py",
        "src/archi_omega/cli.py",
        "tests/test_epistemic.py"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"✗ Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"✓ All {len(required_files)} required files present")
        return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("ARCHI-Ω v1.2 - Verification Script")
    print("=" * 60)
    
    checks = [
        ("File structure", check_files),
        ("Python imports", check_imports),
        ("Epistemic foundation", check_epistemic),
        ("Risk classification", check_risk_classification),
        ("Claim ledger", check_claim_ledger),
        ("Pipeline execution", check_pipeline)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} check crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print("=" * 60)
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Framework is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
