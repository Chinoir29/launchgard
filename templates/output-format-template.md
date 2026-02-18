# ARCHI-Ω v1.2.1 - Output Format Template

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Version:** 1.0
**Risk Classification:** R0 / R1 / R2 / R3
**Mode:** MAXCAP / MAX / LIGHT / PROJET

---

## 0) FACTS [USER]

**User-provided facts (tagged [USER]):**

1. 
2. 
3. 

---

## 1) OPEN QUESTIONS (P0→P2)

### Priority P0 (Critical - Blocks Decision)

1. **Q1:** [Question]
   - **Why critical:** [Explanation]
   - **Impact if unknown:** [Impact]

### Priority P1 (High)

1. **Q1:** [Question]
   - **Impact:** [Impact]

### Priority P2 (Medium)

1. **Q1:** [Question]

---

## 2) ASSUMPTIONS [HYP] (avec impact/risque)

| Assumption | Impact if Wrong | Risk Level | Test Plan |
|------------|-----------------|------------|-----------|
| [HYP] Assumption 1 | [Impact description] | Low/Medium/High | [How to verify] |
| [HYP] Assumption 2 | [Impact description] | Low/Medium/High | [How to verify] |

---

## 3) GAPS [GAP] (obligatoire v1.2.1)

**Information gaps identified (each with GAP→DECISION→TEST→TERM):**

| Gap-ID | Description | Decision (Conservative) | Test (PASS/FAIL) | Impact if Wrong | Status |
|--------|-------------|-------------------------|------------------|-----------------|--------|
| G001 | [Gap description] | [Conservative default decision] | [How to close gap - PASS if...] | [Impact if decision is wrong] | À-CLÔTURER |
| G002 | [Gap description] | [Conservative default decision] | [How to close gap - PASS if...] | [Impact if decision is wrong] | À-CLÔTURER |

**Key GAP→DECISION→TEST→TERM rules:**
- Every gap must have a conservative decision
- Every gap must have a test to close it
- Every gap must document impact if wrong
- No gap can be "the end" - must have resolution path

---

## 4) OPTIONS (2–3) + SCORE (0–5) + TRADE-OFFS

### Option 1: [Name]

**Description:**
```
[Detailed description]
```

**Scores (0-5):**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Robustesse | X/5 | |
| Sécurité/Conformité | X/5 | |
| Simplicité | X/5 | |
| Coût | X/5 | |
| Performance | X/5 | |
| Time-to-ship | X/5 | |
| Opérabilité | X/5 | |
| Évolutivité | X/5 | |
| Risque IA | X/5 | |
| **TOTAL** | **XX/45** | |

**Trade-offs:**
- ✅ Advantage 1
- ✅ Advantage 2
- ❌ Disadvantage 1
- ❌ Disadvantage 2

### Option 2: [Name]

[Same structure as Option 1]

### Option 3: [Name]

[Same structure as Option 1]

### Options Comparison Matrix

| Criterion | Option 1 | Option 2 | Option 3 |
|-----------|----------|----------|----------|
| Robustesse | X/5 | Y/5 | Z/5 |
| Sécurité | X/5 | Y/5 | Z/5 |
| ... | ... | ... | ... |
| **TOTAL** | XX/45 | YY/45 | ZZ/45 |

---

## 5) RECOMMANDATION + RATIONNEL (sous contraintes)

### Recommended Option: [Option X]

**Rationale:**
```
[Detailed explanation of why this option is recommended given the constraints]
```

**Key deciding factors:**
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

**Fallback option:** [Option Y]
- **When to use:** [Conditions]

### ⚠️ SENSITIVITY MAP (Top 5) - MANDATORY

**Information that would change the recommendation:**

| # | Information | Current Assumption | Threshold | Test | Impact if Different |
|---|-------------|-------------------|-----------|------|---------------------|
| 1 | [Info item] | [Current value/assumption] | [PASS if X > threshold] | [How to test] | [Would change to Option Y] |
| 2 | [Info item] | [Current value/assumption] | [PASS if X > threshold] | [How to test] | [Impact description] |
| 3 | [Info item] | [Current value/assumption] | [PASS if X > threshold] | [How to test] | [Impact description] |
| 4 | [Info item] | [Current value/assumption] | [PASS if X > threshold] | [How to test] | [Impact description] |
| 5 | [Info item] | [Current value/assumption] | [PASS if X > threshold] | [How to test] | [Impact description] |

---

## 6) ARCHITECTURE CIBLE (A→I)

### A) Executive Brief (≤10 lignes)

```
[Concise summary of the architecture: what it is, what it does, and why it's structured this way]
```

### B) Scope / Non-scope

**In Scope:**
- 
- 

**Out of Scope:**
- 
- 

### C) Exigences

#### Fonctionnelles (FR)
1. **FR-1:** [Functional requirement]
2. **FR-2:** [Functional requirement]

#### Non-Fonctionnelles (NFR)
| ID | Category | Requirement | Target | Measure |
|----|----------|-------------|--------|---------|
| NFR-1 | Performance | [Requirement] | [Target value] | [How to measure] |
| NFR-2 | Reliability | [Requirement] | [Target value] | [How to measure] |
| NFR-3 | Security | [Requirement] | [Target value] | [How to measure] |
| NFR-4 | Cost | [Requirement] | [Target value] | [How to measure] |
| NFR-5 | Ops | [Requirement] | [Target value] | [How to measure] |

### D) Architecture Cible

#### Composants + Responsabilités

| Component | Responsibility | Technology | Rationale |
|-----------|---------------|------------|-----------|
| [Component 1] | [What it does] | [Tech stack] | [Why chosen] |
| [Component 2] | [What it does] | [Tech stack] | [Why chosen] |

#### Flux de Données

```
[Describe: entrée → traitement → sortie]

1. Input: [Source] → [Component A]
2. Processing: [Component A] → [Component B] → [Component C]
3. Output: [Component C] → [Destination]
```

#### Interfaces/API

| API Endpoint | Method | Input | Output | Auth |
|--------------|--------|-------|--------|------|
| /api/v1/[resource] | GET/POST/PUT/DELETE | [Schema] | [Schema] | [AuthN/AuthZ] |

**Authentication/Authorization:**
- 
- 

#### Stockage

| Store | Type | Schema | Encryption | Retention |
|-------|------|--------|------------|-----------|
| [DB/Store 1] | [SQL/NoSQL/etc] | [Schema design] | [At-rest/in-transit] | [Period] |

**Index Strategy:**
- 

#### Diagramme

```mermaid
[Mermaid diagram or ASCII art diagram]
```

### E) Choix Technologiques

| Technology | Purpose | Justification | Alternatives Considered |
|------------|---------|---------------|------------------------|
| [Tech 1] | [Use case] | [Why chosen] | [Alt 1, Alt 2] |
| [Tech 2] | [Use case] | [Why chosen] | [Alt 1, Alt 2] |

### F) Déploiement

**Environments:**
- Dev: [Configuration]
- Staging: [Configuration]
- Production: [Configuration]

**Infrastructure as Code:**
- Tool: [Terraform/CloudFormation/etc]
- Repository: [Location]

**CI/CD Pipeline:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Release Strategy:**
- [Blue/Green, Canary, Rolling, etc.]
- Rollback plan: [Description]

### G) Observabilité

**Logging:**
- Tool: [ELK, Splunk, CloudWatch, etc.]
- Log levels: [Configuration]
- Retention: [Period]

**Metrics:**
- Tool: [Prometheus, DataDog, etc.]
- Key metrics:
  - [Metric 1]
  - [Metric 2]

**Traces:**
- Tool: [Jaeger, X-Ray, etc.]
- Sampling rate: [%]

**Alerting:**
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| [Alert 1] | [When X > threshold] | Critical/Warning/Info | [Action] |

**SLOs:**
| SLI | SLO Target | Error Budget | Alert Threshold |
|-----|------------|--------------|-----------------|
| [Indicator] | [Target] | [Budget] | [Threshold] |

### H) Résilience & DR

**RPO/RTO:**
- RPO: [Time]
- RTO: [Time]

**Failure Modes:**
| Failure Scenario | Impact | Detection | Recovery | Prevention |
|------------------|--------|-----------|----------|------------|
| [Scenario 1] | [Impact] | [How detected] | [How recovered] | [How prevented] |

**Resilience Patterns:**
- Retries: [Strategy]
- Circuit breakers: [Configuration]
- Timeouts: [Values]
- Bulkheads: [Isolation strategy]
- Graceful degradation: [Fallback behavior]

**Disaster Recovery:**
- Backup strategy: [Frequency, location]
- Recovery procedure: [Steps]
- DR testing: [Schedule]

### I) Coûts

**Cost Drivers:**
1. [Driver 1]: [Estimated cost]
2. [Driver 2]: [Estimated cost]
3. [Driver 3]: [Estimated cost]

**Total Estimated Cost:** $X,XXX/month

**Optimization Levers:**
1. [Lever 1]: [Potential savings]
2. [Lever 2]: [Potential savings]

**Cost Monitoring:**
- Tool: [CloudWatch, Cost Explorer, etc.]
- Alerts: [Budget thresholds]

---

## 7) SÉCURITÉ & CONFORMITÉ

### Threat Model

#### Actifs
1. [Asset 1]: [Value/sensitivity]
2. [Asset 2]: [Value/sensitivity]

#### Adversaires
1. [Adversary type]: [Motivation, capabilities]
2. [Adversary type]: [Motivation, capabilities]

#### Attack Surfaces
1. [Surface 1]: [Description, exposure]
2. [Surface 2]: [Description, exposure]

#### Threat Scenarios
| Scenario | Likelihood | Impact | Risk Score | Mitigation |
|----------|------------|--------|------------|------------|
| [Scenario 1] | Low/Med/High | Low/Med/High | L/M/H/C | [Controls] |

### Contrôles de Sécurité

**IAM (Identity & Access Management):**
- 
- 

**Secrets Management:**
- 
- 

**Encryption:**
- At-rest: [Method, key management]
- In-transit: [TLS version, cipher suites]

**Network Security:**
- Segmentation: [VPC/subnet strategy]
- Firewall rules: [Configuration]
- WAF: [Rules, rate limiting]

### Data Governance

**Data Classification:**
| Data Type | Classification | Handling Requirements |
|-----------|---------------|----------------------|
| [Type 1] | Public/Internal/Confidential/Restricted | [Requirements] |

**Data Minimization:**
- 

**Retention & Disposal:**
- 

**Audit Logging:**
- What: [What is logged]
- Where: [Storage location]
- How long: [Retention period]

### Checklist Revue Sécurité

- [ ] **PASS/FAIL:** Authentication implemented correctly
- [ ] **PASS/FAIL:** Authorization follows least privilege
- [ ] **PASS/FAIL:** Secrets not hardcoded
- [ ] **PASS/FAIL:** Data encrypted at rest and in transit
- [ ] **PASS/FAIL:** Input validation implemented
- [ ] **PASS/FAIL:** SQL injection prevention
- [ ] **PASS/FAIL:** XSS prevention
- [ ] **PASS/FAIL:** CSRF protection
- [ ] **PASS/FAIL:** Rate limiting implemented
- [ ] **PASS/FAIL:** Security headers configured
- [ ] **PASS/FAIL:** Dependency scanning in place
- [ ] **PASS/FAIL:** SAST/DAST in CI/CD
- [ ] **PASS/FAIL:** Incident response plan documented
- [ ] **PASS/FAIL:** Compliance requirements met

**Actions Required:**
1. [Action for any FAIL items]

---

## 8) IA/ML (si applicable)

### Approche

**Type:** [RAG / fine-tune / agents / classification / forecasting / etc.]

**Description:**
```
[Detailed approach description]
```

### Pipeline

```
Collecte → Qualité → Features → Train → Eval → Deploy
```

**Data Collection:**
- Sources: 
- Volume: 
- Quality: 

**Feature Engineering:**
- 

**Training:**
- Model: 
- Framework: 
- Infrastructure: 

**Evaluation:**
- Metrics: 
- Test sets: 

**Deployment:**
- Strategy: 
- Infrastructure: 

### Évaluation

**Metrics:**
| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| [Accuracy/F1/etc] | [Target] | [Current] | PASS/FAIL |

**Robustness:**
- Edge cases tested: 
- Adversarial testing: 

**Bias & Fairness:**
- Protected attributes: 
- Fairness metrics: 
- Mitigation: 

**Drift Detection:**
- Data drift: [Monitoring approach]
- Concept drift: [Monitoring approach]

### Exploitation

**Monitoring:**
- Model performance: 
- Inference latency: 
- Resource usage: 

**Retraining:**
- Trigger: 
- Frequency: 
- Process: 

**Rollback:**
- Procedure: 
- Criteria: 

**A/B Testing:**
- Strategy: 
- Metrics: 

### Sécurité IA

**Threats:**
| Threat | Mitigation |
|--------|------------|
| Prompt injection | [Controls] |
| Data exfiltration | [Controls] |
| Hallucinations | [Controls] |
| Jailbreaks | [Controls] |

### Guardrails

**Policies:**
- 

**Citations/Grounding:**
- 

**Access Controls:**
- 

**Content Filters:**
- Input: 
- Output: 

---

## 9) ADR (DECISION RECORDS)

### ADR-001: [Title]

**Status:** Accepted

**Context:** [Brief context]

**Decision:** [What was decided]

**Consequences:**
- ✅ [Positive consequence]
- ❌ [Negative consequence]

**Alternatives:** [Alternatives considered]

---

[Repeat for ADR-002 through ADR-010]

---

## 10) PLAN DE VÉRIFICATION

### Tests

#### Unit Tests
- Coverage target: [%]
- Critical paths: [List]
- Tools: [Framework]

#### Integration Tests
- Scenarios: [List key scenarios]
- Tools: [Framework]

#### End-to-End Tests
- User journeys: [List]
- Tools: [Framework]

#### Load/Performance Tests
- Scenarios: [List]
- Tools: [JMeter, K6, etc.]
- Targets: [Performance targets]

#### Chaos Engineering
- Experiments: [List]
- Tools: [Chaos Monkey, Gremlin, etc.]

#### Security Tests
- Types: [SAST, DAST, penetration testing]
- Tools: [List]
- Schedule: [Frequency]

### Critères d'Acceptation

| Criterion | Test | Target | Status |
|-----------|------|--------|--------|
| [Criterion 1] | [How tested] | PASS if [condition] | PASS/FAIL/À-CLÔTURER |
| [Criterion 2] | [How tested] | PASS if [condition] | PASS/FAIL/À-CLÔTURER |

### ⚠️ R-SUITE (Régression) - MANDATORY

**Regression test cases (5-10 étalons):**

| ID | Test Case | Input | Expected Output | Status |
|----|-----------|-------|-----------------|--------|
| R-1 | [Scenario] | [Input data] | PASS if [expected result] | PASS/FAIL |
| R-2 | [Scenario] | [Input data] | PASS if [expected result] | PASS/FAIL |
| R-3 | [Scenario] | [Input data] | PASS if [expected result] | PASS/FAIL |
| R-4 | [Scenario] | [Input data] | PASS if [expected result] | PASS/FAIL |
| R-5 | [Scenario] | [Input data] | PASS if [expected result] | PASS/FAIL |

### Migration (si existant)

**Migration Strategy:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Rollback Plan:**
- 

**Data Migration:**
- 

### Backlog Next-Steps (priorisé)

| Priority | Item | Effort | Dependencies |
|----------|------|--------|--------------|
| P0 | [Item] | [T-shirt size] | [Dependencies] |
| P1 | [Item] | [T-shirt size] | [Dependencies] |
| P2 | [Item] | [T-shirt size] | [Dependencies] |

---

## 11) RISKS REGISTER

| Risk ID | Description | Probability | Impact | Risk Score | Mitigation | Owner | Status |
|---------|-------------|-------------|--------|------------|------------|-------|--------|
| R-1 | [Risk description] | Low/Med/High | Low/Med/High | L/M/H/Critical | [Mitigation strategy] | [Name/Role] | Open/Mitigated/Closed |
| R-2 | [Risk description] | Low/Med/High | Low/Med/High | L/M/H/Critical | [Mitigation strategy] | [Name/Role] | Open/Mitigated/Closed |

**Risk Matrix:**
```
         Impact
         Low    Med    High
High    |  M  |  H  |  C  |
Med     |  L  |  M  |  H  |
Low     |  L  |  L  |  M  |
        Probability
```

---

## 12) RAPPORT DE REVUE

### Auto-Review Scores

| Criterion | Score (0-5) | Notes |
|-----------|-------------|-------|
| Exactitude (Accuracy) | X/5 | [Notes on correctness] |
| Complétude (Completeness) | X/5 | [Notes on coverage] |
| Cohérence (Coherence) | X/5 | [Notes on consistency] |
| Testabilité (Testability) | X/5 | [Notes on verifiability] |
| Sécurité (Security) | X/5 | [Notes on security] |
| Coût (Cost) | X/5 | [Notes on cost-effectiveness] |
| **TOTAL** | **XX/30** | |

### Corrections Clés

**Cycle 1 Issues:**
1. [Issue identified]
2. [Issue identified]

**Cycle 2 Improvements:**
1. [Improvement made]
2. [Improvement made]

### ⚠️ ANNEXE A — CLAIM LEDGER (MANDATORY)

**Claim Ledger for this project:**

| Claim-ID | Claim Text | Origin Tag | S-Level | Dependencies | Test | Status |
|----------|------------|------------|---------|--------------|------|--------|
| C001 | [Claim] | [USER/DED/HYP/GAP] | S0-S4 | [IDs] | [Test description] | PASS/FAIL/À-CLÔTURER |
| C002 | [Claim] | [USER/DED/HYP/GAP] | S0-S4 | [IDs] | [Test description] | PASS/FAIL/À-CLÔTURER |
| C003 | [Claim] | [USER/DED/HYP/GAP] | S0-S4 | [IDs] | [Test description] | PASS/FAIL/À-CLÔTURER |

**Summary:**
- Total Claims: X
- By Status: PASS: X, FAIL: Y, À-CLÔTURER: Z
- By Origin: [USER]: W, [DED]: X, [HYP]: Y, [À-CLÔTURER]: Z
- By S-Level: S0: A, S1: B, S2: C, S3: D, S4: E

**Critical Open Items:**
1. [Any critical À-CLÔTURER or FAIL claims]

---

## 13) PROCHAIN PAS UNIQUE + TERM

### Next Immediate Action

**Single next step:** [One clear action to take next]

### Termination Status

**TERM:** ☑ TERM-LIVRÉ / ☐ TERM-PARTIEL / ☐ TERM-PROTOCOLE / ☐ TERM-REFUS

**Explanation:**
```
[Why this termination status was chosen]
```

### ⚠️ RUNBOOK TERM- (3 actions minimales) - MANDATORY

**To proceed/unblock, you must:**

1. **Fournir (Provide):**
   - [What information/data needs to be provided]

2. **Vérifier (Verify):**
   - [What needs to be checked/validated]

3. **Décider (Decide):**
   - [What decision needs to be made]

---

## AS-CODE YAML (if AS-CODE=ON)

```yaml
risk_class: R1
mode: MAXCAP
pcx: ON
nest: ON
auto_gov: ON
auto_tools: ON
modules_active:
  - CLARIFIER
  - ARCHITECT
  - SECURITY
  - AIML
  - VERIFIER
summary: "[Brief summary]"
options:
  - id: O1
    score:
      robust: 4
      security: 5
      simplicity: 3
      cost: 4
      perf: 4
      ops: 3
    tradeoffs:
      - "[Trade-off 1]"
      - "[Trade-off 2]"
  - id: O2
    score:
      robust: 3
      security: 4
      simplicity: 5
      cost: 5
      perf: 3
      ops: 4
    tradeoffs:
      - "[Trade-off 1]"
      - "[Trade-off 2]"
recommendation: "O1"
tests_next:
  - id: X1
    metric: "[Metric name]"
    threshold: "PASS if [condition]"
  - id: X2
    metric: "[Metric name]"
    threshold: "PASS if [condition]"
termination: TERM-LIVRÉ
```

---

**End of ARCHI-Ω v1.2 Deliverable**

**Version:** 1.0
**Generated:** YYYY-MM-DD HH:MM:SS
**Framework:** ARCHI-Ω v1.2
