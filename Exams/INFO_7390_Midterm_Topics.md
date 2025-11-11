# INFO 7390 Midterm Topics

![Data Preprocessing Overview](sandbox:/mnt/data/e6c4a583-6b2f-4cbf-aab5-ac2370af8138.png)

## Introduction

**GIGO Principle: Garbage In, Garbage Out.**
The quality of outputs depends entirely on the quality of inputs. Data preprocessing is the foundation of trustworthy AI.

---

## Statistical Properties of Datasets

### Descriptive Statistics

**Measures of Central Tendency**

1. **Mean** ((\mu) or (\bar{x}))
   *Formula*: (\textstyle \bar{x}=\frac{\sum_i x_i}{n})
   *Use*: Symmetric distributions without extreme outliers
   *Affected by*: Outliers, skewness

2. **Median**
   *Definition*: Middle value when sorted
   *Use*: Skewed distributions or when outliers are present
   *Robust to*: Extreme values

3. **Mode**
   *Definition*: Most frequent value
   *Use*: Categorical data; can be bimodal/multimodal

**When to use which**

* Symmetric data, no outliers → **Mean**
* Skewed data or outliers → **Median**
* Categorical or highly discrete → **Mode**

**Measures of Spread**

1. **Range** = Max − Min (sensitive to outliers)
2. **Variance** ((\sigma^2)) = (\textstyle \frac{1}{n}\sum_i(x_i-\mu)^2) (units squared)
3. **Standard Deviation** ((\sigma)) = (\sqrt{\text{variance}}) (original units; avg. distance from mean)
4. **Interquartile Range (IQR)** = (Q_3-Q_1) (spread of middle 50%; robust)

**Distribution Shape**

* **Skewness**: asymmetry

  * Positive: long right tail ((\text{mean}>\text{median}))
  * Negative: long left tail ((\text{mean}<\text{median}))
* **Kurtosis**: tail heaviness

  * High: heavy tails/outliers; Low: light tails

**Visual Understanding**

* **Histograms** for shape
* **Box plots** for median/quantiles/outliers
* **Q–Q plots** for normality
* **Density plots** for smoothed shape

---

## Handling Missing Data

### Types of Missingness

1. **MCAR** (Missing Completely At Random)
   Missingness unrelated to any variables. Reduces power but not bias. Test by comparing observed vs. missing groups.

2. **MAR** (Missing At Random)
   Missingness related to observed variables, not the value itself. Unbiased if predictors of missingness are modeled (use them in imputation).

3. **MNAR** (Missing Not At Random)
   Missingness related to the missing value itself. Can bias estimates; often requires explicitly modeling the missingness mechanism.

### Imputation Methods

**Deletion**

* **Listwise**: drop any row with missing values. ✅ simple; ❌ power loss; unbiased only if MCAR.
* **Pairwise**: use available data per-analysis. ✅ retains data; ❌ inconsistent samples across analyses.

**Simple Imputation**

* **Mean/Median/Mode**: ✅ simple; ❌ shrinks variance, distorts distributions.
* **Forward/Backward Fill** (time series): ✅ respects temporal continuity; ❌ can propagate error.

**Advanced Imputation**

* **KNN Imputation**: ✅ uses relationships; ❌ sensitive to scaling, expensive.
* **Regression Imputation** (+random residual): ✅ accurate; ❌ can overstate precision.
* **Multiple Imputation**: create (m) completed datasets, analyze, pool. ✅ proper inference; ❌ computationally heavier.

**Decision Framework**

1. Assess pattern/mechanism of missingness
2. Consider amount (<5% vs >20%)
3. Preserve relationships when needed
4. Balance complexity vs accuracy
5. Document and justify the choice

---

## Outlier Detection and Treatment

**What is an outlier?** An observation that deviates markedly from others.

**Types**

* **Error outliers** (entry/measurement mistakes)
* **Valid outliers** (legitimate extremes)
* **Interesting outliers** (rare phenomena)

**Detection Methods**

* **Statistical**

  * **Z-score**: (z=(x-\mu)/\sigma); flag (|z|>3) (assumes ~normal)
  * **IQR rule**: < (Q_1-1.5,\text{IQR}) or > (Q_3+1.5,\text{IQR}) (robust)
  * **Modified Z (MAD-based)**; flag > 3.5

* **Visual**

  * **Box plots** (comparisons across groups)
  * **Scatter plots** (bivariate outliers)
  * **Histograms** (extremes)

* **Model-Based**

  * **Isolation Forest** (high-dimensional anomalies)
  * **DBSCAN** (low-density points)

**Treatment Strategies**

1. **Investigate first** (cause? error? domain knowledge?)
2. **Keep** (valid/important; use robust methods)
3. **Remove** (confirmed errors; document)
4. **Transform** (log, sqrt, Box–Cox)
5. **Cap/Winsorize** (e.g., 99th percentile)
6. **Separate Analyses** / sensitivity checks

> **Never** remove outliers automatically; report sensitivity.

---

## Data Transformation

### Normalization (Scaling to Range)

* **Min–Max**: (x'=\frac{x-\min}{\max-\min}) → ([0,1]) (sensitive to outliers)
* **Max-Abs**: (x'=x/\max(|x|)) → ([-1,1]) (preserves sparsity/sign)

### Standardization (Z-Score)

* (z=\frac{x-\mu}{\sigma}) → mean 0, SD 1
* Useful for distance-based algorithms (KNN, K-means, SVM)

**Why scaling matters**
Features with larger scales dominate distances (e.g., income vs age); scaling equalizes influence.

### Distribution Transformations

* **Log**: (\log x) or (\log(x+1)) for zeros (right-skew reduction)
* **Square Root**: (\sqrt{x}) (counts)
* **Box–Cox**: (\frac{x^\lambda-1}{\lambda}) (choose (\lambda))
* **Reciprocal**: (1/x) (severe right skew)

Only transform when it improves model fit, meets assumptions, or aids interpretation.

---

## Encoding Categorical Variables

* **One-Hot**: binary column per category (nominal; can be high-dimensional)
* **Label Encoding**: integers per category (only for **ordinal** or tree models)
* **Target Encoding**: replace with category-wise target mean (needs regularization)
* **Frequency Encoding**: replace with category frequency (good for high cardinality)

---

## Data Reduction

* **Why**: curse of dimensionality, visualization, efficiency, redundancy reduction, generalization.

**Methods**

1. **Feature Selection** (correlation, mutual information, RFE)
2. **PCA** (uncorrelated components ordered by variance; less interpretable)
3. **Feature Aggregation** (combine related items; e.g., scale scores)

---

## Visual Validation of Preprocessing

* **Distribution plots**: before/after transformations
* **Box plots**: before/after outlier handling
* **Scatter plots**: before/after scaling
* **Correlation heatmaps**: before/after feature engineering
* **Missingness maps**: patterns pre-imputation

**Documentation**: Show original properties, justify steps, visualize impacts, and report before/after statistics.

---

## Basic Terms in Causal Inference    

* **Unit**: entity receiving a treatment (person, store, ad, etc.).
* **Treatment/Exposure ((T))**: intervention or condition (e.g., drug vs placebo).
* **Outcome ((Y))**: variable of interest affected by treatment.
* **Potential Outcomes**: (Y(1)), (Y(0)) for treated/untreated states (counterfactuals).
* **ATE** (Average Treatment Effect): (\mathbb{E}[Y(1)-Y(0)]).
* **ATT** (Avg. Treatment Effect on Treated): (\mathbb{E}[Y(1)-Y(0)\mid T=1]).
* **SUTVA**: no interference between units; one version of treatment.
* **Ignorability/Unconfoundedness**: ({Y(0),Y(1)}\perp T \mid X) (after conditioning on covariates (X)).
* **Positivity/Overlap**: (0<P(T=1\mid X)<1) for all (X) values used.
* **Consistency**: observed outcome equals the potential outcome under the treatment actually received.
* **Confounder**: variable affecting both (T) and (Y).
* **Mediator**: variable on the causal path from (T) to (Y).
* **Collider**: variable influenced by (T) and (Y); conditioning on it induces bias.
* **DAGs**: Directed acyclic graphs for encoding assumptions, identifying backdoor paths.
* **Identification**: conditions under which causal effect is estimable (backdoor/frontdoor criteria).
* **Estimation Tools**: matching, stratification, IPW, g-computation, doubly robust (AIPW/DR), causal forests, TMLE, RCTs.

---

## Stratification and Balance of Data    

**Goal**: approximate randomized comparisons by ensuring treated and control groups are comparable on covariates.

### Stratification / Subclassification

* Partition data into strata (bins) with similar covariates (often via **propensity score** (e(X)=P(T=1\mid X))).
* Estimate effects **within** strata, then average (weighted by stratum size).
* Works best when there is good **overlap** of propensity scores.

### Balance Diagnostics

* **Standardized Mean Difference (SMD)**:
  [
  \text{SMD}=\frac{\bar{x}_T-\bar{x}*C}{s*\text{pooled}}
  ]
  Thresholds: (|\text{SMD}|<0.1) (often acceptable), <0.05 (good).
* **Variance ratios** (target ~1), **KS tests** for distributions.
* **Love plots**: visualize SMDs before/after adjustment.
* **Propensity overlap plots**: check positivity; trim non-overlap regions if justified.

### Methods to Achieve Balance

* **Exact/Coarsened Exact Matching (CEM)**
* **Nearest-neighbor/Caliper Matching**
* **Propensity Score Weighting** (IPW, stabilized weights)
* **Doubly Robust** estimators (e.g., AIPW) combine outcome and treatment models.
* **Post-stratification / Raking** to known marginals.

> Always **report** balance before and after adjustment and conduct **sensitivity analyses** for unobserved confounding.

---

## Marks and Channels in Data Visualization    

**Marks**: the graphical primitives that represent data items.

* **Point**, **Line**, **Area**, **Bar**, **Text**, **Node/Link** (networks), **Geometric regions** (maps).

**Channels** (visual encodings applied to marks):

* **Position (x, y)**
* **Length**, **Angle/Slope**, **Area/Volume**
* **Color** (hue for categories; lightness/saturation for ordered data)
* **Shape** (categorical)
* **Orientation**, **Texture**, **Size**, **Opacity**

**Effectiveness Ranking (approx.)**
Position > Length > Angle/Slope > Area > Color (lightness) > Color (hue) > Shape/Texture.

**Mapping Guidance**

* **Quantitative**: position, length, angle; avoid area for precise comparison.
* **Ordered**: position, lightness, saturation, size.
* **Categorical**: position (facets), color hue, shape.

**Good Practices**

* Prefer **aligned scales** (shared axes) for comparison.
* Use **colorblind-safe** palettes; encode with redundancy (shape + color) when needed.
* Keep **ink-to-data** high; avoid 3D effects and unnecessary gradients.
* Label directly when possible; ensure legible fonts and sufficient contrast.
* Use **faceting** for small multiples; avoid dual y-axes unless carefully justified.
* Add **uncertainty** encodings (error bars, intervals, ribbons) when relevant.

**Common Pitfalls**

* Using area/volume to compare small differences.
* Overplotting points (use jitter, transparency, hex-bins).
* Encoding ordered data with arbitrary color hues.

---

## Appendix: Quick Checklists

**Preprocessing Plan**

* [ ] Describe data, targets, and assumptions
* [ ] Explore distributions & outliers
* [ ] Diagnose missingness (MCAR/MAR/MNAR)
* [ ] Choose imputation with justification
* [ ] Scale/transform where appropriate
* [ ] Encode categoricals with rationale
* [ ] Reduce dimensionality if needed
* [ ] Visualize **before vs after**
* [ ] Document all choices and impacts

**Causal Analysis Plan**

* [ ] Define estimand (ATE/ATT)
* [ ] DAG for assumptions; list confounders
* [ ] Check overlap/positivity
* [ ] Achieve balance (matching/weighting/stratification)
* [ ] Verify balance (SMDs, Love plot)
* [ ] Estimate with robust method; report sensitivity analyses

---
## Bias–Variance Tradeoff    

**Goal:** minimize prediction error on unseen data by balancing model **bias** (systematic error from underfitting) and **variance** (sensitivity to sampling noise / overfitting).

**Decomposition (for squared-error loss):**
[
\operatorname{MSE}(x)=\underbrace{\big(\mathbb{E}[\hat{f}(x)]-f(x)\big)^2}*{\text{Bias}^2}
+\underbrace{\mathbb{V}[\hat{f}(x)]}*{\text{Variance}}
+\underbrace{\sigma^2}_{\text{Irreducible noise}}
]

**Intuition**

* **High bias**: model too simple → underfits (e.g., linear fit to a curved relationship).
* **High variance**: model too flexible → fits noise (e.g., deep tree without pruning).
* **Sweet spot**: slightly biased but much lower variance → best generalization.

**How to tune the tradeoff**

* **Regularization** (L2/Ridge shrinks coefficients smoothly; L1/Lasso can zero-out features): ↑bias, ↓variance.
* **Model capacity**: decrease depth/parameters to reduce variance; increase to reduce bias.
* **Ensembling**: bagging/Random Forest ↓variance; boosting can ↓bias (tune to avoid ↑variance).
* **Data**: more, cleaner, and better-balanced data reduces variance at the same capacity.
* **Diagnostics**: learning curves (train vs. validation error), cross-validation, residual checks.

---

## Bootstrapping    

**What it is:** a resampling method to approximate the sampling distribution of a statistic by repeatedly sampling **with replacement** from the observed data.

**Basic algorithm (nonparametric bootstrap)**

1. From dataset (D) of size (n), draw (B) bootstrap samples (D^{*(b)}) by sampling (n) rows **with replacement**.
2. Compute statistic (\theta^{*(b)} = s(D^{*(b)})) for (b=1,\dots,B).
3. Use the empirical distribution of ({\theta^{*(b)}}) for standard errors, confidence intervals (CIs), and bias estimates.

**CIs**

* **Percentile CI**: ([\theta^{*}_{\alpha/2},\ \theta^{*}_{1-\alpha/2}]).
* **Basic CI**: ([2\hat{\theta}-\theta^{*}_{1-\alpha/2},\ 2\hat{\theta}-\theta^{*}_{\alpha/2}]).
* **BCa CI**: bias-corrected and accelerated; adjusts for bias and skew (often best default).

**Uses**

* SEs and CIs for complex estimators (medians, AUC, variable-importance).
* **Model assessment**: bootstrap .632 or .632+ estimators of prediction error when cross-validation is hard.
* **Stability** of feature selection or clustering.

**Practical tips**

* Choose (B) large enough (e.g., 1000–5000) for stable CIs.
* Respect dependence: for time series use **block bootstrap**; for clustered data use **cluster bootstrap**.
* For tiny (n), bootstrap can be unstable; prefer exact or CV-based methods if possible.

---

## One-Hot Encoding vs. Dummy Variables    

**Context:** linear models with a categorical predictor having (K) categories.

### One-Hot Encoding

Create (K) binary indicators ((D_1,\dots,D_K)) with (D_k=1) if observation is in category (k), else 0.

* **With an intercept**, including **all (K)** indicators causes **perfect multicollinearity** (the “dummy variable trap” since the indicators sum to 1).
* **Without an intercept**, you may include all (K) indicators; each coefficient is the category mean.

**Example (3 categories: A, B, C; no intercept):**
[
y=\beta_A D_A+\beta_B D_B+\beta_C D_C+\varepsilon
]
Interpretation: (\beta_A=\mathbb{E}[y\mid A]), etc.

### Dummy (Reference) Coding

Include an **intercept** and **(K-1)** indicators; the omitted category is the **reference**. Coefficients measure differences vs. reference.

**Example (reference = A; keep intercept):**
[
y=\beta_0 + \beta_B D_B + \beta_C D_C + \varepsilon
]

* (\beta_0=\mathbb{E}[y\mid A])
* (\beta_B=\mathbb{E}[y\mid B]-\mathbb{E}[y\mid A])
* (\beta_C=\mathbb{E}[y\mid C]-\mathbb{E}[y\mid A])

**Two categories (A, B; reference = A):**
[
y=\beta_0+\beta_B D_B+\varepsilon
]
(\beta_B) is the mean difference (B-A).

### When to use which

* **Linear/GLM with intercept** → **Dummy coding** (avoid collinearity; coefficients are contrasts).
* **Tree-based models** → either is fine (trees handle integers or one-hots; one-hot can help with non-ordinal splits).
* **Regularized linear models** → dummy coding preferred; if using one-hot, **drop one column** or drop intercept.
* **Interactions** → build interactions with the **(K-1)** dummies and the interacting variable; interpret as differential slopes vs. reference.

**Notes**

* For **ordinal** categories, consider **ordinal encoding** or monotonic constraints (don’t force arbitrary distances).
* With **high-cardinality** categories, consider **target encoding** (with leakage-safe regularization) or **hashing**.
* Always check for **multicollinearity** and interpretability of the chosen scheme.

-