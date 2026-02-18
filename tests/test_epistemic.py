"""
Tests for ARCHI-Ω v1.3.0 epistemic foundation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from archi_omega.epistemic.foundation import (
    ProofLevel, RiskClass, TestabilityLevel, OriginTag,
    Claim, ClaimLedger, RiskClassifier, ProofValidator, ProofBudget,
    GapClosure, ComplexityClass, ComplexityClassifier, Profile, ProfileSelector
)


def test_proof_levels():
    """Test proof level enumeration"""
    assert ProofLevel.S0.value == "données user"
    assert ProofLevel.S4.value == "recoupement indépendant"
    print("✓ Proof levels test passed")


def test_risk_classes():
    """Test risk classification"""
    assert RiskClass.R0.value == "faible"
    assert RiskClass.R3.value == "illégal/dangereux"
    print("✓ Risk classes test passed")


def test_risk_classifier():
    """Test risk classification logic"""
    # Low risk
    r0 = RiskClassifier.classify()
    assert r0 == RiskClass.R1  # Default is R1
    
    # High risk with financial impact
    r2 = RiskClassifier.classify(has_financial_impact=True)
    assert r2 == RiskClass.R2
    
    # Illegal
    r3 = RiskClassifier.classify(is_illegal=True)
    assert r3 == RiskClass.R3
    
    print("✓ Risk classifier test passed")


def test_proof_budget():
    """Test proof budget calculation"""
    pb_r0 = ProofBudget.for_risk_class(RiskClass.R0)
    assert ProofLevel.S1 in pb_r0.required_levels
    assert pb_r0.minimum_pillars == 1
    
    pb_r2 = ProofBudget.for_risk_class(RiskClass.R2)
    assert pb_r2.minimum_pillars == 2
    assert pb_r2.requires_alternatives
    
    print("✓ Proof budget test passed")


def test_claim_creation():
    """Test claim creation and validation"""
    claim = Claim(
        claim_id="C001",
        text="System will handle 10K QPS",
        origin_tag=OriginTag.USER,
        proof_level=ProofLevel.S0,
        dependencies=[],
        test_description="Load test: 10K QPS for 5 min",
        status="À-CLÔTURER",  # v1.3.0: new status
        testability=TestabilityLevel.T3
    )
    
    assert claim.claim_id == "C001"
    assert claim.origin_tag == OriginTag.USER
    assert claim.status == "À-CLÔTURER"
    
    print("✓ Claim creation test passed")


def test_strong_causality_validation():
    """Test strong causality validation"""
    # Strong causality with adequate testability
    claim_good = Claim(
        claim_id="C002",
        text="Using Redis will cause 70% reduction in DB load",
        origin_tag=OriginTag.HYP,
        proof_level=ProofLevel.S1,
        dependencies=[],
        test_description="A/B test",
        status="À-CLÔTURER",
        testability=TestabilityLevel.T3
    )
    assert claim_good.validate_strong_causality() == True
    
    # Strong causality with inadequate testability
    claim_bad = Claim(
        claim_id="C003",
        text="This will cause significant improvement",
        origin_tag=OriginTag.HYP,
        proof_level=ProofLevel.S1,
        dependencies=[],
        test_description="Observation",
        status="À-CLÔTURER",
        testability=TestabilityLevel.T0
    )
    assert claim_bad.validate_strong_causality() == False
    
    print("✓ Strong causality validation test passed")


def test_claim_ledger():
    """Test claim ledger management"""
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
    
    claim2 = Claim(
        claim_id="C002",
        text="Test claim 2",
        origin_tag=OriginTag.HYP,
        proof_level=ProofLevel.S1,
        dependencies=["C001"],
        test_description="Test 2",
        status="À-CLÔTURER"  # v1.3.0
    )
    
    ledger.add_claim(claim1)
    ledger.add_claim(claim2)
    
    assert len(ledger.claims) == 2
    assert ledger.get_claim("C001") == claim1
    
    stats = ledger.get_statistics()
    assert stats["total_claims"] == 2
    assert stats["by_status"]["PASS"] == 1
    assert stats["by_status"]["À-CLÔTURER"] == 1
    
    print("✓ Claim ledger test passed")


def test_proof_validator():
    """Test proof validation"""
    claim = Claim(
        claim_id="C001",
        text="System handles load",
        origin_tag=OriginTag.USER,
        proof_level=ProofLevel.S0,
        dependencies=[],
        test_description="Load test",
        status="PASS",
        testability=TestabilityLevel.T3
    )
    
    validator = ProofValidator()
    result = validator.validate_claim(claim, RiskClass.R1)
    
    assert "valid" in result
    assert "issues" in result
    assert "warnings" in result
    
    print("✓ Proof validator test passed")


def test_markdown_table_generation():
    """Test markdown table generation"""
    ledger = ClaimLedger()
    
    claim = Claim(
        claim_id="C001",
        text="Test claim",
        origin_tag=OriginTag.USER,
        proof_level=ProofLevel.S0,
        dependencies=[],
        test_description="Test",
        status="PASS"
    )
    
    ledger.add_claim(claim)
    table = ledger.to_markdown_table()
    
    assert "Claim-ID" in table
    assert "C001" in table
    assert "[USER]" in table
    
    print("✓ Markdown table generation test passed")


def test_gap_closure():
    """Test GAP closure (v1.3.0)"""
    gap_closure = GapClosure(
        gap_id="G001",
        gap_description="Exact AWS cost unknown",
        decision="Conservative budget 500$/month (2x margin)",
        test="Verify actual bill after 1 month; alert if >400$",
        impact="±200$ depending on traffic; may need instance adjustment",
        term_code="TERM-PROTOCOLE"
    )
    
    validation = gap_closure.validate()
    assert validation["valid"] == True
    assert len(validation["issues"]) == 0
    
    # Test incomplete gap closure
    incomplete_gap = GapClosure(
        gap_id="G002",
        gap_description="Some gap",
        decision="",  # Missing
        test="",  # Missing
        impact="Unknown",
        term_code=""  # Missing
    )
    
    validation = incomplete_gap.validate()
    assert validation["valid"] == False
    assert len(validation["issues"]) > 0
    
    print("✓ GAP closure test passed")


def test_gap_claim_validation():
    """Test claim with GAP tag requires closure (v1.3.0)"""
    # GAP claim with proper closure
    gap_closure = GapClosure(
        gap_id="G001",
        gap_description="Cost estimate unknown",
        decision="Use conservative estimate",
        test="Verify after implementation",
        impact="May affect budget",
        term_code="TERM-PROTOCOLE"
    )
    
    claim_with_closure = Claim(
        claim_id="C001",
        text="System cost estimated",
        origin_tag=OriginTag.GAP,
        proof_level=ProofLevel.S1,
        dependencies=[],
        test_description="Cost validation",
        status="À-CLÔTURER",
        gap_closure=gap_closure
    )
    
    validation = claim_with_closure.validate_gap_closure()
    assert validation["valid"] == True
    
    # GAP claim without closure (should fail)
    claim_without_closure = Claim(
        claim_id="C002",
        text="Another estimate",
        origin_tag=OriginTag.GAP,
        proof_level=ProofLevel.S1,
        dependencies=[],
        test_description="Test",
        status="À-CLÔTURER",
        gap_closure=None  # Missing!
    )
    
    validation = claim_without_closure.validate_gap_closure()
    assert validation["valid"] == False
    assert len(validation["issues"]) > 0
    
    print("✓ GAP claim validation test passed")


def test_complexity_classifier():
    """Test complexity classification (v1.3.0)"""
    # C0 - Trivial
    c0 = ComplexityClassifier.classify()
    assert c0 == ComplexityClass.C0
    
    # C1 - Simple
    c1 = ComplexityClassifier.classify(has_repo_ci_docs=True)
    assert c1 == ComplexityClass.C1
    
    # C2 - Moderate
    c2 = ComplexityClassifier.classify(
        has_repo_ci_docs=True,
        has_auth_payment_storage_api=True,
        has_security_compliance_sensitive_data=True
    )
    assert c2 == ComplexityClass.C2
    
    # C3 - Complex
    c3 = ComplexityClassifier.classify(
        has_repo_ci_docs=True,
        has_auth_payment_storage_api=True,
        has_security_compliance_sensitive_data=True,
        has_perf_load_sla=True,
        is_prod_business=True
    )
    assert c3 == ComplexityClass.C3
    
    print("✓ Complexity classifier test passed")


def test_profile_selector():
    """Test profile selection (v1.3.0)"""
    # P-SIMPLE
    profile = ProfileSelector.select_profile(RiskClass.R0, ComplexityClass.C0)
    assert profile == Profile.P_SIMPLE
    
    # P-STANDARD
    profile = ProfileSelector.select_profile(RiskClass.R1, ComplexityClass.C2)
    assert profile == Profile.P_STANDARD
    
    # P-COMPLEX (high risk)
    profile = ProfileSelector.select_profile(RiskClass.R2, ComplexityClass.C1)
    assert profile == Profile.P_COMPLEX
    
    # P-PROJET (C3 always triggers)
    profile = ProfileSelector.select_profile(RiskClass.R1, ComplexityClass.C3)
    assert profile == Profile.P_PROJET
    
    print("✓ Profile selector test passed")


def run_all_tests():
    """Run all tests"""
    print("\n=== Running ARCHI-Ω v1.3.0 Epistemic Foundation Tests ===\n")
    
    try:
        test_proof_levels()
        test_risk_classes()
        test_risk_classifier()
        test_proof_budget()
        test_claim_creation()
        test_strong_causality_validation()
        test_claim_ledger()
        test_proof_validator()
        test_markdown_table_generation()
        
        # v1.3.0 new tests
        test_gap_closure()
        test_gap_claim_validation()
        test_complexity_classifier()
        test_profile_selector()
        
        print("\n=== All tests passed! ✓ ===\n")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
