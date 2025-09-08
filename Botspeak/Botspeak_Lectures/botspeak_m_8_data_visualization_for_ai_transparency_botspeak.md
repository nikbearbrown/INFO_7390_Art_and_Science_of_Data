# Lesson (Markdown): Module 8 — Data Visualization for AI Transparency

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M8 – Data Visualization for AI Transparency  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, critique labs, rapid‑prototyping, and code‑optional plotting exercises

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Explain how **human perception** shapes understanding of AI outputs and why design choices affect trust.  
2. Identify **misleading visualization patterns** and propose ethical alternatives for AI dashboards and reports.  
3. Apply **McLuhan’s** idea—*the medium is the message*—to critique how dashboards frame AI systems and user agency.  
4. Build and iterate **AI transparency visualizations** (calibration, confusion matrices, drift/fairness small‑multiples, explanation plots) suited to different audiences.  
5. Integrate visualization work into Botspeak pillars **Effective Communication** and **Rapid Prototyping**, with explicit acceptance tests and usability checks.

**Botspeak Pillar Alignment:** Effective Communication, Rapid Prototyping, Critical Evaluation, Technical Understanding, Ethical Reasoning, Theoretical Foundation.

---

## Key Terms
- **Preattentive attributes:** Visual properties (position, length, orientation, hue, saturation, shape) processed rapidly without focused attention.  
- **Gestalt principles:** Proximity, similarity, continuity, closure; govern how we perceive groups and patterns.  
- **Data‑ink ratio (Tufte):** Maximize ink devoted to data, minimize non‑informative decoration.  
- **Lie factor (Tufte):** Ratio of effect shown in the graphic to the effect in the data.  
- **Small multiples:** Series of similar charts for easy comparison across slices/time.  
- **Calibration plot (reliability diagram):** Shows agreement between predicted probabilities and observed frequencies.  
- **PSI (Population Stability Index):** Drift measure comparing distributions across periods.  
- **Dashboard theater:** Interfaces that *appear* transparent but hide uncertainty, bias, or decision context.

---

## Theory Blocks

### 1) Philosophical Foundations — Perception & Understanding AI Decisions
**Claim.** Transparency is not just disclosure; it is *perception‑ready* evidence. Visual encodings either reduce or increase cognitive load.

**Perception facts to exploit ethically**  
- **Position/length** encodings support more accurate comparisons than angle/area (Cleveland & McGill).  
- **Ordered hue/lightness** aids ordinal judgments; categorical palettes should avoid implying order.  
- **Annotations** (thresholds, uncertainty bands) anchor interpretation; absence invites overconfidence.  
- **Accessibility**: color‑blind‑safe palettes, sufficient contrast, text alternatives.

**Implication for AI**: When showing model performance, prefer **position/length** (bars/lines) for error rates and **bands** for uncertainty; reserve vivid hues for alarms to avoid alarm fatigue.

---

### 2) Critical Thinking — Can Visualizations Mislead Us?
**Yes—easily.** Common failure modes:
- **Truncated/dual y‑axes** exaggerate effects; hidden baselines distort risk deltas.  
- **Cherry‑picked time windows** conceal seasonality or post‑incident recovery.  
- **Aggregation hides harm** (Simpson’s paradox): overall accuracy up while a subgroup collapses.  
- **Ambiguous denominators** (rates vs counts) and **noncomparable bins**.  
- **Decorative metaphors** (gauges, 3D, pictograms) inflate lie factor.  
- **Uncertainty omission** (no CIs or coverage) ⇒ false precision.

**Ethical alternative:** Declare what’s unknown; show uncertainty and slices; pre‑register dashboard acceptance tests (e.g., *must* include subgroup metrics and clear baselines).

---

### 3) McLuhan’s Lens — *The Medium is the Message*
**Reading.** Interfaces shape meaning. A dashboard defaults users into some **form of life**: what’s surfaced becomes “the truth.”  
- **Message of the medium (examples):**  
  - A single KPI with a green check = “ship it” (invites Automation).  
  - Small multiples of subgroup error with red flags = “investigate before action” (invites Augmentation).  
- **Design duty:** Choose a medium whose message aligns with **safety** and **accountability**; avoid dashboard theater.  
- **Trust is situated:** Executives, engineers, auditors, and end‑users need *different* views.

---

### 4) Design Principles for AI Transparency
- **Match audience → task → graphic.** Engineer: fine‑grained debugging; executive: trend + risk flags; regulator: compliance evidence; end‑user: decision reason & recourse.  
- **Show uncertainty by default** (CIs, predictive intervals, error bars).  
- **Always slice** by protected or risk‑relevant groups; use **small multiples**.  
- **Prefer comparable scales** and **fixed axes** across panels.  
- **Narrate** with succinct **callouts**: “AUROC=0.87 ±0.02; subgroup FNR up 40% week‑over‑week.”  
- **Link to evidence**: dataset cards, model cards, validation memos, incident logs.  
- **Version & provenance**: every chart stamped with data time window, model version, code hash.

---

## Botspeak Integration
**Define → Delegate → Direct → Diagnose → Decide → Document**  
- **Define:** Audience, decisions supported, risks; pick KPIs (utility + harm) and uncertainty forms.  
- **Delegate:** Mode choice affects visuals: Agency demands stricter transparency (alerts, red‑teaming panes) than Augmentation/Automation.  
- **Direct:** Prompt/Task Specs include *visualization acceptance tests* (see below).  
- **Diagnose:** Use calibration, subgroup small‑multiples, drift/incident timelines, explanation summaries.  
- **Decide:** Gate shipping on *visual* evidence meeting thresholds.  
- **Document:** Export dashboard snapshots to the audit trail; keep a change log; include rationale for any visual design changes.

**Visualization Acceptance Tests (examples)**  
- Baselines and axis ranges declared; no dual axes without explicit rationale.  
- At least one uncertainty element per performance chart.  
- Subgroup small‑multiples present for fairness‑relevant dimensions.  
- Data provenance/version stamped; links to model/datasheet.

---

## Hands‑On Exercises

### Exercise A — Perception Audit & Chart Triage (No‑Code)
**Time:** 20–25 min | **Format:** Triads  
**Prompt:** You receive four charts from a model team: (1) ROC curve with no CIs; (2) Accuracy over time with truncated y‑axis; (3) Single confusion matrix; (4) Overall selection rate bar plot.  
**Tasks:**  
1. Identify at least **six** perception/design issues.  
2. Rewrite the visual brief: audience → task → graphic recommendation.  
3. Sketch corrected charts (paper prototype) including uncertainty and subgroup views.  
**Deliverable:** 1‑page triage memo with sketches (photos allowed) and an *acceptance test* checklist.

---

### Exercise B — Build a Mini Transparency Dashboard (Code‑Optional)
**Time:** 40–55 min | **Format:** Pairs  
**Goal:** Produce four panels: Confusion Matrix, ROC/PR, Reliability Diagram, and Subgroup Error Small‑Multiples.  

```python
# Minimal scaffolding (scikit-learn + matplotlib)
import numpy as np, pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, brier_score_loss
import matplotlib.pyplot as plt

# 1) Data (with a synthetic sensitive attribute for slicing)
X, y = make_classification(n_samples=6000, n_features=12, n_informative=6,
                           weights=[0.7,0.3], random_state=7)
# Pretend group A/B depends on a hidden feature threshold
A = (X[:,0] > np.median(X[:,0])).astype(int)  # 0/1 groups
Xtr, Xte, ytr, yte, Atr, Ate = train_test_split(X, y, A, test_size=0.4, random_state=7)

# 2) Train
clf = RandomForestClassifier(n_estimators=300, random_state=7)
clf.fit(Xtr, ytr)
proba = clf.predict_proba(Xte)[:,1]
yhat = (proba>=0.5).astype(int)

# 3a) Confusion Matrix
cm = confusion_matrix(yte, yhat)
fig, ax = plt.subplots()
im = ax.imshow(cm)
ax.set_title('Confusion Matrix'); ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, cm[i,j], ha='center', va='center')
plt.show()

# 3b) ROC & PR
fpr, tpr, _ = roc_curve(yte, proba); roc_auc = auc(fpr, tpr)
pr_p, pr_r, _ = precision_recall_curve(yte, proba)
fig, ax = plt.subplots(); ax.plot(fpr, tpr, label=f'ROC AUC={roc_auc:.2f}')
ax.plot([0,1],[0,1],'--'); ax.set_xlabel('FPR'); ax.set_ylabel('TPR'); ax.legend(); plt.show()
fig, ax = plt.subplots(); ax.plot(pr_r, pr_p); ax.set_xlabel('Recall'); ax.set_ylabel('Precision'); plt.show()

# 3c) Reliability Diagram (10-bin)
bins = np.linspace(0,1,11)
ids = np.digitize(proba, bins)-1
acc = [yte[ids==i].mean() if np.any(ids==i) else np.nan for i in range(10)]
conf = [proba[ids==i].mean() if np.any(ids==i) else np.nan for i in range(10)]
fig, ax = plt.subplots(); ax.plot([0,1],[0,1])
ax.scatter(conf, acc); ax.set_title('Reliability'); ax.set_xlabel('Mean predicted'); ax.set_ylabel('Observed'); plt.show()
print('Brier score:', brier_score_loss(yte, proba))

# 3d) Subgroup Small-Multiples (FNR by group)
fnr = {}
for g in [0,1]:
    mask = (Ate==g)
    y_g, yhat_g = yte[mask], yhat[mask]
    fnr[g] = ((y_g==1) & (yhat_g==0)).sum() / max(1,(y_g==1).sum())

fig, ax = plt.subplots(); ax.bar(['Group 0','Group 1'], [fnr[0], fnr[1]])
ax.set_title('False Negative Rate by Group'); plt.show()
```

**Extensions:** Add **uncertainty bands** via bootstrapping; add **drift** by computing PSI of key features month‑over‑month and line‑plotting.  
**Deliverable:** A PNG or notebook with the four panels and a brief read‑me explaining **who** the dashboard is for and **what decision** it supports.

---

### Exercise C — Rapid Prototyping & Usability Test (No‑/Low‑Code)
**Time:** 30–40 min | **Format:** Teams  
**Goal:** Apply McLuhan: design two versions of the same transparency interface with different *messages* (e.g., “proceed with caution” vs “ready to deploy”).  
**Tasks:**  
1. Create **two paper/Figma wireframes** of a model dashboard for executives.  
2. Run a 5‑minute **think‑aloud** usability test with another team; time to task completion: “Can you tell if subgroup FNR worsened this week?”  
3. Record misinterpretations; revise to reduce cognitive load and misreads.  
**Deliverable:** Before/after wireframes + a one‑paragraph McLuhan critique: how did the *medium* shift the message?

---

## Assessment
- **Formative:** In‑class critique (Exercise A); code review or screen‑share (Exercise B); usability feedback (Exercise C).  
- **Summative (Homework):** Submit (a) the mini dashboard artifact, (b) a short *Transparency Spec* (below), and (c) a 1‑page **Dashboard Ethics Note** describing how the medium shapes user trust and decisions.

**Rubric (30 pts total).**  
- **Design correctness (10):** Proper encodings, baselines, uncertainty, subgroup slices.  
- **Technical soundness (10):** Accurate calculations; clear labeling; provenance/versioning.  
- **Communication & ethics (10):** Audience fit; McLuhan critique; actionability.

---

## Templates (Copy‑Paste)

**Transparency Spec**  
- **Audience & decisions supported:**  
- **KPIs (utility + harm) & definitions:**  
- **Uncertainty elements:**  
- **Slices & small‑multiples:**  
- **Drift & incident views:**  
- **Provenance/versioning:**  
- **Accessibility checklist:**  

**Dashboard Acceptance Tests**  
1. Baselines/axes visible; no dual axes (or justified).  
2. At least one uncertainty depiction per performance view.  
3. Subgroup small‑multiples present with fixed scales.  
4. Data time window and model version labeled.  
5. Links to model/datasheet; export button writes to audit log.

**Annotation & Caption Guide**  
- **Title:** task + timeframe  
- **Lead:** 1–2 sentences with the key decision implication  
- **Callouts:** thresholds, alerts, subgroup outliers  
- **Footers:** data source, model/version, run time, author  

---

## Instructor Notes & Facilitation Tips
- Invite *critical* readings of visuals; ask “What is this chart trying to make you believe?”  
- Use **small datasets** for quick iteration; the point is design, not compute.  
- Enforce an **accessibility pass** (contrast, font, alt‑text) before grading.  
- Tie back to Module 3 (bias), 4 (explainability), and 5 (uncertainty): every dashboard should show **fairness slices**, **explanations**, and **calibration**.

---

## References (Selected, APA‑style)
- Bertin, J. (2011). *Semiology of Graphics* (W. J. Berg, Trans.). Esri Press.  
- Cairo, A. (2013). *The Functional Art: An Introduction to Information Graphics and Visualization*. New Riders.  
- Cleveland, W. S., & McGill, R. (1984). Graphical perception: Theory, experimentation, and application. *Journal of the American Statistical Association, 79*(387), 531–554.  
- Few, S. (2013). *Information Dashboard Design* (2nd ed.). Analytics Press.  
- McLuhan, M. (1964). *Understanding Media: The Extensions of Man*. McGraw‑Hill.  
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.  
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.  
- Ware, C. (2012). *Information Visualization: Perception for Design* (3rd ed.). Morgan Kaufmann.  
- D’Ignazio, C., & Klein, L. F. (2020). *Data Feminism*. MIT Press.  

> Supplement: Model Cards, Datasheets, What‑If Tool, SHAP/ALE plots for explanation views; Fairlearn for fairness slices; NIST TEVV for validation visual evidence.

