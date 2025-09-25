# Lesson (Markdown): Module 4 — Explainability & Interpretability of AI Models

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M4 – Explainability & Interpretability  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, labs with SHAP & LIME, and communication artifacts

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Distinguish model **interpretability** (intrinsic transparency) from **explainability** (post‑hoc justifications) and argue when each is appropriate.  
2. Analyze whether *understanding* is necessary for *trust* using the **Black Box Problem** and perspectives from philosophy of language and science.  
3. Implement **local** and **global** explanations with **SHAP** and **LIME**; interpret outputs responsibly.  
4. Evaluate explanations for **faithfulness**, **stability**, and **usefulness**; identify failure modes (e.g., spurious saliency).  
5. Produce audience‑appropriate explanation artifacts (plots, short prose) aligned with Botspeak pillars **Technical Understanding** and **Effective Communication**.  

**Botspeak Pillar Alignment:** Technical Understanding, Effective Communication, Critical Evaluation, Theoretical Foundation, Learning by Doing.

---

## Key Terms
- **Interpretability:** The degree to which a human can *directly* understand a model (e.g., small decision trees, linear models).  
- **Explainability:** Post‑hoc methods describing a trained model’s behavior (e.g., LIME, SHAP, counterfactuals).  
- **Local vs Global explanations:** Local explain a single prediction; global summarize behavior across the dataset.  
- **Faithfulness:** Explanations accurately track the model’s internal decision logic (not merely plausible stories).  
- **Stability/Robustness:** Similar inputs produce similar explanations; explanations resist small perturbations.  
- **Simulatability:** A human can mentally simulate the model; often requires simple models or distilled surrogates.  
- **Language game (Wittgenstein):** Meaning arises from use within social practices—guides how we evaluate whether explanations are meaningful for audiences.  

---

## Theory Blocks

### 1) The Black Box Problem: Is Understanding Necessary for Trust?
- **Epistemic trust vs. practical reliability.** We can trust an instrument without full mechanistic understanding (airplane autopilot), but stakes, contestability, and moral accountability raise the bar for AI.  
- **Positions:**  
  - *Instrumentalist:* If a model is validated under diverse conditions and monitored, understanding is optional.  
  - *Interpretabilist:* Understanding matters for error diagnosis, fairness, and accountability; some contexts demand intrinsically interpretable models (Rudin).  
- **Botspeak stance:** Pick the **interaction mode** and explanation burden by risk: higher stakes → stronger demands for transparency, oversight, and interpretability.

### 2) Does it Matter if We Don’t Know *How* Good Predictions Are Made?
- **Pros:** Fast progress with complex models; post‑hoc checks can be sufficient for many low‑risk tasks.  
- **Cons:** Hidden shortcuts (spurious correlations), distribution shift, and inability to reason about counterfactuals or provide recourse to affected individuals.  
- **Governance tie‑in:** TEVV requires evidence of performance, harms, and monitoring; explanations help satisfy stakeholder information rights (appeals, adverse action notices).

### 3) Wittgenstein’s Language Games: Are AI Explanations Meaningful—or Tricks?
- **Meaning‑as‑use.** An explanation is meaningful if it *does work* in a specific practice (e.g., helps a clinician decide, informs an appeal).  
- **Risk of “explanation theater.”** Plausible‑sounding rationales may not be **faithful** (Slack et al.; Adebayo et al.).  
- **Design cue:** Tailor explanations to the *form of life* (stakeholder role): data scientist (feature attributions), regulator (simple rules and thresholds), end‑user (counterfactual recourse).

### 4) Method Landscape
- **Intrinsic interpretability:** Sparse linear models; small trees; monotonic GBMs; scoring systems; rule lists.  
- **Post‑hoc global:** Permutation importance; Partial Dependence (PDP); Accumulated Local Effects (ALE); SHAP summary.  
- **Post‑hoc local:** LIME; SHAP (Kernel/Tree/Linear); saliency for images; counterfactuals.  
- **Surrogates:** Train a transparent model to mimic a black box; validate fidelity (R², stability).

### 5) Pitfalls & Validity Checks
- **Sanity checks** (Adebayo): Explanations should change when model or data are randomized.  
- **Fooling explainers** (Slack et al.): Adversarial artifacts can yield misleading explanations.  
- **Stability tests:** Repeat explanations under small perturbations; require bounded variance.  
- **Faithfulness probes:** Feature removal/occlusion tests; deletion/insertion curves; infidelity metrics.  
- **Communication risks:** Over‑precision; hiding uncertainty; implying causality from correlation.

---

## Botspeak Integration
**Define → Delegate → Direct → Diagnose → Decide → Document** with explainability:
- **Define:** Stakeholder questions ("What would change the decision?") and risk; pick explanation goals (debugging, compliance, user recourse).  
- **Delegate:** Choose **Automation/Augmentation/Agency** and the minimum explanation standard by risk.  
- **Direct:** Prompt Spec includes *explanation format*, audience, and acceptance tests (e.g., stability ≥ threshold).  
- **Diagnose:** Run SHAP/LIME, PDP/ALE; compute faithfulness/stability metrics.  
- **Decide:** Act on insights; adjust thresholds; choose interpretable substitutes where needed.  
- **Document:** Explanation Cards, Model Cards (global + subgroup), user‑facing FAQs and counterfactual recourse language.

---

## Hands‑On Labs (SHAP & LIME)

> **Setup (students):** A Python environment with `scikit‑learn`, `matplotlib`, `pandas`, `numpy`, `shap`, and `lime`. If new, create a fresh virtual env.

```bash
# suggested setup
python -m venv venv && source venv/bin/activate  # or conda create -n botspeak-m4 python=3.10
pip install -U scikit-learn pandas numpy matplotlib shap lime
```

### Lab A — Local & Global Explanations on a Classifier (Breast Cancer dataset)
**Goal:** Train a tree ensemble and produce SHAP & LIME explanations; compare and check stability.

```python
# ====== Train a model ======
import numpy as np, pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7, stratify=y)
clf = RandomForestClassifier(n_estimators=300, random_state=7)
clf.fit(Xtr, ytr)
proba = clf.predict_proba(Xte)[:,1]
print('AUROC:', roc_auc_score(yte, proba))

# ====== SHAP: global & local ======
import shap
shap.explainers._tree.TreeExplainer  # sanity check that tree explainer is available
explainer = shap.TreeExplainer(clf)
shap_values = explainer.shap_values(Xte)

# Global: beeswarm summary (class 1)
shap.summary_plot(shap_values[1], Xte, show=False)

# Local: force plot for a single case
i = 0
shap.initjs()
shap.force_plot(explainer.expected_value[1], shap_values[1][i], Xte.iloc[i,:])

# Dependence plot for a key feature
top_feature = X.columns[np.abs(shap_values[1]).mean(0).argmax()]
shap.dependence_plot(top_feature, shap_values[1], Xte, show=False)
```

```python
# ====== LIME: local explanation for the same case ======
from lime.lime_tabular import LimeTabularExplainer

expl = LimeTabularExplainer(
    Xtr.values,
    feature_names=X.columns,
    class_names=['benign','malignant'],
    discretize_continuous=True,
    mode='classification')

exp = expl.explain_instance(
    Xte.iloc[i,:].values,
    clf.predict_proba,
    num_features=8)

print(exp.as_list())  # top local features
fig = exp.as_pyplot_figure()
```

**Checks & Questions**  
1. Do SHAP and LIME agree on the top‑k features for this case?  
2. **Stability:** Repeat the LIME run with different `random_state`; how much do weights vary?  
3. **Faithfulness probe:** Zero‑out the top 1–3 features and re‑score; does proba drop as expected?  

**Deliverable:** 1‑page *Explanation Card* with AUROC, SHAP summary plot, one LIME local list, and notes on stability/faithfulness checks.

---

### Lab B — Global Behavior on a Regressor (California Housing)
**Goal:** Use SHAP to summarize a regressor globally; compare PDP vs. SHAP dependence.

```python
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score

Xy = fetch_california_housing(as_frame=True)
X, y = Xy.data, Xy.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7)
reg = GradientBoostingRegressor(random_state=7)
reg.fit(Xtr, ytr)
pred = reg.predict(Xte)
print('R^2:', r2_score(yte, pred))

expl = shap.Explainer(reg, Xtr)
sv = expl(Xte)
shap.plots.beeswarm(sv, show=False)

# SHAP dependence for MedInc
shap.plots.scatter(sv[:, 'MedInc'], color=sv)
```

```python
# PDP for comparison
from sklearn.inspection import plot_partial_dependence
import matplotlib.pyplot as plt
plot_partial_dependence(reg, Xte, ['MedInc'])
plt.show()
```

**Checks & Questions**  
- Do PDP and SHAP dependence tell a consistent story?  
- Are there signs of **interaction effects** (color variation in SHAP scatter)?  
- Draft one sentence explaining the global driver of predictions for non‑experts.

**Deliverable:** Global *Explanation Card* with beeswarm plot, one dependence/PDP comparison, and a plain‑language summary (≤80 words).

---

### Lab C — Faithfulness & Stability Mini‑Audit (Methodology)
**Goal:** Quantify whether explanations are behaving sensibly.

**Steps**  
1. **Sanity check:** Randomize labels or shuffle features; verify SHAP importances degrade.  
2. **Deletion curve:** Rank features by attribution; iteratively remove and re‑score; plot performance drop.  
3. **Stability test:** Add small Gaussian noise to inputs; compute attribution distance (e.g., cosine distance of top‑k vectors) across 20 runs; report mean ± sd.  

**Deliverable:** 1‑page *Explainability QA Memo* with plots and a Go/No‑Go recommendation for your use case.

---

## Communication Artifact Templates

**Explanation Card (Local)**  
- Context & stake  
- Input snapshot (key features)  
- Prediction & uncertainty  
- Top contributors (method + values)  
- Counterfactual recourse (“Decision would change if …”)  
- Caveats (data limits, stability notes)

**Explanation Card (Global)**  
- Model & data summary  
- Performance (with CIs)  
- Top features (global)  
- Key plots (beeswarm/dependence)  
- Known shortcuts/risks  
- Monitoring hooks (drift, feature ranges)

---

## Assessment
- **Formative:** Lab check‑ins, short share‑outs; collect Explanation Cards for feedback.  
- **Summative (Homework):** Submit (a) Local and Global Explanation Cards, (b) Explainability QA Memo, (c) updated Prompt Spec including explanation format and acceptance tests.

**Rubric (30 pts total).**  
- **Technical (12):** Correct use of SHAP/LIME; coherent plots; basic checks performed.  
- **Faithfulness/Stability (8):** Evidence from sanity, deletion, or perturbation tests; clear interpretation.  
- **Communication (10):** Audience‑appropriate summaries; limitations and uncertainty stated; Botspeak artifacts complete.

---

## Instructor Notes & Facilitation Tips
- Emphasize **use‑case‑first** explanation design; avoid explanation theater.  
- For sensitive domains, consider **intrinsically interpretable** models before resorting to post‑hoc methods.  
- Require students to report **uncertainty** in performance and explanations (e.g., bootstrap CIs for metrics; variance of attributions).  
- Encourage side‑by‑side **PDP vs. SHAP** to illustrate when linear narratives mask interactions.  
- If compute is limited, use smaller subsets or Kernel/Linear SHAP.

---

## References (Selected, APA‑style)
- Adebayo, J., Gilmer, J., Muelly, M., et al. (2018). Sanity checks for saliency maps. In *NeurIPS*.  
- Doshi‑Velez, F., & Kim, B. (2017). Towards a rigorous science of interpretable machine learning. *arXiv:1702.08608*.  
- Gilpin, L. H., Bau, D., Yuan, B. Z., et al. (2018). Explaining explanations in AI. In *WSDM Workshop*.  
- Lipton, Z. C. (2018). The mythos of model interpretability. *Communications of the ACM, 61*(10), 36–43.  
- Lundberg, S. M., & Lee, S.‑I. (2017). A unified approach to interpreting model predictions. In *NeurIPS*.  
- Miller, T. (2019). Explanation in AI: Insights from the social sciences. *Artificial Intelligence, 267*, 1–38.  
- Molnar, C. (2022). *Interpretable Machine Learning* (2nd ed.). Leanpub.  
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). “Why should I trust you?” Explaining any classifier. In *KDD*.  
- Rudin, C. (2019). Stop explaining black‑box machine learning models for high‑stakes decisions and use interpretable models instead. *Nature Machine Intelligence, 1*(5), 206–215.  
- Slack, D., Hilgard, S., Jia, E., et al. (2020). Fooling LIME and SHAP: Adversarial attacks on post hoc explanation methods. In *AIES*.  
- Wittgenstein, L. (1953). *Philosophical Investigations*. Blackwell.  

> See also: PDP/ALE resources; What‑If Tool; DiCE for counterfactuals; NIST TEVV.

