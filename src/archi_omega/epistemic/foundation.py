"""
ARCHI-Ω v1.3.0 - Epistemic Foundation

This module implements the epistemic foundation of the ARCHI-Ω framework:
- Proof levels (S0-S4)
- Risk classes (R0-R3)
- Complexity classes (C0-C3)
- Proof budgets
- Testability levels (T0-T3)
- Origin tags with [GAP] mandatory closure
- Profile selection (P-SIMPLE/STANDARD/COMPLEX/PROJET)
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
    USER = "USER"  # User-provided information (explicit in chat)
    DED = "DED"  # Deduced from available information (explicit chain, no jumps)
    HYP = "HYP"  # Hypothesis - proposed (not proven) with impact/risk + test
    GAP = "GAP"  # Information missing / unstable / not verifiable here and now


class ComplexityClass(Enum):
    """Complexity classification (C0-C3)"""
    C0 = "trivial"  # Trivial task
    C1 = "simple"  # Simple single deliverable (skeleton repo, short doc)
    C2 = "moderate"  # Multiple components/CI/tests/integrations
    C3 = "complex"  # Complete product / security / scale / multi-phase → PROJET


class Profile(Enum):
    """Profile classification based on Rk/Ck"""
    P_SIMPLE = "P-SIMPLE"  # R0-R1 & C0-C1
    P_STANDARD = "P-STANDARD"  # R1 or C1-C2
    P_COMPLEX = "P-COMPLEX"  # R2 or C2-C3
    P_PROJET = "P-PROJET"  # C3 or multi-phase objective


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
    gap_closure: Optional['GapClosure'] = None  # Required if origin_tag == GAP
    
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
    
    def validate_gap_closure(self) -> Dict[str, Any]:
        """
        Validate that GAP tags have mandatory closure.
        RULE: A [GAP] can never be "the end" - must have DECISION+TEST+IMPACT+TERM
        """
        if self.origin_tag == OriginTag.GAP:
            if self.gap_closure is None:
                return {
                    "valid": False,
                    "issues": [f"Claim {self.claim_id} has [GAP] tag but missing gap_closure (DECISION+TEST+IMPACT+TERM)"]
                }
            return self.gap_closure.validate()
        return {"valid": True, "issues": []}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert claim to dictionary for ledger"""
        result = {
            "claim_id": self.claim_id,
            "text": self.text,
            "origin_tag": self.origin_tag.value,
            "proof_level": self.proof_level.value,
            "dependencies": self.dependencies,
            "test": self.test_description,
            "status": self.status,
            "testability": self.testability.value
        }
        
        if self.gap_closure:
            result["gap_closure"] = self.gap_closure.to_dict()
        
        return result


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


class ComplexityClassifier:
    """
    Classifies project complexity (C0-C3) using additive heuristic.
    Section 4.1: fail-closed approach with deterministic scoring.
    """
    
    @staticmethod
    def classify(
        has_repo_ci_docs: bool = False,
        has_auth_payment_storage_api: bool = False,
        has_security_compliance_sensitive_data: bool = False,
        has_perf_load_sla: bool = False,
        is_prod_business: bool = False
    ) -> ComplexityClass:
        """
        Classify complexity using additive scoring (fail-closed).
        
        Heuristic:
        +1 if repo+CI+docs
        +1 if auth/payment/storage/API externe
        +1 if security/compliance/sensitive data
        +1 if perf/load/SLA
        +1 if "prod/sales/users/business"
        
        Mapping: 0-1→C1; 2-3→C2; ≥4→C3
        
        Returns:
            ComplexityClass: C0, C1, C2, or C3
        """
        score = 0
        
        if has_repo_ci_docs:
            score += 1
        if has_auth_payment_storage_api:
            score += 1
        if has_security_compliance_sensitive_data:
            score += 1
        if has_perf_load_sla:
            score += 1
        if is_prod_business:
            score += 1
        
        if score == 0:
            return ComplexityClass.C0  # Trivial
        elif score <= 1:
            return ComplexityClass.C1  # Simple
        elif score <= 3:
            return ComplexityClass.C2  # Moderate
        else:  # score >= 4
            return ComplexityClass.C3  # Complex


class ProfileSelector:
    """
    Selects appropriate profile (P-SIMPLE/STANDARD/COMPLEX/PROJET) based on Rk/Ck.
    Section 4.2-4.3: Conservative choice if doubt.
    """
    
    @staticmethod
    def select_profile(risk_class: RiskClass, complexity_class: ComplexityClass) -> Profile:
        """
        Select profile based on risk and complexity.
        
        Rules:
        - P-SIMPLE: R0-R1 & C0-C1
        - P-STANDARD: R1 or C1-C2
        - P-COMPLEX: R2 or C2-C3
        - P-PROJET: C3 or multi-phase
        
        Conservative: if in doubt, select higher profile.
        
        Returns:
            Profile: Selected profile
        """
        # C3 always triggers P-PROJET
        if complexity_class == ComplexityClass.C3:
            return Profile.P_PROJET
        
        # R2 always triggers P-COMPLEX (high risk)
        if risk_class == RiskClass.R2:
            return Profile.P_COMPLEX
        
        # R3 would be TERM-REFUS, but handle conservatively as P-COMPLEX
        if risk_class == RiskClass.R3:
            return Profile.P_COMPLEX
        
        # C2 → P-STANDARD or P-COMPLEX
        if complexity_class == ComplexityClass.C2:
            return Profile.P_COMPLEX if risk_class == RiskClass.R2 else Profile.P_STANDARD
        
        # C1 with R1 → P-STANDARD
        if complexity_class == ComplexityClass.C1 and risk_class == RiskClass.R1:
            return Profile.P_STANDARD
        
        # C0-C1 with R0-R1 → P-SIMPLE
        if complexity_class in [ComplexityClass.C0, ComplexityClass.C1] and \
           risk_class in [RiskClass.R0, RiskClass.R1]:
            return Profile.P_SIMPLE
        
        # Default conservative: P-STANDARD
        return Profile.P_STANDARD


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
        
        # Check GAP closure (mandatory in v1.3.0)
        gap_validation = claim.validate_gap_closure()
        if not gap_validation["valid"]:
            results["issues"].extend(gap_validation["issues"])
            results["valid"] = False
        
        # Check origin tag
        if claim.origin_tag == OriginTag.GAP and risk_class in [RiskClass.R2, RiskClass.R3]:
            results["warnings"].append(
                f"Claim {claim.claim_id} has [GAP] origin for high-risk ({risk_class.value}) - "
                f"ensure DECISION is conservative and TEST is defined"
            )
        
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
        
        # Check for invalid status
        if claim.status not in ["PASS", "FAIL", "À-CLÔTURER"]:
            results["issues"].append(
                f"Claim {claim.claim_id} has invalid status '{claim.status}' "
                f"(must be PASS, FAIL, or À-CLÔTURER)"
            )
            results["valid"] = False
        
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
        gaps_count = 0
        gaps_with_closure = 0
        
        for claim in self.claims.values():
            by_status[claim.status] = by_status.get(claim.status, 0) + 1
            by_origin[claim.origin_tag.value] += 1
            by_proof[claim.proof_level.value] += 1
            
            if claim.origin_tag == OriginTag.GAP:
                gaps_count += 1
                if claim.gap_closure is not None:
                    gaps_with_closure += 1
        
        return {
            "total_claims": total,
            "by_status": by_status,
            "by_origin": by_origin,
            "by_proof_level": by_proof,
            "gaps_total": gaps_count,
            "gaps_with_closure": gaps_with_closure,
            "gaps_without_closure": gaps_count - gaps_with_closure
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
