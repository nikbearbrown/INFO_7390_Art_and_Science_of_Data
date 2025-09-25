# Lesson (Markdown): Framework Overview – The Botspeak System

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M1.2 – Framework Overview: The Botspeak System  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures with hands‑on exercises and artifacts

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Describe the Botspeak framework as a structured methodology for human‑AI collaboration.  
2. Operationalize human oversight by selecting interaction modes (Automation, Augmentation, Agency) and defining guardrails, RACI roles, and escalation paths.  
3. Design a continuous validation loop aligned with NIST TEVV (Test, Evaluation, Validation, Verification) and AI RMF concepts.  
4. Integrate philosophical skepticism (Descartes, Hume, Popper) into practical collaboration steps.  
5. Produce three course artifacts: a Prompt Spec, an Acceptance‑Test plan, and an Oversight & Monitoring canvas.

**Botspeak Pillar Alignment:** Strategic Delegation, Effective Communication, Critical Evaluation, Technical Understanding, Ethical Reasoning, Stochastic Reasoning, Learning by Doing, Rapid Prototyping, Theoretical Foundation.

---

## Key Terms
- **Botspeak Loop:** A repeatable cycle for human‑AI work: *Define → Delegate → Direct → Diagnose → Decide → Document*.  
- **Interaction Mode:** The level of AI autonomy in context: *Automation*, *Augmentation*, *Agency* (with progressive guardrails).  
- **Guardrail:** A policy, constraint, or mechanism that prevents or limits undesirable behavior (e.g., PII block, refusal policy, rate/role caps).  
- **Acceptance Test:** Observable, pre‑registered criteria used to judge whether an AI output is acceptable for the task.  
- **RACI:** Responsibility matrix for oversight: *Responsible, Accountable, Consulted, Informed*.  
- **TEVV:** *Test, Evaluation, Validation, Verification* (NIST); the set of activities that establish whether an AI system meets specified requirements.  
- **Drift/Shift:** Distribution or concept changes between training and deployment that degrade performance or change risk.

---

## Theory: The Botspeak System as a Structured Methodology

### A. The Botspeak Loop
A practical operating system for human‑AI collaboration:

```
+---------+    +----------+    +---------+    +----------+    +---------+    +------------+
| Define  | -> | Delegate | -> | Direct  | -> | Diagnose | -> | Decide  | -> | Document   |
+---------+    +----------+    +---------+    +----------+    +---------+    +------------+
   Goal         Task split      Prompting      Evaluate/       Ship,            Record
  & risks       & mode          & inputs       test/triage     mitigate         evidence
```

**Define.** Clarify stakeholder goals, constraints (time, cost, legal, ethical), risk tolerance, and success metrics. Map benefits vs. harms; identify where certainty matters.  
**Delegate.** Choose the *Interaction Mode* (Automation/Augmentation/Agency). Allocate subtasks across human vs. AI based on risk, reversibility, observability, and skill availability.  
**Direct.** Turn tasks into a *Prompt Spec* with explicit roles, schemas, examples, and acceptance tests. Provide references/contexts; set iteration budgets.  
**Diagnose.** Critically evaluate outputs: run acceptance tests, check uncertainty/calibration, look for biases/leakage, conduct adversarial/negative testing; log findings.  
**Decide.** Take action: accept, revise, mitigate, escalate, or roll back. Apply pre‑committed decision rules.  
**Document.** Preserve artifacts: prompt spec, decision memo, validation evidence, risk register, model card updates, monitoring plan.

**Why this order?** The loop encodes philosophical skepticism into practice: *Define* guards against goal drift (Descartes’ discipline); *Diagnose* counters induction fallacies (Hume) with evidence; *Decide* implements falsifiable thresholds (Popper) via Go/No‑Go rules.

---

### B. Balancing AI Capability with Human Oversight

**Interaction Modes**
- **Automation:** AI executes within narrow, reversible bounds. Human monitors aggregates and handles exceptions. Use when harm is low and reversibility high (e.g., dedupe suggestions).
- **Augmentation:** AI proposes; humans decide. The default for ambiguous or ethically sensitive tasks (e.g., medical radiology triage, content moderation queues).
- **Agency:** AI acts with limited autonomy against goals, under explicit constraints and *human override*. Suitable only when guardrails, audits, and recovery are mature.

**Choosing a Mode: Risk Heuristics**
- **Harm severity × likelihood** (risk score); **reversibility** (can we undo?); **observability** (can we detect errors quickly?); **maturity** of data/metrics/monitoring.

**Oversight Mechanisms**
- **RACI** for each decision point (who approves model changes? who handles incidents?).  
- **Guardrails:** policy filters (PII/violence), constrained decoding/templates, retrieval whitelists, rate limits, chain‑of‑thought redaction, refusal criteria.  
- **Escalation Paths:** thresholds for human review; adverse‑action appeals; break‑glass protocols; rollback triggers.

---

### C. Continuous Validation & Critical Assessment
Botspeak integrates with NIST TEVV and the AI Risk Management mindset:

- **Test:** Scenario/edge coverage; adversarial and negative controls; data quality checks; leakage probes.  
- **Evaluation:** Utility metrics (task success, latency, cost) and *harm* metrics (bias, safety, compliance). Include uncertainty and calibration checks.  
- **Validation:** Stakeholder alignment; requirements traceability; human factors review; ethics/privacy checks.  
- **Verification:** Conformance to specs; reproducibility; documentation; approvals and audit logs.

**Monitoring & Drift**  
- Signals: PSI, subgroup performance deltas, calibration shift, incident reports.  
- Playbooks: alert thresholds, retraining cadence, rollback criteria, incident postmortems.

---

### D. Philosophical Rigor in Practice
- **Descartes (Methodic Doubt):** Treat every claim as defeasible until assumptions are evidenced. Convert claims into checklists and tests.  
- **Hume (Induction Skepticism):** Expect distribution shifts; privilege out‑of‑time/‑domain evidence; avoid shortcut features; monitor for feedback loops.  
- **Popper (Falsifiability):** Pre‑register thresholds; prefer risky predictions; publish Go/No‑Go rules; embrace refutation as progress.

---

## Hands‑On Exercises

### Exercise 1 — Prompt Spec & Acceptance Tests (Botspeak: Direct → Diagnose)
**Time:** 30–40 min | **Format:** Pairs  
**Scenario (choose one):**  
1. Draft a policy‑aware product description generator for an ecommerce site (copyright/claims risk).  
2. Create a code‑review assistant for Python PRs (false‑positive fatigue risk).  
3. Build a research summarizer constrained to supplied PDFs (hallucination/attribution risk).

**Tasks.**  
1. **Prompt Spec:** Fill the template below (role, inputs, output schema, constraints, examples, counter‑examples, refusal policy).  
2. **Acceptance Tests:** Write 5 test cases with expected outcomes, including at least 1 negative control and 1 bias probe.  
3. **Run & Diagnose (conceptual or with tools):** Execute once (or simulate) and score against tests; identify failure patterns; propose a refinement.

**Template – Prompt Spec**  
- **Role & Audience:**  
- **Inputs & Sources (and licenses):**  
- **Output Schema:** (fields, types, ranges)  
- **Style & Constraints:** (readability, length, terminology bans)  
- **Refusal & Safety Rules:** (e.g., no medical/financial advice)  
- **Examples / Counter‑Examples:**  
- **Acceptance Tests:** (see separate table)

**Template – Acceptance Tests**  
| ID | Test description | Input | Expected outcome | Metric/Check | Pass/Fail |
|----|------------------|-------|------------------|--------------|-----------|

**Debrief Prompts.** Which acceptance test prevented the most risk? What additional evidence would you gather next?

---

### Exercise 2 — Choosing Interaction Mode & Designing Oversight (Botspeak: Delegate)
**Time:** 25–30 min | **Format:** Teams of 3–4  
**Scenario (choose one):**  
- **ER Triage Assistant** (flag likely priority; clinician decides).  
- **Credit Line Increase Recommender** (consumer finance; adverse‑action obligations).  
- **Marketing Image Generator** (brand/IP/safety risks).

**Tasks.**  
1. **Mode Decision:** Pick *Automation*, *Augmentation*, or *Agency*; justify with a 2×2: (Harm Severity × Reversibility).  
2. **RACI:** Fill at least four roles (Model Owner, Responsible Reviewer, Accountable Exec, Incident Manager).  
3. **Guardrails & Escalation:** Define 5 guardrails (e.g., PII redaction; fair‑use image sources only; subgroup error caps) and a 3‑step escalation ladder.  
4. **Decision Rule:** When must a human review? When do you auto‑rollback?

**Templates**  
- **Risk Matrix (sketch)**  
  - Axes: Harm Severity (Low→High) × Reversibility (Easy→Hard).  
- **RACI Table**  
  | Decision point | R | A | C | I |
  |---------------|---|---|---|---|

**Deliverable:** 1‑page Oversight Canvas with Mode, RACI, Guardrails, Escalation, and Decision Rules.

---

### Exercise 3 — Continuous Validation & Monitoring Plan (Botspeak: Diagnose → Decide → Document)
**Time:** 30–35 min | **Format:** Teams of 3–4  
**Scenario:** Continue with your Exercise 2 system.

**Tasks.**  
1. **Metrics & Thresholds:** Choose utility and harm metrics; set pre‑registered thresholds with rationale.  
2. **TEVV Touchpoints:** Specify tests (edge cases, negative controls), evaluation datasets (incl. out‑of‑time), validation sign‑offs, and verification steps (reproducibility checklist).  
3. **Monitoring:** Define drift/incident signals (PSI, calibration delta, subgroup deltas), alert levels, and rollback criteria.  
4. **Documentation:** Draft a mini *Model Card* section: intended use, limits, ethical considerations, performance by subgroup.

**Deliverable:** 1‑page Validation & Monitoring Plan.

**Debrief:** What is your fastest reliable signal of trouble? What data do you need for a defensible rollback decision?

---

## Assessment
- **Formative:** Share‑outs from each exercise; instructor feedback on artifacts.  
- **Summative (Homework):** Submit the three artifacts (Prompt Spec; Oversight Canvas; Validation & Monitoring Plan).  

**Rubric (30 pts total).**  
- **Prompt Spec & Tests (10):** Completeness, clarity, presence of negative/bias tests, traceable acceptance criteria.  
- **Oversight Canvas (10):** Appropriate mode selection, coherent RACI, concrete guardrails, plausible escalation.  
- **Validation Plan (10):** Measured thresholds, TEVV mapping, actionable monitoring + rollback.

---

## Instructor Notes & Facilitation Tips
- Encourage students to *numericalize* decisions (thresholds, budgets, error costs).  
- Ask “Where do we place the human?” repeatedly; use reversibility to argue for/against autonomy.  
- Make logs an artifact: prompt, version, input sources, output, tests, and decision should be reproducible.  
- Use short timeboxes; perfection is less important than a complete loop through Define→Document.  
- Tie back to philosophy: label each artifact with D/H/P tags (Descartes/Hume/Popper) indicating which skeptical move it encodes.

---

## Templates (Copy‑Paste)

**Botspeak Prompt Canvas**  
- Task goal & non‑goals:  
- Inputs & provenance/licensing:  
- Output schema (fields, formats):  
- Constraints (policy/ethics/brand):  
- Examples & counter‑examples:  
- Acceptance tests (IDs):  
- Iteration budget & stop conditions:  

**Oversight Canvas**  
- Interaction Mode (why):  
- RACI (names/roles):  
- Guardrails (5+):  
- Escalation ladder (3 steps):  
- Decision rules (human‑in‑the‑loop, rollback):  

**Validation & Monitoring Plan**  
- Metrics (utility + harm) & thresholds:  
- Datasets (holdout, OOT, sensitive slices):  
- Tests (edge, adversarial, negative controls):  
- Verification (reproducibility, approvals):  
- Monitoring (signals, alerting, SLOs) & rollback:  
- Documentation (model card summary):  

---

## References (Selected, APA‑style)
- National Institute of Standards and Technology. (2023). *AI Risk Management Framework (AI RMF 1.0).* NIST.  
- National Institute of Standards and Technology. (2024). *Test, Evaluation, Validation, and Verification (TEVV) for AI Systems.* NIST.  
- Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). Model Cards for Model Reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAT").*  
- Gebru, T., Morgenstern, J., Vecchione, B., et al. (2018). Datasheets for Datasets. *arXiv:1803.09010.*  
- Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control.* Viking.  
- Floridi, L. (2014). *The Fourth Revolution: How the Infosphere is Reshaping Human Reality.* Oxford University Press.  
- Partnership on AI. (2021). *Managing Machine Learning Projects: From Design to Deployment* (case studies).  

> See course Resource list for SHAP, LIME, Fairlearn, and What‑If Tool links that support Diagnose and Validation stages.

---

## Appendix: Quick Checklists

**Acceptance Test Drafting (5‑point)**  
1) Observable and objective  
2) Tied to a stakeholder requirement  
3) Includes at least one negative control  
4) Names a metric or rule  
5) Pass/Fail is unambiguous

**Mode Decision (4‑factor)**  
- Harm severity  
- Likelihood  
- Reversibility  
- Observability & monitoring maturity

**Rollback Triggers (examples)**  
- PSI > 0.25 on a key feature  
- Subgroup FNR > 1.2× global for 3 days  
- Incident count above weekly SLO  
- Calibration Brier score worsens by >20% OOT vs. baseline

