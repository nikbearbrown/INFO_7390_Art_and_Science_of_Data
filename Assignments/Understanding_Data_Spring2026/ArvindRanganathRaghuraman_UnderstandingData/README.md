# Binary Classification for Cardiovascular Disease Prediction: Comparing Logistic Regression and Random Forest
📘 INFO 7390 — Art and Science of Data

**Author:** Arvind Ranganath Raghuraman  
**Institution:** Northeastern University  
**Instructor:** Prof. Nicholas Brown  
**Term:** Spring 2026

---

## 🧭 Project Overview

This project explores **binary classification for cardiovascular disease prediction** using two distinct medical datasets: stroke prediction and heart disease diagnosis. The goal is to understand which patient characteristics most strongly predict cardiovascular events and to evaluate how algorithm choice (linear vs ensemble) affects prediction accuracy in medical contexts.

Through a complete data science lifecycle—from exploratory analysis to model deployment readiness—the project demonstrates how proper preprocessing, rigorous evaluation, and clinical validation enable trustworthy machine learning in healthcare applications.

**Key Finding:** Data quality fundamentally determines success. Heart disease prediction achieved **99% accuracy** with objective clinical measurements, while stroke prediction reached only **50%** with self-reported lifestyle factors—despite having 15× more samples.

---

## 🧱 Objectives

* Compare **Logistic Regression** (linear, interpretable) and **Random Forest** (non-linear, ensemble) for cardiovascular prediction
* Handle **class imbalance** through stratified sampling and class weighting techniques
* Perform comprehensive **EDA** including normality testing, correlation analysis, and distribution visualization
* Implement proper **encoding strategies** for binary, ordinal, and nominal categorical variables
* Evaluate using **medical-appropriate metrics** (ROC-AUC, sensitivity, specificity) beyond simple accuracy
* Extract and **validate feature importance** against established medical literature
* Demonstrate when ML succeeds (quality features) vs fails (weak features)

---

## 🧩 Methodology

### 1. Data Preprocessing

**Dataset 1: Stroke Prediction (15,000 patients)**
* Handled missing BMI values with median imputation
* Encoded 22 features using type-appropriate strategies:
  * Binary features (Gender, Residence) → Label Encoding
  * Ordinal features (Physical Activity, Symptoms) → Order-preserving mapping (Low=0, Moderate=1, High=2)
  * Nominal features (Marital Status, Work Type) → One-Hot Encoding (drop_first=True)
* Target encoding: "Stroke"/"No Stroke" → 1/0
* Stratified 80-20 split maintaining ~5% stroke prevalence

**Dataset 2: Heart Disease (1,025 patients)**
* No missing values (complete dataset)
* Features already numerical (no encoding needed)
* Stratified 80-20 split maintaining 70-30 disease distribution
* StandardScaler for continuous features (mandatory for Logistic Regression)

### 2. Exploratory Data Analysis

**Distribution Analysis:**
* Normality testing (Shapiro-Wilk) for continuous features
* Histograms with normal curve overlays
* Q-Q plots for visual normality assessment

**Correlation Analysis:**
* Heatmaps revealing feature relationships
* Feature-target correlation rankings
* Multicollinearity detection

**Class Balance:**
* Target distribution analysis
* Imbalance ratio calculation
* Visualization of class proportions

**Univariate & Bivariate:**
* Box plots by target class
* Violin plots showing distribution differences
* Scatter plots for feature interactions

### 3. Modeling and Evaluation

**Algorithms:**
* **Logistic Regression:** Linear baseline with class_weight='balanced' for imbalance
* **Random Forest:** 100 trees, max_depth=10, class_weight='balanced'

**Evaluation Metrics:**
* **ROC-AUC:** Primary metric for imbalanced data (discrimination ability)
* **Accuracy:** Overall correctness (contextualized with baseline)
* **Sensitivity/Recall:** Critical for medical screening (minimize missed cases)
* **Specificity:** Correctly identifying healthy patients
* **Precision:** Positive predictive value
* **F1-Score:** Harmonic mean balancing precision-recall
* **Confusion Matrix:** Detailed error breakdown (TP, TN, FP, FN)

---

## 📊 Key Results

### Dataset 1: Stroke Prediction

| Model | Accuracy | Recall (Stroke) | ROC-AUC | Assessment |
|-------|----------|----------------|---------|------------|
| Linear Regression | 49.63% | 50% | ~0.51 |  Random performance |
| Random Forest | 51.00% | 50% | ~0.52 |  Random performance |

**Outcome:** Both models failed to learn meaningful patterns (performance equivalent to coin flipping)

**Root Cause:** Weak features (self-reported lifestyle data) lack predictive power for stroke

### Dataset 2: Heart Disease Diagnosis

| Model | Accuracy ↑ | Sensitivity ↑ | Specificity ↑ | ROC-AUC ↑ | Assessment |
|-------|-----------|--------------|--------------|-----------|------------|
| Logistic Regression | 78.05% | 87% | 69% | ~0.89 |  Good baseline |
| Random Forest | **98.54%** | **97%** | **100%** | **~0.99** |  Near-perfect! |

**Outcome:** Random Forest achieved exceptional, near-deployment-ready performance

**Key Achievement:** Zero false positives (100% specificity) with only 3 false negatives (3% miss rate)

---

## 💡 Key Insights

### 1. Data Quality is Paramount
* **Heart disease** (objective clinical tests): 1,025 samples → **99% accuracy**
* **Stroke** (self-reported lifestyle): 15,000 samples → **50% accuracy**
* **Lesson:** Quality > quantity—15× more data couldn't overcome weak features

### 2. Algorithm Choice Matters—When Data Permits
* **Heart disease:** Random Forest +21% better than Logistic Regression (78% → 99%)
* **Stroke:** Both algorithms equally failed (50% vs 51%)
* **Insight:** Sophisticated algorithms only help when features contain signal

### 3. Feature Importance Validates Medical Knowledge

**Heart Disease Top 5 (Both Models Agree):**
1. **cp** (Chest Pain Type) - Classic symptom presentation
2. **ca** (Vessels Colored) - Direct disease severity measure
3. **oldpeak** (ST Depression) - Ischemia indicator
4. **thalach** (Max Heart Rate) - Exercise capacity
5. **thal** (Thallium Test) - Perfusion defect detection


### 4. Class Imbalance Requires Specialized Handling
* Stratified splitting maintains distribution across train/test
* class_weight='balanced' prevents majority class bias
* ROC-AUC more reliable than accuracy for imbalanced data

### 5. Interpretability-Performance Tradeoff
* Logistic Regression: 78% accurate, fully interpretable (coefficients)
* Random Forest: 99% accurate, black box (100 trees)
* **Solution:** Use both—RF for predictions, LR for explanations

---

## 🛠️ Technologies Used

| Category | Tools / Libraries |
|----------|------------------|
| **Language** | Python 3.10+ |
| **Data Handling** | pandas, numpy |
| **Modeling** | scikit-learn (LogisticRegression, RandomForestClassifier) |
| **Visualization** | matplotlib, seaborn |
| **Environment** | Jupyter Notebook |

---


