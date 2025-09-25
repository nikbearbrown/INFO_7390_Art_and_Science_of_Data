# Data Science and AI Practice Exam #4 (100 Points)

## Instructions
- Each question is worth 5 points
- Select all correct answers for each question
- There may be multiple correct answers per question
- A detailed answer key is provided at the end of the exam

## Section 1: Generative AI and Deep Learning (35 points)

### Question 1
Which statements accurately describe the architecture and capabilities of modern transformer-based language models?
- [x] A) Layer normalization helps stabilize training in deep transformer networks
- [ ] B) Transformers process tokens sequentially from left to right during both training and inference
- [x] C) Residual connections help mitigate the vanishing gradient problem in deep networks
- [x] D) The embedding dimension determines the representational capacity of tokens
- [ ] E) The number of attention heads must equal the model dimension for optimal performance

### Question 2
Which approaches effectively enable language models to interface with external tools and systems?
- [x] A) Function calling with structured JSON output
- [x] B) Tool-use frameworks that translate natural language to API calls
- [ ] C) Increasing context window size indefinitely
- [x] D) Retrieval-augmented generation to access external information
- [ ] E) Training larger models without external interfaces

### Question 3
What methods help generative AI models balance helpfulness with safety?
- [x] A) Constitutional AI approaches with rule-based constraints
- [x] B) Red-teaming to identify and address potential vulnerabilities
- [ ] C) Limiting model capabilities uniformly across all use cases
- [x] D) Context-aware safety mechanisms that adapt to conversation topics
- [ ] E) Implementing overly cautious responses for all potentially sensitive queries

### Question 4
What are valid approaches for fine-tuning language models on domain-specific tasks?
- [x] A) Parameter-efficient methods that update only a small subset of weights
- [x] B) Using high-quality, diverse examples representing the target distribution
- [ ] C) Setting identical learning rates for all model layers
- [x] D) Implementing early stopping based on validation set performance
- [ ] E) Using the same hyperparameters for all domains regardless of data characteristics

### Question 5
Which statements about the evaluation of generative AI systems are correct?
- [x] A) Human evaluation provides insights that automated metrics often miss
- [x] B) Evaluation should include both capability and safety assessments
- [ ] C) BLEU score is the gold standard for evaluating all generative language tasks
- [x] D) Task-specific benchmarks are more informative than general-purpose evaluations
- [ ] E) Larger models automatically score better on all evaluation metrics

### Question 6
What challenges do current generative AI systems face with reasoning tasks?
- [x] A) Difficulty maintaining logical consistency in extended reasoning chains
- [ ] B) Complete inability to follow multi-step instructions
- [x] C) Challenges with complex mathematical proofs and derivations
- [x] D) Susceptibility to reasoning shortcuts that lead to incorrect conclusions
- [ ] E) Inability to understand basic logical operations like AND, OR, and NOT

### Question 7
Which techniques are effective for controlling the output of generative AI models?
- [x] A) System prompts that establish roles and constraints
- [x] B) Temperature adjustment to control randomness in generation
- [ ] C) Increasing token generation length for all responses
- [x] D) Few-shot examples that demonstrate the desired output format
- [ ] E) Hard-coding responses to all possible queries

## Section 2: Causal Inference (35 points)

### Question 8
Which study designs can provide evidence for causal relationships?
- [x] A) Randomized controlled trials with proper randomization
- [x] B) Natural experiments with plausible as-if randomization
- [ ] C) Cross-sectional studies without controlling for confounders
- [x] D) Difference-in-differences designs with parallel trends assumption
- [ ] E) Ecological studies correlating population-level variables

### Question 9
What assumptions are necessary for instrumental variable estimation of causal effects?
- [x] A) The instrument affects the treatment (relevance)
- [x] B) The instrument affects the outcome only through the treatment (exclusion restriction)
- [x] C) The instrument is independent of unmeasured confounders
- [ ] D) Treatment effects must be homogeneous across all subpopulations
- [ ] E) The outcome must be continuous rather than binary

### Question 10
Which statements about marginal structural models (MSMs) and inverse probability weighting are correct?
- [x] A) MSMs can handle time-varying treatments and confounders
- [x] B) Inverse probability weighting creates a pseudo-population where treatment is unconfounded
- [ ] C) MSMs require fewer assumptions than standard regression approaches
- [x] D) Extreme weights can lead to instability in causal effect estimates
- [ ] E) MSMs automatically adjust for unmeasured confounding

### Question 11
What are valid methods to address selection bias in causal inference?
- [x] A) Inverse probability of censoring weights
- [x] B) Bounds analysis for partially identified effects
- [ ] C) Simply restricting analysis to complete cases
- [x] D) Multiple imputation methods with appropriate missingness assumptions
- [ ] E) Ignoring missing data patterns in randomized studies

### Question 12
Which statements about causal effects in longitudinal data are correct?
- [x] A) Lagged variables can serve as controls for time-varying confounding
- [x] B) Fixed effects models address time-invariant unobserved confounding
- [ ] C) Standard regression adjustment is sufficient for time-varying confounding
- [x] D) G-methods can handle treatment-confounder feedback loops
- [ ] E) Longer follow-up always provides more robust causal estimates

### Question 13
In causal mediation analysis, which statements are correct?
- [x] A) Natural direct and indirect effects require strong assumptions about cross-world counterfactuals
- [x] B) Controlled direct effects can be identified under weaker assumptions than natural effects
- [ ] C) Baron and Kenny's approach accounts for exposure-mediator interactions
- [x] D) Sensitive mediation analysis requires no unmeasured mediator-outcome confounding
- [ ] E) The sum of direct and indirect effects always equals the total effect

### Question 14
What are valid methods for sensitivity analysis in causal inference?
- [x] A) E-values that quantify the minimum strength of unmeasured confounding needed to explain away an effect
- [x] B) Modeling the potential impact of unmeasured confounders on effect estimates
- [ ] C) Simply comparing results from different study populations
- [x] D) Bounding approaches that estimate worst-case scenarios under violations of assumptions
- [ ] E) Increasing sample size to eliminate need for sensitivity analysis

## Section 3: Machine Learning and Data Concepts (30 points)

### Question 15
Which statements about regularization in machine learning are correct?
- [x] A) L1 regularization (Lasso) can produce sparse models by forcing some coefficients to zero
- [x] B) L2 regularization (Ridge) shrinks coefficients proportionally to their magnitude
- [ ] C) Regularization always improves both training and test performance
- [x] D) The optimal regularization strength typically increases as dataset size decreases
- [ ] E) Regularization only affects linear models, not complex models like neural networks

### Question 16
For feature engineering in machine learning, which approaches are valid?
- [x] A) Creating polynomial features to capture non-linear relationships
- [x] B) Implementing domain-specific transformations based on subject knowledge
- [ ] C) Always using all available features regardless of relevance
- [x] D) Encoding cyclical features like time of day using sine and cosine transformations
- [ ] E) Standardizing all variables including binary indicators

### Question 17
In clustering analysis, which validation approaches and metrics are appropriate?
- [x] A) Silhouette coefficient to measure cluster cohesion and separation
- [x] B) External validation using known class labels when available
- [ ] C) Visual inspection as the sole validation criterion
- [x] D) Stability analysis by rerunning clustering on data subsets
- [ ] E) Always selecting the solution with the most clusters

### Question 18
Which techniques are effective for interpreting complex machine learning models?
- [x] A) SHAP values to quantify feature contributions to individual predictions
- [x] B) Partial dependence plots to visualize relationships between features and predictions
- [x] C) Local interpretable model-agnostic explanations (LIME)
- [ ] D) Focusing solely on global model accuracy rather than interpretability
- [ ] E) Using only model coefficients regardless of model type

### Question 19
For time series forecasting, which approaches are valid?
- [x] A) Testing for and addressing seasonality in the data
- [x] B) Using rolling-window cross-validation for model selection
- [ ] C) Applying standard random cross-validation without accounting for time
- [x] D) Combining multiple forecasting methods in ensemble approaches
- [ ] E) Always differencing time series data regardless of stationarity tests

### Question 20
Which statements about imbalanced data handling in machine learning are correct?
- [x] A) Synthetic minority oversampling (SMOTE) creates new minority class examples
- [ ] B) Performance metrics like accuracy are usually sufficient for imbalanced datasets
- [x] C) Cost-sensitive learning assigns higher penalties to minority class misclassifications
- [x] D) Class weights can help models adjust decision boundaries appropriately
- [ ] E) Anomaly detection problems typically have balanced class distributions

---

# Answer Key with Detailed Explanations

## Section 1: Generative AI and Deep Learning

### Question 1
**Correct answers: A, C, D**

- **A) Layer normalization helps stabilize training in deep transformer networks** ✓
  - Layer normalization standardizes inputs across features, stabilizing training by mitigating internal covariate shift.

- **C) Residual connections help mitigate the vanishing gradient problem in deep networks** ✓
  - Residual connections provide gradient shortcuts, helping information flow through deep networks during backpropagation.

- **D) The embedding dimension determines the representational capacity of tokens** ✓
  - The embedding dimension defines the vector space size for representing tokens, affecting the model's capacity to encode meaning.

- **B) Transformers process tokens sequentially from left to right during both training and inference** ✗
  - Transformers process all tokens in parallel during training; only during autoregressive generation do they process sequentially.

- **E) The number of attention heads must equal the model dimension for optimal performance** ✗
  - The number of attention heads is a hyperparameter independent of model dimension; they're typically a fraction of the model dimension.

### Question 2
**Correct answers: A, B, D**

- **A) Function calling with structured JSON output** ✓
  - Structured function-calling APIs enable models to interact with external systems through well-defined interfaces.

- **B) Tool-use frameworks that translate natural language to API calls** ✓
  - Tool-use frameworks allow models to leverage external capabilities by translating requests into appropriate API calls.

- **D) Retrieval-augmented generation to access external information** ✓
  - RAG enables models to access and incorporate up-to-date or domain-specific information from external sources.

- **C) Increasing context window size indefinitely** ✗
  - While larger contexts help, they don't enable true tool use or system integration capabilities.

- **E) Training larger models without external interfaces** ✗
  - Model scale alone doesn't provide the structured interaction capabilities needed for tool use.

### Question 3
**Correct answers: A, B, D**

- **A) Constitutional AI approaches with rule-based constraints** ✓
  - Constitutional AI implements rule-based guidance to balance helpfulness with safety constraints.

- **B) Red-teaming to identify and address potential vulnerabilities** ✓
  - Red-teaming systematically tests models to find and mitigate safety issues before deployment.

- **D) Context-aware safety mechanisms that adapt to conversation topics** ✓
  - Context-sensitive safety allows appropriate responses across varying conversation contexts.

- **C) Limiting model capabilities uniformly across all use cases** ✗
  - Uniform limitations reduce utility unnecessarily; targeted safeguards are more effective.

- **E) Implementing overly cautious responses for all potentially sensitive queries** ✗
  - Excessive caution reduces model helpfulness for legitimate queries; balanced approaches are preferred.

### Question 4
**Correct answers: A, B, D**

- **A) Parameter-efficient methods that update only a small subset of weights** ✓
  - Techniques like LoRA or adapter-based fine-tuning effectively adapt models while reducing computational requirements.

- **B) Using high-quality, diverse examples representing the target distribution** ✓
  - Dataset quality and representativeness significantly impact fine-tuning success.

- **D) Implementing early stopping based on validation set performance** ✓
  - Early stopping prevents overfitting by halting training when validation performance plateaus or declines.

- **C) Setting identical learning rates for all model layers** ✗
  - Different layers often benefit from different learning rates; often later layers require higher rates than earlier ones.

- **E) Using the same hyperparameters for all domains regardless of data characteristics** ✗
  - Optimal hyperparameters vary based on domain, data size, and task complexity.

### Question 5
**Correct answers: A, B, D**

- **A) Human evaluation provides insights that automated metrics often miss** ✓
  - Human evaluation captures nuances in quality, relevance, and helpfulness that automated metrics may not detect.

- **B) Evaluation should include both capability and safety assessments** ✓
  - Comprehensive evaluation must consider both what models can do and how they handle potentially problematic requests.

- **D) Task-specific benchmarks are more informative than general-purpose evaluations** ✓
  - Specialized benchmarks provide more detailed insights into performance on particular tasks or domains.

- **C) BLEU score is the gold standard for evaluating all generative language tasks** ✗
  - BLEU is primarily for machine translation; different tasks require different evaluation metrics.

- **E) Larger models automatically score better on all evaluation metrics** ✗
  - While scale often helps, model size alone doesn't guarantee better performance across all metrics.

### Question 6
**Correct answers: A, C, D**

- **A) Difficulty maintaining logical consistency in extended reasoning chains** ✓
  - Models often introduce inconsistencies in complex multi-step reasoning processes.

- **C) Challenges with complex mathematical proofs and derivations** ✓
  - Advanced mathematical reasoning remains challenging for current models.

- **D) Susceptibility to reasoning shortcuts that lead to incorrect conclusions** ✓
  - Models may take heuristic shortcuts rather than performing rigorous logical analysis.

- **B) Complete inability to follow multi-step instructions** ✗
  - Modern LLMs can follow multi-step instructions reasonably well in many cases.

- **E) Inability to understand basic logical operations like AND, OR, and NOT** ✗
  - Current models generally handle basic logic operations effectively.

### Question 7
**Correct answers: A, B, D**

- **A) System prompts that establish roles and constraints** ✓
  - System prompts effectively define the model's persona, capabilities, and limitations.

- **B) Temperature adjustment to control randomness in generation** ✓
  - Temperature settings balance deterministic responses with creative variation.

- **D) Few-shot examples that demonstrate the desired output format** ✓
  - Examples in the prompt help guide the model's output structure and style.

- **C) Increasing token generation length for all responses** ✗
  - Longer isn't always better; appropriate length depends on the task.

- **E) Hard-coding responses to all possible queries** ✗
  - This defeats the purpose of generative AI and isn't feasible for open-domain systems.

## Section 2: Causal Inference

### Question 8
**Correct answers: A, B, D**

- **A) Randomized controlled trials with proper randomization** ✓
  - Randomization balances confounders across groups, allowing causal interpretation.

- **B) Natural experiments with plausible as-if randomization** ✓
  - Natural experiments with exogenous assignment can approximate randomized trials.

- **D) Difference-in-differences designs with parallel trends assumption** ✓
  - DiD designs can identify causal effects if the parallel trends assumption holds.

- **C) Cross-sectional studies without controlling for confounders** ✗
  - Without confounder control, cross-sectional studies only establish association.

- **E) Ecological studies correlating population-level variables** ✗
  - Ecological studies are susceptible to ecological fallacy and generally can't establish individual-level causation.

### Question 9
**Correct answers: A, B, C**

- **A) The instrument affects the treatment (relevance)** ✓
  - A valid instrument must have a non-zero effect on the treatment variable.

- **B) The instrument affects the outcome only through the treatment (exclusion restriction)** ✓
  - The instrument must have no direct effect on the outcome except through treatment.

- **C) The instrument is independent of unmeasured confounders** ✓
  - The instrument must not share common causes with the outcome.

- **D) Treatment effects must be homogeneous across all subpopulations** ✗
  - IV can accommodate heterogeneous treatment effects under certain conditions.

- **E) The outcome must be continuous rather than binary** ✗
  - IV methods exist for both continuous and binary outcomes.

### Question 10
**Correct answers: A, B, D**

- **A) MSMs can handle time-varying treatments and confounders** ✓
  - MSMs are specifically designed for longitudinal settings with time-varying factors.

- **B) Inverse probability weighting creates a pseudo-population where treatment is unconfounded** ✓
  - IPW reweights observations to break the association between treatment and confounders.

- **D) Extreme weights can lead to instability in causal effect estimates** ✓
  - Practical positivity violations can create very large weights that destabilize estimates.

- **C) MSMs require fewer assumptions than standard regression approaches** ✗
  - MSMs require similar assumptions (no unmeasured confounding, positivity, consistency) as standard approaches.

- **E) MSMs automatically adjust for unmeasured confounding** ✗
  - No purely statistical method can adjust for unmeasured confounding without additional assumptions.

### Question 11
**Correct answers: A, B, D**

- **A) Inverse probability of censoring weights** ✓
  - IPCW adjusts for selection bias due to differential loss to follow-up.

- **B) Bounds analysis for partially identified effects** ✓
  - Bounds provide range estimates for causal effects under various selection mechanisms.

- **D) Multiple imputation methods with appropriate missingness assumptions** ✓
  - Multiple imputation can address selection bias when missingness is MAR conditional on observed variables.

- **C) Simply restricting analysis to complete cases** ✗
  - Complete-case analysis introduces selection bias if missingness depends on treatment or outcome.

- **E) Ignoring missing data patterns in randomized studies** ✗
  - Even in randomized studies, non-random attrition can introduce selection bias.

### Question 12
**Correct answers: A, B, D**

- **A) Lagged variables can serve as controls for time-varying confounding** ✓
  - Lagged variables help control for confounding when past values affect current treatment and outcomes.

- **B) Fixed effects models address time-invariant unobserved confounding** ✓
  - Fixed effects control for all time-invariant individual characteristics, observed or unobserved.

- **D) G-methods can handle treatment-confounder feedback loops** ✓
  - G-methods specifically address scenarios where treatments affect future confounders.

- **C) Standard regression adjustment is sufficient for time-varying confounding** ✗
  - Standard regression fails when confounders are affected by previous treatment.

- **E) Longer follow-up always provides more robust causal estimates** ✗
  - Longer follow-up may introduce more bias from attrition or intervention changes.

### Question 13
**Correct answers: A, B, D**

- **A) Natural direct and indirect effects require strong assumptions about cross-world counterfactuals** ✓
  - Natural effects involve counterfactuals that cannot occur in the same world, requiring strong assumptions.

- **B) Controlled direct effects can be identified under weaker assumptions than natural effects** ✓
  - Controlled direct effects do not require assumptions about potential mediator values under alternative exposures.

- **D) Sensitive mediation analysis requires no unmeasured mediator-outcome confounding** ✓
  - Mediator-outcome confounding must be addressed for valid mediation analysis.

- **C) Baron and Kenny's approach accounts for exposure-mediator interactions** ✗
  - Traditional approaches like Baron and Kenny's don't accommodate exposure-mediator interactions.

- **E) The sum of direct and indirect effects always equals the total effect** ✗
  - With interactions or non-linearities, effects may not decompose additively.

### Question 14
**Correct answers: A, B, D**

- **A) E-values that quantify the minimum strength of unmeasured confounding needed to explain away an effect** ✓
  - E-values provide an interpretable metric for how strong unmeasured confounding would need to be.

- **B) Modeling the potential impact of unmeasured confounders on effect estimates** ✓
  - Incorporating hypothetical unmeasured confounders helps assess result robustness.

- **D) Bounding approaches that estimate worst-case scenarios under violations of assumptions** ✓
  - Bounds provide ranges of possible effects under various assumption violations.

- **C) Simply comparing results from different study populations** ✗
  - Population differences may reflect true effect heterogeneity rather than bias.

- **E) Increasing sample size to eliminate need for sensitivity analysis** ✗
  - Larger samples reduce random error but don't address systematic bias from assumption violations.

## Section 3: Machine Learning and Data Concepts

### Question 15
**Correct answers: A, B, D**

- **A) L1 regularization (Lasso) can produce sparse models by forcing some coefficients to zero** ✓
  - L1 penalty's mathematical properties enable feature selection by zeroing out less important features.

- **B) L2 regularization (Ridge) shrinks coefficients proportionally to their magnitude** ✓
  - L2 penalty reduces coefficient sizes while typically keeping all non-zero.

- **D) The optimal regularization strength typically increases as dataset size decreases** ✓
  - Smaller datasets benefit from stronger regularization to prevent overfitting.

- **C) Regularization always improves both training and test performance** ✗
  - Regularization typically reduces training performance while improving test performance.

- **E) Regularization only affects linear models, not complex models like neural networks** ✗
  - Regularization techniques (weight decay, dropout, etc.) are widely used in neural networks.

### Question 16
**Correct answers: A, B, D**

- **A) Creating polynomial features to capture non-linear relationships** ✓
  - Polynomial features enable linear models to learn non-linear patterns.

- **B) Implementing domain-specific transformations based on subject knowledge** ✓
  - Domain knowledge often suggests transformations that improve model performance.

- **D) Encoding cyclical features like time of day using sine and cosine transformations** ✓
  - Sine/cosine encoding preserves the cyclical nature of time features.

- **C) Always using all available features regardless of relevance** ✗
  - Irrelevant features can introduce noise and reduce model performance.

- **E) Standardizing all variables including binary indicators** ✗
  - Standardizing binary features is unnecessary and can complicate interpretation.

### Question 17
**Correct answers: A, B, D**

- **A) Silhouette coefficient to measure cluster cohesion and separation** ✓
  - Silhouette measures how similar objects are to their cluster compared to other clusters.

- **B) External validation using known class labels when available** ✓
  - When ground truth is available, metrics like ARI or NMI can validate clustering quality.

- **D) Stability analysis by rerunning clustering on data subsets** ✓
  - Stable clustering results across data subsets indicate robustness.

- **C) Visual inspection as the sole validation criterion** ✗
  - While visualization helps, objective metrics are needed for reliable validation.

- **E) Always selecting the solution with the most clusters** ✗
  - More clusters aren't always better; optimal cluster count depends on data structure.

### Question 18
**Correct answers: A, B, C**

- **A) SHAP values to quantify feature contributions to individual predictions** ✓
  - SHAP values provide theoretically sound attribution of prediction contributions to features.

- **B) Partial dependence plots to visualize relationships between features and predictions** ✓
  - PDPs show how predictions change as a feature varies, holding others constant.

- **C) Local interpretable model-agnostic explanations (LIME)** ✓
  - LIME explains individual predictions by approximating the model locally.

- **D) Focusing solely on global model accuracy rather than interpretability** ✗
  - Interpretability is crucial for trust, debugging, and deployment in many contexts.

- **E) Using only model coefficients regardless of model type** ✗
  - Coefficients are meaningful for linear models but insufficient for complex non-linear models.

### Question 19
**Correct answers: A, B, D**

- **A) Testing for and addressing seasonality in the data** ✓
  - Identifying and modeling seasonal patterns improves forecast accuracy.

- **B) Using rolling-window cross-validation for model selection** ✓
  - Rolling window CV respects temporal order and simulates real forecasting scenarios.

- **D) Combining multiple forecasting methods in ensemble approaches** ✓
  - Ensemble forecasts often outperform individual methods by leveraging diverse strengths.

- **C) Applying standard random cross-validation without accounting for time** ✗
  - Random CV causes data leakage in time series by using future data to predict past values.

- **E) Always differencing time series data regardless of stationarity tests** ✗
  - Differencing should be applied based on stationarity tests; unnecessary differencing can harm performance.

### Question 20
**Correct answers: A, C, D**

- **A) Synthetic minority oversampling (SMOTE) creates new minority class examples** ✓
  - SMOTE generates synthetic examples in feature space, balancing classes without simple duplication.

- **C) Cost-sensitive learning assigns higher penalties to minority class misclassifications** ✓
  - Cost-sensitive approaches adjust the learning objective to prioritize minority class accuracy.

- **D) Class weights can help models adjust decision boundaries appropriately** ✓
  - Weighting classes inversely to their frequency helps balance class importance during training.

- **B) Performance metrics like accuracy are usually sufficient for imbalanced datasets** ✗
  - Accuracy is misleading for imbalanced data; precision, recall, and F1 provide better assessment.

- **E) Anomaly detection problems typically have balanced class distributions** ✗
  - Anomaly detection is inherently imbalanced, with anomalies being rare by definition.