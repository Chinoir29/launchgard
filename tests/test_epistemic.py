"""
Tests for ARCHI-Ω v1.2.1 epistemic foundation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from archi_omega.epistemic.foundation import (
    ProofLevel, RiskClass, TestabilityLevel, OriginTag,
    Claim, ClaimLedger, Gap, GapLedger, RiskClassifier, ProofValidator, ProofBudget
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
        status="À-CLÔTURER",
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
        status="À-CLÔTURER"
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


def test_gap_creation():
    """Test gap creation and validation (v1.2.1)"""
    gap = Gap(
        gap_id="G001",
        description="Load requirements not specified",
        decision="Assume 1K QPS as conservative default",
        test="Verify actual load requirements with stakeholders",
        impact_if_wrong="May under-provision infrastructure"
    )
    
    assert gap.gap_id == "G001"
    assert gap.validate() == True
    assert gap.status == "À-CLÔTURER"
    
    # Test invalid gap (missing fields)
    invalid_gap = Gap(
        gap_id="G002",
        description="Something",
        decision="",
        test="",
        impact_if_wrong=""
    )
    assert invalid_gap.validate() == False
    
    print("✓ Gap creation test passed")


def test_gap_ledger():
    """Test gap ledger management (v1.2.1)"""
    ledger = GapLedger()
    
    gap1 = Gap(
        gap_id="G001",
        description="Budget not specified",
        decision="Proceed with cost optimization approach",
        test="Clarify budget with finance team",
        impact_if_wrong="May exceed budget constraints"
    )
    
    gap2 = Gap(
        gap_id="G002",
        description="SLA requirements unclear",
        decision="Target 99.9% availability",
        test="Review SLA requirements with stakeholders",
        impact_if_wrong="May not meet business needs",
        status="PASS"
    )
    
    ledger.add_gap(gap1)
    ledger.add_gap(gap2)
    
    assert len(ledger.gaps) == 2
    assert ledger.get_gap("G001") == gap1
    
    # Test validation
    validation = ledger.validate_all()
    assert validation["valid"] == True
    
    # Test markdown table
    table = ledger.to_markdown_table()
    assert "Gap-ID" in table
    assert "G001" in table
    
    print("✓ Gap ledger test passed")


def run_all_tests():
    """Run all tests"""
    print("\n=== Running ARCHI-Ω v1.2.1 Epistemic Foundation Tests ===\n")
    
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
        test_gap_creation()
        test_gap_ledger()
        
        print("\n=== All tests passed! ✓ ===\n")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
