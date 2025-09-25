# Data Science and AI Practice Exam #5 (100 Points)

## Instructions
- Each question is worth 5 points
- Select all correct answers for each question
- There may be multiple correct answers per question
- A detailed answer key is provided at the end of the exam

## Section 1: Generative AI and Deep Learning (35 points)

### Question 1
Which statements about the training process of large language models are correct?
- [x] A) Pre-training typically uses self-supervised learning objectives
- [ ] B) Fine-tuning requires more computational resources than pre-training
- [x] C) Training data quality significantly impacts model capabilities and biases
- [x] D) Curriculum learning can improve efficiency by organizing training examples
- [ ] E) Models are typically trained on a fixed set of predefined tasks

### Question 2
What are valid approaches for reducing hallucinations in generative AI systems?
- [x] A) Citing sources within model generations
- [x] B) Grounding responses in external knowledge bases
- [ ] C) Generating longer responses to include all possible information
- [x] D) Training on datasets that reward accuracy and penalize fabrications
- [ ] E) Focusing exclusively on creative tasks rather than factual ones

### Question 3
Which techniques effectively address context length limitations in transformer models?
- [x] A) Sliding window attention patterns
- [x] B) Hierarchical summarization of earlier context
- [x] C) Memory-efficient attention mechanisms
- [ ] D) Simply increasing model parameters proportionally to context length
- [ ] E) Converting all long-form inputs to short summaries before processing

### Question 4
What capabilities distinguish multimodal generative AI models from text-only models?
- [x] A) Understanding visual concepts and their relationships
- [x] B) Generating text conditioned on image inputs
- [ ] C) Fundamentally different neural architecture from text models
- [x] D) Connecting vision and language representations in shared embedding space
- [ ] E) Eliminating the need for language understanding entirely

### Question 5
Which model alignment techniques help ensure that generative AI systems behave according to human preferences?
- [x] A) Reinforcement Learning from Human Feedback (RLHF)
- [x] B) Direct Preference Optimization
- [ ] C) Maximizing prediction accuracy on next-token prediction
- [x] D) Constitutional AI with critical self-revision
- [ ] E) Increasing model size without specific alignment techniques

### Question 6
Which techniques enable efficient fine-tuning of large language models?
- [x] A) Low-Rank Adaptation (LoRA) that updates a small number of parameters
- [x] B) Adapter modules inserted between transformer layers
- [ ] C) Always retraining all parameters regardless of dataset size
- [x] D) Quantized training to reduce memory requirements
- [ ] E) Using aggressive learning rates to speed up convergence

### Question 7
In the context of generative AI deployment, which approaches help mitigate potential harms?
- [x] A) Systematic red-teaming to identify vulnerabilities
- [ ] B) Releasing model capabilities without safety evaluations to enable faster innovation
- [x] C) Implementing content filtering systems based on harmful categories
- [x] D) Iterative deployment with monitoring and feedback loops
- [ ] E) Restricting access to all applications regardless of risk level

## Section 2: Causal Inference (35 points)

### Question 8
Which research designs allow for valid causal inference in the presence of unmeasured confounding?
- [x] A) Regression discontinuity designs with a clear cutoff rule
- [x] B) Instrumental variable designs with valid instruments
- [ ] C) Simple cross-sectional observational studies
- [x] D) Difference-in-differences designs with parallel trends
- [ ] E) Case-control studies without adjustment

### Question 9
Which statements about the backdoor criterion in causal inference are correct?
- [x] A) It identifies sufficient adjustment sets to block all backdoor paths
- [x] B) It requires a causal graph as input
- [ ] C) It guarantees identification even with unmeasured confounders
- [x] D) Minimal sufficient adjustment sets may exclude some measured confounders
- [ ] E) It applies only to randomized experiments

### Question 10
What assumptions are necessary for valid application of propensity score methods?
- [x] A) No unmeasured confounding (conditional exchangeability)
- [x] B) Positivity (non-zero probability of each treatment for all covariate patterns)
- [x] C) Consistency (well-defined interventions)
- [ ] D) Homogeneous treatment effects across all subgroups
- [ ] E) Normally distributed outcomes

### Question 11
Which methodological challenges specifically affect causal inference with longitudinal data?
- [x] A) Time-varying confounding affected by previous treatment
- [x] B) Selection bias from informative loss to follow-up
- [ ] C) Inability to estimate lagged effects
- [x] D) Treatment-confounder feedback loops
- [ ] E) Requirement for perfectly balanced repeated measures

### Question 12
In the context of causal mediation analysis, which statements are correct?
- [x] A) The product method requires no exposure-mediator interaction
- [ ] B) The controlled direct effect equals the natural direct effect in all cases
- [x] C) Multiple mediators can be analyzed simultaneously using appropriate methods
- [x] D) Sensitivity analysis can assess robustness to violations of the no unmeasured mediator-outcome confounding assumption
- [ ] E) Mediation analysis always requires randomized assignment of both exposure and mediator

### Question 13
Which statements about effect modification and interaction are correct?
- [x] A) Effect modification refers to variation in the causal effect across strata of another variable
- [ ] B) Effect modification and interaction are interchangeable concepts
- [x] C) Additive interaction means the joint effect deviates from the sum of individual effects
- [x] D) Multiplicative interaction means the joint effect deviates from the product of individual effects
- [ ] E) Effect modification requires that the modifier be a cause of the outcome

### Question 14
What approaches can address violations of the positivity assumption in causal inference?
- [x] A) Trimming the population to regions of common support
- [x] B) Stabilized weights in inverse probability weighting
- [ ] C) Ignoring areas of limited overlap between treatment groups
- [x] D) Transportability methods to extrapolate from areas with sufficient data
- [ ] E) Simply assuming positivity holds regardless of data patterns

## Section 3: Machine Learning and Data Concepts (30 points)

### Question 15
Which statements about model evaluation metrics are correct?
- [x] A) The area under the ROC curve (AUC) measures discrimination ability
- [ ] B) Accuracy is always the most appropriate metric regardless of class distribution
- [x] C) Log loss provides a continuous penalty based on prediction confidence
- [x] D) Precision and recall have different trade-offs depending on the application context
- [ ] E) All evaluation metrics require known ground truth for all test examples

### Question 16
For feature selection in machine learning, which approaches are methodologically sound?
- [x] A) Forward selection that iteratively adds the most valuable features
- [x] B) Recursive feature elimination that removes the least important features
- [ ] C) Selecting features based solely on univariate correlation with the target
- [x] D) L1 regularization (Lasso) to encourage sparse feature selection
- [ ] E) Always using domain expertise instead of data-driven approaches

### Question 17
Which statements about ensemble methods in machine learning are correct?
- [x] A) Bagging reduces variance by training models on bootstrap samples
- [x] B) Boosting reduces bias by focusing on misclassified examples
- [ ] C) Random Forests always outperform single decision trees regardless of data characteristics
- [x] D) Stacking combines multiple models by training a meta-learner on their predictions
- [ ] E) Ensemble methods always increase model complexity without improving performance

### Question 18
In the context of unsupervised learning, which statements are valid?
- [x] A) DBSCAN can identify clusters of arbitrary shapes
- [ ] B) K-means always finds the optimal global clustering solution
- [x] C) Hierarchical clustering provides a dendrogram showing nested cluster relationships
- [x] D) Dimensionality reduction techniques can improve clustering by removing noise
- [ ] E) Unsupervised learning always requires a predefined number of clusters

### Question 19
Which approaches effectively address catastrophic forgetting in continual learning?
- [x] A) Elastic weight consolidation that penalizes changes to important parameters
- [x] B) Experience replay that revisits examples from previous tasks
- [ ] C) Simply increasing model size for each new task
- [x] D) Parameter regularization based on task-specific importance
- [ ] E) Training exclusively on the newest data

### Question 20
Which statements about responsible machine learning practices are correct?
- [x] A) Data collection and annotation should consider potential biases
- [x] B) Models should be evaluated for performance across different demographic groups
- [ ] C) Tradeoffs between accuracy and fairness are irrelevant in practical applications
- [x] D) Documentation should include model limitations and intended use cases
- [ ] E) Ethical considerations only apply to specific domains like healthcare

---

# Answer Key with Detailed Explanations

## Section 1: Generative AI and Deep Learning

### Question 1
**Correct answers: A, C, D**

- **A) Pre-training typically uses self-supervised learning objectives** ✓
  - Pre-training commonly employs self-supervised objectives like masked language modeling or next-token prediction, generating supervision signals from the data itself without human labels.

- **C) Training data quality significantly impacts model capabilities and biases** ✓
  - The composition, diversity, and quality of training data directly influence what the model learns, including both capabilities and limitations or biases.

- **D) Curriculum learning can improve efficiency by organizing training examples** ✓
  - Presenting training examples in order of increasing difficulty can accelerate learning and lead to better generalization.

- **B) Fine-tuning requires more computational resources than pre-training** ✗
  - Fine-tuning is typically far less computationally intensive than pre-training, as it starts from pre-trained weights and requires fewer steps on smaller datasets.

- **E) Models are typically trained on a fixed set of predefined tasks** ✗
  - Modern LLMs are often trained using general objectives rather than predefined tasks, allowing them to learn a broad range of capabilities.

### Question 2
**Correct answers: A, B, D**

- **A) Citing sources within model generations** ✓
  - Source citation enables verification and helps models distinguish between known facts and uncertain information.

- **B) Grounding responses in external knowledge bases** ✓
  - External knowledge retrieval (as in RAG systems) provides factual grounding for responses.

- **D) Training on datasets that reward accuracy and penalize fabrications** ✓
  - Training signals that specifically discourage hallucination and reward factual accuracy help reduce false information.

- **C) Generating longer responses to include all possible information** ✗
  - Verbose responses often increase hallucination by encouraging the model to continue generating beyond what it knows with confidence.

- **E) Focusing exclusively on creative tasks rather than factual ones** ✗
  - Avoiding factual tasks doesn't solve hallucination and severely limits model utility.

### Question 3
**Correct answers: A, B, C**

- **A) Sliding window attention patterns** ✓
  - Sliding window approaches limit attention to local regions, reducing computational complexity from quadratic to linear.

- **B) Hierarchical summarization of earlier context** ✓
  - Compressing earlier context through summarization allows models to maintain important information over long sequences.

- **C) Memory-efficient attention mechanisms** ✓
  - Techniques like FlashAttention optimize memory usage during attention computation, enabling longer contexts.

- **D) Simply increasing model parameters proportionally to context length** ✗
  - Parameter count and context length aren't directly related; attention complexity remains a constraint regardless of parameter count.

- **E) Converting all long-form inputs to short summaries before processing** ✗
  - This would lose critical information; the challenge is maintaining detail while handling long contexts.

### Question 4
**Correct answers: A, B, D**

- **A) Understanding visual concepts and their relationships** ✓
  - Multimodal models can recognize and reason about visual elements and their relationships.

- **B) Generating text conditioned on image inputs** ✓
  - These models can describe, answer questions about, and reason based on visual inputs.

- **D) Connecting vision and language representations in shared embedding space** ✓
  - Multimodal models align visual and textual representations to enable cross-modal understanding.

- **C) Fundamentally different neural architecture from text models** ✗
  - Many multimodal models use similar transformer architectures with added vision encoders rather than completely different architectures.

- **E) Eliminating the need for language understanding entirely** ✗
  - Multimodal models enhance language understanding with visual context rather than replacing it.

### Question 5
**Correct answers: A, B, D**

- **A) Reinforcement Learning from Human Feedback (RLHF)** ✓
  - RLHF uses human preferences to train a reward model that guides policy optimization.

- **B) Direct Preference Optimization** ✓
  - DPO directly optimizes models to follow human preferences without an explicit reward model.

- **D) Constitutional AI with critical self-revision** ✓
  - Constitutional AI uses model-generated critiques and revisions guided by principles to improve outputs.

- **C) Maximizing prediction accuracy on next-token prediction** ✗
  - Standard language modeling objectives don't specifically align with human preferences or values.

- **E) Increasing model size without specific alignment techniques** ✗
  - Scale alone doesn't ensure alignment with human preferences.

### Question 6
**Correct answers: A, B, D**

- **A) Low-Rank Adaptation (LoRA) that updates a small number of parameters** ✓
  - LoRA inserts trainable low-rank matrices that adapt model behavior with minimal parameter updates.

- **B) Adapter modules inserted between transformer layers** ✓
  - Adapter modules add small trainable components while keeping most of the model frozen.

- **D) Quantized training to reduce memory requirements** ✓
  - Quantization reduces the precision of model weights, decreasing memory usage during training.

- **C) Always retraining all parameters regardless of dataset size** ✗
  - Full fine-tuning is inefficient for small datasets and can lead to catastrophic forgetting or overfitting.

- **E) Using aggressive learning rates to speed up convergence** ✗
  - High learning rates typically cause training instability rather than efficient convergence.

### Question 7
**Correct answers: A, C, D**

- **A) Systematic red-teaming to identify vulnerabilities** ✓
  - Red-teaming involves targeted testing to discover and address potential harmful outputs before deployment.

- **C) Implementing content filtering systems based on harmful categories** ✓
  - Content filters provide guardrails against generating harmful content across various categories.

- **D) Iterative deployment with monitoring and feedback loops** ✓
  - Continuous monitoring and improvement help catch and address issues that emerge during real-world use.

- **B) Releasing model capabilities without safety evaluations to enable faster innovation** ✗
  - Skipping safety evaluations increases risk of harm; responsible innovation includes safety assessment.

- **E) Restricting access to all applications regardless of risk level** ✗
  - Risk-appropriate access policies are more effective than blanket restrictions.

## Section 2: Causal Inference

### Question 8
**Correct answers: A, B, D**

- **A) Regression discontinuity designs with a clear cutoff rule** ✓
  - RD designs exploit quasi-random assignment around thresholds to identify causal effects despite unmeasured confounding.

- **B) Instrumental variable designs with valid instruments** ✓
  - Valid instruments provide a source of variation in treatment unrelated to unmeasured confounders.

- **D) Difference-in-differences designs with parallel trends** ✓
  - DiD controls for time-invariant unmeasured confounding by comparing changes over time between groups.

- **C) Simple cross-sectional observational studies** ✗
  - Without additional design elements, cross-sectional studies cannot address unmeasured confounding.

- **E) Case-control studies without adjustment** ✗
  - Case-control studies require adjustment for confounders and are susceptible to unmeasured confounding.

### Question 9
**Correct answers: A, B, D**

- **A) It identifies sufficient adjustment sets to block all backdoor paths** ✓
  - The backdoor criterion identifies variable sets that block all non-causal paths between treatment and outcome.

- **B) It requires a causal graph as input** ✓
  - Applying the backdoor criterion requires specifying the causal relationships through a DAG.

- **D) Minimal sufficient adjustment sets may exclude some measured confounders** ✓
  - Some measured confounders may be redundant if other variables already block all backdoor paths.

- **C) It guarantees identification even with unmeasured confounders** ✗
  - The backdoor criterion cannot overcome unmeasured confounding on backdoor paths.

- **E) It applies only to randomized experiments** ✗
  - The backdoor criterion is specifically designed for observational studies; randomized experiments already achieve exchangeability.

### Question 10
**Correct answers: A, B, C**

- **A) No unmeasured confounding (conditional exchangeability)** ✓
  - Propensity score methods require that all confounders are measured and included in the propensity model.

- **B) Positivity (non-zero probability of each treatment for all covariate patterns)** ✓
  - All units must have a non-zero probability of receiving each treatment level.

- **C) Consistency (well-defined interventions)** ✓
  - Treatment must be well-defined with no hidden variations that affect outcomes.

- **D) Homogeneous treatment effects across all subgroups** ✗
  - Propensity score methods allow for heterogeneous treatment effects.

- **E) Normally distributed outcomes** ✗
  - Propensity score methods don't require normally distributed outcomes.

### Question 11
**Correct answers: A, B, D**

- **A) Time-varying confounding affected by previous treatment** ✓
  - When prior treatment affects subsequent confounders, standard regression fails.

- **B) Selection bias from informative loss to follow-up** ✓
  - Differential attrition related to treatment or outcomes can bias causal estimates.

- **D) Treatment-confounder feedback loops** ✓
  - Bidirectional relationships between treatment and confounders over time create complex causal structures.

- **C) Inability to estimate lagged effects** ✗
  - Longitudinal data actually enables estimation of lagged effects through appropriate modeling.

- **E) Requirement for perfectly balanced repeated measures** ✗
  - Methods exist to handle unbalanced measurement schedules in longitudinal data.

### Question 12
**Correct answers: A, C, D**

- **A) The product method requires no exposure-mediator interaction** ✓
  - The traditional product method assumes no interaction between exposure and mediator.

- **C) Multiple mediators can be analyzed simultaneously using appropriate methods** ✓
  - Methods exist for analyzing multiple mediators, though assumptions become more complex.

- **D) Sensitivity analysis can assess robustness to violations of the no unmeasured mediator-outcome confounding assumption** ✓
  - Sensitivity analysis helps quantify how unmeasured mediator-outcome confounding might affect conclusions.

- **B) The controlled direct effect equals the natural direct effect in all cases** ✗
  - These effects differ when there is exposure-mediator interaction.

- **E) Mediation analysis always requires randomized assignment of both exposure and mediator** ✗
  - While ideal, mediation analysis can be conducted with observational data under appropriate assumptions.

### Question 13
**Correct answers: A, C, D**

- **A) Effect modification refers to variation in the causal effect across strata of another variable** ✓
  - Effect modification describes how the effect of a treatment varies across subgroups.

- **C) Additive interaction means the joint effect deviates from the sum of individual effects** ✓
  - Additive interaction occurs when the combined effect differs from the sum of separate effects.

- **D) Multiplicative interaction means the joint effect deviates from the product of individual effects** ✓
  - Multiplicative interaction occurs when the combined effect differs from the product of separate effects.

- **B) Effect modification and interaction are interchangeable concepts** ✗
  - Effect modification refers to variation across strata; interaction refers to joint effects of two exposures.

- **E) Effect modification requires that the modifier be a cause of the outcome** ✗
  - Effect modifiers need not cause the outcome; they simply stratify the population into groups with different treatment effects.

### Question 14
**Correct answers: A, B, D**

- **A) Trimming the population to regions of common support** ✓
  - Restricting analysis to regions where treatments overlap improves validity but limits generalizability.

- **B) Stabilized weights in inverse probability weighting** ✓
  - Stabilized weights reduce extreme values that arise from near-violations of positivity.

- **D) Transportability methods to extrapolate from areas with sufficient data** ✓
  - Transportability frameworks can extend inferences to regions with limited positivity under certain assumptions.

- **C) Ignoring areas of limited overlap between treatment groups** ✗
  - Ignoring positivity violations without addressing them leads to biased estimates.

- **E) Simply assuming positivity holds regardless of data patterns** ✗
  - Assuming positivity without checking can lead to severely biased estimates.

## Section 3: Machine Learning and Data Concepts

### Question 15
**Correct answers: A, C, D**

- **A) The area under the ROC curve (AUC) measures discrimination ability** ✓
  - AUC quantifies how well a model ranks positive instances above negative ones across thresholds.

- **C) Log loss provides a continuous penalty based on prediction confidence** ✓
  - Log loss increasingly penalizes confident incorrect predictions, providing gradient information.

- **D) Precision and recall have different trade-offs depending on the application context** ✓
  - Different applications prioritize minimizing false positives versus false negatives differently.

- **B) Accuracy is always the most appropriate metric regardless of class distribution** ✗
  - For imbalanced data, accuracy can be misleading by rewarding majority class predictions.

- **E) All evaluation metrics require known ground truth for all test examples** ✗
  - Some metrics like coherence or diversity can evaluate generation quality without ground truth.

### Question 16
**Correct answers: A, B, D**

- **A) Forward selection that iteratively adds the most valuable features** ✓
  - Forward selection builds a feature set by sequentially adding the most beneficial features.

- **B) Recursive feature elimination that removes the least important features** ✓
  - RFE iteratively removes features with the smallest impact on model performance.

- **D) L1 regularization (Lasso) to encourage sparse feature selection** ✓
  - Lasso naturally performs feature selection by shrinking less important coefficients to zero.

- **C) Selecting features based solely on univariate correlation with the target** ✗
  - Univariate selection ignores feature interactions and can miss important multivariate relationships.

- **E) Always using domain expertise instead of data-driven approaches** ✗
  - Both domain expertise and data-driven methods have value; combining them typically works best.

### Question 17
**Correct answers: A, B, D**

- **A) Bagging reduces variance by training models on bootstrap samples** ✓
  - Bagging creates diverse models through sampling with replacement, reducing overfitting.

- **B) Boosting reduces bias by focusing on misclassified examples** ✓
  - Boosting sequentially builds models that correct errors made by previous models.

- **D) Stacking combines multiple models by training a meta-learner on their predictions** ✓
  - Stacking uses model predictions as features for a higher-level model that learns optimal combinations.

- **C) Random Forests always outperform single decision trees regardless of data characteristics** ✗
  - While often better, Random Forests may underperform for very simple relationships or very small datasets.

- **E) Ensemble methods always increase model complexity without improving performance** ✗
  - Ensembles typically improve performance, especially on complex tasks or noisy data.

### Question 18
**Correct answers: A, C, D**

- **A) DBSCAN can identify clusters of arbitrary shapes** ✓
  - DBSCAN defines clusters based on density, allowing it to find irregularly shaped clusters.

- **C) Hierarchical clustering provides a dendrogram showing nested cluster relationships** ✓
  - Dendrograms visualize how clusters merge or split at different similarity thresholds.

- **D) Dimensionality reduction techniques can improve clustering by removing noise** ✓
  - Reducing dimensions can eliminate noise and highlight structure that improves clustering quality.

- **B) K-means always finds the optimal global clustering solution** ✗
  - K-means can converge to local optima depending on initial centroids.

- **E) Unsupervised learning always requires a predefined number of clusters** ✗
  - Some algorithms like DBSCAN or hierarchical clustering don't require specifying cluster count in advance.

### Question 19
**Correct answers: A, B, D**

- **A) Elastic weight consolidation that penalizes changes to important parameters** ✓
  - EWC adds regularization terms that preserve parameters critical for previous tasks.

- **B) Experience replay that revisits examples from previous tasks** ✓
  - Replaying past examples prevents forgetting by maintaining representation of earlier tasks.

- **D) Parameter regularization based on task-specific importance** ✓
  - Techniques that penalize changes to parameters based on their importance for specific tasks reduce forgetting.

- **C) Simply increasing model size for each new task** ✗
  - While capacity helps, simply increasing size without specific mechanisms doesn't prevent forgetting.

- **E) Training exclusively on the newest data** ✗
  - This approach maximizes catastrophic forgetting rather than preventing it.

### Question 20
**Correct answers: A, B, D**

- **A) Data collection and annotation should consider potential biases** ✓
  - Representative data collection and careful annotation are fundamental to mitigating algorithmic bias.

- **B) Models should be evaluated for performance across different demographic groups** ✓
  - Disaggregated evaluation helps identify disparate performance that might harm certain groups.

- **D) Documentation should include model limitations and intended use cases** ✓
  - Transparent documentation enables responsible deployment by communicating capabilities and constraints.

- **C) Tradeoffs between accuracy and fairness are irrelevant in practical applications** ✗
  - These tradeoffs are central to responsible ML and require explicit consideration in practice.

- **E) Ethical considerations only apply to specific domains like healthcare** ✗
  - Ethical considerations apply across all domains where ML affects people's lives and opportunities.