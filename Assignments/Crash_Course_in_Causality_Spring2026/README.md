{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# INFO 7390: Crash Course in Causality - Assignment Template\n",
    "\n",
    "**Total Points:** 100  \n",
    "**Student Name:** [Your Name]  \n",
    "**Topic:** [Your Causality Topic]  \n",
    "**Date:** [Submission Date]\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Table of Contents\n",
    "\n",
    "1. [Title & Abstract](#title-abstract)\n",
    "2. [Theory Section](#theory)\n",
    "3. [Practical Code Examples](#code-examples)\n",
    "4. [Worked Example 1](#example-1)\n",
    "5. [Worked Example 2](#example-2)\n",
    "6. [Visualizations and Results](#visualizations)\n",
    "7. [Conclusion](#conclusion)\n",
    "8. [References](#references)\n",
    "9. [License](#license)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 1: Jupyter Notebook (35 points)\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='title-abstract'></a>\n",
    "## 1.1 Title & Abstract (4 points)\n",
    "\n",
    "### Title\n",
    "*[Your Clear, Concise Title Reflecting Main Topic]*\n",
    "\n",
    "### Abstract (150-200 words)\n",
    "*[Write your abstract here covering:*\n",
    "- *Key points readers will learn*\n",
    "- *Role of your topic in causal analysis for ML*\n",
    "- *Practical applications and importance]*\n",
    "\n",
    "**Points:** 4/4  \n",
    "- Title (2 points)  \n",
    "- Abstract (2 points)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='theory'></a>\n",
    "## 1.2 Theory Section (10 points)\n",
    "\n",
    "### 1.2.1 Foundational Concepts in Causality Principles (3 points)\n",
    "\n",
    "*[Explain foundational causality concepts relevant to your topic]*\n",
    "\n",
    "Key concepts to cover:\n",
    "- Correlation vs. Causation\n",
    "- Counterfactuals\n",
    "- Treatment and Outcome\n",
    "- Causal Graphs (DAGs)\n",
    "\n",
    "### 1.2.2 Data Preparation Techniques in Causal Framework (3 points)\n",
    "\n",
    "*[Explain data preparation specific to causal analysis]*\n",
    "\n",
    "Topics to include:\n",
    "- Handling missing data in causal contexts\n",
    "- Feature selection for causal inference\n",
    "- Encoding categorical variables\n",
    "- Balancing treatment and control groups\n",
    "\n",
    "### 1.2.3 Supporting Causal Relationship Interpretation (2 points)\n",
    "\n",
    "*[Explain how preparation supports causal interpretation]*\n",
    "\n",
    "### 1.2.4 Integration of Causal Concepts (2 points)\n",
    "\n",
    "*[Integrate concepts like:]*\n",
    "- **Confounding:** Variables affecting both treatment and outcome\n",
    "- **Colliders:** Variables affected by both treatment and outcome\n",
    "- **Mediators:** Variables in the causal pathway\n",
    "- **Selection Bias**\n",
    "- **Backdoor Paths**\n",
    "- **Front-door Criterion**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import necessary libraries for causal analysis\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from scipy import stats\n",
    "\n",
    "# Causal inference libraries\n",
    "# pip install dowhy causalml econml\n",
    "import dowhy\n",
    "from dowhy import CausalModel\n",
    "\n",
    "# Additional libraries for specific methods\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Set visualization style\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (10, 6)\n",
    "\n",
    "print(\"✅ Libraries imported successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='code-examples'></a>\n",
    "## 1.3 Practical Code Examples (12 points)\n",
    "\n",
    "### Example: Demonstrating Confounding\n",
    "\n",
    "In this example, we'll demonstrate how confounding variables can create spurious correlations."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Generate synthetic data with confounding\n",
    "np.random.seed(42)\n",
    "n = 1000\n",
    "\n",
    "# Confounder (e.g., socioeconomic status)\n",
    "confounder = np.random.normal(0, 1, n)\n",
    "\n",
    "# Treatment (affected by confounder)\n",
    "treatment = (confounder + np.random.normal(0, 0.5, n)) > 0\n",
    "treatment = treatment.astype(int)\n",
    "\n",
    "# Outcome (affected by both confounder and treatment)\n",
    "outcome = 2 * confounder + 3 * treatment + np.random.normal(0, 1, n)\n",
    "\n",
    "# Create DataFrame\n",
    "df_example = pd.DataFrame({\n",
    "    'confounder': confounder,\n",
    "    'treatment': treatment,\n",
    "    'outcome': outcome\n",
    "})\n",
    "\n",
    "print(\"Dataset created:\")\n",
    "print(df_example.head())\n",
    "print(f\"\\nDataset shape: {df_example.shape}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Visualization of Confounding"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visualize the confounding relationship\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "# Plot 1: Treatment vs Outcome (naive)\n",
    "axes[0].scatter(df_example['treatment'], df_example['outcome'], alpha=0.5)\n",
    "axes[0].set_xlabel('Treatment')\n",
    "axes[0].set_ylabel('Outcome')\n",
    "axes[0].set_title('Naive Association: Treatment vs Outcome')\n",
    "\n",
    "# Plot 2: Colored by confounder\n",
    "scatter = axes[1].scatter(df_example['treatment'], df_example['outcome'], \n",
    "                          c=df_example['confounder'], alpha=0.6, cmap='viridis')\n",
    "axes[1].set_xlabel('Treatment')\n",
    "axes[1].set_ylabel('Outcome')\n",
    "axes[1].set_title('Association Accounting for Confounder')\n",
    "plt.colorbar(scatter, ax=axes[1], label='Confounder')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Interpretation:**  \n",
    "*[Explain what the visualization shows about confounding and why controlling for confounders is essential]*\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 3: Worked Examples (20 points)\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='example-1'></a>\n",
    "## 3.1 Example 1: Causal Analysis on Primary Dataset (10 points)\n",
    "\n",
    "### Dataset Description (2 points)\n",
    "\n",
    "**Dataset:** [Dataset Name]  \n",
    "**Source:** [URL or reference]  \n",
    "**Size:** [n rows × m columns]  \n",
    "\n",
    "**Description:**  \n",
    "*[Clear explanation of:*\n",
    "- *What the dataset contains*\n",
    "- *Why it's relevant for causal analysis*\n",
    "- *Potential causal relationships to explore]*\n",
    "\n",
    "**Variables:**\n",
    "- **Treatment Variable:** [variable name and description]\n",
    "- **Outcome Variable:** [variable name and description]\n",
    "- **Confounders:** [list and describe]\n",
    "- **Other Variables:** [relevant covariates]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load Example 1 Dataset\n",
    "# Replace with your actual dataset loading\n",
    "\n",
    "# Option 1: From CSV\n",
    "# df1 = pd.read_csv('Example1_Dataset/dataset.csv')\n",
    "\n",
    "# Option 2: From built-in datasets or generate synthetic\n",
    "from sklearn.datasets import make_classification\n",
    "\n",
    "# Placeholder - replace with your actual data\n",
    "X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, \n",
    "                           n_redundant=2, random_state=42)\n",
    "df1 = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])\n",
    "df1['treatment'] = (df1['feature_0'] > 0).astype(int)\n",
    "df1['outcome'] = y\n",
    "\n",
    "print(\"Example 1 Dataset Loaded:\")\n",
    "print(f\"Shape: {df1.shape}\")\n",
    "print(f\"\\nFirst few rows:\")\n",
    "df1.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Problem Setup (2 points)\n",
    "\n",
    "**Causal Question:**  \n",
    "*[State your causal question clearly, e.g., \"What is the causal effect of X on Y?\"]*\n",
    "\n",
    "**Hypothesis:**  \n",
    "*[Your hypothesis about the expected causal relationship]*\n",
    "\n",
    "**Identification Strategy:**\n",
    "- **Treatment:** [Define treatment]\n",
    "- **Outcome:** [Define outcome]\n",
    "- **Confounders:** [List confounders that must be controlled]\n",
    "- **Causal Assumptions:**\n",
    "  - Unconfoundedness: [explain]\n",
    "  - SUTVA (Stable Unit Treatment Value Assumption): [explain]\n",
    "  - Overlap/Common Support: [explain]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 1: Exploratory Causal Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Exploratory Data Analysis with causal lens\n",
    "\n",
    "# Check for missing values\n",
    "print(\"Missing Values:\")\n",
    "print(df1.isnull().sum())\n",
    "\n",
    "# Summary statistics\n",
    "print(\"\\nSummary Statistics:\")\n",
    "print(df1.describe())\n",
    "\n",
    "# Treatment distribution\n",
    "print(\"\\nTreatment Distribution:\")\n",
    "print(df1['treatment'].value_counts())\n",
    "\n",
    "# Outcome by treatment\n",
    "print(\"\\nOutcome by Treatment:\")\n",
    "print(df1.groupby('treatment')['outcome'].describe())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 2: Construct Causal Graph (DAG)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Define the causal graph using DoWhy\n",
    "# Example causal graph structure\n",
    "\n",
    "causal_graph = \"\"\"\n",
    "digraph {\n",
    "    confounder -> treatment;\n",
    "    confounder -> outcome;\n",
    "    treatment -> outcome;\n",
    "}\n",
    "\"\"\"\n",
    "\n",
    "# Visualize the DAG (you may need graphviz installed)\n",
    "# import graphviz\n",
    "# graph = graphviz.Source(causal_graph)\n",
    "# graph.render('causal_dag', format='png', cleanup=True)\n",
    "# from IPython.display import Image\n",
    "# Image('causal_dag.png')\n",
    "\n",
    "print(\"Causal Graph Defined\")\n",
    "print(causal_graph)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 3: Create Causal Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create causal model using DoWhy\n",
    "model = CausalModel(\n",
    "    data=df1,\n",
    "    treatment='treatment',\n",
    "    outcome='outcome',\n",
    "    graph=causal_graph\n",
    ")\n",
    "\n",
    "print(\"Causal Model Created\")\n",
    "print(model)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 4: Identify Causal Effect"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Identify the causal effect\n",
    "identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)\n",
    "\n",
    "print(\"Identified Estimand:\")\n",
    "print(identified_estimand)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 5: Estimate Causal Effect"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Estimate the causal effect using different methods\n",
    "\n",
    "# Method 1: Propensity Score Matching\n",
    "estimate_psm = model.estimate_effect(\n",
    "    identified_estimand,\n",
    "    method_name=\"backdoor.propensity_score_matching\"\n",
    ")\n",
    "\n",
    "print(\"Causal Estimate (Propensity Score Matching):\")\n",
    "print(estimate_psm)\n",
    "print(f\"\\nEstimated Effect: {estimate_psm.value}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 6: Refute the Estimate (Sensitivity Analysis)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Perform refutation tests\n",
    "\n",
    "# Refutation 1: Add random common cause\n",
    "refute_random_cause = model.refute_estimate(\n",
    "    identified_estimand,\n",
    "    estimate_psm,\n",
    "    method_name=\"random_common_cause\"\n",
    ")\n",
    "print(\"Refutation - Random Common Cause:\")\n",
    "print(refute_random_cause)\n",
    "\n",
    "# Refutation 2: Placebo treatment\n",
    "refute_placebo = model.refute_estimate(\n",
    "    identified_estimand,\n",
    "    estimate_psm,\n",
    "    method_name=\"placebo_treatment_refuter\"\n",
    ")\n",
    "print(\"\\nRefutation - Placebo Treatment:\")\n",
    "print(refute_placebo)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Results and Interpretation\n",
    "\n",
    "**Causal Effect Estimate:**  \n",
    "*[State the estimated causal effect and confidence intervals]*\n",
    "\n",
    "**Interpretation:**  \n",
    "*[Explain what this means in context:*\n",
    "- *Magnitude of the effect*\n",
    "- *Statistical significance*\n",
    "- *Practical significance*\n",
    "- *How it answers your causal question]*\n",
    "\n",
    "**Robustness:**  \n",
    "*[Discuss refutation test results and whether the estimate is robust]*\n",
    "\n",
    "**Limitations:**  \n",
    "*[Acknowledge limitations:*\n",
    "- *Potential unmeasured confounders*\n",
    "- *Assumption violations*\n",
    "- *Generalizability concerns]*\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='example-2'></a>\n",
    "## 3.2 Example 2: Causal Exercise on Different Dataset (10 points)\n",
    "\n",
    "### Dataset Description (2 points)\n",
    "\n",
    "**Dataset:** [Different Dataset Name]  \n",
    "**Source:** [URL or reference]  \n",
    "**Size:** [n rows × m columns]  \n",
    "\n",
    "**Description:**  \n",
    "*[New dataset with different causal structure]*\n",
    "\n",
    "**Key Difference from Example 1:**  \n",
    "*[Explain how this dataset/problem differs - e.g., different method, time series, instrumental variable setup, etc.]*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load Example 2 Dataset\n",
    "# Replace with your second dataset\n",
    "\n",
    "# Placeholder - replace with actual data\n",
    "df2 = pd.DataFrame({\n",
    "    'pre_treatment': np.random.normal(50, 10, 200),\n",
    "    'post_treatment': np.random.normal(55, 10, 200),\n",
    "    'group': ['treatment']*100 + ['control']*100\n",
    "})\n",
    "\n",
    "print(\"Example 2 Dataset Loaded:\")\n",
    "print(f\"Shape: {df2.shape}\")\n",
    "df2.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Problem Setup (2 points)\n",
    "\n",
    "**Causal Question:**  \n",
    "*[Different causal question from Example 1]*\n",
    "\n",
    "**Method:**  \n",
    "*[e.g., Difference-in-Differences, Instrumental Variables, Regression Discontinuity, etc.]*\n",
    "\n",
    "**Causal Assumptions:**  \n",
    "*[State assumptions specific to this method]*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step-by-Step Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 1: Data Preparation\n",
    "# [Your data preparation code]\n",
    "\n",
    "print(\"Data prepared for analysis\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 2: Apply Causal Method\n",
    "# [Your causal analysis code]\n",
    "\n",
    "# Example: Difference-in-Differences\n",
    "# Calculate means\n",
    "treatment_pre = df2[df2['group']=='treatment']['pre_treatment'].mean()\n",
    "treatment_post = df2[df2['group']=='treatment']['post_treatment'].mean()\n",
    "control_pre = df2[df2['group']=='control']['pre_treatment'].mean()\n",
    "control_post = df2[df2['group']=='control']['post_treatment'].mean()\n",
    "\n",
    "# Calculate DiD estimate\n",
    "did_estimate = (treatment_post - treatment_pre) - (control_post - control_pre)\n",
    "\n",
    "print(f\"Difference-in-Differences Estimate: {did_estimate:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 3: Visualize Results\n",
    "# [Your visualization code]\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "# Add your visualization\n",
    "plt.title('Causal Effect Visualization')\n",
    "plt.xlabel('Variable')\n",
    "plt.ylabel('Outcome')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Results and Interpretation\n",
    "\n",
    "**Findings:**  \n",
    "*[Your causal effect estimates]*\n",
    "\n",
    "**Interpretation:**  \n",
    "*[What do these results mean?]*\n",
    "\n",
    "**Sensitivity Analysis:**  \n",
    "*[Robustness checks performed]*\n",
    "\n",
    "**Potential Biases:**  \n",
    "*[Discuss potential sources of bias]*\n",
    "\n",
    "**Limitations:**  \n",
    "*[Acknowledge limitations specific to this analysis]*\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='visualizations'></a>\n",
    "## 1.4 Visualizations and Results (4 points)\n",
    "\n",
    "### Key Visualizations Summary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create comprehensive visualizations\n",
    "\n",
    "fig, axes = plt.subplots(2, 2, figsize=(15, 12))\n",
    "\n",
    "# Visualization 1: Distribution of Treatment and Control\n",
    "# [Your code]\n",
    "\n",
    "# Visualization 2: Effect Estimates with Confidence Intervals\n",
    "# [Your code]\n",
    "\n",
    "# Visualization 3: Covariate Balance Before/After Matching\n",
    "# [Your code]\n",
    "\n",
    "# Visualization 4: Sensitivity Analysis Results\n",
    "# [Your code]\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Overall Results Interpretation\n",
    "\n",
    "*[Provide comprehensive interpretation of all visualizations within causal framework]*\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='conclusion'></a>\n",
    "## 1.5 Conclusion (2 points)\n",
    "\n",
    "### Key Takeaways\n",
    "\n",
    "1. **[First Key Takeaway]**  \n",
    "   *[Explanation]*\n",
    "\n",
    "2. **[Second Key Takeaway]**  \n",
    "   *[Explanation]*\n",
    "\n",
    "3. **[Third Key Takeaway]**  \n",
    "   *[Explanation]*\n",
    "\n",
    "### Importance of Data Preparation in Causal Analysis\n",
    "\n",
    "*[Reiterate the critical role of proper data preparation in causal inference and how it impacts:*\n",
    "- *Validity of causal estimates*\n",
    "- *Model development and deployment*\n",
    "- *Decision-making based on causal models]*\n",
    "\n",
    "### Future Directions\n",
    "\n",
    "*[Suggest areas for further research or improvement]*\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='references'></a>\n",
    "## 1.6 References (2 points)\n",
    "\n",
    "### Academic Papers\n",
    "\n",
    "1. Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.\n",
    "\n",
    "2. Imbens, G. W., & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction*. Cambridge University Press.\n",
    "\n",
    "3. [Add your references]\n",
    "\n",
    "### Software and Libraries\n",
    "\n",
    "1. Sharma, A., & Kiciman, E. (2020). DoWhy: An End-to-End Library for Causal Inference. *arXiv preprint arXiv:2011.04216*.\n",
    "\n",
    "2. [Add your tool references]\n",
    "\n",
    "### Online Resources\n",
    "\n",
    "1. [Add reputable online resources]\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a id='license'></a>\n",
    "## 1.7 License (1 point)\n",
    "\n",
    "### License Information\n",
    "\n",
    "**License Type:** [e.g., MIT License, Creative Commons BY 4.0, etc.]\n",
    "\n",
    "**Copyright:** © [Year] [Your Name]\n",
    "\n",
    "**Permissions:**  \n",
    "*[Specify reuse permissions, e.g.:]*\n",
    "- This work is licensed under [License Name]\n",
    "- You are free to share and adapt this material for any purpose\n",
    "- Attribution must be given to the original author\n",
    "\n",
    "**Citation:**  \n",
    "If you use this notebook, please cite as:\n",
    "```\n",
    "[Your Name]. (2024). [Notebook Title]. \n",
    "INFO 7390: Crash Course in Causality. \n",
    "Northeastern University.\n",
    "```\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Assignment Checklist\n",
    "---\n",
    "\n",
    "### Part 1: Jupyter Notebook (35 points)\n",
    "- [ ] 1.1 Title & Abstract (4 points)\n",
    "- [ ] 1.2 Theory Section (10 points)\n",
    "- [ ] 1.3 Practical Code Examples (12 points)\n",
    "- [ ] 1.4 Visualizations and Results (4 points)\n",
    "- [ ] 1.5 Conclusion (2 points)\n",
    "- [ ] 1.6 References (2 points)\n",
    "- [ ] 1.7 License (1 point)\n",
    "\n",
    "### Part 2: Video Presentation (15 points)\n",
    "- [ ] Record 3-5 minute video\n",
    "- [ ] Upload to YouTube/Drive\n",
    "- [ ] Add link to Video_Link.txt\n",
    "\n",
    "### Part 3: Worked Examples (20 points)\n",
    "- [ ] Example 1 Complete (10 points)\n",
    "- [ ] Example 2 Complete (10 points)\n",
    "- [ ] Both examples use different datasets\n",
    "- [ ] Both examples demonstrate different causal methods\n",
    "\n",
    "### Part 4: Quiz Questions (10 points)\n",
    "- [ ] Create 15 multiple-choice questions\n",
    "- [ ] Save to QuizQuestions.md\n",
    "- [ ] Include explanations for all answers\n",
    "\n",
    "### Submission\n",
    "- [ ] GitHub repository created with proper structure\n",
    "- [ ] All code tested and executable\n",
    "- [ ] README.md completed\n",
    "- [ ] Submit to Canvas\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Appendix: Additional Code and Resources\n",
    "\n",
    "*[Add any additional code, helper functions, or supplementary materials here]*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Additional helper functions\n",
    "\n",
    "def calculate_ate(df, treatment_col, outcome_col):\n",
    "    \"\"\"\n",
    "    Calculate Average Treatment Effect (ATE)\n",
    "    \"\"\"\n",
    "    treated = df[df[treatment_col] == 1][outcome_col].mean()\n",
    "    control = df[df[treatment_col] == 0][outcome_col].mean()\n",
    "    ate = treated - control\n",
    "    return ate\n",
    "\n",
    "def check_balance(df, treatment_col, covariates):\n",
    "    \"\"\"\n",
    "    Check covariate balance between treatment and control groups\n",
    "    \"\"\"\n",
    "    balance_results = {}\n",
    "    for cov in covariates:\n",
    "        treated_mean = df[df[treatment_col]==1][cov].mean()\n",
    "        control_mean = df[df[treatment_col]==0][cov].mean()\n",
    "        std_diff = (treated_mean - control_mean) / df[cov].std()\n",
    "        balance_results[cov] = std_diff\n",
    "    return balance_results\n",
    "\n",
    "print(\"Helper functions loaded\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "\n",
    "## End of Notebook\n",
    "\n",
    "**Total Points:** 100  \n",
    "**Submission Date:** [Date]  \n",
    "**Student:** [Your Name]\n",
    "\n",
    "---"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}