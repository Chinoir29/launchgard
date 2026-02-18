# Example: Simple Web API Architecture

This example demonstrates how to use ARCHI-Ω v1.2 framework to design a simple web API.

## Input (User Request)

Using the user input template:

```yaml
GOAL: "Build a REST API for task management to improve team productivity by 30%"

DELIVERABLE: "Architecture document with deployment plan"

USERS/LOAD:
  - Number of users: 1000 active users
  - QPS: ~50 QPS average, 200 QPS peak
  - Data volume: ~100k tasks/year
  - Expected latency: <200ms p95

SLA/SLO:
  - Availability: 99.5%
  - Latency: p95 < 200ms
  - RPO: 1 hour
  - RTO: 2 hours

DATA:
  - Types: Task metadata, user info, attachments
  - Sensitivity: Internal (no PII)
  - Residency: EU preferred
  - Retention: 2 years
  - Quality: Consistent, validated

CONSTRAINTS:
  - Budget: $500/month max
  - Timeline: 3 months to launch
  - Stack: Node.js preferred
  - Cloud: AWS
  - Regulation: GDPR compliance

INTEGRATIONS:
  - SSO with corporate IdP (SAML)
  - Email notifications (SendGrid)
  - Slack webhooks for alerts

OPS:
  - CI/CD: GitHub Actions
  - Monitoring: CloudWatch + basic alerts
  - Support: Business hours (9-5)
  - No on-call initially

SECURITY:
  - Standard web app threats
  - Corporate security review required
  - No pen testing initially

AI/ML: N/A

DONE:
  Pass Criteria:
    1. API responds to all CRUD operations with <200ms p95
    2. 99.5% uptime over 30 days
    3. Passes security review
    4. Costs <$500/month
  
  Fail Criteria:
    1. Any data loss incident
    2. Security critical vulnerability
    3. Budget overrun >20%
```

## Framework Processing

### Risk Classification: R1

**Rationale [DED]:**
- Operational system with moderate impact
- No financial transactions
- Internal use only
- No PII data
- Conclusion: R1 (opérationnel faible impact)

### Proof Budget: PB(R1)

Required: S0/S1 + (S2 si instable)
- Architecture choices: S1 (reasoning) + S2 (AWS pricing, Node.js docs)
- Performance claims: S3 (load testing)
- Cost estimates: S2 (AWS calculator)

### Pipeline Execution

#### 1. COMPILER
- Risk: R1
- Proof Budget: S0/S1 + S2
- Modules: CLARIFIER, ARCHITECT, SECURITY, VERIFIER
- Tools: AWS pricing API, load testing
- Stop-rules: Budget constraint (hard limit $500/month)

#### 2. EXPAND
**FACTS [USER]:**
- 1000 users, 50 QPS avg, 200 QPS peak
- Budget: $500/month
- Timeline: 3 months
- Stack: Node.js, AWS

**CONSTRAINTS [USER]:**
- Must use AWS
- Must integrate with SAML SSO
- Must comply with GDPR

**UNKNOWNS:**
- Attachment size limits? → [UNKNOWN] P1
- Task complexity (fields, relations)? → [UNKNOWN] P2

#### 3. BRANCH

**Option 1: Serverless (Lambda + API Gateway + DynamoDB)**
- Pros: Low ops, auto-scaling, pay-per-use
- Cons: Cold starts, vendor lock-in

**Option 2: Container (ECS + PostgreSQL RDS)**
- Pros: More control, better cold start, familiar stack
- Cons: Higher fixed costs, more ops

**Option 3: Managed Platform (Heroku)**
- Pros: Simplest ops, fast deployment
- Cons: Higher cost, less control

#### 4. LINT

Checked:
- ✅ All claims tagged [USER], [DED], [HYP], or [UNKNOWN]
- ✅ No promises ("will guarantee 100% uptime")
- ✅ Recency flagged: AWS pricing verified [S2] 2026-02
- ✅ No secrets in example
- ✅ Testability: Performance claims have T3 tests

#### 5. STRESS

Tests performed:
- ✅ Budget: Option 1 ~$250/mo, Option 2 ~$450/mo, Option 3 ~$700/mo
- ✅ Performance: Both Options 1 & 2 can meet <200ms at 200 QPS
- ✅ Security: All options support required controls
- ⚠️ Dependency: Option 1 requires DynamoDB modeling expertise

#### 6. SELECT

**Recommended: Option 1 (Serverless)**

Reasons:
1. Meets budget constraint with 50% margin
2. Handles peak load naturally
3. Lowest ops burden
4. Acceptable cold start impact at 50 QPS avg

**Fallback: Option 2** if cold starts become problematic

## Output (Abbreviated)

### 0) FACTS [USER]
1. 1000 active users, 50 QPS average, 200 QPS peak [USER]
2. Budget constraint: $500/month [USER]
3. Timeline: 3 months to launch [USER]

### 1) OPEN QUESTIONS
**P1:**
1. What are the attachment size limits? (impacts storage costs)
   - Impact: Could affect cost estimate by 20-50%

**P2:**
1. How many fields/relations per task? (impacts data model)

### 2) ASSUMPTIONS [HYP]

| Assumption | Impact if Wrong | Risk | Test |
|------------|-----------------|------|------|
| [HYP] Attachments <5MB avg, <10 files/task | Cost overrun 20-30% | Medium | Monitor S3 costs weekly |
| [HYP] Cold starts acceptable (<1% requests) | UX degradation | Low | Measure cold start rate in production |
| [HYP] Simple task model (10 fields, 2 relations) | DynamoDB redesign | Low | Validate with stakeholders |

### 3) OPTIONS + SCORES

**Option 1: Serverless**
- Robustesse: 4/5
- Sécurité: 5/5
- Simplicité: 4/5
- Coût: 5/5
- Performance: 4/5
- Time-to-ship: 5/5
- Opérabilité: 5/5
- Évolutivité: 5/5
- **TOTAL: 37/40**

**Option 2: Container**
- **TOTAL: 33/40**

**Option 3: Managed Platform**
- **TOTAL: 30/40**

### 4) RECOMMANDATION

**Option 1: Serverless (Lambda + API Gateway + DynamoDB)**

**Sensitivity Map:**
1. QPS increases to >500: PASS if load testing shows <200ms p95 at 500 QPS → Would need provisioned concurrency
2. Attachment size >5MB avg: PASS if S3 costs stay <$200/month → Would need cost optimization
3. Cold start rate >5%: PASS if user complaints <5/month → Would switch to Option 2
4. Complex queries needed: PASS if DynamoDB query patterns work → Would switch to PostgreSQL (Option 2)
5. Budget reduced to <$300: PASS if can optimize to $300 → Would need to reconsider architecture

### 5) ARCHITECTURE CIBLE

**A) Executive Brief:**
Serverless REST API using AWS Lambda (Node.js), API Gateway, and DynamoDB. Provides CRUD operations for tasks with SAML SSO integration, email notifications, and Slack webhooks. Optimized for cost (<$300/month) and simplicity. No cold start optimization initially; can add if needed.

**D) Components:**
- API Gateway: HTTP routing, throttling, API keys
- Lambda Functions: Business logic (Node.js 18)
- DynamoDB: Task storage (single-table design)
- Cognito: SAML federation
- S3: Attachment storage
- SES/SendGrid: Email notifications
- CloudWatch: Logs and metrics

**Diagram:**
```
[Client] → [API Gateway] → [Lambda] → [DynamoDB]
                ↓              ↓
           [Cognito]      [S3 (attachments)]
                           ↓
                      [SendGrid, Slack]
```

### 9) PLAN DE VÉRIFICATION

**R-SUITE (Regression):**
| ID | Test | Input | Expected | Status |
|----|------|-------|----------|--------|
| R-1 | Create task | POST /tasks {title:"Test"} | 201 Created, <200ms | UNKNOWN |
| R-2 | Read task | GET /tasks/{id} | 200 OK, <100ms | UNKNOWN |
| R-3 | Peak load | 200 req/s for 60s | p95 <200ms, no errors | UNKNOWN |
| R-4 | Auth failure | Invalid token | 401 Unauthorized | UNKNOWN |
| R-5 | Cost validation | Run for 1 month | Total cost <$300 | UNKNOWN |

### 12) TERM

**TERM-PROTOCOLE**

**RUNBOOK:**
1. **Provide:** Attachment size limits and usage patterns
2. **Verify:** Stakeholder approval of DynamoDB single-table design
3. **Decide:** Proceed with Option 1, or switch to Option 2 if cold starts are unacceptable

---

## Key Takeaways

This example demonstrates:

1. **Fail-closed**: Unknown attachment sizes flagged, not assumed
2. **Proof budget**: Cost estimates use S2 (AWS calculator), not invented
3. **Origin tagging**: All claims tagged [USER], [DED], [HYP], or [UNKNOWN]
4. **Testability**: Performance claims have T3 tests (load testing with metrics)
5. **Sensitivity map**: Lists 5 factors that would change recommendation
6. **No overpromising**: 99.5% target, not "guaranteed 100% uptime"
7. **TERM-PROTOCOLE**: Critical information missing, questions provided

The framework forces rigor, prevents fabrication, and ensures testability.
