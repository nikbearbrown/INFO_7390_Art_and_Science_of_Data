# INFO 7390 Midterm — Study Guide

## 0) Exam Strategy (5-min read)

* **Show work & assumptions.** If missingness mechanism is unclear, state MCAR/MAR/MNAR assumptions and proceed.
* **Units & scales.** When reporting variance/SD/IQR, mind units (variance is squared).
* **Plots beat prose.** If time allows, sketch a quick histogram/box plot/PS overlap/Love plot.
* **Answer what’s asked.** If the prompt is about *causal* effects, avoid purely predictive language.

---

## 1) Statistical Properties of Datasets

### Learning goals

* Choose the right **center** (mean/median/mode) and **spread** (SD/IQR) for the distribution.
* Diagnose **skewness** vs. **kurtosis** and know their implications.
* Match **visuals** to questions (histogram/QQ/box).

### Must-know

* Mean (\bar x=\frac{1}{n}\sum x_i); Variance (s^2=\frac{1}{n}\sum (x_i-\bar x)^2); IQR (=Q_3-Q_1).
* Positive skew ⇒ mean > median; heavy tails ⇒ high kurtosis.

### Pitfalls

* Using mean/SD on highly skewed data with outliers.
* Calling a distribution “normal” from a bell-ish histogram without a Q–Q check.

### Quick practice

1. A variable has extreme right tail. Which center/spread? **Ans:** Median + IQR.
2. On a QQ plot you see upward curvature in upper tail. **Ans:** Right-tail heavier than normal.

---

## 2) Handling Missing Data

### Learning goals

* Classify MCAR/MAR/MNAR and pick an imputation consistent with mechanism.
* Understand pros/cons of listwise, KNN, regression, **multiple imputation**.

### Must-know

* MAR: missingness depends on **observed** variables; include them in the imputation model.
* Multiple Imputation: analyze (m) datasets and **pool** estimates (captures imputation uncertainty).

### Pitfalls

* Mean imputation shrinking variance; mixing different analysis samples (pairwise deletion) without noting it.

### Quick practice

Give a MAR example and a fitting method. **Ans:** Income missing depends on age/education → multiple imputation including age/edu.

---

## 3) Outliers: Detection & Treatment

### Learning goals

* Use **Z-score**, **IQR rule**, and **MAD/modified Z** appropriately.
* Choose keep/remove/transform/Winsorize with justification.

### Must-know

* IQR rule: outliers if (x<Q_1-1.5,\text{IQR}) or (x>Q_3+1.5,\text{IQR}).
* Modified Z (MAD-based) is robust.

### Pitfalls

* Automatic deletion; failing to report sensitivity.

### Quick practice

Data are right-skewed with legitimate high values. **Ans:** Keep; log-transform; report with and without transform.

---

## 4) Data Transformation & Scaling

### Learning goals

* When to use **standardization** vs **min–max** vs distribution transforms.
* Impact on **distance-based** methods.

### Must-know

* Standardize for KNN/K-means/SVM; log for multiplicative/right-skewed data.

### Pitfalls

* Min–max on outlier-ridden features.

### Quick practice

Age (20–60) and income (10k–300k) in KNN. **Ans:** Standardize both.

---

## 5) Encoding Categorical Variables

### Learning goals

* Choose one-hot, dummy/reference coding, ordinal encoding, target/frequency encoding.

### Must-know

* With intercept, **drop one column** (dummy/reference) to avoid the **dummy variable trap**.

### Pitfalls

* Treating nominal as ordinal; leaking target in naive target encoding.

### Quick practice

3 categories in linear regression with intercept. **Ans:** Use (K-1) dummies; interpret coefficients as differences vs reference.

---

## 6) Data Reduction

### Learning goals

* Feature selection vs **PCA** vs aggregation; tradeoffs of interpretability vs variance capture.

### Must-know

* PCA components are **uncorrelated** linear combos ordered by explained variance.

### Pitfalls

* Interpreting PCA loadings as causal or as original features.

### Quick practice

Many correlated features, want 2D viz. **Ans:** PCA to 2 components.

---

## 7) Visual Validation of Preprocessing

### Learning goals

* Show **before/after** distributions, scaling effects, missingness patterns, correlation shifts.

### Must-know

* Correlation heatmaps change after transformations/engineering; justify.

### Pitfalls

* Declaring “improved” without a comparative plot/stat.

---

## 8) Causal Inference: Basic Terms

### Learning goals

* Speak in **potential outcomes**; define **ATE/ATT**, **SUTVA**, **ignorability**, **positivity**.
* Distinguish **confounder/mediator/collider**; use **DAGs**.

### Must-know

* Ignorability: ({Y(0),Y(1)}\perp T\mid X).
* Do **not** control colliders; do control confounders.

### Pitfalls

* Conditioning on post-treatment variables; “controlling everything” indiscriminately.

---

## 9) Stratification & Balance

### Learning goals

* Use **propensity score** stratification/matching/weighting; read **balance diagnostics**.

### Must-know

* **SMD** target (|\text{SMD}|<0.1); Love plots; overlap checks for positivity.

### Pitfalls

* Estimating effects without verifying balance; poor overlap (lack of common support).

---

## 10) Marks & Channels in Visualization

### Learning goals

* Map data types to **marks** (points/lines/bars) and **channels** (position, length, angle, color, shape, size).
* Apply the **effectiveness ranking** (position > length > angle > area > color > shape/texture).

### Pitfalls

* Using area/volume for precise comparisons; non-CB-safe palettes.

---

## 11) Bias–Variance Tradeoff

### Learning goals

* Diagnose **underfit vs overfit**; pick tools to shift the balance.

### Must-know

[
\text{MSE}=\text{Bias}^2+\text{Variance}+\sigma^2
]

* **Ridge/Lasso** ↑bias ↓variance; **bagging/Random Forest** ↓variance; **boosting** ↓bias (tune to avoid ↑variance).

### Quick practice

Train error low, val error high. **Ans:** High variance → regularize, simplify model, more data, or bagging.

---

## 12) Bootstrapping

### Learning goals

* Build **SEs** and **CIs** from resampling; know **percentile**, **basic**, **BCa**.

### Must-know

* Sample **with replacement** (B) times; use the empirical distribution of the statistic.
* Respect dependence (block/cluster bootstrap).

### Pitfalls

* Using iid bootstrap on time series; too small (B) (unstable CIs).

### Quick practice

Median CI for skewed data. **Ans:** Bootstrap with BCa CI.

---

## 13) One-Hot vs Dummy Variables

### Learning goals

* Prevent multicollinearity; interpret coefficients.

### Must-know

* With intercept, include **(K-1)** indicators (reference coding).
* Without intercept, include **all (K)**; coefficients equal category means.

### Pitfalls

* Keeping intercept **and** all (K) indicators (singularity).

---

# One-Page Formula & Checklist Sheet

**Center/Spread**

* (\bar x=\frac{1}{n}\sum x_i), (s=\sqrt{\frac{1}{n}\sum (x_i-\bar x)^2}), IQR (=Q_3-Q_1)

**Outliers**

* IQR rule: (x<Q_1-1.5\text{IQR}) or (x>Q_3+1.5\text{IQR})

**Scaling**

* Standardize: (z=\frac{x-\mu}{\sigma})
* Min–Max: (x'=\frac{x-\min}{\max-\min})

**Causal**

* ATE (=\mathbb E[Y(1)-Y(0)]), Ignorability, Positivity, SUTVA
* SMD (=\frac{\bar x_T-\bar x_C}{s_\text{pooled}})\ (\rightarrow\ |\text{SMD}|<0.1)

**Bias–Variance**

* (\text{MSE}=\text{Bias}^2+\text{Var}+\sigma^2)

**Bootstrap CIs**

* Percentile ([q_{\alpha/2}, q_{1-\alpha/2}])
* Basic ([2\hat\theta-q_{1-\alpha/2},,2\hat\theta-q_{\alpha/2}])
* BCa (use when skewed)

**Encoding**

* With intercept: (K-1) dummies; without intercept: all (K)

---

# Mini Practice Set (with brief keys)

1. **Choose center/spread.** Right-skewed income with outliers.
   **Key:** Median + IQR; also consider log transform for modeling.

2. **Missingness.** Younger respondents less likely to report income.
   **Key:** MAR; multiple imputation including age.

3. **Outliers.** Heavy-tailed variable, legitimate extremes.
   **Key:** Use modified Z or IQR; keep; log transform; do sensitivity.

4. **Scaling.** KNN on features at very different scales.
   **Key:** Standardize.

5. **Causal diagram.** Treatment (T) → Outcome (Y); covariate (X) affects both.
   **Key:** (X) is a confounder; condition on (X). Don’t condition on collider.

6. **Balance check.** After weighting, SMDs drop from 0.25–0.30 to 0.04–0.07.
   **Key:** Acceptable balance (typically < 0.1).

7. **Bias–variance.** Train MSE = 2, Val MSE = 8.
   **Key:** High variance; regularize / simplify / more data / bagging.

8. **Bootstrap.** CI for median AUC.
   **Key:** Bootstrap with BCa CI; (B \ge 1000).

9. **Encoding.** 4 categories in GLM with intercept.
   **Key:** Use 3 dummies (reference coding); interpret contrasts.

-