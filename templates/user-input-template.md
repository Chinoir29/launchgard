# ARCHI-Ω v1.2 - User Input Template

**Instructions**: Fill in the sections below as completely as possible. If a section is not applicable, mark it as "N/A" with a brief explanation. Critical missing information will trigger P0 questions.

---

## GOAL (objectif métier + valeur)

**What business objective are you trying to achieve? What value will it deliver?**

```
[Describe the business goal, expected outcomes, and value proposition]
```

---

## DELIVERABLE (ce que tu dois produire, format attendu)

**What specific deliverable is expected? What format should it be in?**

```
[Describe the expected output: architecture document, implementation plan, code, etc.]
```

---

## USERS/LOAD (utilisateurs, QPS, pics, volumétrie, latence)

**Who are the users? What are the expected usage patterns?**

- **Number of users**: 
- **QPS (Queries Per Second)**: 
- **Peak load patterns**: 
- **Data volume**: 
- **Expected latency**: 

---

## SLA/SLO (disponibilité, latence, RPO/RTO)

**What are the service level requirements?**

- **Availability target**: 
- **Latency SLO**: 
- **RPO (Recovery Point Objective)**: 
- **RTO (Recovery Time Objective)**: 
- **Other SLAs**: 

---

## DATA (types, sensibilité, résidence, rétention, qualité)

**What data will be handled?**

- **Data types**: 
- **Sensitivity level** (public/internal/confidential/restricted): 
- **Data residency requirements**: 
- **Retention period**: 
- **Data quality requirements**: 

---

## CONSTRAINTS (budget, délai, stack imposée, cloud/on-prem, réglementation)

**What are the constraints and limitations?**

- **Budget**: 
- **Timeline/Deadline**: 
- **Technology stack requirements**: 
- **Cloud/On-prem preference**: 
- **Regulatory requirements** (GDPR, HIPAA, PCI-DSS, etc.): 
- **Other constraints**: 

---

## INTEGRATIONS (APIs externes, SSO, paiements, etc.)

**What external systems need to be integrated?**

- **External APIs**: 
- **Authentication/SSO**: 
- **Payment systems**: 
- **Third-party services**: 
- **Legacy systems**: 

---

## OPS (CI/CD, observabilité, support, astreinte, runbooks)

**What are the operational requirements?**

- **CI/CD requirements**: 
- **Monitoring/Observability**: 
- **Support model** (24/7, business hours): 
- **On-call/Astreinte**: 
- **Runbook requirements**: 
- **Maintenance windows**: 

---

## SECURITY (menaces, exigences, audits)

**What are the security requirements and threats?**

- **Threat model concerns**: 
- **Security requirements**: 
- **Compliance audits**: 
- **Penetration testing**: 
- **Security certifications**: 

---

## AI/ML (si applicable : cas d'usage, modèles, données, explicabilité)

**If AI/ML is involved, provide details:**

- **Use case**: 
- **Model types**: 
- **Training data requirements**: 
- **Explainability requirements**: 
- **Bias/Fairness considerations**: 
- **Model monitoring**: 

**If not applicable, mark as N/A**

---

## DONE (critères d'acceptation PASS/FAIL)

**What are the measurable acceptance criteria?**

### Pass Criteria
1. 
2. 
3. 

### Fail Criteria
1. 
2. 
3. 

---

## ADDITIONAL CONTEXT (optionnel)

**Any additional context, requirements, or considerations?**

```
[Add any other relevant information]
```

---

## FORM METADATA

- **Filled by**: 
- **Date**: 
- **Version**: 
- **Risk classification** (to be determined): R0 / R1 / R2 / R3

---

**Next steps**: Submit this completed form to initiate the ARCHI-Ω pipeline. The framework will:
1. Classify the risk level (R0-R3)
2. Determine required proof budget (PB)
3. Execute the full pipeline (COMPILER → EXPAND → BRANCH → LINT → STRESS → SELECT → COMMIT)
4. Deliver a complete architectural analysis with verification plan
