# launchgard

Deterministic quality gate for product docs, prompts, and repos. Enforces claim tagging ([USER]/[HYP]/[DED]/[GAP]), blocks overpromises, flags recency, detects secrets, and generates PASS/FAIL reports via CLI + GitHub Action.

## 🟥🟩 ARCHI-Ω v1.3.0 Framework

This repository now includes **ARCHI-Ω v1.3.0**, a comprehensive architectural framework with:

- **Fail-closed authority** and context firewall (anti-injection)
- **Proof-level system** (S0-S4) with mandatory origin tagging
- **[GAP] tag with mandatory closure**: DECISION + TEST + IMPACT + TERM
- **Risk classification** (R0-R3) with proof budgets
- **Complexity classification** (C0-C3) and profile selection (P-SIMPLE/STANDARD/COMPLEX/PROJET)
- **AUTO-TUNE**: Automatic parameter adjustment based on Rk/Ck/Lk
- **AUTO-SPEC**: Automatic generation of GOAL/DELIVERABLE/DONE
- **AUTO-CORRECT**: GATE checks + REPAIR-LOOP at each pipeline stage
- **MODERATION=STRICT**: No promises, no invention, stable output, branches capped
- **Enhanced pipeline**: AUTO-TUNE → COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT
- **Testability levels** (T0-T3) for claim verification

### Key Features

- ✅ **Zero fabrication**: No invention of facts, sources, or recency assumptions
- ✅ **Origin tagging**: Every claim tagged [USER]/[DED]/[HYP]/[GAP]
- ✅ **GAP closure mandatory**: Every [GAP] has DECISION+TEST+IMPACT+TERM (no naked GAPs!)
- ✅ **Proof budgets**: Risk-based evidence requirements (S0-S4)
- ✅ **Testability**: All strong causality claims require TRACE ≥ T2
- ✅ **AUTO-TUNE**: Automatic classification and parameter tuning
- ✅ **AUTO-CORRECT**: GATE checks with repair loops at each stage
- ✅ **Security**: Data hygiene, secrets management, PII protection
- ✅ **Fail-closed**: GAP info triggers conservative DECISION + TERM-PROTOCOLE
- ✅ **Claim ledger**: Track all important assertions with tests and status
- ✅ **MODERATION=STRICT**: External options ≤3, no explosion, conservative decisions

### What's New in v1.3.0

**Major Enhancements:**
- **[GAP] replaces [UNKNOWN]**: Mandatory closure with DECISION+TEST+IMPACT+TERM
- **AUTO-TUNE**: Automatic Rk/Ck/Lk classification and profile selection
- **AUTO-SPEC**: Automatic GOAL/DELIVERABLE/DONE generation if missing
- **AUTO-CORRECT**: GATE checks + REPAIR-LOOP (up to REPAIR_MAX attempts)
- **MODERATION=STRICT**: Conservative decisions, capped alternatives, no promises
- **Complexity classes (C0-C3)**: Additive heuristic for project complexity
- **Profiles (P-SIMPLE/STANDARD/COMPLEX/PROJET)**: Auto-selected based on Rk/Ck
- **Enhanced pipeline**: AUTO-TUNE stage added at beginning
- **Status change**: "UNKNOWN" → "À-CLÔTURER" (to be closed)

### Quick Start

1. **Use the framework**: See [ARCHI-OMEGA-v1.3.0.md](./ARCHI-OMEGA-v1.3.0.md) for complete framework
2. **Fill user input**: Use [templates/user-input-template.md](./templates/user-input-template.md)
3. **Review example**: Check [examples/simple-web-api-example.md](./examples/simple-web-api-example.md)
4. **Generate output**: Follow [templates/output-format-template.md](./templates/output-format-template.md)

### Validation

**Local validation (3 commands):**
```bash
python scripts/archi_omega_lint.py  # Fail-closed validation
python tests/test_epistemic.py       # Unit tests
python verify.py                     # Framework verification
```

See [VALIDATION.md](./VALIDATION.md) for detailed validation guide.

**CI/CD:** GitHub Actions automatically runs all validation checks on push.

### Configuration

Default configuration in [archi-omega-config-v1.3.yaml](./archi-omega-config-v1.3.yaml):

```yaml
version: "1.3.0"
mode: MAXCAP
budget: long
evidence: mid
divergence: mid
auto_gov: ON
auto_tools: ON
auto_tune: ON      # NEW in v1.3.0
auto_correct: ON   # NEW in v1.3.0
repair_max: 2      # NEW in v1.3.0
show: OFF          # OFF | STATE
as_code: OFF       # OFF | ON | auto
moderation: STRICT # NEW in v1.3.0
pcx: ON  # Proof cross-check
nest: ON # Nested verification
```

### Templates

- **User Input**: [templates/user-input-template.md](./templates/user-input-template.md)
- **ADR**: [templates/adr-template.md](./templates/adr-template.md)
- **Claim Ledger**: [templates/claim-ledger-template.md](./templates/claim-ledger-template.md)
- **Output Format**: [templates/output-format-template.md](./templates/output-format-template.md)

### Framework Principles (v1.3.0)

1. **SAFETY > TRUTH > ROBUSTNESS > OPS > STYLE**
2. **Fail-closed**: When in doubt, don't conclude; degrade, test, decide conservatively
3. **No ghost tools**: Don't claim verification without explicit capability
4. **Mandatory proof**: Claims need appropriate evidence level (S0-S4)
5. **Testability**: Strong causality requires explicit tests (≥T2)
6. **GAP closure**: Every [GAP] must have DECISION+TEST+IMPACT+TERM (no naked GAPs!)
7. **MODERATION=STRICT**: No promises, no invention, stable output, alternatives capped at 3
8. **Autopilot**: System makes decisions without asking user (unless P0 blocker)

### Risk Classes & Proof Budgets

| Risk | Type | Proof Budget |
|------|------|--------------|
| R0 | Low | S1 (reasoning) |
| R1 | Operational, low impact | S0/S1 + S2 if unstable |
| R2 | High impact (finance/legal/security) | ≥2 independent pillars (S2/S4) |
| R3 | Illegal/dangerous | STOP or strict framework |

### Execution Pipeline (v1.3.0)

```
AUTO-TUNE → Classify Rk/Ck/Lk, select profile, tune parameters
   ↓
COMPILER  → Determine risk, proof budget, active modules
   ↓
EXPAND    → Extract facts, constraints, GAPs, claims (+ AUTO-SPEC)
   ↓
BRANCH    → Generate 3 internal + 2-3 external options (MODERATION)
   ↓
LINT      → Verify invariants, tags, recency, testability, GAP closure
   ↓
STRESS    → Test for contradictions, missing proofs, security
   ↓
SELECT    → Choose most robust option + fallback
   ↓
COMMIT    → Produce deliverable + TERM + PROCHAIN PAS + RUNBOOK
```

Each stage has **GATE checks** with **AUTO-CORRECT** (REPAIR-LOOP up to REPAIR_MAX).

### Output Format

Every deliverable includes (in order):

0. FACTS [USER]
1. OPEN QUESTIONS (P0→P2) - with [GAP] closures
2. ASSUMPTIONS [HYP]
3. OPTIONS + SCORES (max 3 external, MODERATION)
4. RECOMMANDATION + SENSITIVITY MAP
5. ARCHITECTURE CIBLE
6. SÉCURITÉ & CONFORMITÉ
7. IA/ML (if applicable)
8. ADR (Decision Records)
9. PLAN DE VÉRIFICATION + R-SUITE
10. RISKS REGISTER
11. RAPPORT DE REVUE + CLAIM LEDGER (with GAP closures)
12. PROCHAIN PAS + TERM + RUNBOOK (3 actions)

**Termination Codes:**
- TERM-LIVRE: Complete deliverable
- TERM-PARTIEL: Partial - critical constraint missing
- TERM-PROTOCOLE: P0 questions + minimal assumptions + tests
- TERM-REFUS: Refused - illegal/dangerous

### Examples

- [Simple Web API](./examples/simple-web-api-example.md) - Complete walkthrough

### Limitations & Scope

**What the framework does:**
- Enforces structured reasoning with proof levels and origin tagging
- Validates claims against risk-based proof budgets
- Provides templates and pipelines for architectural analysis
- Prevents fabrication through fail-closed validation

**What the framework does not do:**
- Does not make architectural decisions for you (provides structure for your decisions)
- Does not replace domain expertise or professional judgment
- Does not access external APIs or real-time data automatically
- Does not provide legal, financial, or medical advice
- Cannot verify claims beyond the tools and sources you provide
- Does not eliminate all risks (reduces them through systematic validation)

**Known limitations:**
- Requires manual input of project requirements
- Option scoring requires domain knowledge to calibrate
- External tool integration (pricing APIs, etc.) not included in base implementation
- Pipeline assumes human review of generated options
- Does not enforce ARCHI-Ω principles on external content automatically

### License

[To be determined]

---

**Version**: ARCHI-Ω v1.3.0  
**Last Updated**: 2026-02-18
