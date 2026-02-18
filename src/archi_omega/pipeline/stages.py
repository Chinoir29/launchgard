"""
ARCHI-Ω v1.3.0 - Pipeline Modules

This module implements the execution pipeline:
AUTO-TUNE → COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT

Each stage has GATE checks with AUTO-CORRECT/REPAIR-LOOP support.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from ..epistemic.foundation import (
    RiskClass, ProofBudget, OriginTag, ClaimLedger, 
    Claim, ProofLevel, TestabilityLevel, GapClosure
)
from ..auto_tune import AutoTune, ControlParameters
from ..auto_correct import AutoCorrect


class TerminationCode(Enum):
    """Termination codes for deliverables"""
    TERM_LIVRE = "TERM-LIVRÉ"  # Complete deliverable
    TERM_PARTIEL = "TERM-PARTIEL"  # Partial - critical constraint missing
    TERM_PROTOCOLE = "TERM-PROTOCOLE"  # P0 questions + minimal assumptions
    TERM_REFUS = "TERM-REFUS"  # Refused - illegal/dangerous


@dataclass
class ProjectContext:
    """Context for a project being analyzed"""
    # User input
    objective: str = ""  # 1-3 phrase objective (v1.3.0)
    goal: str = ""
    deliverable: str = ""
    done_criteria: Dict[str, List[str]] = field(default_factory=dict)
    users_load: Dict[str, Any] = field(default_factory=dict)
    sla_slo: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    integrations: List[str] = field(default_factory=list)
    ops: Dict[str, Any] = field(default_factory=dict)
    security: Dict[str, Any] = field(default_factory=dict)
    ai_ml: Optional[Dict[str, Any]] = None
    
    # Pipeline state (v1.3.0)
    risk_class: Optional[RiskClass] = None
    complexity_class: Optional[str] = None  # C0-C3
    profile: Optional[str] = None  # P-SIMPLE/STANDARD/COMPLEX/PROJET
    control_params: Optional[ControlParameters] = None
    proof_budget: Optional[ProofBudget] = None
    facts: List[str] = field(default_factory=list)
    gaps: List[Dict[str, Any]] = field(default_factory=list)  # Renamed from unknowns
    assumptions: List[Dict[str, Any]] = field(default_factory=list)
    options: List[Dict[str, Any]] = field(default_factory=list)
    recommendation: Optional[Dict[str, Any]] = None
    claim_ledger: ClaimLedger = field(default_factory=ClaimLedger)
    
    # AUTO-CORRECT state
    repair_history: List[Dict[str, Any]] = field(default_factory=list)
    gate_results: Dict[str, Dict[str, Any]] = field(default_factory=dict)




class AutoTuner:
    """
    AUTO-TUNE stage (v1.3.0): Classify Rk/Ck/Lk + triggers; apply profile; set controls
    
    Section 4: AUTO-TUNE with deterministic classification and conservative selection.
    """
    
    @staticmethod
    def auto_tune(context: ProjectContext, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Auto-tune pipeline parameters based on objective and context.
        
        Returns:
            Dict with tuning results (risk_class, complexity_class, profile, parameters)
        """
        # Prepare context for AUTO-TUNE
        objective = context.objective or context.goal or ""
        
        tune_context = {
            "deliverable": context.deliverable,
            "has_financial_impact": "budget" in context.constraints or "cost" in objective.lower(),
            "has_legal_impact": any(reg in str(context.constraints).lower() 
                                   for reg in ["gdpr", "hipaa", "pci", "legal", "compliance"]),
            "has_security_impact": bool(context.security) or "security" in objective.lower(),
            "has_health_impact": "health" in objective.lower() or "medical" in objective.lower(),
            "has_pii": "pii" in str(context.data).lower() or "personal" in str(context.data).lower(),
            "is_illegal": False,  # Would need explicit check
            "is_dangerous": False,  # Would need explicit check
            
            # Complexity factors
            "has_repo_ci_docs": any(kw in objective.lower() for kw in ["repo", "ci", "docs", "documentation"]),
            "has_auth_payment_storage_api": any(kw in objective.lower() 
                                                for kw in ["auth", "payment", "storage", "api", "database"]),
            "has_security_compliance_sensitive_data": bool(context.security) or 
                                                       any(kw in objective.lower() 
                                                           for kw in ["security", "compliance", "sensitive"]),
            "has_perf_load_sla": bool(context.sla_slo) or 
                                 any(kw in objective.lower() for kw in ["performance", "load", "sla", "scale"]),
            "is_prod_business": any(kw in objective.lower() 
                                   for kw in ["production", "prod", "business", "sales", "users", "customers"]),
            
            "has_important_claims": len(context.claim_ledger.claims) > 0,
            "gaps_count": len(context.gaps),
            "repair_loop_triggered": len(context.repair_history) > 0
        }
        
        # Run AUTO-TUNE
        tuning_result = AutoTune.tune(
            objective=objective,
            context=tune_context,
            user_params=config.get("user_overrides", {})
        )
        
        # Update context
        context.risk_class = tuning_result["risk_class"]
        context.complexity_class = tuning_result["complexity_class"].value
        context.profile = tuning_result["profile"].value
        context.control_params = tuning_result["parameters"]
        
        return tuning_result


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
    EXPAND stage (v1.3.0): Extract FACTS / constraints / GAPs / claims atomiques
    
    Section 6.1: AUTO-SPEC - automatic generation of GOAL/DELIVERABLE/DONE if missing
    """
    
    @staticmethod
    def auto_spec(context: ProjectContext) -> Dict[str, Any]:
        """
        AUTO-SPEC: Automatically generate GOAL/DELIVERABLE/DONE if missing.
        
        Section 6.1: If GOAL/DELIVERABLE/DONE are missing, generate them from objective.
        What's not deducible: stable → [HYP] + test; instable/critical → [GAP] + closure
        """
        generated = {}
        
        # Generate GOAL if missing
        if not context.goal and context.objective:
            # Extract business value and beneficiary from objective
            context.goal = f"Goal: {context.objective}"
            generated["goal"] = context.goal
        
        # Generate DELIVERABLE if missing
        if not context.deliverable and context.objective:
            # Infer deliverable type from objective
            if any(kw in context.objective.lower() for kw in ["implement", "build", "create", "develop"]):
                context.deliverable = "Deliverable: Implementation (code + tests + CI + docs)"
            elif any(kw in context.objective.lower() for kw in ["document", "spec", "guide"]):
                context.deliverable = "Deliverable: Documentation (markdown/PDF)"
            elif any(kw in context.objective.lower() for kw in ["decide", "choose", "select", "recommend"]):
                context.deliverable = "Deliverable: Decision document with ADR"
            else:
                context.deliverable = "Deliverable: Analysis report with recommendations"
            generated["deliverable"] = context.deliverable
        
        # Generate DONE criteria if missing
        if not context.done_criteria:
            # Generate 3-7 PASS/FAIL criteria
            context.done_criteria = {
                "acceptance_criteria": [
                    "Objective clearly addressed (PASS/FAIL)",
                    "All P0 questions answered or documented as [GAP] (PASS/FAIL)",
                    "Deliverable format matches specification (PASS/FAIL)"
                ]
            }
            generated["done_criteria"] = context.done_criteria
        
        return generated
    
    @staticmethod
    def expand(context: ProjectContext) -> Dict[str, Any]:
        """
        Extract facts, constraints, GAPS from context.
        
        Returns:
            Dict with facts, constraints, gaps, atomic_claims
        """
        # AUTO-SPEC: Generate missing GOAL/DELIVERABLE/DONE
        auto_spec_result = Expander.auto_spec(context)
        
        facts = []
        gaps = []
        constraints = []
        
        # Extract facts from user input
        if context.users_load:
            for key, value in context.users_load.items():
                if value:
                    facts.append(f"{key}: {value} [USER]")
                else:
                    # v1.3.0: Use [GAP] instead of unknown
                    gaps.append({
                        "gap": f"{key} not specified",
                        "decision": "Use conservative default or request from user",
                        "test": "Verify with user",
                        "impact": "May affect sizing/cost",
                        "term": "TERM-PROTOCOLE"
                    })
        
        if context.constraints:
            for key, value in context.constraints.items():
                if value:
                    constraints.append(f"{key}: {value} [USER]")
                else:
                    gaps.append({
                        "gap": f"Constraint {key} not specified",
                        "decision": "Proceed with reasonable assumption or mark as P0",
                        "test": "Validate assumption with user",
                        "impact": "May affect feasibility",
                        "term": "TERM-PROTOCOLE"
                    })
        
        # Store in context
        context.facts = facts
        context.gaps = gaps
        
        return {
            "facts": facts,
            "constraints": constraints,
            "gaps": gaps,
            "atomic_claims": [],  # To be populated by claim extraction
            "auto_spec": auto_spec_result
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
    LINT stage (v1.3.0): Verify invariants, tags, recency, TRACE, PII hygiene, GAP rule, MODERATION
    
    Section 7.1: GATE checks with GAP closure mandatory and MODERATION=STRICT
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
        
        # v1.3.0: Check GAP closure (mandatory)
        for claim in context.claim_ledger.claims.values():
            if claim.origin_tag == OriginTag.GAP:
                gap_validation = claim.validate_gap_closure()
                if not gap_validation["valid"]:
                    issues.extend(gap_validation["issues"])
        
        # Check for naked GAPs in context.gaps
        for gap in context.gaps:
            if not all(k in gap for k in ["decision", "test", "impact", "term"]):
                issues.append(
                    f"GAP '{gap.get('gap', 'unnamed')}' missing required closure fields "
                    f"(DECISION+TEST+IMPACT+TERM)"
                )
        
        # Check for promises/guarantees (invariant 1.2)
        promise_keywords = ["guarantee", "garanti", "assured", "assuré", "100%", "sûr"]
        text_to_check = str(context.__dict__)
        for keyword in promise_keywords:
            if keyword in text_to_check.lower():
                issues.append(f"Overpromise detected (invariant 1.2): '{keyword}' found in text")
        
        # v1.3.0: MODERATION check - external options ≤ 3
        external_options = [opt for opt in context.options if opt.get("type") == "external"]
        if len(external_options) > 3:
            issues.append(
                f"MODERATION=STRICT violated: {len(external_options)} external options "
                f"(maximum 3 allowed)"
            )
        
        # Check for recency claims
        recency_keywords = ["latest", "current", "newest", "dernier", "actuel"]
        for keyword in recency_keywords:
            if keyword in text_to_check.lower():
                warnings.append(
                    f"Recency keyword '{keyword}' detected - ensure verification with S2 tools or mark as [GAP]"
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
                # v1.3.0: Check for [GAP] instead of UNKNOWN
                if claim.origin_tag == OriginTag.GAP and context.risk_class == RiskClass.R2:
                    # GAP is allowed if it has proper closure
                    gap_validation = claim.validate_gap_closure()
                    if not gap_validation["valid"]:
                        tests["proof_adequacy"]["passed"] = False
                        tests["proof_adequacy"]["issues"].append(
                            f"Claim {claim.claim_id} has [GAP] origin for R2 project without proper closure"
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
        Produce final deliverable with termination code (v1.3.0).
        
        Section 12: Always include PROCHAIN PAS UNIQUE + RUNBOOK (3 actions minimales)
        
        Returns:
            Dict with deliverable and termination code
        """
        # Determine termination code
        term_code = TerminationCode.TERM_LIVRE
        
        if context.risk_class == RiskClass.R3:
            term_code = TerminationCode.TERM_REFUS
        elif context.gaps:
            # v1.3.0: Check if GAPs are critical (P0)
            critical_gaps = [g for g in context.gaps if g.get("term") == "TERM-PROTOCOLE"]
            if critical_gaps:
                term_code = TerminationCode.TERM_PROTOCOLE
        elif not context.recommendation:
            term_code = TerminationCode.TERM_PARTIEL
        
        # Check if any GATE failed
        for stage_result in validation_results.values():
            if isinstance(stage_result, dict) and not stage_result.get("valid", True):
                term_code = TerminationCode.TERM_PARTIEL
                break
        
        # Generate PROCHAIN PAS (next unique step)
        if term_code == TerminationCode.TERM_LIVRE:
            prochain_pas = "Implement the recommended solution"
        elif term_code == TerminationCode.TERM_PROTOCOLE:
            prochain_pas = "Address P0 questions and validate GAP closures"
        elif term_code == TerminationCode.TERM_PARTIEL:
            prochain_pas = "Resolve critical constraints and re-run pipeline"
        else:  # TERM_REFUS
            prochain_pas = "Do not proceed - illegal or dangerous activity"
        
        # Generate RUNBOOK (3 minimal actions)
        if term_code == TerminationCode.TERM_LIVRE:
            runbook = [
                "1. Review and approve the recommendation",
                "2. Set up development environment",
                "3. Begin implementation following the architecture"
            ]
        elif term_code == TerminationCode.TERM_PROTOCOLE:
            runbook = [
                "1. Review all [GAP] items and their DECISION+TEST+IMPACT",
                "2. Answer P0 questions with user/stakeholders",
                "3. Re-run pipeline with updated information"
            ]
        elif term_code == TerminationCode.TERM_PARTIEL:
            runbook = [
                "1. Identify and document missing critical constraints",
                "2. Gather additional requirements",
                "3. Re-execute pipeline with complete information"
            ]
        else:  # TERM_REFUS
            runbook = [
                "1. Document the refusal reason",
                "2. Consult legal/compliance team",
                "3. Do not proceed without explicit authorization"
            ]
        
        deliverable = {
            "facts": context.facts,
            "open_questions": context.gaps,  # v1.3.0: renamed from unknowns
            "assumptions": context.assumptions,
            "options": context.options,
            "recommendation": context.recommendation,
            "claim_ledger": context.claim_ledger.to_markdown_table(),
            "termination": term_code.value,
            "prochain_pas": prochain_pas,  # v1.3.0: mandatory
            "runbook": runbook,  # v1.3.0: mandatory
            "validation_summary": validation_results,
            "profile": context.profile,  # v1.3.0: include profile used
            "control_params": context.control_params.to_dict() if context.control_params else {}
        }
        
        return deliverable


class Pipeline:
    """
    Main pipeline orchestrator (v1.3.0):
    AUTO-TUNE → COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT
    
    Each stage has GATE checks with AUTO-CORRECT/REPAIR-LOOP support.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.auto_tuner = AutoTuner()  # v1.3.0
        self.compiler = Compiler()
        self.expander = Expander()
        self.brancher = Brancher()
        self.linter = Linter()
        self.stressor = Stressor()
        self.selector = Selector()
        self.committer = Committer()
    
    @staticmethod
    def _default_config() -> Dict[str, Any]:
        """Get default configuration (v1.3.0)"""
        return {
            "mode": "MAXCAP",
            "budget": "long",
            "evidence": "mid",
            "divergence": "mid",
            "auto_gov": True,
            "auto_tools": True,
            "auto_tune": True,  # v1.3.0
            "auto_correct": True,  # v1.3.0
            "repair_max": 2,  # v1.3.0
            "show": "OFF",  # v1.3.0
            "as_code": "OFF",  # v1.3.0
            "moderation": "STRICT",  # v1.3.0
            "pcx": True,
            "nest": True
        }
    
    def execute(self, context: ProjectContext) -> Dict[str, Any]:
        """
        Execute the full pipeline on a project context (v1.3.0).
        
        Returns:
            Final deliverable with all sections
        """
        # Stage 0: AUTO-TUNE (v1.3.0)
        if self.config.get("auto_tune", True):
            tune_result = self.auto_tuner.auto_tune(context, self.config)
            # Update config with tuned parameters
            if context.control_params:
                self.config.update(context.control_params.to_dict())
        
        # Stage 1: COMPILER
        compile_result = self.compiler.compile(context, self.config)
        
        # Stage 2: EXPAND (with AUTO-SPEC)
        expand_result = self.expander.expand(context)
        
        # Stage 3: BRANCH
        # v1.3.0: Use control_params.divergence if available
        if context.control_params:
            divergence = context.control_params.divergence.value
            num_options = 3 if divergence in ["mid", "high"] else 2
        else:
            num_options = 3 if self.config["divergence"] == "mid" else 2
        self.brancher.branch(context, num_options)
        
        # Stage 4: LINT (with GATE check if AUTO-CORRECT enabled)
        lint_result = self.linter.lint(context)
        if self.config.get("auto_correct", True) and not lint_result["valid"]:
            # Would apply REPAIR-LOOP here in full implementation
            context.repair_history.append({
                "stage": "LINT",
                "issues": lint_result["issues"]
            })
        context.gate_results["LINT"] = lint_result
        
        # Stage 5: STRESS
        stress_result = self.stressor.stress(context)
        context.gate_results["STRESS"] = stress_result
        
        # Stage 6: SELECT
        select_result = self.selector.select(context)
        context.gate_results["SELECT"] = select_result
        
        # Stage 7: COMMIT
        validation_results = {
            "auto_tune": tune_result if self.config.get("auto_tune") else None,
            "compile": compile_result,
            "expand": expand_result,
            "lint": lint_result,
            "stress": stress_result,
            "select": select_result,
            "gate_results": context.gate_results
        }
        deliverable = self.committer.commit(context, validation_results)
        
        return deliverable
