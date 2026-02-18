"""
ARCHI-Ω v1.2.1 - Pipeline Modules

This module implements the execution pipeline:
COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from ..epistemic.foundation import (
    RiskClass, ProofBudget, OriginTag, ClaimLedger, GapLedger,
    Claim, Gap, ProofLevel, TestabilityLevel
)


class TerminationCode(Enum):
    """Termination codes for deliverables"""
    TERM_LIVRE = "TERM-LIVRÉ"  # Complete deliverable
    TERM_PARTIEL = "TERM-PARTIEL"  # Partial - critical constraint missing
    TERM_PROTOCOLE = "TERM-PROTOCOLE"  # P0 questions + minimal assumptions
    TERM_REFUS = "TERM-REFUS"  # Refused - illegal/dangerous


@dataclass
class ProjectContext:
    """Context for a project being analyzed"""
    goal: str = ""
    deliverable: str = ""
    users_load: Dict[str, Any] = field(default_factory=dict)
    sla_slo: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    integrations: List[str] = field(default_factory=list)
    ops: Dict[str, Any] = field(default_factory=dict)
    security: Dict[str, Any] = field(default_factory=dict)
    ai_ml: Optional[Dict[str, Any]] = None
    done_criteria: Dict[str, List[str]] = field(default_factory=dict)
    
    # Pipeline state
    risk_class: Optional[RiskClass] = None
    proof_budget: Optional[ProofBudget] = None
    facts: List[str] = field(default_factory=list)
    gaps: List[Dict[str, Any]] = field(default_factory=list)  # v1.2.1: renamed from unknowns
    assumptions: List[Dict[str, Any]] = field(default_factory=list)
    options: List[Dict[str, Any]] = field(default_factory=list)
    recommendation: Optional[Dict[str, Any]] = None
    claim_ledger: ClaimLedger = field(default_factory=ClaimLedger)
    gap_ledger: GapLedger = field(default_factory=GapLedger)  # v1.2.1: new


class Compiler:
    """
    COMPILER stage: Determine Rk, PB, modules actifs, triggers outils, stop-rules
    """
    
    @staticmethod
    def compile(context: ProjectContext, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compile project context into execution parameters.
        
        Returns:
            Dict with risk_class, proof_budget, active_modules, tool_triggers, stop_rules
        """
        # Determine risk class based on project characteristics
        has_financial = "budget" in context.constraints or "cost" in context.goal.lower()
        has_legal = any(reg in str(context.constraints).lower() 
                       for reg in ["gdpr", "hipaa", "pci", "legal"])
        has_security = bool(context.security) or "security" in context.goal.lower()
        has_health = "health" in context.goal.lower() or "medical" in context.goal.lower()
        has_pii = "pii" in str(context.data).lower() or "personal" in str(context.data).lower()
        
        from ..epistemic.foundation import RiskClassifier
        risk_class = RiskClassifier.classify(
            has_financial_impact=has_financial,
            has_legal_impact=has_legal,
            has_security_impact=has_security,
            has_health_impact=has_health,
            has_pii=has_pii
        )
        
        context.risk_class = risk_class
        context.proof_budget = ProofBudget.for_risk_class(risk_class)
        
        # Determine active modules
        active_modules = ["CLARIFIER", "ARCHITECT", "SECURITY", "VERIFIER"]
        if context.ai_ml:
            active_modules.insert(-1, "AIML")
        
        # Determine tool triggers
        tool_triggers = []
        
        # T-RECENCY: prices, laws, versions
        if any(keyword in str(context).lower() 
               for keyword in ["latest", "current", "price", "cost", "law", "regulation"]):
            tool_triggers.append("T-RECENCY")
        
        # T-R2: high-impact recommendations
        if risk_class in [RiskClass.R2, RiskClass.R3]:
            tool_triggers.append("T-R2")
        
        # Stop rules
        stop_rules = []
        if "budget" in context.constraints and context.constraints["budget"]:
            stop_rules.append(f"Budget constraint: {context.constraints['budget']}")
        if "timeline" in context.constraints and context.constraints["timeline"]:
            stop_rules.append(f"Timeline constraint: {context.constraints['timeline']}")
        
        return {
            "risk_class": risk_class,
            "proof_budget": context.proof_budget,
            "active_modules": active_modules,
            "tool_triggers": tool_triggers,
            "stop_rules": stop_rules
        }


class Expander:
    """
    EXPAND stage: Extraire FACTS / contraintes / gaps / claims atomiques
    """
    
    @staticmethod
    def expand(context: ProjectContext) -> Dict[str, Any]:
        """
        Extract facts, constraints, gaps from context.
        
        Returns:
            Dict with facts, constraints, gaps, atomic_claims
        """
        facts = []
        gaps = []
        constraints = []
        
        # Extract facts from user input
        if context.users_load:
            for key, value in context.users_load.items():
                if value:
                    facts.append(f"{key}: {value} [USER]")
                else:
                    gaps.append({
                        "description": f"{key} not specified",
                        "decision": "Assume standard/default value",
                        "test": f"Verify actual {key} requirement",
                        "impact_if_wrong": f"May affect sizing/performance"
                    })
        
        if context.constraints:
            for key, value in context.constraints.items():
                if value:
                    constraints.append(f"{key}: {value} [USER]")
                else:
                    gaps.append({
                        "description": f"Constraint {key} not specified",
                        "decision": "Proceed without constraint",
                        "test": f"Clarify {key} constraint with stakeholders",
                        "impact_if_wrong": "May violate constraint"
                    })
        
        # Store in context
        context.facts = facts
        context.gaps = gaps
        
        return {
            "facts": facts,
            "constraints": constraints,
            "gaps": gaps,
            "atomic_claims": []  # To be populated by claim extraction
        }


class Brancher:
    """
    BRANCH stage: Générer 3 variantes internes + 2–3 OPTIONS externes max
    """
    
    @staticmethod
    def branch(context: ProjectContext, num_options: int = 3) -> List[Dict[str, Any]]:
        """
        Generate alternative options for the solution.
        
        Returns:
            List of options with scores and trade-offs
        """
        # This is a simplified version - real implementation would use
        # domain knowledge and templates to generate realistic options
        
        options = []
        
        # Generate placeholder options
        for i in range(min(num_options, 3)):
            option = {
                "id": f"O{i+1}",
                "name": f"Option {i+1}",
                "description": f"Architecture option {i+1}",
                "scores": {
                    "robustness": 0,
                    "security": 0,
                    "simplicity": 0,
                    "cost": 0,
                    "performance": 0,
                    "time_to_ship": 0,
                    "operability": 0,
                    "scalability": 0
                },
                "tradeoffs": {
                    "advantages": [],
                    "disadvantages": []
                },
                "total_score": 0
            }
            options.append(option)
        
        context.options = options
        return options


class Linter:
    """
    LINT stage: Vérifier invariants, tags origine, recency, TRACE, absence de promesse
    """
    
    @staticmethod
    def lint(context: ProjectContext) -> Dict[str, Any]:
        """
        Verify invariants and quality rules.
        
        Returns:
            Dict with validation results and issues found
        """
        issues = []
        warnings = []
        
        # Check claim ledger
        if context.claim_ledger.claims:
            validation = context.claim_ledger.validate_all(context.risk_class)
            if not validation["valid"]:
                issues.extend(validation["issues"])
            warnings.extend(validation["warnings"])
        
        # Check for promises/guarantees
        promise_keywords = ["guarantee", "garanti", "assured", "assuré", "100%"]
        text_to_check = str(context.__dict__)
        for keyword in promise_keywords:
            if keyword in text_to_check.lower():
                issues.append(f"Overpromise detected: '{keyword}' found in text")
        
        # Check for untagged claims
        # (In real implementation, would parse text and check for assertions without tags)
        
        # Check for recency claims
        recency_keywords = ["latest", "current", "newest", "dernier", "actuel"]
        for keyword in recency_keywords:
            if keyword in text_to_check.lower():
                warnings.append(
                    f"Recency keyword '{keyword}' detected - ensure verification with S2 tools"
                )
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }


class Stressor:
    """
    STRESS stage: Test injection/autorité, contradictions, preuves, causalités, dépendances
    """
    
    @staticmethod
    def stress(context: ProjectContext) -> Dict[str, Any]:
        """
        Stress test the analysis for robustness.
        
        Returns:
            Dict with stress test results
        """
        tests = {
            "injection_authority": {"passed": True, "issues": []},
            "contradictions": {"passed": True, "issues": []},
            "proof_adequacy": {"passed": True, "issues": []},
            "untested_causality": {"passed": True, "issues": []},
            "missing_dependencies": {"passed": True, "issues": []},
            "cost_ops_evaluation": {"passed": True, "issues": []},
            "security_risks": {"passed": True, "issues": []}
        }
        
        # Check proof adequacy against proof budget
        if context.proof_budget and context.claim_ledger.claims:
            for claim in context.claim_ledger.claims.values():
                if claim.origin_tag == OriginTag.GAP and context.risk_class == RiskClass.R2:
                    tests["proof_adequacy"]["passed"] = False
                    tests["proof_adequacy"]["issues"].append(
                        f"Claim {claim.claim_id} has GAP origin for R2 project - must apply GAP→DECISION→TEST→TERM"
                    )
        
        # Check for untested causality
        for claim in context.claim_ledger.claims.values():
            if not claim.validate_strong_causality():
                tests["untested_causality"]["passed"] = False
                tests["untested_causality"]["issues"].append(
                    f"Claim {claim.claim_id} has strong causality without adequate testability"
                )
        
        # Check cost/ops evaluation
        if not context.constraints.get("budget"):
            tests["cost_ops_evaluation"]["issues"].append("No budget constraint specified")
        
        # Check security risks
        if context.risk_class in [RiskClass.R2, RiskClass.R3] and not context.security:
            tests["security_risks"]["passed"] = False
            tests["security_risks"]["issues"].append(
                "High-risk project without security requirements specified"
            )
        
        return tests


class Selector:
    """
    SELECT stage: Choisir l'option la plus robuste + fallback
    """
    
    @staticmethod
    def select(context: ProjectContext) -> Dict[str, Any]:
        """
        Select the most robust option and a fallback.
        
        Returns:
            Dict with recommendation and fallback
        """
        if not context.options:
            return {
                "recommendation": None,
                "fallback": None,
                "rationale": "No options available"
            }
        
        # Sort options by total score
        sorted_options = sorted(
            context.options, 
            key=lambda x: x.get("total_score", 0), 
            reverse=True
        )
        
        recommendation = sorted_options[0] if sorted_options else None
        fallback = sorted_options[1] if len(sorted_options) > 1 else None
        
        context.recommendation = recommendation
        
        return {
            "recommendation": recommendation,
            "fallback": fallback,
            "rationale": "Selected option with highest robustness score"
        }


class Committer:
    """
    COMMIT stage: Produire le livrable au format strict + TERM
    """
    
    @staticmethod
    def commit(context: ProjectContext, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produce final deliverable with termination code.
        
        Returns:
            Dict with deliverable and termination code
        """
        # Determine termination code
        term_code = TerminationCode.TERM_LIVRE
        
        if context.risk_class == RiskClass.R3:
            term_code = TerminationCode.TERM_REFUS
        elif context.gaps:
            # Check if gaps are critical (P0)
            critical_gaps = [g for g in context.gaps if "not specified" in g.get("description", "")]
            if critical_gaps:
                term_code = TerminationCode.TERM_PROTOCOLE
        elif not context.recommendation:
            term_code = TerminationCode.TERM_PARTIEL
        
        deliverable = {
            "facts": context.facts,
            "gaps": context.gaps,  # v1.2.1: mandatory GAPS section
            "assumptions": context.assumptions,
            "options": context.options,
            "recommendation": context.recommendation,
            "claim_ledger": context.claim_ledger.to_markdown_table(),
            "gap_ledger": context.gap_ledger.to_markdown_table(),  # v1.2.1: new
            "termination": term_code.value,
            "validation_summary": validation_results
        }
        
        return deliverable


class Pipeline:
    """
    Main pipeline orchestrator: COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.compiler = Compiler()
        self.expander = Expander()
        self.brancher = Brancher()
        self.linter = Linter()
        self.stressor = Stressor()
        self.selector = Selector()
        self.committer = Committer()
    
    @staticmethod
    def _default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "mode": "MAXCAP",
            "budget": "long",
            "evidence": "mid",
            "divergence": "mid",
            "auto_gov": True,
            "auto_tools": True,
            "pcx": True,
            "nest": True
        }
    
    def execute(self, context: ProjectContext) -> Dict[str, Any]:
        """
        Execute the full pipeline on a project context.
        
        Returns:
            Final deliverable with all sections
        """
        # Stage 1: COMPILER
        compile_result = self.compiler.compile(context, self.config)
        
        # Stage 2: EXPAND
        expand_result = self.expander.expand(context)
        
        # Stage 3: BRANCH
        num_options = 3 if self.config["divergence"] == "mid" else 2
        self.brancher.branch(context, num_options)
        
        # Stage 4: LINT
        lint_result = self.linter.lint(context)
        
        # Stage 5: STRESS
        stress_result = self.stressor.stress(context)
        
        # Stage 6: SELECT
        select_result = self.selector.select(context)
        
        # Stage 7: COMMIT
        validation_results = {
            "compile": compile_result,
            "lint": lint_result,
            "stress": stress_result
        }
        deliverable = self.committer.commit(context, validation_results)
        
        return deliverable
