"""
ARCHI-Ω v1.3.0 - AUTO-TUNE Module

Implements AUTO-TUNE functionality (Section 4):
- Auto-classification of Rk (risk), Ck (complexity), Lk (deliverable type)
- Profile selection (P-SIMPLE/STANDARD/COMPLEX/PROJET)
- Auto-adjustment of control parameters based on profile
- Auto-AS-CODE and Auto-SHOW logic
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .epistemic.foundation import (
    RiskClass, RiskClassifier,
    ComplexityClass, ComplexityClassifier,
    Profile, ProfileSelector
)


class DeliverableType(Enum):
    """Deliverable type (Lk)"""
    REPO_CODE = "repo/code"
    DOC = "doc"
    DECISION = "decision"
    AUDIT = "audit"
    PLAN = "plan"
    MIXED = "mixed"


class Mode(Enum):
    """Execution mode"""
    LIGHT = "LIGHT"  # Minimal
    MAX = "MAX"  # Complete standard
    MAXCAP = "MAXCAP"  # Complete + stress + auto-correct, no branch explosion
    PROJET = "PROJET"  # Multi-phase pipeline


class Budget(Enum):
    """Budget configuration"""
    COURT = "court"  # Short
    MOYEN = "moyen"  # Medium
    LONG = "long"  # Long


class Evidence(Enum):
    """Evidence level"""
    LOW = "low"  # S0/S1
    MID = "mid"  # S2/S3 if triggered
    HIGH = "high"  # S2+S4


class Divergence(Enum):
    """Divergence level (number of alternatives)"""
    LOW = "low"  # 1-2
    MID = "mid"  # 2-3
    HIGH = "high"  # 3 max (with MODERATION)


@dataclass
class ControlParameters:
    """Control parameters for framework execution"""
    mode: Mode = Mode.MAXCAP
    budget: Budget = Budget.LONG
    evidence: Evidence = Evidence.MID
    divergence: Divergence = Divergence.MID
    cross: bool = True  # Cross-check support/attack/dependencies
    pcx: bool = True  # Proof cross-check
    nest: bool = True  # Nested mini-cycles
    auto_gov: bool = True  # Execute pipeline without asking
    auto_tools: bool = True  # Use tools when required
    auto_tune: bool = True  # Auto-adjust parameters
    auto_correct: bool = True  # GATES + REPAIR-LOOP
    repair_max: int = 2  # Max corrections per stage
    show: str = "OFF"  # OFF | STATE
    as_code: str = "OFF"  # OFF | ON | auto
    moderation: str = "STRICT"  # STRICT = no promises, no invention, etc.
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "mode": self.mode.value,
            "budget": self.budget.value,
            "evidence": self.evidence.value,
            "divergence": self.divergence.value,
            "cross": "ON" if self.cross else "OFF",
            "pcx": "ON" if self.pcx else "OFF",
            "nest": "ON" if self.nest else "OFF",
            "auto_gov": "ON" if self.auto_gov else "OFF",
            "auto_tools": "ON" if self.auto_tools else "OFF",
            "auto_tune": "ON" if self.auto_tune else "OFF",
            "auto_correct": "ON" if self.auto_correct else "OFF",
            "repair_max": self.repair_max,
            "show": self.show,
            "as_code": self.as_code,
            "moderation": self.moderation
        }


class AutoTune:
    """
    AUTO-TUNE: Automatically adjust control parameters based on objective and context.
    
    Implements Section 4: AUTO-TUNE logic with deterministic classification
    and conservative profile selection.
    """
    
    @staticmethod
    def classify_deliverable_type(objective: str, deliverable: Optional[str] = None) -> DeliverableType:
        """
        Classify deliverable type (Lk) based on objective and deliverable description.
        
        Keywords for classification:
        - repo/code: repo, code, CI, workflow, YAML, package, CLI, infra
        - doc: documentation, guide, spec, README
        - decision: decision, choice, recommendation, ADR
        - audit: audit, review, assessment, analysis
        - plan: plan, roadmap, timeline, schedule
        """
        text = (objective + " " + (deliverable or "")).lower()
        
        code_keywords = ["repo", "code", "ci", "workflow", "yaml", "package", "cli", "infra", "api", "implement"]
        doc_keywords = ["documentation", "guide", "spec", "readme", "doc ", "docs"]
        decision_keywords = ["decision", "choice", "recommendation", "adr", "choose", "select"]
        audit_keywords = ["audit", "review", "assessment", "analysis", "evaluate"]
        plan_keywords = ["plan", "roadmap", "timeline", "schedule", "strategy"]
        
        matches = {
            DeliverableType.REPO_CODE: sum(1 for kw in code_keywords if kw in text),
            DeliverableType.DOC: sum(1 for kw in doc_keywords if kw in text),
            DeliverableType.DECISION: sum(1 for kw in decision_keywords if kw in text),
            DeliverableType.AUDIT: sum(1 for kw in audit_keywords if kw in text),
            DeliverableType.PLAN: sum(1 for kw in plan_keywords if kw in text)
        }
        
        # Find primary type
        max_matches = max(matches.values())
        if max_matches == 0:
            return DeliverableType.MIXED
        
        # Count how many types have significant matches
        significant_types = [dtype for dtype, count in matches.items() if count > 0]
        
        if len(significant_types) > 1:
            return DeliverableType.MIXED
        
        # Return type with most matches
        for dtype, count in matches.items():
            if count == max_matches:
                return dtype
        
        return DeliverableType.MIXED
    
    @staticmethod
    def detect_triggers(objective: str, context: Dict[str, Any]) -> Dict[str, bool]:
        """
        Detect auto-tools triggers (Section 5):
        - T-RECENCY: prices, laws, versions, people, news
        - T-NICHE: specialized domain knowledge
        - T-R2: high-impact decisions
        """
        text = objective.lower()
        
        recency_keywords = ["latest", "current", "price", "cost", "law", "regulation", 
                           "version", "news", "recent", "today", "market"]
        niche_keywords = ["specialized", "specific", "technical", "expert", 
                         "advanced", "detailed", "precise"]
        
        return {
            "T-RECENCY": any(kw in text for kw in recency_keywords),
            "T-NICHE": any(kw in text for kw in niche_keywords),
            "T-R2": context.get("risk_class") == RiskClass.R2
        }
    
    @staticmethod
    def get_profile_parameters(profile: Profile, has_important_claims: bool = False) -> ControlParameters:
        """
        Get control parameters for a given profile (Section 4.3).
        
        Args:
            profile: Profile to use
            has_important_claims: Whether there are important claims or non-trivial decisions
        
        Returns:
            ControlParameters with settings for the profile
        """
        if profile == Profile.P_SIMPLE:
            # P-SIMPLE: R0-R1 & C0-C1
            # *CROSS/PCX/NEST become ON if ≥1 important claim
            return ControlParameters(
                mode=Mode.LIGHT,
                budget=Budget.COURT,
                evidence=Evidence.LOW,
                divergence=Divergence.LOW,
                cross=has_important_claims,  # OFF* → ON if important claims
                pcx=has_important_claims,
                nest=has_important_claims,
                repair_max=1,
                show="OFF",
                as_code="auto"
            )
        
        elif profile == Profile.P_STANDARD:
            # P-STANDARD: R1 or C1-C2
            return ControlParameters(
                mode=Mode.MAX,
                budget=Budget.MOYEN,
                evidence=Evidence.MID,
                divergence=Divergence.MID,
                cross=True,
                pcx=True,
                nest=True,
                repair_max=2,
                show="OFF",  # → STATE if degradation
                as_code="auto"
            )
        
        elif profile == Profile.P_COMPLEX:
            # P-COMPLEX: R2 or C2-C3
            return ControlParameters(
                mode=Mode.MAXCAP,
                budget=Budget.LONG,
                evidence=Evidence.HIGH,  # or mid + S2/S3 mandatory
                divergence=Divergence.HIGH,  # external capped at 3
                cross=True,
                pcx=True,  # hardened
                nest=True,  # hardened
                repair_max=3,
                show="STATE",
                as_code="auto"
            )
        
        else:  # P-PROJET
            # P-PROJET: C3 or multi-phase
            return ControlParameters(
                mode=Mode.PROJET,
                budget=Budget.LONG,
                evidence=Evidence.MID,  # → high depending on Rk
                divergence=Divergence.MID,  # prefer ADR
                cross=True,
                pcx=True,
                nest=True,
                repair_max=2,
                show="STATE",
                as_code="auto"
            )
    
    @staticmethod
    def apply_auto_as_code(params: ControlParameters, deliverable_type: DeliverableType) -> ControlParameters:
        """
        Apply auto-AS-CODE logic (Section 4.4).
        
        AS-CODE=ON if deliverable contains: repo|code|CI|workflow|YAML|package|CLI|infra
        """
        if params.as_code == "auto":
            if deliverable_type in [DeliverableType.REPO_CODE, DeliverableType.MIXED]:
                params.as_code = "ON"
            else:
                params.as_code = "OFF"
        
        return params
    
    @staticmethod
    def apply_auto_show(
        params: ControlParameters, 
        risk_class: RiskClass,
        repair_loop_triggered: bool = False,
        gaps_count: int = 0,
        term_code: Optional[str] = None
    ) -> ControlParameters:
        """
        Apply auto-SHOW logic (Section 4.5).
        
        SHOW=STATE if:
        - (a) R2
        - (b) REPAIR-LOOP triggered
        - (c) ≥3 GAPS
        - (d) TERM-PROTOCOLE/PARTIEL
        """
        if params.show == "OFF":
            if risk_class == RiskClass.R2 or \
               repair_loop_triggered or \
               gaps_count >= 3 or \
               term_code in ["TERM-PROTOCOLE", "TERM-PARTIEL"]:
                params.show = "STATE"
        
        return params
    
    @staticmethod
    def tune(
        objective: str,
        context: Optional[Dict[str, Any]] = None,
        user_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main AUTO-TUNE function: classify and configure parameters.
        
        Args:
            objective: User objective (1-3 phrases)
            context: Optional context (constraints, requirements, etc.)
            user_params: Optional user-specified parameters (override defaults)
        
        Returns:
            Dict with tuning results including classifications and parameters
        """
        context = context or {}
        user_params = user_params or {}
        
        # Step 1: Classify risk (Rk)
        risk_class = RiskClassifier.classify(
            has_financial_impact=context.get("has_financial_impact", False),
            has_legal_impact=context.get("has_legal_impact", False),
            has_security_impact=context.get("has_security_impact", False),
            has_health_impact=context.get("has_health_impact", False),
            has_pii=context.get("has_pii", False),
            is_illegal=context.get("is_illegal", False),
            is_dangerous=context.get("is_dangerous", False)
        )
        
        # Step 2: Classify complexity (Ck)
        complexity_class = ComplexityClassifier.classify(
            has_repo_ci_docs=context.get("has_repo_ci_docs", False),
            has_auth_payment_storage_api=context.get("has_auth_payment_storage_api", False),
            has_security_compliance_sensitive_data=context.get("has_security_compliance_sensitive_data", False),
            has_perf_load_sla=context.get("has_perf_load_sla", False),
            is_prod_business=context.get("is_prod_business", False)
        )
        
        # Step 3: Classify deliverable type (Lk)
        deliverable_type = AutoTune.classify_deliverable_type(
            objective,
            context.get("deliverable")
        )
        
        # Step 4: Detect triggers
        triggers = AutoTune.detect_triggers(objective, {
            **context,
            "risk_class": risk_class
        })
        
        # Step 5: Select profile
        profile = ProfileSelector.select_profile(risk_class, complexity_class)
        
        # Step 6: Get base parameters for profile
        has_important_claims = context.get("has_important_claims", False)
        params = AutoTune.get_profile_parameters(profile, has_important_claims)
        
        # Step 7: Apply auto-AS-CODE
        params = AutoTune.apply_auto_as_code(params, deliverable_type)
        
        # Step 8: Apply auto-SHOW (can be updated later based on execution)
        params = AutoTune.apply_auto_show(
            params,
            risk_class,
            repair_loop_triggered=context.get("repair_loop_triggered", False),
            gaps_count=context.get("gaps_count", 0),
            term_code=context.get("term_code")
        )
        
        # Step 9: Apply user overrides
        for key, value in user_params.items():
            if hasattr(params, key):
                setattr(params, key, value)
        
        return {
            "risk_class": risk_class,
            "complexity_class": complexity_class,
            "deliverable_type": deliverable_type,
            "profile": profile,
            "triggers": triggers,
            "parameters": params,
            "tuning_summary": {
                "risk": risk_class.value,
                "complexity": complexity_class.value,
                "deliverable": deliverable_type.value,
                "profile": profile.value,
                "mode": params.mode.value,
                "evidence": params.evidence.value
            }
        }
