# ARCHI-Ω v1.3.0 — Quick Reference

**One-page cheat sheet for the ARCHI-Ω v1.3.0 framework**

---

## 🎯 Core Principle

**SAFETY > VÉRITÉ > ROBUSTESSE > OPS > STYLE**

Fail-closed: When in doubt → don't conclude → [GAP] + DECISION + TEST + TERM

---

## 🏷️ Origin Tags (Mandatory on all claims)

| Tag | Meaning | When to Use |
|-----|---------|-------------|
| **[USER]** | User-provided explicit information | Info directly from user in chat |
| **[DED]** | Deduced logically (explicit chain, no jumps) | Derived from [USER] via reasoning |
| **[HYP]** | Hypothesis (not proven) + test | Assumption needing verification |
| **[GAP]** | Missing/unstable/not verifiable now | **MUST have closure!** |

### ⚠️ [GAP] Closure (Mandatory)

**RULE:** A [GAP] can never be "the end"

Every [GAP] MUST include:
1. **DECISION**: Conservative choice (minimizes impact/risk)
2. **TEST**: How to close the gap (PASS/FAIL)
3. **IMPACT**: Risk/cost/time if not resolved
4. **TERM**: Usually TERM-PROTOCOLE if critical

**Example:**
```
[GAP]: Exact AWS cost unknown
DECISION: Budget 500$/month (2x safety margin)
TEST: Verify actual bill after 1 month; alert if >400$
IMPACT: ±200$ depending on traffic
TERM: TERM-PROTOCOLE
```

---

## 📊 Proof Levels (S0-S4)

| Level | Name | Description |
|-------|------|-------------|
| **S0** | données user | User-provided data |
| **S1** | raisonnement | Reasoning/calculation |
| **S2** | outils/sources | Tools/external sources |
| **S3** | tests reproductibles | Reproducible tests |
| **S4** | recoupement indépendant | ≥2 independent sources |

---

## ⚡ Risk Classes (R0-R3) → Proof Budgets

| Risk | Type | Proof Budget | Notes |
|------|------|--------------|-------|
| **R0** | Faible | S1 | Low risk |
| **R1** | Opérationnel | S0/S1 + S2 si instable | Low impact |
| **R2** | Fort impact | ≥2 piliers (S2/S4) + alternatives | Finance/legal/security |
| **R3** | Illégal/dangereux | STOP/TERM-REFUS | Do not proceed |

---

## 🧪 Testability (TRACE - T0-T3)

| Level | Name | Requirement |
|-------|------|-------------|
| **T0** | Non testable | Avoid |
| **T1** | Implicite | Vague observation |
| **T2** | PASS/FAIL explicite | **Minimum for strong causality** |
| **T3** | Reproductible | Metric + threshold + procedure |

**Rule:** Strong causality ("X causes Y") requires TRACE ≥ T2

---

## 🔧 v1.3.0 NEW: Classifications

### Complexity (Ck) - Additive Heuristic
| Score | Class | Description |
|-------|-------|-------------|
| 0 | **C0** | Trivial |
| 1 | **C1** | Simple (skeleton repo, short doc) |
| 2-3 | **C2** | Moderate (components/CI/tests) |
| ≥4 | **C3** | Complex (product/security/scale) → PROJET |

**Scoring:**
- +1 if repo+CI+docs
- +1 if auth/payment/storage/API
- +1 if security/compliance/sensitive-data
- +1 if perf/load/SLA
- +1 if prod/business

### Profiles (P-*)
| Profile | Triggers | Parameters |
|---------|----------|------------|
| **P-SIMPLE** | R0-R1 & C0-C1 | MODE=LIGHT, BUDGET=court, EVIDENCE=low |
| **P-STANDARD** | R1 or C1-C2 | MODE=MAX, BUDGET=moyen, EVIDENCE=mid |
| **P-COMPLEX** | R2 or C2-C3 | MODE=MAXCAP, BUDGET=long, EVIDENCE=high |
| **P-PROJET** | C3 or multi-phase | MODE=PROJET, multi-phase pipeline |

---

## 🤖 v1.3.0 NEW: AUTO Features

### AUTO-TUNE
- **Rk** classification (risk)
- **Ck** classification (complexity)
- **Lk** classification (deliverable type)
- Profile selection
- Parameter tuning

### AUTO-SPEC
If missing, generates:
- **GOAL**: Business value + beneficiary
- **DELIVERABLE**: Concrete artifact + format + location
- **DONE**: 3-7 PASS/FAIL criteria

### AUTO-CORRECT
- **GATE** checks at each stage
- **REPAIR-LOOP** up to REPAIR_MAX
- Degradation to TERM-PARTIEL/PROTOCOLE if fails

### MODERATION=STRICT
- External options ≤ 3
- No promises ("garanti", "sûr", "100%")
- Stable output
- Conservative [GAP] decisions

---

## 🔄 Pipeline (8 Stages)

```
AUTO-TUNE  → Classify Rk/Ck/Lk, select profile, tune params
   ↓
COMPILER   → Determine risk, PB, modules, triggers
   ↓
EXPAND     → Extract FACTS/GAPs/claims + AUTO-SPEC
   ↓
BRANCH     → 3 internal + 2-3 external OPTIONS (MODERATION)
   ↓
LINT       → Invariants, tags, GAP closure, MODERATION
   ↓
STRESS     → Contradictions, proofs, causality, security
   ↓
SELECT     → Robust option + fallback
   ↓
COMMIT     → Deliverable + TERM + PROCHAIN PAS + RUNBOOK
```

**Each stage has GATE checks with AUTO-CORRECT**

---

## 📋 Output (12 Sections)

0. **FACTS** [USER]
1. **OPEN QUESTIONS** (P0→P2) with [GAP] closures
2. **ASSUMPTIONS** [HYP]
3. **OPTIONS + SCORES** (max 3 external)
4. **RECOMMANDATION + SENSITIVITY MAP**
5. **ARCHITECTURE CIBLE**
6. **SÉCURITÉ & CONFORMITÉ**
7. **IA/ML** (if applicable)
8. **ADR** (Architecture Decision Records)
9. **PLAN DE VÉRIFICATION + R-SUITE**
10. **RISKS REGISTER**
11. **RAPPORT DE REVUE + CLAIM LEDGER**
12. **PROCHAIN PAS + TERM + RUNBOOK** (3 actions)

---

## 🚦 Termination Codes

| Code | Meaning | When |
|------|---------|------|
| **TERM-LIVRE** | Complete deliverable | All criteria met |
| **TERM-PARTIEL** | Partial deliverable | Critical constraint missing |
| **TERM-PROTOCOLE** | Protocol mode | P0 questions + tests for user |
| **TERM-REFUS** | Refused | Illegal/dangerous (R3) |

**Always include:**
- PROCHAIN PAS UNIQUE (next single step)
- RUNBOOK (3 minimal actions)

---

## ⛔ Invariants (Global Prohibitions)

1. **Zero fabrication**: No invention of facts/sources/tool results
2. **Zero ghost tools**: Don't claim verification without capability
3. **Zero overpromise**: No "garanti", "sûr", "argent assuré"
4. **Mandatory origin**: Every assertion needs tag
5. **[GAP] closure**: Every [GAP] needs DECISION+TEST+IMPACT+TERM
6. **Strong causality**: Needs TRACE ≥ T2
7. **No naked [GAP]**: Must have closure
8. **Status**: Use À-CLÔTURER, not "UNKNOWN"

---

## 🎛️ Control Parameters (v1.3.0)

```yaml
MODE: MAXCAP             # LIGHT | MAX | MAXCAP | PROJET
BUDGET: long             # court | moyen | long
EVIDENCE: mid            # low | mid | high
DIVERGENCE: mid          # low | mid | high (max 3 external)
AUTO_GOV: ON             # Execute without asking
AUTO_TOOLS: ON           # Use tools if needed
AUTO_TUNE: ON            # Auto-adjust params
AUTO_CORRECT: ON         # GATE + REPAIR-LOOP
REPAIR_MAX: 2            # Max repairs before degradation
SHOW: OFF                # OFF | STATE
AS_CODE: OFF             # OFF | ON | auto
MODERATION: STRICT       # No promises, stable output
```

---

## ✅ Checklist Before COMMIT

- [ ] All [GAP] have DECISION+TEST+IMPACT+TERM
- [ ] No promises ("garanti", "sûr", etc.)
- [ ] PB(Rk) respected or degradation explicit
- [ ] Strong causalities have TRACE ≥ T2
- [ ] External options ≤ 3 (MODERATION)
- [ ] Claim Ledger complete
- [ ] PROCHAIN PAS + RUNBOOK present
- [ ] TERM-CODE assigned
- [ ] All GATES passed (or REPAIR_MAX reached)

---

## 📚 Example: [GAP] Handling

**BAD (v1.2):**
```
[UNKNOWN]: Exact cost not known
```

**GOOD (v1.3.0):**
```
[GAP]: Exact AWS Lambda cost for 10K users/month unknown

DECISION: Budget conservative 500$/month (2x safety margin)
TEST: Monitor actual AWS bill after 1 month; set alert at 400$
IMPACT: ±200$ depending on real traffic patterns; may need instance adjustment
TERM: TERM-PROTOCOLE (user must validate budget before proceeding)
```

---

## 🔑 Key Differences v1.2 → v1.3.0

| v1.2 | v1.3.0 |
|------|--------|
| [UNKNOWN] | [GAP] with mandatory closure |
| Status "UNKNOWN" | Status "À-CLÔTURER" |
| No AUTO-TUNE | AUTO-TUNE (Rk/Ck/Lk + profile) |
| No AUTO-SPEC | AUTO-SPEC (GOAL/DELIVERABLE/DONE) |
| No AUTO-CORRECT | AUTO-CORRECT (GATE + REPAIR-LOOP) |
| No MODERATION | MODERATION=STRICT (options ≤3) |
| 7 stages | 8 stages (AUTO-TUNE added) |
| No complexity class | Complexity (C0-C3) |
| No profile | Profile (P-SIMPLE/STANDARD/COMPLEX/PROJET) |

---

**Version:** ARCHI-Ω v1.3.0  
**Date:** 2026-02-18  
**Reference:** See [ARCHI-OMEGA-v1.3.0.md](./ARCHI-OMEGA-v1.3.0.md) for complete specification
