# Lesson (Markdown): Module 3 — Bias Detection & Mitigation in AI

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M3 – Bias Detection & Mitigation  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, code‑optional labs, and design artifacts

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Explain how **implicit bias** and **cognitive bias** shape AI datasets, labels, features, and decisions.  
2. Critically assess whether and how AI systems can **reinforce existing power structures** through feedback loops and institutional choices.  
3. Apply key notions from **postmodern and critical theory** (e.g., power/knowledge, situated knowledge, metanarratives) to interrogate “ground truth.”  
4. Conduct a **bias audit** using group fairness metrics (e.g., demographic parity, equalized odds) and uncertainty reporting.  
5. Implement at least one **mitigation** approach (pre‑, in‑, or post‑processing) and articulate the trade‑offs.  
6. Integrate findings into **Botspeak artifacts**: Prompt Spec constraints, Oversight Canvas, and a TEVV‑lite Validation & Monitoring plan under the **Ethical Reasoning** and **Stochastic Reasoning** pillars.

**Botspeak Pillar Alignment:** Ethical Reasoning, Stochastic Reasoning, Critical Evaluation, Technical Understanding, Theoretical Foundation, Learning by Doing.

---

## Key Terms
- **Implicit bias:** Unconscious associations affecting judgments (e.g., Banaji & Greenwald).  
- **Cognitive bias:** Systematic thinking errors (e.g., availability, anchoring, confirmation) that influence problem framing, feature choices, and evaluation.  
- **Historical bias:** Pre‑existing structural inequities embedded in data before collection.  
- **Representation bias:** Under/over‑representation of subgroups in data.  
- **Measurement/label bias:** Noisy, proxy, or prejudiced labels; inconsistent annotation guidelines.  
- **Aggregation bias:** Using one model for heterogeneous populations without subgroup adaptation.  
- **Demographic parity:** Outcome rates are equal (or within a tolerance) across groups.  
- **Equalized odds:** True positive and false positive rates are equal (or within a tolerance) across groups.  
- **Calibration:** Predicted probabilities match observed frequencies within groups.  
- **Counterfactual fairness:** Decisions invariant under changes to protected attributes in a causal model, ceteris paribus.  
- **Feedback loops:** Model outputs alter data generation (e.g., predictive policing), entrenching power.  

---

## Theory: Philosophical Foundations & Critical Questions

### A. Implicit Bias & Cognitive Bias in AI Practice
- **From minds to models.** Developers, annotators, and stakeholders carry biases that shape problem definitions (target choice), features (proxy variables), labeling, and acceptance tests.  
- **Skeptical posture.** Apply **Descartes’ methodic doubt**: list assumptions behind labels and features; confront uncertainty and error costs. Use **Hume** to question generalization: will past patterns hold under deployment? Use **Popper** to pre‑commit fairness hypotheses and refutation tests.  

**Common bias pathways**  
1. **Problem framing:** Choosing targets that operationalize a normative ideal (e.g., “creditworthiness”) in ways that mirror existing exclusions.  
2. **Data collection:** Sampling that misses vulnerable subgroups; annotation instructions that encode stereotypes.  
3. **Modeling:** Shortcut learning (e.g., background artifacts); aggregation bias (single global model despite heterogeneity).  
4. **Evaluation:** Metrics that hide harm (e.g., overall accuracy obscures subgroup errors).  
5. **Deployment:** Choice of autonomy mode; lack of redress; monitoring gaps; incentives that reward speed over safety.

---

### B. Do AI Models Reinforce Existing Power Structures?
- **Power/knowledge (Foucault).** Institutions define what counts as knowledge and normality; predictive systems can stabilize these definitions by making them appear objective.  
- **Situated knowledges (Haraway).** Data are partial and perspectival; model “views” reflect locus of collection and annotation practices.  
- **Abstraction traps (Selbst et al.).** Over‑abstracting socio‑technical context causes technical fixes to miss institutional harms.  
- **Algorithmic amplification.** Ranking, ad delivery, and policing models can magnify unequal visibility, opportunity, and scrutiny (see Noble; Benjamin; Crawford).  

**Guiding questions**  
- *Whose* objective function is optimized? *Which* harms are measured vs. invisible? *Who* can appeal? *What* incentives drive the deployment?

---

### C. Postmodernism & AI: Truth or Mirrors of Bias?
- **Incredulity toward metanarratives (Lyotard).** Resist totalizing claims like “AI reveals the truth in data”; interrogate how “ground truth” is constructed.  
- **Constructed labels.** Many labels (e.g., “toxicity,” “risk”) are normative; operationalizations must be justified, contested, and made auditable.  
- **Pragmatic stance.** We seek *useful* and *ethical* models, not metaphysical truth. Botspeak encodes this through falsifiable claims, audits, and documented limits.

---

## Method: Bias Audits within the Botspeak Loop
**Define → Delegate → Direct → Diagnose → Decide → Document**  
- **Define:** Specify protected attributes, legal/ethical constraints, and harm hypotheses; set acceptable disparity tolerances (e.g., ΔFPR ≤ 0.03).  
- **Delegate:** Default to **Augmentation** in sensitive contexts; add human review and appeals.  
- **Direct:** Prompt Specs must include banned inputs (e.g., PII), source whitelists, and bias probes among acceptance tests.  
- **Diagnose:** Compute group metrics with intervals; run counterfactual tests; perform slice discovery.  
- **Decide:** Use pre‑registered Go/No‑Go criteria; choose mitigations; plan rollback.  
- **Document:** Model Cards, Datasheets, audit logs, incident reports, and ongoing monitoring plan.

---

## Hands‑On Exercises

### Exercise 1 — Bias Mapping & Risk Storyboard (No‑Code)
**Time:** 25–30 min | **Format:** Teams of 3–4  
**Scenario (choose one):**  
- Hiring résumé pre‑screening  
- Credit line increase recommendations  
- Toxic speech moderation for a gaming forum  

**Tasks.**  
1. Fill the **Bias Hypothesis Canvas** (template below).  
2. Draft **three falsifiable fairness hypotheses** (utility + harm).  
3. Propose **acceptance tests** and **appeal workflow**.

**Bias Hypothesis Canvas**  
- **Protected attributes & proxies:**  
- **Data sources & representativeness risks:**  
- **Label construction (who/when/how):**  
- **Likely bias types:** historical / representation / measurement / aggregation / emergent feedback  
- **Stakeholders & power:** who benefits, who bears risk, who can appeal  
- **Fairness hypotheses (3):**  
- **Acceptance tests & thresholds:**  

**Deliverable:** 1‑page canvas + a short justification of thresholds.

---

### Exercise 2 — Bias Audit with Metrics (Code‑Optional)
**Time:** 35–45 min | **Format:** Pairs or teams  
**Dataset options:** Adult Income (UCI), COMPAS (with caution and context), or a course‑provided tabular set with `sex`/`race` proxies.  

**Part A (no‑code):** Compute by hand (from provided contingency tables) selection rates, TPR, FPR, and disparities for two groups.  

**Part B (Python option using Fairlearn)**  
```python
# Bias audit template with Fairlearn
import numpy as np, pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
from fairlearn.metrics import MetricFrame, selection_rate, true_positive_rate, false_positive_rate

# Load your dataframe `df` with X cols, y target, and a sensitive feature `sex` (e.g., 'Female','Male')
X = df.drop(columns=['target'])
y = df['target']
A = df['sex']  # sensitive feature

num = X.select_dtypes(include='number').columns
cat = X.select_dtypes(exclude='number').columns
pre = ColumnTransformer([
    ('num', 'passthrough', num),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat)
])

clf = Pipeline(steps=[('pre', pre), ('lr', LogisticRegression(max_iter=1000))])
clf.fit(X, y)
p = clf.predict_proba(X)[:,1]

# Overall utility
print('AUROC:', roc_auc_score(y, p))

# Group metrics
mf = MetricFrame(metrics={'sel': selection_rate,
                          'tpr': true_positive_rate,
                          'fpr': false_positive_rate},
                 y_true=y, y_pred=(p>0.5).astype(int), sensitive_features=A)
print(mf.by_group)
print('Demographic parity diff (sel):', mf.difference(method='between_groups')['sel'])
print('Equalized odds diffs:', {m: mf.difference(method='between_groups')[m] for m in ['tpr','fpr']})
```

**Analysis prompts:**  
- Where are the largest disparities? Are they within your tolerance?  
- How does uncertainty (CIs) affect your decision?  

**Deliverable:** A short audit memo with a table of metrics + decision recommendation (ship/mitigate/hold).

---

### Exercise 3 — Mitigation Lab: Pre‑, In‑, and Post‑Processing
**Time:** 40–50 min | **Format:** Teams  
**Goal:** Apply one mitigation path and evaluate trade‑offs.

**Options (choose one):**  
1. **Pre‑processing (Reweighing or Resampling):** Adjust sample weights to equalize representation before training.  
2. **In‑processing (Constrained learning):** Use Fairlearn’s `ExponentiatedGradient` with `DemographicParity` or `EqualizedOdds`.  
3. **Post‑processing (ThresholdOptimizer):** Group‑specific thresholds to satisfy a fairness constraint at decision time.

**Starter code (in‑processing)**  
```python
from fairlearn.reductions import ExponentiatedGradient, DemographicParity, EqualizedOdds
from sklearn.linear_model import LogisticRegression

base = LogisticRegression(max_iter=1000)
constraint = EqualizedOdds()  # or DemographicParity()
redu = ExponentiatedGradient(base, constraints=constraint)
redu.fit(X, y, sensitive_features=A)
yp = redu.predict(X)

mf2 = MetricFrame(metrics={'sel': selection_rate,
                           'tpr': true_positive_rate,
                           'fpr': false_positive_rate},
                  y_true=y, y_pred=yp, sensitive_features=A)
print(mf2.by_group)
```

**Evaluate:** Compare utility (AUROC/accuracy) vs. disparity metrics pre/post mitigation. Discuss where harm decreased and at what cost.  

**Deliverable:** 1‑page Mitigation Report (before/after metrics, chosen constraint, decision rule, monitoring plan).

---

## Assessment
- **Formative:** Instructor checks on Exercise 1 canvases; quick stand‑ups during Exercises 2–3.  
- **Summative (Homework):** Submit (a) Bias Audit Memo, (b) Mitigation Report, (c) updated Oversight Canvas with Guardrails and Monitoring thresholds.  

**Rubric (30 pts total).**  
- **Bias Audit (10):** Correct metrics, clear disparities, uncertainty discussed.  
- **Mitigation Report (10):** Appropriate method, quantitative before/after, trade‑offs explicit.  
- **Oversight Canvas (10):** Guardrails, appeal path, monitoring signals & rollback triggers.

---

## Instructor Notes & Facilitation Tips
- Use *realistic* but de‑identified examples; address the ethics of using datasets like COMPAS (historical context, critiques).  
- Push for **numbers**: disparity tolerances, confidence intervals; require pre‑registered thresholds.  
- Link back to **interaction modes**: default to Augmentation for consequential decisions; specify human review and redress.  
- Encourage students to write **datasheets** and **model cards** for all exercises.  
- If time permits, demonstrate **slice discovery** (e.g., error clustering) to reveal hidden groups.

---

## Templates (Copy‑Paste)

**Fairness Acceptance Tests**  
| ID | Metric | Groups | Threshold | Rationale |
|----|--------|--------|-----------|-----------|
| F‑1 | Demographic parity diff (selection) | A vs. B | ≤ 0.03 | Regulation/Policy |
| F‑2 | Equalized odds (TPR diff) | A vs. B | ≤ 0.05 | Harm minimization |
| F‑3 | Equalized odds (FPR diff) | A vs. B | ≤ 0.03 | False‑positive harms |
| F‑4 | Calibration slope/intecept | Both | within 10% of 1/0 | Decision quality |
| F‑5 | Subgroup min‑perf floor | All | AUROC ≥ 0.75 | Reliability |

**Oversight Canvas (bias‑specific)**  
- Mode: Automation / Augmentation / Agency (why)  
- Guardrails: PII scrubbing; policy filters; subgroup error caps; logging  
- RACI: Model Owner / Reviewer / Accountable Exec / Incident Manager  
- Appeals: user‑facing explanation + human adjudication  
- Monitoring: PSI thresholds; subgroup deltas; incident SLOs  
- Rollback triggers: e.g., FNR disparity >1.2× for 3 days  

**Bias Audit Memo Outline**  
- Context & stakes  
- Data & label provenance  
- Metrics & thresholds  
- Findings (tables/plots)  
- Risks & ethical considerations  
- Recommendation & monitoring plan  

---

## References (Selected, APA‑style)
- Banaji, M. R., & Greenwald, A. G. (2013). *Blindspot: Hidden Biases of Good People.* Delacorte.  
- Barocas, S., & Selbst, A. D. (2016). Big data’s disparate impact. *California Law Review, 104*(3), 671–732.  
- Benjamin, R. (2019). *Race After Technology: Abolitionist Tools for the New Jim Code.* Polity.  
- Crawford, K. (2021). *Atlas of AI: Power, Politics, and the Planetary Costs of Artificial Intelligence.* Yale University Press.  
- Haraway, D. (1988). Situated knowledges: The science question in feminism... *Feminist Studies, 14*(3), 575–599.  
- Kahneman, D. (2011). *Thinking, Fast and Slow.* Farrar, Straus and Giroux.  
- Lyotard, J.‑F. (1984). *The Postmodern Condition: A Report on Knowledge.* University of Minnesota Press.  
- Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). Model Cards for Model Reporting. In *FAT* (pp. 220–229).  
- Noble, S. U. (2018). *Algorithms of Oppression: How Search Engines Reinforce Racism.* NYU Press.  
- Selbst, A. D., Boyd, D., Friedler, S., Venkatasubramanian, S., & Vertesi, J. (2019). Fairness and abstraction in sociotechnical systems. In *FAT* (pp. 59–68).  
- Gebru, T., Morgenstern, J., Vecchione, B., et al. (2018). Datasheets for Datasets. *arXiv:1803.09010*.  
- National Institute of Standards and Technology. (2023). *AI Risk Management Framework (AI RMF 1.0).* NIST.  

> Tools: Fairlearn, AIF360; SHAP/LIME for slice‑level diagnostics; What‑If Tool; NIST TEVV. Cite and disclose any AI assistance when submitting.

