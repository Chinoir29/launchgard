"""
ARCHI-Ω v1.2 - Architectural Framework

A comprehensive architectural framework with:
- Fail-closed authority and context firewall
- Proof-level system (S0-S4) with mandatory origin tagging
- Risk classification (R0-R3) with proof budgets
- Execution pipeline (COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT)
- Auto-governance and auto-tools routing
- Testability levels (T0-T3) for claim verification
"""

__version__ = "1.2.0"
__author__ = "launchgard"

from .epistemic.foundation import (
    ProofLevel,
    RiskClass,
    TestabilityLevel,
    OriginTag,
    ProofBudget,
    Claim,
    ClaimLedger,
    RiskClassifier,
    ProofValidator
)

from .pipeline.stages import (
    Pipeline,
    ProjectContext,
    TerminationCode,
    Compiler,
    Expander,
    Brancher,
    Linter,
    Stressor,
    Selector,
    Committer
)

__all__ = [
    # Epistemic
    "ProofLevel",
    "RiskClass",
    "TestabilityLevel",
    "OriginTag",
    "ProofBudget",
    "Claim",
    "ClaimLedger",
    "RiskClassifier",
    "ProofValidator",
    
    # Pipeline
    "Pipeline",
    "ProjectContext",
    "TerminationCode",
    "Compiler",
    "Expander",
    "Brancher",
    "Linter",
    "Stressor",
    "Selector",
    "Committer"
]
