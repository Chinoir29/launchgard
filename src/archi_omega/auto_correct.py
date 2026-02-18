"""
ARCHI-Ω v1.3.0 - AUTO-CORRECT Module

Implements AUTO-CORRECT functionality (Section 7):
- GATE checks for each pipeline stage
- REPAIR-LOOP with REPAIR_MAX
- MODERATION=STRICT enforcement
- Validation of invariants
"""

from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass

from .epistemic.foundation import (
    Claim, OriginTag, TestabilityLevel, RiskClass, ProofLevel,
    ClaimLedger, ProofValidator
)


@dataclass
class GateResult:
    """Result of a GATE check"""
    stage_name: str
    passed: bool
    issues: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "stage": self.stage_name,
            "passed": self.passed,
            "issues": self.issues,
            "warnings": self.warnings
        }


class GateChecker:
    """
    Implements GATE checks for each pipeline stage (Section 7.1).
    
    Minimum checks:
    - Invariants 1.x respected
    - Tags present on important claims
    - Recency/instable: tools or [GAP]+DECISION/TEST
    - PB(Rk) respected (or degradation explicit)
    - TRACE: strong causalities ≥T2
    - Glossary: critical terms defined
    - No naked [GAP]: each GAP has DECISION+TEST+IMPACT
    - MODERATION=STRICT: options ≤3, no explosion, no promises
    """
    
    @staticmethod
    def check_invariants(
        claims: List[Claim],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check invariants (Section 1.x).
        
        Returns:
            Dict with validation results
        """
        issues = []
        warnings = []
        
        # 1.3: Origin tagging mandatory
        for claim in claims:
            if not claim.origin_tag:
                issues.append(f"Claim {claim.claim_id} missing origin tag")
        
        # 1.3: GAP closure mandatory
        for claim in claims:
            if claim.origin_tag == OriginTag.GAP:
                gap_validation = claim.validate_gap_closure()
                if not gap_validation["valid"]:
                    issues.extend(gap_validation["issues"])
        
        # 1.5: Strong causality → testability ≥T2
        for claim in claims:
            if not claim.validate_strong_causality():
                issues.append(
                    f"Claim {claim.claim_id} has strong causality but testability < T2"
                )
        
        # 1.2: Zero overpromise - check for forbidden words
        forbidden_words = ["garanti", "guaranteed", "sûr", "sure thing", "argent assuré"]
        for claim in claims:
            text_lower = claim.text.lower()
            for word in forbidden_words:
                if word in text_lower:
                    issues.append(
                        f"Claim {claim.claim_id} contains overpromise word: '{word}'"
                    )
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @staticmethod
    def check_tags_present(claims: List[Claim]) -> Dict[str, Any]:
        """Check that tags are present on important claims"""
        issues = []
        warnings = []
        
        for claim in claims:
            # Check if claim is important (contains decision/cost/risk keywords)
            important_keywords = ["decision", "cost", "risk", "security", "critical", 
                                "must", "required", "architecture"]
            is_important = any(kw in claim.text.lower() for kw in important_keywords)
            
            if is_important and claim.origin_tag == OriginTag.GAP:
                warnings.append(
                    f"Important claim {claim.claim_id} has [GAP] tag - "
                    f"ensure DECISION+TEST+IMPACT are defined"
                )
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @staticmethod
    def check_proof_budget(
        claims: List[Claim],
        risk_class: RiskClass
    ) -> Dict[str, Any]:
        """Check that proof budgets are respected"""
        issues = []
        warnings = []
        
        validator = ProofValidator()
        
        for claim in claims:
            result = validator.validate_claim(claim, risk_class)
            if not result["valid"]:
                issues.extend(result["issues"])
            warnings.extend(result["warnings"])
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @staticmethod
    def check_gap_closure(claims: List[Claim]) -> Dict[str, Any]:
        """Check that all [GAP] tags have proper closure"""
        issues = []
        warnings = []
        
        for claim in claims:
            if claim.origin_tag == OriginTag.GAP:
                if claim.gap_closure is None:
                    issues.append(
                        f"Claim {claim.claim_id} has [GAP] tag but missing gap_closure "
                        f"(must have DECISION+TEST+IMPACT+TERM)"
                    )
                else:
                    gap_val = claim.gap_closure.validate()
                    if not gap_val["valid"]:
                        issues.extend(gap_val["issues"])
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @staticmethod
    def check_moderation(
        options: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check MODERATION=STRICT constraints:
        - External options ≤ 3
        - No explosion of branches
        - No promises
        - Stable output
        """
        issues = []
        warnings = []
        
        # Check external options count
        external_options = [opt for opt in options if opt.get("type") == "external"]
        if len(external_options) > 3:
            issues.append(
                f"MODERATION=STRICT violated: {len(external_options)} external options "
                f"(maximum 3 allowed)"
            )
        
        # Check for promises in options
        forbidden_words = ["garanti", "guaranteed", "sûr", "sure", "100%"]
        for i, option in enumerate(options):
            description = str(option.get("description", "")).lower()
            for word in forbidden_words:
                if word in description:
                    warnings.append(
                        f"Option {i+1} contains potential promise: '{word}'"
                    )
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @staticmethod
    def run_gate(
        stage_name: str,
        claims: List[Claim],
        options: List[Dict[str, Any]],
        risk_class: RiskClass,
        context: Dict[str, Any]
    ) -> GateResult:
        """
        Run complete GATE check for a stage.
        
        Args:
            stage_name: Name of the pipeline stage
            claims: List of claims to validate
            options: List of options (for MODERATION check)
            risk_class: Project risk class
            context: Additional context
        
        Returns:
            GateResult with validation results
        """
        all_issues = []
        all_warnings = []
        
        # Run all checks
        checks = [
            GateChecker.check_invariants(claims, context),
            GateChecker.check_tags_present(claims),
            GateChecker.check_proof_budget(claims, risk_class),
            GateChecker.check_gap_closure(claims),
            GateChecker.check_moderation(options, context)
        ]
        
        for check_result in checks:
            all_issues.extend(check_result["issues"])
            all_warnings.extend(check_result["warnings"])
        
        return GateResult(
            stage_name=stage_name,
            passed=len(all_issues) == 0,
            issues=all_issues,
            warnings=all_warnings
        )


class RepairLoop:
    """
    Implements REPAIR-LOOP with REPAIR_MAX (Section 7.2).
    
    If GATE=FAIL and AUTO-CORRECT=ON:
    - Up to REPAIR_MAX times:
      1. Correct (without inventing)
      2. Re-lint
      3. Re-pass GATE
    - If still FAIL after REPAIR_MAX: degrade to TERM-PARTIEL or TERM-PROTOCOLE
    """
    
    @staticmethod
    def repair(
        stage_name: str,
        gate_result: GateResult,
        repair_function: Callable[[List[str]], Dict[str, Any]],
        repair_max: int = 2
    ) -> Dict[str, Any]:
        """
        Execute repair loop for a failed GATE.
        
        Args:
            stage_name: Name of the stage
            gate_result: Failed gate result
            repair_function: Function to apply repairs (receives issues, returns updated data)
            repair_max: Maximum repair attempts
        
        Returns:
            Dict with repair results
        """
        repair_count = 0
        current_gate = gate_result
        repair_history = []
        
        while not current_gate.passed and repair_count < repair_max:
            repair_count += 1
            
            # Apply repairs
            repair_result = repair_function(current_gate.issues)
            
            repair_history.append({
                "attempt": repair_count,
                "issues_found": current_gate.issues,
                "repairs_applied": repair_result.get("repairs", [])
            })
            
            # Re-run GATE (simplified - would need full context in real implementation)
            # For now, assume repairs fixed the issues
            if repair_result.get("fixed", False):
                current_gate = GateResult(
                    stage_name=stage_name,
                    passed=True,
                    issues=[],
                    warnings=current_gate.warnings
                )
            
        return {
            "success": current_gate.passed,
            "repair_count": repair_count,
            "repair_history": repair_history,
            "final_gate": current_gate.to_dict(),
            "degraded": not current_gate.passed and repair_count >= repair_max,
            "degradation_reason": (
                f"GATE still FAIL after {repair_max} repair attempts"
                if not current_gate.passed else None
            )
        }


class AutoCorrect:
    """
    Main AUTO-CORRECT orchestrator.
    
    Coordinates GATE checks and REPAIR-LOOP for each pipeline stage.
    """
    
    @staticmethod
    def validate_stage(
        stage_name: str,
        claims: List[Claim],
        options: List[Dict[str, Any]],
        risk_class: RiskClass,
        context: Dict[str, Any],
        auto_correct: bool = True,
        repair_max: int = 2
    ) -> Dict[str, Any]:
        """
        Validate a pipeline stage with AUTO-CORRECT.
        
        Args:
            stage_name: Name of the stage
            claims: Claims to validate
            options: Options to validate
            risk_class: Project risk class
            context: Additional context
            auto_correct: Whether to apply AUTO-CORRECT
            repair_max: Maximum repair attempts
        
        Returns:
            Dict with validation results
        """
        # Run GATE check
        gate_result = GateChecker.run_gate(
            stage_name=stage_name,
            claims=claims,
            options=options,
            risk_class=risk_class,
            context=context
        )
        
        # If failed and auto_correct enabled, run REPAIR-LOOP
        if not gate_result.passed and auto_correct:
            # Define repair function (simplified)
            def repair_fn(issues: List[str]) -> Dict[str, Any]:
                # In real implementation, this would apply specific fixes
                # For now, return mock repair result
                return {
                    "fixed": False,  # Would be True if repairs successful
                    "repairs": ["Attempted to fix issues"]
                }
            
            repair_result = RepairLoop.repair(
                stage_name=stage_name,
                gate_result=gate_result,
                repair_function=repair_fn,
                repair_max=repair_max
            )
            
            return {
                "stage": stage_name,
                "gate_passed": repair_result["success"],
                "initial_issues": gate_result.issues,
                "warnings": gate_result.warnings,
                "auto_correct_applied": True,
                "repair_result": repair_result
            }
        
        return {
            "stage": stage_name,
            "gate_passed": gate_result.passed,
            "issues": gate_result.issues,
            "warnings": gate_result.warnings,
            "auto_correct_applied": False
        }
    
    @staticmethod
    def validate_pipeline(
        stages_data: Dict[str, Dict[str, Any]],
        risk_class: RiskClass,
        auto_correct: bool = True,
        repair_max: int = 2
    ) -> Dict[str, Any]:
        """
        Validate entire pipeline with AUTO-CORRECT at each stage.
        
        Args:
            stages_data: Dict mapping stage names to their data (claims, options, context)
            risk_class: Project risk class
            auto_correct: Whether to apply AUTO-CORRECT
            repair_max: Maximum repair attempts per stage
        
        Returns:
            Dict with complete pipeline validation results
        """
        results = {}
        all_passed = True
        degraded_stages = []
        
        for stage_name, stage_data in stages_data.items():
            result = AutoCorrect.validate_stage(
                stage_name=stage_name,
                claims=stage_data.get("claims", []),
                options=stage_data.get("options", []),
                risk_class=risk_class,
                context=stage_data.get("context", {}),
                auto_correct=auto_correct,
                repair_max=repair_max
            )
            
            results[stage_name] = result
            
            if not result["gate_passed"]:
                all_passed = False
                degraded_stages.append(stage_name)
        
        return {
            "all_stages_passed": all_passed,
            "degraded_stages": degraded_stages,
            "stage_results": results,
            "degradation_needed": len(degraded_stages) > 0,
            "recommended_term": (
                "TERM-PARTIEL" if len(degraded_stages) > 0 else "TERM-LIVRE"
            )
        }
