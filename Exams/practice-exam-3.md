# Data Science and AI Practice Exam #3 (100 Points)

## Instructions
- Each question is worth 5 points
- Select all correct answers for each question
- There may be multiple correct answers per question
- A detailed answer key is provided at the end of the exam

## Section 1: Generative AI and Deep Learning (35 points)

### Question 1
Which statements about self-attention mechanisms in transformer models are correct?
- [x] A) Each token can attend to all other tokens in the sequence
- [x] B) Attention weights sum to 1 for each token
- [ ] C) Computation time scales linearly with sequence length
- [x] D) The query, key, and value matrices are learned parameters
- [ ] E) Self-attention requires fixed-size inputs to function properly

### Question 2
What are valid training strategies to improve generative AI model performance?
- [x] A) Reinforcement Learning from Human Feedback (RLHF)
- [x] B) Instruction tuning on diverse tasks
- [ ] C) Training on the largest possible dataset regardless of quality
- [x] D) Constitutional AI approaches that incorporate model self-critique
- [ ] E) Minimizing pre-training time by using only task-specific data

### Question 3
Which limitations apply to current large language models?
- [x] A) Difficulty with complex mathematical reasoning
- [ ] B) Complete inability to follow multi-step instructions
- [x] C) Challenges maintaining factual accuracy for specialized knowledge
- [x] D) Limited temporal understanding of recent events
- [ ] E) Inability to generate creative content

### Question 4
In the context of LLM evaluation, which methods effectively assess reasoning capabilities?
- [x] A) Multi-step problem-solving benchmarks
- [x] B) Chain-of-thought evaluation protocols
- [ ] C) Simple perplexity measurements on standard corpora
- [x] D) Adversarial reasoning challenges
- [ ] E) Token prediction speed on benchmark tasks

### Question 5
Which statements about prompt engineering for generative AI are correct?
- [x] A) Well-structured prompts can elicit better reasoning from models
- [ ] B) Prompt engineering effects disappear entirely in the most advanced models
- [x] C) Few-shot examples can guide model responses effectively
- [x] D) System prompts help establish model personas and constraints
- [ ] E) The exact wording of prompts has minimal impact on output quality

### Question 6
What are valid approaches to mitigate hallucinations in language models?
- [x] A) Retrieving information from trusted knowledge bases
- [x] B) Training models to express uncertainty when appropriate
- [ ] C) Increasing temperature settings during generation
- [x] D) Fine-tuning on datasets that reward accuracy
- [ ] E) Generating shorter responses for all queries

### Question 7
Which statements accurately describe techniques for improving efficiency in transformer models?
- [x] A) Sparse attention patterns that focus on relevant tokens
- [x] B) Knowledge distillation from larger to smaller models
- [x] C) Parameter-efficient fine-tuning methods like LoRA
- [ ] D) Increasing model depth rather than width
- [ ] E) Using larger batch sizes without optimization adjustments

## Section 2: Causal Inference (35 points)

### Question 8
Which conditions are required for valid causal inference in observational studies?
- [x] A) No unmeasured confounding between treatment and outcome
- [x] B) Positivity (non-zero probability of each treatment for all covariate patterns)
- [x] C) Consistency (well-defined interventions)
- [ ] D) Homogeneous treatment effects across all subpopulations
- [ ] E) Complete absence of measurement error

### Question 9
Which methods can help address unmeasured confounding in causal inference?
- [x] A) Instrumental variable analysis
- [x] B) Difference-in-differences designs
- [ ] C) Simple multivariate regression
- [x] D) Sensitivity analysis for unmeasured confounders
- [ ] E) Increasing sample size without addressing confounding

### Question 10
In the context of mediation analysis, which statements are correct?
- [x] A) Direct effects measure the impact of treatment not through the mediator
- [x] B) Indirect effects capture the treatment effect that operates through the mediator
- [ ] C) Mediation analysis requires no additional assumptions beyond those for total effects
- [x] D) Counterfactual definitions allow for decomposition of total effects
- [ ] E) Mediation analysis cannot be represented in causal diagrams

### Question 11
Which scenarios present threats to internal validity in causal inference studies?
- [x] A) Differential attrition between treatment groups
- [ ] B) Limited generalizability to other populations
- [x] C) Measurement error correlated with treatment assignment
- [x] D) Spillover effects between treatment and control units
- [ ] E) Small sample size with adequate randomization

### Question 12
When working with causal diagrams (DAGs), which operations are valid?
- [x] A) Determining minimally sufficient adjustment sets
- [x] B) Identifying instrumental variables
- [x] C) Testing for conditional independence implications
- [ ] D) Quantifying the magnitude of causal effects
- [ ] E) Proving causation from observational data without assumptions

### Question 13
Which statements about propensity score methods are correct?
- [x] A) They estimate the probability of treatment given observed covariates
- [x] B) They can be used for matching, stratification, or weighting
- [ ] C) They eliminate the need for the positivity assumption
- [x] D) They help balance covariates between treatment groups
- [ ] E) They adjust for unmeasured confounders by design

### Question 14
Which principles apply to causal effect heterogeneity analysis?
- [x] A) Effect modification can occur without interaction
- [ ] B) Subgroup analyses require no multiple testing adjustment
- [x] C) Pre-specification of effect modifiers reduces false positives
- [x] D) Additive interaction may exist without multiplicative interaction
- [ ] E) Post-hoc subgroup analyses have the same validity as pre-specified ones

## Section 3: Machine Learning and Data Concepts (30 points)

### Question 15
Which techniques are appropriate for handling multicollinearity in regression models?
- [x] A) Principal Component Regression
- [x] B) Ridge Regression
- [ ] C) Increasing model complexity
- [x] D) Feature selection to remove redundant predictors
- [ ] E) Ignoring correlation structure entirely

### Question 16
For time series data analysis, which approaches are valid?
- [x] A) Testing for stationarity before modeling
- [x] B) Using autocorrelation functions to identify temporal patterns
- [ ] C) Applying standard cross-validation without time considerations
- [x] D) Implementing seasonality decomposition
- [ ] E) Ignoring temporal ordering when splitting training and test sets

### Question 17
Which statements about ensemble methods in machine learning are correct?
- [x] A) Random Forests combine multiple decision trees to reduce variance
- [x] B) Boosting methods build sequential models that correct previous errors
- [ ] C) Ensembles always increase model interpretability
- [x] D) Bagging uses bootstrap sampling to create diversity in base learners
- [ ] E) Ensemble methods always perform better than single models regardless of data quality

### Question 18
For model validation in machine learning, which practices are recommended?
- [x] A) Time-based splitting for temporal data
- [x] B) K-fold cross-validation for limited datasets
- [x] C) Holdout validation sets for final model assessment
- [ ] D) Validating only on the most recent data points
- [ ] E) Using the same data for feature selection and model validation

### Question 19
In the context of data visualization, which principles support effective communication?
- [x] A) Aligning visualization type with the specific analytical question
- [x] B) Using color intentionally to highlight patterns or categories
- [ ] C) Maximizing the number of variables displayed in a single visualization
- [x] D) Providing clear context and labels for proper interpretation
- [ ] E) Prioritizing aesthetic appeal over information clarity

### Question 20
When addressing class imbalance in classification problems, which approaches are effective?
- [x] A) Oversampling the minority class
- [x] B) Undersampling the majority class
- [x] C) Using class-weighted loss functions
- [ ] D) Focusing exclusively on accuracy as the performance metric
- [ ] E) Always choosing the majority class for maximum performance

---

# Answer Key with Detailed Explanations

## Section 1: Generative AI and Deep Learning

### Question 1
**Correct answers: A, B, D**

- **A) Each token can attend to all other tokens in the sequence** ✓
  - Standard self-attention allows each token to attend to all other tokens in the sequence, enabling global context awareness.

- **B) Attention weights sum to 1 for each token** ✓
  - Attention weights are normalized using softmax, ensuring they sum to 1 for each token, creating a probability distribution over other tokens.

- **D) The query, key, and value matrices are learned parameters** ✓
  - These projection matrices are learned during training and transform input embeddings into query, key, and value representations.

- **C) Computation time scales linearly with sequence length** ✗
  - Self-attention computation scales quadratically with sequence length (O(n²)), which creates challenges for very long sequences.

- **E) Self-attention requires fixed-size inputs to function properly** ✗
  - Self-attention can handle variable-length inputs, which is one of its key advantages.

### Question 2
**Correct answers: A, B, D**

- **A) Reinforcement Learning from Human Feedback (RLHF)** ✓
  - RLHF aligns model outputs with human preferences through reinforcement learning from human evaluations.

- **B) Instruction tuning on diverse tasks** ✓
  - Training on diverse instruction-following examples improves model capability to understand and follow user requests.

- **D) Constitutional AI approaches that incorporate model self-critique** ✓
  - Constitutional AI uses self-critique and revision to improve outputs based on predefined principles.

- **C) Training on the largest possible dataset regardless of quality** ✗
  - Data quality is crucial; low-quality data can introduce errors and biases regardless of size.

- **E) Minimizing pre-training time by using only task-specific data** ✗
  - Pre-training on broad data is essential for developing general capabilities before task-specific adaptation.

### Question 3
**Correct answers: A, C, D**

- **A) Difficulty with complex mathematical reasoning** ✓
  - Current LLMs still struggle with multi-step mathematical reasoning and problem-solving.

- **C) Challenges maintaining factual accuracy for specialized knowledge** ✓
  - Models often make factual errors in specialized domains where training data may be limited.

- **D) Limited temporal understanding of recent events** ✓
  - Models have knowledge cutoffs and cannot reliably comment on events after their training data.

- **B) Complete inability to follow multi-step instructions** ✗
  - Modern LLMs can follow multi-step instructions reasonably well, though performance varies.

- **E) Inability to generate creative content** ✗
  - LLMs are capable of generating various forms of creative content like stories, poems, and art prompts.

### Question 4
**Correct answers: A, B, D**

- **A) Multi-step problem-solving benchmarks** ✓
  - Problems requiring sequential reasoning steps effectively test a model's reasoning capabilities.

- **B) Chain-of-thought evaluation protocols** ✓
  - Evaluating intermediate reasoning steps provides insight into a model's thought process.

- **D) Adversarial reasoning challenges** ✓
  - Challenging problems designed to test reasoning limitations reveal model capabilities and weaknesses.

- **C) Simple perplexity measurements on standard corpora** ✗
  - Perplexity measures language modeling quality but doesn't specifically assess reasoning.

- **E) Token prediction speed on benchmark tasks** ✗
  - Generation speed is unrelated to reasoning quality.

### Question 5
**Correct answers: A, C, D**

- **A) Well-structured prompts can elicit better reasoning from models** ✓
  - Prompt structure significantly affects a model's reasoning and response quality.

- **C) Few-shot examples can guide model responses effectively** ✓
  - Including examples in prompts helps models understand the expected format and reasoning approach.

- **D) System prompts help establish model personas and constraints** ✓
  - System prompts define the model's role, behavior, and limitations in a conversation.

- **B) Prompt engineering effects disappear entirely in the most advanced models** ✗
  - Even the most advanced models benefit from well-engineered prompts.

- **E) The exact wording of prompts has minimal impact on output quality** ✗
  - Specific wording choices can significantly affect response quality and approach.

### Question 6
**Correct answers: A, B, D**

- **A) Retrieving information from trusted knowledge bases** ✓
  - RAG systems ground responses in factual information from reliable sources.

- **B) Training models to express uncertainty when appropriate** ✓
  - Teaching models to acknowledge uncertainty reduces confidently stated inaccuracies.

- **D) Fine-tuning on datasets that reward accuracy** ✓
  - Training models to prioritize factual correctness improves accuracy.

- **C) Increasing temperature settings during generation** ✗
  - Higher temperature increases randomness and can actually increase hallucinations.

- **E) Generating shorter responses for all queries** ✗
  - Response length doesn't directly correlate with factual accuracy.

### Question 7
**Correct answers: A, B, C**

- **A) Sparse attention patterns that focus on relevant tokens** ✓
  - Patterns like local, dilated, or clustered attention reduce computation while preserving performance.

- **B) Knowledge distillation from larger to smaller models** ✓
  - Transferring knowledge from large teacher models to smaller student models maintains capability with lower compute.

- **C) Parameter-efficient fine-tuning methods like LoRA** ✓
  - Techniques that update only a small subset of parameters reduce memory and computation requirements.

- **D) Increasing model depth rather than width** ✗
  - Deeper models typically require more computation, not less.

- **E) Using larger batch sizes without optimization adjustments** ✗
  - Larger batches without proper optimization can lead to training instability and memory issues.

## Section 2: Causal Inference

### Question 8
**Correct answers: A, B, C**

- **A) No unmeasured confounding between treatment and outcome** ✓
  - This is the exchangeability or "no unobserved confounding" assumption, fundamental for causal inference.

- **B) Positivity (non-zero probability of each treatment for all covariate patterns)** ✓
  - Positivity ensures that causal effects can be estimated for all relevant subpopulations.

- **C) Consistency (well-defined interventions)** ✓
  - Consistency links observed outcomes to counterfactual outcomes when treatment matches.

- **D) Homogeneous treatment effects across all subpopulations** ✗
  - Effect heterogeneity is allowed and often expected; causal inference doesn't require homogeneous effects.

- **E) Complete absence of measurement error** ✗
  - While measurement error can bias causal estimates, methods exist to address it; perfect measurement isn't required.

### Question 9
**Correct answers: A, B, D**

- **A) Instrumental variable analysis** ✓
  - Instrumental variables provide a source of exogenous variation to address unmeasured confounding.

- **B) Difference-in-differences designs** ✓
  - DiD accounts for unmeasured confounders that are constant over time.

- **D) Sensitivity analysis for unmeasured confounders** ✓
  - Sensitivity analysis quantifies how strong unmeasured confounding would need to be to invalidate results.

- **C) Simple multivariate regression** ✗
  - Regression alone cannot address unmeasured confounding.

- **E) Increasing sample size without addressing confounding** ✗
  - Larger samples don't solve unmeasured confounding problems; bias remains regardless of sample size.

### Question 10
**Correct answers: A, B, D**

- **A) Direct effects measure the impact of treatment not through the mediator** ✓
  - Direct effects capture causal pathways that don't involve the mediator of interest.

- **B) Indirect effects capture the treatment effect that operates through the mediator** ✓
  - Indirect effects measure how much of the treatment effect is mediated through the variable of interest.

- **D) Counterfactual definitions allow for decomposition of total effects** ✓
  - The counterfactual framework enables mathematical decomposition of effects into direct and indirect components.

- **C) Mediation analysis requires no additional assumptions beyond those for total effects** ✗
  - Mediation requires stronger assumptions, including no unmeasured confounding of the mediator-outcome relationship.

- **E) Mediation analysis cannot be represented in causal diagrams** ✗
  - Causal diagrams clearly illustrate mediation relationships and can help identify necessary adjustment sets.

### Question 11
**Correct answers: A, C, D**

- **A) Differential attrition between treatment groups** ✓
  - When loss to follow-up is related to both treatment and potential outcomes, it creates selection bias.

- **C) Measurement error correlated with treatment assignment** ✓
  - Differential measurement error by treatment status can create spurious treatment effects.

- **D) Spillover effects between treatment and control units** ✓
  - Interference violates the Stable Unit Treatment Value Assumption (SUTVA).

- **B) Limited generalizability to other populations** ✗
  - This affects external validity, not internal validity.

- **E) Small sample size with adequate randomization** ✗
  - Small samples affect precision but not internal validity if randomization is properly implemented.

### Question 12
**Correct answers: A, B, C**

- **A) Determining minimally sufficient adjustment sets** ✓
  - DAGs can identify minimal sets of variables needed to control for confounding.

- **B) Identifying instrumental variables** ✓
  - DAGs help identify valid instruments that affect treatment but not outcome except through treatment.

- **C) Testing for conditional independence implications** ✓
  - DAGs imply specific conditional independence relationships that can be empirically tested.

- **D) Quantifying the magnitude of causal effects** ✗
  - DAGs represent qualitative causal relationships but don't provide quantitative effect sizes.

- **E) Proving causation from observational data without assumptions** ✗
  - DAGs make causal assumptions explicit but cannot eliminate the need for untestable assumptions.

### Question 13
**Correct answers: A, B, D**

- **A) They estimate the probability of treatment given observed covariates** ✓
  - Propensity scores model the conditional probability of treatment assignment given covariates.

- **B) They can be used for matching, stratification, or weighting** ✓
  - Propensity scores can be implemented through various analytical approaches.

- **D) They help balance covariates between treatment groups** ✓
  - The primary purpose of propensity scores is to balance confounders across treatment groups.

- **C) They eliminate the need for the positivity assumption** ✗
  - Propensity score methods still require positivity; extreme scores near 0 or 1 create estimation problems.

- **E) They adjust for unmeasured confounders by design** ✗
  - Propensity scores only balance observed confounders, not unmeasured ones.

### Question 14
**Correct answers: A, C, D**

- **A) Effect modification can occur without interaction** ✓
  - Effect modification refers to variation in effects across subgroups, which can occur without formal interaction.

- **C) Pre-specification of effect modifiers reduces false positives** ✓
  - Pre-specifying hypothesized effect modifiers limits multiple testing problems.

- **D) Additive interaction may exist without multiplicative interaction** ✓
  - Effects can interact on one scale (e.g., additive) but not another (e.g., multiplicative).

- **B) Subgroup analyses require no multiple testing adjustment** ✗
  - Multiple subgroup analyses increase the risk of false positives and typically require adjustment.

- **E) Post-hoc subgroup analyses have the same validity as pre-specified ones** ✗
  - Post-hoc analyses have higher risk of false positive findings and should be interpreted more cautiously.

## Section 3: Machine Learning and Data Concepts

### Question 15
**Correct answers: A, B, D**

- **A) Principal Component Regression** ✓
  - PCR addresses multicollinearity by projecting predictors onto orthogonal components.

- **B) Ridge Regression** ✓
  - Ridge adds L2 regularization that stabilizes coefficient estimates for correlated predictors.

- **D) Feature selection to remove redundant predictors** ✓
  - Removing highly correlated predictors can reduce multicollinearity.

- **C) Increasing model complexity** ✗
  - Higher complexity typically worsens the impacts of multicollinearity.

- **E) Ignoring correlation structure entirely** ✗
  - Ignoring multicollinearity leads to unstable coefficient estimates and inflated standard errors.

### Question 16
**Correct answers: A, B, D**

- **A) Testing for stationarity before modeling** ✓
  - Stationarity tests ensure that statistical properties remain constant over time, which many time series models assume.

- **B) Using autocorrelation functions to identify temporal patterns** ✓
  - ACF and PACF plots help identify appropriate model structures like AR, MA, or ARIMA.

- **D) Implementing seasonality decomposition** ✓
  - Decomposing time series into trend, seasonal, and residual components helps understand underlying patterns.

- **C) Applying standard cross-validation without time considerations** ✗
  - This can lead to data leakage; time series requires specialized validation approaches that respect temporal ordering.

- **E) Ignoring temporal ordering when splitting training and test sets** ✗
  - This creates unrealistic evaluation settings where future data is used to predict past events.

### Question 17
**Correct answers: A, B, D**

- **A) Random Forests combine multiple decision trees to reduce variance** ✓
  - Random Forests use bagging and feature randomization to create diverse trees that reduce overfitting.

- **B) Boosting methods build sequential models that correct previous errors** ✓
  - Boosting algorithms like AdaBoost and Gradient Boosting focus on examples that previous models misclassified.

- **D) Bagging uses bootstrap sampling to create diversity in base learners** ✓
  - Bootstrap Aggregating (bagging) trains models on different random subsets of the data with replacement.

- **C) Ensembles always increase model interpretability** ✗
  - Ensembles typically reduce interpretability compared to single models, trading it for performance.

- **E) Ensemble methods always perform better than single models regardless of data quality** ✗
  - Poor-quality data or improperly configured ensembles can still lead to poor performance.

### Question 18
**Correct answers: A, B, C**

- **A) Time-based splitting for temporal data** ✓
  - Temporal data should be split chronologically to prevent data leakage and realistic evaluation.

- **B) K-fold cross-validation for limited datasets** ✓
  - K-fold cross-validation makes efficient use of limited data while providing robust performance estimates.

- **C) Holdout validation sets for final model assessment** ✓
  - A separate holdout set provides an unbiased final evaluation of model performance.

- **D) Validating only on the most recent data points** ✗
  - While recent data is important, validating on only the most recent points may not represent overall performance.

- **E) Using the same data for feature selection and model validation** ✗
  - This creates data leakage, as information from the validation set influences the model through feature selection.

### Question 19
**Correct answers: A, B, D**

- **A) Aligning visualization type with the specific analytical question** ✓
  - Different visualization types support different analytical goals (comparison, distribution, relationship, etc.).

- **B) Using color intentionally to highlight patterns or categories** ✓
  - Strategic color use enhances pattern recognition and focuses attention on key insights.

- **D) Providing clear context and labels for proper interpretation** ✓
  - Clear titles, labels, and annotations ensure viewers correctly interpret the visualization.

- **C) Maximizing the number of variables displayed in a single visualization** ✗
  - Too many variables create cognitive overload and confusion; focused visualizations are often more effective.

- **E) Prioritizing aesthetic appeal over information clarity** ✗
  - While aesthetics matter, the primary purpose of data visualization is to clearly communicate information.

### Question 20
**Correct answers: A, B, C**

- **A) Oversampling the minority class** ✓
  - Techniques like SMOTE increase representation of minority class examples to balance the dataset.

- **B) Undersampling the majority class** ✓
  - Reducing majority class examples can balance classes without information duplication.

- **C) Using class-weighted loss functions** ✓
  - Assigning higher costs to minority class errors focuses model learning on rare classes.

- **D) Focusing exclusively on accuracy as the performance metric** ✗
  - Accuracy is misleading for imbalanced data; metrics like precision, recall, and F1 are more appropriate.

- **E) Always choosing the majority class for maximum performance** ✗
  - While this might maximize accuracy, it results in a useless model that never detects minority class instances.