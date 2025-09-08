# Lesson (Markdown): Module 2 — Data Validation Techniques for AI Systems

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M2 – Data Validation Techniques  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, EDA labs, data audits, and documentation artifacts

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Explain **truth** and **falsifiability** in the context of data‑driven conclusions, and apply Popperian tests to dataset assumptions.  
2. Critique the idea that data are **objective**, recognizing measurement, construct, and sampling biases.  
3. Use **Plato’s Allegory of the Cave** to reason about datasets as partial, projected shadows of reality, and identify the limits of representativeness.  
4. Conduct **Exploratory Data Analysis (EDA)** to surface assumptions, detect leakage, and evaluate label/data quality.  
5. Design **data acceptance tests** (schema, ranges, constraints, drift, label quality) and produce documentation (Datasheet for Datasets).  
6. Integrate data‑validation practices into Botspeak’s **Strategic Delegation** and **Critical Evaluation** pillars across the Define→Delegate→Direct→Diagnose→Decide→Document loop.

---

## Key Terms
- **Construct validity:** Degree to which a variable truly measures the concept it purports to measure.  
- **Measurement error:** Random (noise) and systematic (bias) deviations from true values.  
- **Ground truth:** Operationalized labels used for training/evaluation; often **constructed**, not metaphysically true.  
- **Target leakage:** Using information at training/test time that would not be available at decision time.  
- **Sampling bias:** Non‑representative sample that skews estimates.  
- **Drift:** Changes in data distribution over time (covariate, label, concept).  
- **Inter‑annotator agreement:** Degree of labeler consistency (e.g., Cohen’s κ).  
- **PSI (Population Stability Index):** Simple measure of distribution shift for a feature over time or between samples.  
- **Data acceptance tests:** Pre‑registered checks a dataset must pass before modeling (schema, ranges, missingness, uniqueness, leakage guards, drift).

---

## Theory Blocks

### 1) Philosophical Foundations — Truth & Falsifiability in Data‑Driven Conclusions
**Popper’s falsifiability.** A claim is scientific when it is testable and **refutable**. Apply this to datasets: treat each data assumption as a hypothesis to test. Examples:
- *Hypothesis:* Labels reflect the intended concept. **Tests:** Inter‑annotator agreement; content validity review; holdout re‑labeling.  
- *Hypothesis:* No target leakage. **Tests:** Train on suspect features alone; time‑based split; shuffle tests.  
- *Hypothesis:* Sample represents deployment population. **Tests:** Compare demographics/feature distributions to deployment proxies; sensitivity analyses.

**Error‑centric epistemology.** We progress by **finding and fixing errors**—bad joins, mislabeled rows, outliers with causal explanations, and mismatched time windows. Documentation of rejected hypotheses is part of the truth‑seeking process.

---

### 2) Critical Question — Can Data Ever Be Truly Objective?
**Short answer:** No—data are **made**, not found. Choices in **measurement**, **labeling**, **sampling**, and **cleaning** embed values and constraints.  
- **Measurement & construct bias:** Does “toxicity” equal the presence of taboo words, or intent and harm?  
- **Sampling bias:** Who is included/excluded (time, geography, platform)?  
- **Observer effects:** Model use changes behavior (feedback loops).  

**Practical stance:** Strive for **fitness‑for‑purpose** with explicit uncertainty and limitations; expose contestable decisions; invite audit.

---

### 3) Plato’s Cave — Are Datasets Shadows of Reality?
In Plato’s allegory, prisoners mistake **shadows** for reality. Likewise, datasets are **projections**—partial, filtered by collection mechanisms, schemas, and incentives.  
**Design cues:**
- Catalog what your dataset cannot see (blind spots).  
- Map proxies (shadows) to constructs (forms) and specify where the mapping is weak.  
- Prefer multiple, independent **projections** (triangulation) to reduce shadow‑specific artifacts.

---

## Method — A Practical Data‑Validation Workflow
**Define → Delegate → Direct → Diagnose → Decide → Document** with data at the center:
- **Define:** Stakeholders, constructs, decision context, harm model; propose falsifiable **data hypotheses**.  
- **Delegate:** Assign *who* validates what (analyst, domain expert, annotator QA, privacy counsel). Use AI tools to **propose** checks; humans **approve** and handle edge cases.  
- **Direct:** Write a *Data Validation Spec* (see template) with acceptance tests and thresholds.  
- **Diagnose:** Run EDA, drift/leakage tests, label audits; record failures and fixes.  
- **Decide:** Gate data use on passing tests; choose mitigation (prune features, relabel, re‑sample, collect more data).  
- **Document:** Publish a **Datasheet for Datasets**, validation report, and change log; register in the AI Use‑Case inventory.

**Data Acceptance Test Categories**
1) **Schema & types** (columns, dtypes, unique keys)  
2) **Ranges & constraints** (valid values, monotonicity, regex for IDs)  
3) **Missingness & uniqueness** (NA rates, duplicates)  
4) **Integrity** (joins, referential consistency, timestamp order)  
5) **Leakage guards** (time splits, feature blacklists, decision‑time availability)  
6) **Label quality** (agreement, prevalence sanity, re‑label audit)  
7) **Representativeness** (slice coverage, class balance)  
8) **Drift** (PSI/KS vs reference; seasonality)  
9) **Privacy & policy** (PII handling, consent, retention)  
10) **Provenance** (source, licensing, versioning)

---

## Hands‑On Exercises (code‑optional; Python suggested)
> **Setup:** Python with `pandas`, `numpy`, `matplotlib`, `scikit‑learn`, `scipy`. Optional: `textstat` or `re` for regex checks.  
> `pip install -U pandas numpy scikit-learn scipy matplotlib`

### Exercise A — EDA Scavenger Hunt: Surface Assumptions & Risks
**Time:** 30–40 min | **Format:** Pairs  
**Goal:** Conduct EDA to reveal schema issues, missingness, outliers, label prevalence, and potential leakage features.

```python
import pandas as pd, numpy as np
from scipy import stats

# Load your dataset
df = pd.read_csv('data.csv')  # replace with your path

# 1) Schema snapshot
print(df.dtypes)
print(df.head())

# 2) Missingness & duplicates
na_rate = df.isna().mean().sort_values(ascending=False).head(10); print(na_rate)
print('Duplicate rows:', df.duplicated().sum())

# 3) Numeric ranges & outliers
num = df.select_dtypes(include='number')
sumstats = num.describe(percentiles=[.01,.05,.5,.95,.99]).T; print(sumstats.head())
z = np.abs(stats.zscore(num.fillna(num.median())))
print('Potential outliers (z>4) per column:', (z>4).sum(axis=0))

# 4) Categorical top‑k
cat = df.select_dtypes(exclude='number')
for c in cat.columns[:5]:
    print(c, df[c].value_counts(dropna=False).head(5))

# 5) Label prevalence (binary example)
if 'target' in df:
    print('Target prevalence:', df['target'].mean())
```

**Checklist:** Note suspicious features (post‑event IDs, future timestamps), imbalanced classes, implausible ranges (age < 0 or > 120), and proxies for protected attributes.  
**Deliverable:** 1‑page **EDA Findings Memo** with top 10 risks and proposed tests.

---

### Exercise B — Split Design & Leakage Detection
**Time:** 30–40 min | **Format:** Teams  
**Goal:** Propose and implement a split strategy; detect leakage by sanity tests.

```python
from sklearn.model_selection import train_test_split, GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# Example: time‑based or group split
df = df.sort_values('event_time')  # if available
train = df[df['event_time'] < '2025-01-01']
 test  = df[df['event_time'] >= '2025-01-01']

X_tr = train.drop(columns=['target'])
X_te = test.drop(columns=['target'])
y_tr = train['target']
 y_te = test['target']

# Baseline model
model = LogisticRegression(max_iter=1000).fit(X_tr.select_dtypes(include='number').fillna(0), y_tr)
proba = model.predict_proba(X_te.select_dtypes(include='number').fillna(0))[:,1]
print('OOT AUROC:', roc_auc_score(y_te, proba))

# Leakage probes: can a single suspect feature predict too well?
suspects = [c for c in df.columns if 'id' in c.lower() or 'flag' in c.lower() or 'future' in c.lower()]
for c in suspects:
    if c != 'target' and df[c].dtype != 'O':
        try:
            auc = roc_auc_score(y_te, X_te[c].fillna(X_te[c].median()))
            print('Single‑feature AUROC for', c, ':', round(auc,3))
        except Exception: pass

# Shuffle test: break label→feature relationship
X_tr_shuffled = X_tr.sample(frac=1.0, random_state=7).reset_index(drop=True)
model2 = LogisticRegression(max_iter=1000).fit(X_tr_shuffled.select_dtypes(include='number').fillna(0), y_tr.reset_index(drop=True))
proba2 = model2.predict_proba(X_te.select_dtypes(include='number').fillna(0))[:,1]
print('Shuffled AUROC (should drop):', roc_auc_score(y_te, proba2))
```

**Deliverable:** **Split & Leakage Report** explaining your split choice (time/group/stratified), leakage evidence, and any quarantined features.

---

### Exercise C — Label Quality Audit (Agreement & Relabeling)
**Time:** 30–40 min | **Format:** Pairs  
**Goal:** Quantify label reliability; perform a small **re‑label** and estimate error rate.

```python
from sklearn.metrics import cohen_kappa_score

# Suppose two annotators A1, A2 labeled a subset
subset = df.sample(200, random_state=7)
A1 = subset['labeler1']
A2 = subset['labeler2']
print('Cohen kappa:', cohen_kappa_score(A1, A2))

# Prevalence sanity: compare to historical or external references if available
print('Label prevalence in subset:', subset['target'].mean())
```

**Manual step:** Choose 50 random rows; perform **blind re‑labeling** with written guidelines; compute disagreement and categorize root causes (ambiguous cases, poor instructions, true hard cases).  
**Deliverable:** **Label Audit Memo** with κ, estimated error rate, and guideline improvements.

---

### Exercise D (Optional) — Drift & Stability Checks (PSI/KS)
**Time:** 25–35 min | **Format:** Teams  
**Goal:** Compare training vs. recent data; flag features with material shift.

```python
import numpy as np

def psi(expected, actual, bins=10):
    # expected: train; actual: production batch
    quantiles = np.quantile(expected, np.linspace(0,1,bins+1))
    e_counts = np.histogram(expected, bins=quantiles)[0] / len(expected)
    a_counts = np.histogram(actual,   bins=quantiles)[0] / len(actual)
    a_counts = np.where(a_counts==0, 1e-6, a_counts)
    e_counts = np.where(e_counts==0, 1e-6, e_counts)
    return np.sum((a_counts - e_counts) * np.log(a_counts / e_counts))

# Example usage:
# psi_value = psi(train[col].dropna().values, prod[col].dropna().values)
```

**Deliverable:** **Drift Summary** listing top‑shifted features with PSI, hypothesis about causes, and monitoring thresholds.

---

## Assessment
- **Formative:** In‑class EDA share‑outs; code/analysis walkthroughs; quick oral checks on philosophical framing.  
- **Summative (Homework):** Submit (a) EDA Findings Memo, (b) Split & Leakage Report, (c) Label Audit Memo, and (d) (optional) Drift Summary + a completed **Datasheet for Datasets**.

**Rubric (30 pts total).**  
- **EDA & risks (10):** Depth of analysis; identification of plausible risks; clear visuals/tables.  
- **Split & leakage (10):** Justified split; convincing leakage probes; mitigation steps.  
- **Label audit (8):** Agreement metrics; error taxonomy; guideline revisions.  
- **Documentation (2):** Datasheet completeness and clarity.

---

## Templates (Copy‑Paste)

**Data Validation Spec (Acceptance Tests)**  
- **Schema:** Columns, dtypes, primary keys  
- **Ranges & constraints:** Min/max, regex, monotonicity  
- **Missingness & duplicates:** Thresholds, remediation plan  
- **Integrity:** Join keys, timestamp order, dedup keys  
- **Leakage guards:** Decision‑time availability list; feature quarantine  
- **Label quality:** Agreement ≥ κ*, re‑label audit cadence  
- **Representativeness:** Slice coverage; class balance limits  
- **Drift:** PSI/KS thresholds and windows  
- **Privacy & policy:** PII handling; consent; retention  
- **Provenance:** Source, license, owner, version

**Datasheet for Datasets (Abbrev.)**  
- **Motivation & composition:** Purpose, target population, sampling method  
- **Collection & preprocessing:** Instruments, timeframes, cleaning  
- **Labeling:** Guidelines, training, QA, known ambiguities  
- **Uses & limits:** Intended/Out‑of‑scope uses, ethical risks, known failure modes  
- **Distribution:** Access controls, license, PII handling  
- **Maintenance:** Updates, versioning, contact

**Data Risk Register (Starter)**  
| ID | Risk | Category | Severity | Likelihood | Owner | Mitigation | Monitor |
|----|------|----------|----------|------------|-------|------------|---------|

**Split Decision Matrix**  
- **Time‑based:** prevents temporal leakage; use for forecasting/deployment shifts.  
- **Group‑based:** prevents entity bleed (user/product).  
- **Stratified random:** maintains label balance; lowest leakage guard.  
- **K‑fold OOS:** for small data; beware of group/time leakage.

---

## Botspeak Integration
- **Strategic Delegation:** Use AI tools to propose tests and summarize EDA, but keep **human approval** for leakage/ethics decisions and for writing the **Datasheet**.  
- **Critical Evaluation:** Convert every data assumption into a falsifiable hypothesis with a specific test and threshold; log both **passes** and **failures**.

---

## References (Selected, APA‑style)
- Breck, E., Zinkevich, M., Polyzotis, N., Whang, S., & Roy, S. (2017). The ML Test Score: A rubric for ML production readiness. *Google Research whitepaper*.  
- Gebru, T., Morgenstern, J., Vecchione, B., et al. (2018). Datasheets for datasets. *arXiv:1803.09010*.  
- Koh, P. W., & Liang, P. (2017). Understanding black‑box predictions via influence functions. In *ICML*.  
- Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. University of Chicago Press.  
- Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). Model Cards for Model Reporting. In *FAccT*.  
- Northcutt, C. G., Jiang, L., & Chuang, I. L. (2021). Confident learning: Estimating uncertainty in dataset labels. *JMLR, 22*(268), 1–52.  
- Plato. (c. 375 BCE/1992). *Republic* (G. M. A. Grube & C. D. C. Reeve, Trans.). Hackett Publishing.  
- Popper, K. (1959). *The Logic of Scientific Discovery*. Routledge.  
- Polyzotis, N., Zinkevich, M., Roy, S., Breck, E., & Whang, S. (2017). Data validation for ML via analysis of production issues. In *Proceedings of MLSys/Systems Papers*.  
- Sculley, D., Holt, G., Golovin, D., et al. (2015). Hidden technical debt in ML systems. In *NIPS*.  
- Wardrop, M., Kapoor, S., & Narayanan, A. (2020). Leakage and the reproducibility crisis in ML‑based science. *arXiv:2007.XXXX*.  

> Supplement: Great Expectations; TensorFlow Data Validation; What‑If Tool; Fairlearn for slice‑aware EDA; NIST AI RMF & TEVV for governance ties.

