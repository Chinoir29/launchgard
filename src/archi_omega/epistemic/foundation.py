"""
ARCHI-Ω v1.2.1 - Epistemic Foundation

This module implements the epistemic foundation of the ARCHI-Ω framework:
- Proof levels (S0-S4)
- Risk classes (R0-R3)
- Proof budgets
- Testability levels (T0-T3)
- Origin tags (with GAP instead of UNKNOWN)
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


class ProofLevel(Enum):
    """Proof levels (S0-S4)"""
    S0 = "données user"  # User-provided data
    S1 = "raisonnement/calcul"  # Reasoning/calculation
    S2 = "outils/sources"  # Tools/external sources
    S3 = "tests reproductibles"  # Reproducible tests
    S4 = "recoupement indépendant"  # Independent cross-checking (≥2 sources/methods)


class RiskClass(Enum):
    """Risk classification (R0-R3)"""
    R0 = "faible"  # Low risk
    R1 = "opérationnel faible impact"  # Operational with low impact
    R2 = "fort impact"  # High impact (finance/legal/security/health)
    R3 = "illégal/dangereux"  # Illegal/dangerous - STOP


class TestabilityLevel(Enum):
    """TRACE testability levels (T0-T3)"""
    T0 = "non testable"  # Not testable - avoid
    T1 = "test implicite"  # Implicit test / vague observation
    T2 = "test explicite PASS/FAIL"  # Explicit PASS/FAIL (minimum for strong causality)
    T3 = "test reproductible"  # Reproducible + metric + threshold + procedure


class OriginTag(Enum):
    """Origin tags for claims"""
    USER = "USER"  # User-provided information
    DED = "DED"  # Deduced from available information
    HYP = "HYP"  # Hypothesis - needs testing
    GAP = "GAP"  # Information gap - requires decision, test, and termination


@dataclass
class ProofBudget:
    """Proof budget requirements for a risk class"""
    risk_class: RiskClass
    required_levels: List[ProofLevel]
    minimum_pillars: int = 1
    requires_alternatives: bool = False
    requires_guardrails: bool = False
    
    @classmethod
    def for_risk_class(cls, risk_class: RiskClass) -> 'ProofBudget':
        """Get proof budget for a risk class"""
        if risk_class == RiskClass.R0:
            return cls(
                risk_class=risk_class,
                required_levels=[ProofLevel.S1],
                minimum_pillars=1,
                requires_alternatives=False,
                requires_guardrails=False
            )
        elif risk_class == RiskClass.R1:
            return cls(
                risk_class=risk_class,
                required_levels=[ProofLevel.S0, ProofLevel.S1],
                minimum_pillars=1,
                requires_alternatives=False,
                requires_guardrails=False
            )
        elif risk_class == RiskClass.R2:
            return cls(
                risk_class=risk_class,
                required_levels=[ProofLevel.S2, ProofLevel.S4],
                minimum_pillars=2,
                requires_alternatives=True,
                requires_guardrails=True
            )
        else:  # R3
            return cls(
                risk_class=risk_class,
                required_levels=[],
                minimum_pillars=0,
                requires_alternatives=False,
                requires_guardrails=True
            )


@dataclass
class Gap:
    """
    Represents an information gap with mandatory decision, test, and impact.
    Enforces the GAP→DECISION→TEST→TERM rule from v1.2.1.
    """
    gap_id: str
    description: str
    decision: str  # Conservative decision/default choice
    test: str  # How to close the gap (PASS/FAIL criteria)
    impact_if_wrong: str  # Impact if the decision is incorrect
    status: str = "À-CLÔTURER"  # Status: PASS, FAIL, or À-CLÔTURER
    
    def validate(self) -> bool:
        """Validate that gap has all required fields"""
        return bool(self.description and self.decision and self.test and self.impact_if_wrong)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert gap to dictionary"""
        return {
            "gap_id": self.gap_id,
            "description": self.description,
            "decision": self.decision,
            "test": self.test,
            "impact_if_wrong": self.impact_if_wrong,
            "status": self.status
        }


@dataclass
class Claim:
    """Represents a claim with origin tag, proof level, and testability"""
    claim_id: str
    text: str
    origin_tag: OriginTag
    proof_level: ProofLevel
    dependencies: List[str]  # List of claim IDs this depends on
    test_description: str
    status: str  # "PASS", "FAIL", "À-CLÔTURER"
    testability: TestabilityLevel = TestabilityLevel.T2
    
    def validate_strong_causality(self) -> bool:
        """
        Validate that strong causality claims have adequate testability.
        Strong causality requires TRACE ≥ T2.
        """
        causality_keywords = ["will cause", "causes", "results in", "leads to", "guarantees"]
        is_causal = any(keyword in self.text.lower() for keyword in causality_keywords)
        
        if is_causal:
            return self.testability in [TestabilityLevel.T2, TestabilityLevel.T3]
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert claim to dictionary for ledger"""
        return {
            "claim_id": self.claim_id,
            "text": self.text,
            "origin_tag": self.origin_tag.value,
            "proof_level": self.proof_level.value,
            "dependencies": self.dependencies,
            "test": self.test_description,
            "status": self.status,
            "testability": self.testability.value
        }


class RiskClassifier:
    """Classifies project risk based on criteria"""
    
    @staticmethod
    def classify(
        has_financial_impact: bool = False,
        has_legal_impact: bool = False,
        has_security_impact: bool = False,
        has_health_impact: bool = False,
        has_pii: bool = False,
        is_illegal: bool = False,
        is_dangerous: bool = False
    ) -> RiskClass:
        """
        Classify risk level based on project characteristics.
        
        Returns:
            RiskClass: R0, R1, R2, or R3
        """
        if is_illegal or is_dangerous:
            return RiskClass.R3
        
        high_impact_factors = [
            has_financial_impact,
            has_legal_impact,
            has_security_impact,
            has_health_impact,
            has_pii
        ]
        
        if any(high_impact_factors):
            return RiskClass.R2
        
        # Default to R1 for operational systems, R0 for low-risk
        return RiskClass.R1


class ProofValidator:
    """Validates proof levels against requirements"""
    
    @staticmethod
    def validate_claim(claim: Claim, risk_class: RiskClass) -> Dict[str, Any]:
        """
        Validate that a claim has adequate proof for the risk class.
        
        Returns:
            Dict with validation results
        """
        proof_budget = ProofBudget.for_risk_class(risk_class)
        
        results = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check origin tag
        if claim.origin_tag == OriginTag.GAP and risk_class in [RiskClass.R2, RiskClass.R3]:
            results["issues"].append(
                f"Claim {claim.claim_id} has GAP origin for high-risk ({risk_class.value}) - must apply GAP→DECISION→TEST→TERM"
            )
            results["valid"] = False
        
        # Check testability for strong causality
        if not claim.validate_strong_causality():
            results["issues"].append(
                f"Claim {claim.claim_id} has strong causality but insufficient testability "
                f"(has {claim.testability.value}, needs ≥T2)"
            )
            results["valid"] = False
        
        # Check proof level adequacy
        if risk_class == RiskClass.R2:
            if claim.proof_level in [ProofLevel.S0, ProofLevel.S1]:
                results["warnings"].append(
                    f"Claim {claim.claim_id} for R2 should have proof level ≥S2 "
                    f"(currently {claim.proof_level.value})"
                )
        
        # Check hypothesis status
        if claim.origin_tag == OriginTag.HYP and claim.status == "À-CLÔTURER":
            results["warnings"].append(
                f"Claim {claim.claim_id} is hypothesis but not yet tested"
            )
        
        return results


class ClaimLedger:
    """Manages a ledger of claims"""
    
    def __init__(self):
        self.claims: Dict[str, Claim] = {}
    
    def add_claim(self, claim: Claim) -> None:
        """Add a claim to the ledger"""
        self.claims[claim.claim_id] = claim
    
    def get_claim(self, claim_id: str) -> Optional[Claim]:
        """Get a claim by ID"""
        return self.claims.get(claim_id)
    
    def validate_all(self, risk_class: RiskClass) -> Dict[str, Any]:
        """Validate all claims in the ledger"""
        validator = ProofValidator()
        all_results = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "claim_validations": {}
        }
        
        for claim_id, claim in self.claims.items():
            result = validator.validate_claim(claim, risk_class)
            all_results["claim_validations"][claim_id] = result
            
            if not result["valid"]:
                all_results["valid"] = False
                all_results["issues"].extend(result["issues"])
            
            all_results["warnings"].extend(result["warnings"])
        
        return all_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about claims in the ledger"""
        total = len(self.claims)
        
        by_status = {"PASS": 0, "FAIL": 0, "À-CLÔTURER": 0}
        by_origin = {tag.value: 0 for tag in OriginTag}
        by_proof = {level.value: 0 for level in ProofLevel}
        
        for claim in self.claims.values():
            by_status[claim.status] = by_status.get(claim.status, 0) + 1
            by_origin[claim.origin_tag.value] += 1
            by_proof[claim.proof_level.value] += 1
        
        return {
            "total_claims": total,
            "by_status": by_status,
            "by_origin": by_origin,
            "by_proof_level": by_proof
        }
    
    def to_markdown_table(self) -> str:
        """Generate markdown table for claim ledger"""
        lines = [
            "| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status |",
            "|----------|------------|------------|---------|--------------|------|--------|"
        ]
        
        for claim in self.claims.values():
            deps = ", ".join(claim.dependencies) if claim.dependencies else "-"
            lines.append(
                f"| {claim.claim_id} | {claim.text[:50]}... | "
                f"[{claim.origin_tag.value}] | {claim.proof_level.name} | "
                f"{deps} | {claim.test_description[:30]}... | {claim.status} |"
            )
        
        return "\n".join(lines)


class GapLedger:
    """Manages a ledger of gaps with mandatory GAP→DECISION→TEST→TERM rule"""
    
    def __init__(self):
        self.gaps: Dict[str, Gap] = {}
    
    def add_gap(self, gap: Gap) -> None:
        """Add a gap to the ledger"""
        if not gap.validate():
            raise ValueError(f"Gap {gap.gap_id} missing required fields (decision, test, or impact)")
        self.gaps[gap.gap_id] = gap
    
    def get_gap(self, gap_id: str) -> Optional[Gap]:
        """Get a gap by ID"""
        return self.gaps.get(gap_id)
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate all gaps - ensure no gap has status À-CLÔTURER without action"""
        results = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        for gap in self.gaps.values():
            if not gap.validate():
                results["valid"] = False
                results["issues"].append(
                    f"Gap {gap.gap_id} missing required fields"
                )
            
            if gap.status == "À-CLÔTURER" and not gap.test:
                results["valid"] = False
                results["issues"].append(
                    f"Gap {gap.gap_id} has status À-CLÔTURER but no test assigned"
                )
        
        return results
    
    def to_markdown_table(self) -> str:
        """Generate markdown table for gap ledger"""
        if not self.gaps:
            return "No gaps identified."
        
        lines = [
            "| Gap-ID | Description | Decision (Conservative) | Test (PASS/FAIL) | Impact if Wrong | Status |",
            "|--------|-------------|-------------------------|------------------|-----------------|--------|"
        ]
        
        for gap in self.gaps.values():
            lines.append(
                f"| {gap.gap_id} | {gap.description[:40]}... | "
                f"{gap.decision[:30]}... | {gap.test[:30]}... | "
                f"{gap.impact_if_wrong[:30]}... | {gap.status} |"
            )
        
        return "\n".join(lines)

