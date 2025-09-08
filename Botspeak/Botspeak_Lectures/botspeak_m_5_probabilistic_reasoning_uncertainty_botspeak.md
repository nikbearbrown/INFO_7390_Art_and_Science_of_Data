# Lesson (Markdown): Module 5 — Probabilistic Reasoning & Uncertainty in AI

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M5 – Probabilistic Reasoning & Uncertainty  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, code‑optional labs, decision‑focused artifacts  

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Explain **Hume’s Problem of Induction** and its implications for model generalization and deployment risk.  
2. Contrast **Bayesian** and **Frequentist** views of probability; interpret **confidence** vs **credible** intervals and **p‑values** vs **Bayes factors**.  
3. Distinguish **aleatoric** and **epistemic** uncertainty and identify practical estimation techniques (calibration, ensembles, conformal prediction).  
4. Use probability distributions to express model **confidence**, compute predictive **intervals/sets**, and make **cost‑aware** decisions.  
5. Integrate uncertainty practices into the Botspeak pillars **Stochastic Reasoning** and **Theoretical Foundation**, and into the **Define→Delegate→Direct→Diagnose→Decide→Document** loop.

---

## Key Terms
- **Induction (Hume):** Inference from observed cases to unobserved; lacks deductive justification.  
- **Aleatoric uncertainty:** Irreducible randomness in data (noise, inherent variability).  
- **Epistemic uncertainty:** Uncertainty due to limited data/knowledge; reducible with more/better data or model class.  
- **Frequentist probability:** Long‑run relative frequency; parameters are fixed, data are random.  
- **Bayesian probability:** Degree of belief; parameters are random with priors; data update beliefs via Bayes’ rule.  
- **Confidence interval (CI):** Procedure that covers the true parameter at a specified frequency under repeated sampling.  
- **Credible interval (CrI):** Posterior probability interval for a parameter (e.g., 95% probability mass).  
- **Calibration (probability):** Agreement between predicted probabilities and observed frequencies (reliability).  
- **Proper scoring rules:** Metrics that incentivize honest probability forecasts (e.g., log loss, Brier score).  
- **Conformal prediction:** Distribution‑free method to produce prediction **intervals/sets** with guaranteed coverage under exchangeability.  

---

## Theory Blocks

### 1) Philosophical Foundations — Hume’s Induction & Trust in Prediction
- **Problem.** No finite set of observations logically guarantees future outcomes; ML models inherit this limitation.  
- **Implications.** Validation must approximate the future (out‑of‑time/-domain tests), and uncertainty must be **quantified** and **communicated**; decision rules must account for **risk** and **error costs**.  
- **Botspeak stance.** Treat predictions as **claims with uncertainty**; pre‑register acceptance thresholds; monitor for shift.

### 2) Are Probabilities “Real” or Tools?
- **Subjective (de Finetti):** Probability as coherent degrees of belief; priors encode knowledge; Dutch book arguments justify consistency.  
- **Objective/Frequentist/Propensity:** Probabilities reflect long‑run frequencies or physical tendencies.  
- **Pragmatic view.** In engineering, probabilities are **instruments** for decisions; what matters is *coherence, calibration, and consequences*.  

### 3) Bayesian vs Frequentist — A Comparative Map
| Aspect | Bayesian | Frequentist |
|---|---|---|
| Unknowns | Random with **priors** | Fixed constants |
| Inference | **Posterior** ∝ prior × likelihood | Estimators, confidence intervals, p‑values |
| Evidence | Bayes factor, posterior odds | Hypothesis tests (α), likelihood ratio tests |
| Intervals | **Credible** intervals (probability statements) | **Confidence** intervals (coverage properties) |
| Pros | Integrates prior info; natural uncertainty quantification | Prior‑free; well‑studied procedures and guarantees |
| Cautions | Prior sensitivity, computation | Misinterpretation of p/CIs; limited direct probability statements |

**Posterior predictive** distributions translate parameter uncertainty into **forecast uncertainty**, vital for decisions and intervals.

### 4) Uncertainty Taxonomy & Estimation
- **Aleatoric:** noise models, quantile regression, heteroscedastic models.  
- **Epistemic:** model class uncertainty—ensembles, Bayesian NNs (MC dropout), bootstrapping.  
- **Calibration:** temperature scaling, Platt scaling, isotonic regression; evaluate with **reliability diagrams**, **ECE**, **Brier**, **log loss**.  
- **Distribution shift:** express uncertainty via wider intervals, abstention options, or **conformal** sets with guaranteed coverage.

### 5) Decision‑Making with Uncertainty
- **Expected utility / cost curves:** choose thresholds to minimize expected cost; define error budgets.  
- **Value of information:** quantify benefit of collecting more data vs deciding now.  
- **Abstain/triage policies:** defer to humans when uncertainty exceeds limits.

---

## Botspeak Integration
- **Define:** Specify uncertainty‑sensitive objectives (e.g., false negative cost), risk tolerances, and reporting format (calibration tables, intervals).  
- **Delegate:** Choose **Interaction Mode** based on reversibility and observability; higher stakes → Augmentation with human review.  
- **Direct:** Prompt Specs include probability outputs, interval requirements, and acceptance tests for calibration/coverage.  
- **Diagnose:** Compute scoring rules, reliability diagrams, and coverage diagnostics; run shift probes.  
- **Decide:** Thresholds chosen by expected cost; enable abstain pathways.  
- **Document:** Uncertainty appendix in Model Cards; monitoring SLOs for calibration/coverage.

---

## Hands‑On Labs (code‑optional; Python suggested)
> **Setup:** Python env with `numpy`, `pandas`, `scikit‑learn`, `matplotlib`, `scipy`, and optionally `mapie` (conformal).  
> `pip install -U numpy pandas scikit-learn matplotlib scipy mapie`

### Lab A — Beta‑Bernoulli Posterior & Credible Intervals (Bayesian CTR)
**Goal:** Use a **Beta prior** for a Bernoulli rate (e.g., click‑through) and compute posteriors, credible intervals, and **posterior predictive**. Explore **prior sensitivity**.  

```python
import numpy as np
from scipy.stats import beta, bernoulli

# Observed data: clicks out of impressions
n, k = 500, 37  # impressions, clicks
alpha0, beta0 = 1, 1   # uniform prior Beta(1,1)
alphaN, betaN = alpha0 + k, beta0 + (n - k)

# 95% credible interval
lo, hi = beta.ppf([0.025, 0.975], alphaN, betaN)
print((lo, hi))

# Posterior predictive: probability next 10 users yield >= 2 clicks
from scipy.stats import binom
p_mean = alphaN / (alphaN + betaN)
print('Posterior mean p:', p_mean)
print('P(X>=2 of 10):', 1 - binom.cdf(1, 10, p_mean))
```

**Explorations**  
1. Change priors: Beta(2,10) vs Beta(10,2). How does the credible interval shift?  
2. Decision: If a campaign ships only when **p ≥ 0.08** with ≥80% posterior probability, does it ship?  

**Deliverable:** 1‑page memo with prior/ posterior plots, 95% CrI, and a **Go/No‑Go** decision rule.

---

### Lab B — Calibration Clinic: Reliability Diagrams & Temperature Scaling
**Goal:** Train a classifier; compute **Brier**, **log loss**, and **reliability**; apply **temperature scaling** or **isotonic** to improve calibration.  

```python
import numpy as np, pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import brier_score_loss, log_loss
import matplotlib.pyplot as plt

X, y = make_classification(n_samples=5000, n_features=10, n_informative=6,
                           weights=[0.7,0.3], random_state=7)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, random_state=7)

clf = RandomForestClassifier(n_estimators=300, random_state=7)
clf.fit(Xtr, ytr)
proba = clf.predict_proba(Xte)[:,1]

# Metrics
print('Brier:', brier_score_loss(yte, proba))
print('LogLoss:', log_loss(yte, proba))

# Reliability diagram
bins = np.linspace(0,1,11)
ids = np.digitize(proba, bins) - 1
acc = [yte[ids==i].mean() if np.any(ids==i) else np.nan for i in range(10)]
conf = [proba[ids==i].mean() if np.any(ids==i) else np.nan for i in range(10)]
plt.plot([0,1],[0,1])
plt.scatter(conf, acc)
plt.xlabel('Predicted probability'); plt.ylabel('Observed frequency')
plt.title('Reliability (before)'); plt.show()

# Isotonic calibration
iso = IsotonicRegression(out_of_bounds='clip')
proba_cal = iso.fit_transform(proba, yte)
print('Brier (iso):', brier_score_loss(yte, proba_cal))
print('LogLoss (iso):', log_loss(yte, np.c_[1-proba_cal, proba_cal]))
```

**Checks & Questions**  
- Did calibration improve Brier/log loss?  
- Where is over‑confidence vs under‑confidence?  
- Propose an **abstain** rule: if calibrated p ∈ [0.45,0.55], defer to a human. Estimate expected workload.

**Deliverable:** Reliability plots (before/after) with a short calibration report and abstention policy.

---

### Lab C — Prediction Intervals & Conformal Coverage
**Goal:** Build **prediction intervals** (regression) or **prediction sets** (classification) and evaluate coverage.

**Option 1: Regression Intervals (split conformal)**  
```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=4000, n_features=15, noise=8.0, random_state=7)
Xtr, Xcal, ytr, ycal = train_test_split(X, y, test_size=0.5, random_state=7)
model = RandomForestRegressor(n_estimators=300, random_state=7)
model.fit(Xtr, ytr)

# calibration residuals
resid = np.abs(ycal - model.predict(Xcal))
q = np.quantile(resid, 0.9)  # ~90% marginal coverage

# For a new point x*, interval is [f(x*)-q, f(x*)+q]
```

**Option 2: Classification Sets (score‑based)**  
```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
X, y = make_classification(n_samples=4000, n_features=20, random_state=7)
Xtr, Xcal, ytr, ycal = train_test_split(X, y, test_size=0.5, random_state=7)
clf = RandomForestClassifier(n_estimators=300, random_state=7).fit(Xtr, ytr)
cal_scores = 1 - clf.predict_proba(Xcal).max(axis=1)
alpha = 0.1
tau = np.quantile(cal_scores, 1 - alpha)
# For new x*, prediction set = {classes with 1 - p_k <= tau} (i.e., p_k >= 1 - tau)
```

**Checks & Questions**  
- Empirically estimate coverage on a held‑out set; does it meet the target (e.g., 90%)?  
- How does **interval width** change under shift (perturb features)—what is the trade‑off?  

**Deliverable:** A *Coverage Report* with empirical coverage, average interval width/set size, and a decision rule for using intervals/sets in production.

---

## Assessment
- **Formative:** Quick checks during labs; minute papers on “What changed in your decision after seeing uncertainty?”  
- **Summative (Homework):** Submit (a) Bayesian CTR memo (Lab A), (b) Calibration report + abstain policy (Lab B), (c) Coverage report (Lab C), and an updated **Model Card** section on uncertainty.

**Rubric (30 pts total).**  
- **Bayesian memo (10):** Prior/posterior clarity, CrI computation, decision link.  
- **Calibration report (10):** Correct metrics/plots, improvement shown, abstain policy quantified.  
- **Coverage report (10):** Correct construction, coverage verification, trade‑offs explained.

---

## Instructor Notes & Facilitation Tips
- Emphasize **interpretation** over mechanics: students must connect numbers to **decisions** and **risk**.  
- Encourage small‑n sensitivity checks; show how priors/assumptions shift results.  
- Tie back to **Module 3 (Bias):** report subgroup calibration and coverage.  
- For limited compute, subsample or prefer logistic regression over ensembles in Lab B.

---

## Templates (Copy‑Paste)

**Uncertainty Reporting Block (Model Card)**  
- Performance with 95% CI (bootstrap):  
- Calibration (Brier, ECE) + reliability diagram:  
- Predictive intervals/sets (target coverage, empirical coverage):  
- Abstain/triage rules:  
- Known failure modes under shift:  
- Monitoring SLOs (calibration drift, coverage drift):  

**Decision Threshold Worksheet**  
- Cost(false positive) =  
- Cost(false negative) =  
- Prior/base rate =  
- Threshold minimizing expected cost =  
- Human‑review band =  

---

## References (Selected, APA‑style)
- de Finetti, B. (1974). *Theory of Probability* (Vols. 1–2). Wiley.  
- Gelman, A., Carlin, J., Stern, H., Dunson, D., Vehtari, A., & Rubin, D. (2013). *Bayesian Data Analysis* (3rd ed.). CRC.  
- Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA, 102*(477), 359–378.  
- Hume, D. (1748/2007). *An Enquiry Concerning Human Understanding* (P. Millican, Ed.). OUP.  
- Jaynes, E. T. (2003). *Probability Theory: The Logic of Science*. Cambridge University Press.  
- Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press.  
- Platt, J. (1999). Probabilistic outputs for SVMs and comparisons to regularized likelihood methods. *NIPS*.  
- Vovk, V., Gammerman, A., & Shafer, G. (2005). *Algorithmic Learning in a Random World*. Springer.  
- Zadrozny, B., & Elkan, C. (2002). Transforming classifier scores into accurate multiclass probability estimates. *KDD*.  

> Also see: NIST AI TEVV for uncertainty reporting; Dawid (1982) on calibration; Kuleshov et al. (2018) on calibrated regression.

