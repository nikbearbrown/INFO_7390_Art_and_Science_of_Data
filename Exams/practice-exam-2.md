# Data Science and AI Practice Exam #2 (100 Points)

## Instructions
- Each question is worth 5 points
- Select all correct answers for each question
- There may be multiple correct answers per question
- A detailed answer key is provided at the end of the exam

## Section 1: Generative AI and Deep Learning (35 points)

### Question 1
Which components are essential to the transformer architecture used in modern generative AI?
- [ ] A) Recurrent connections between encoder and decoder
- [x] B) Multi-head attention mechanisms
- [x] C) Positional encodings to maintain sequence information
- [x] D) Layer normalization and residual connections
- [ ] E) Convolutional layers for token processing

### Question 2
What are valid approaches for improving factual accuracy in large language models?
- [x] A) Retrieval-Augmented Generation (RAG)
- [ ] B) Increasing model size indefinitely
- [x] C) Fine-tuning on domain-specific factual datasets
- [x] D) Adding external knowledge bases for reference
- [ ] E) Using only greedy decoding strategies

### Question 3
In the context of generative AI evaluation, which metrics are appropriate for assessing factual accuracy?
- [x] A) Hallucination rate on benchmark datasets
- [ ] B) Perplexity on the training corpus
- [x] C) Fact verification against trusted sources
- [ ] D) Token generation speed
- [x] E) Consistency of answers to related questions

### Question 4
When fine-tuning a large language model, which of the following are best practices?
- [x] A) Using a learning rate smaller than the pre-training rate
- [ ] B) Always fine-tuning all model parameters regardless of dataset size
- [x] C) Evaluating on a held-out validation set during training
- [x] D) Using a diverse, high-quality dataset aligned with the target task
- [ ] E) Using the same hyperparameters as during pre-training

### Question 5
Which statements accurately describe zero-shot, few-shot, and fine-tuned learning in LLMs?
- [x] A) Zero-shot learning enables models to perform tasks without explicit examples
- [x] B) Few-shot learning provides example inputs and outputs in the prompt
- [ ] C) Zero-shot learning always outperforms fine-tuning for domain-specific tasks
- [x] D) Fine-tuning typically yields better performance than few-shot learning for complex tasks
- [ ] E) Few-shot learning requires modifying model weights

### Question 6
What are the primary technical challenges in scaling large language models to greater capabilities?
- [x] A) Computational requirements growing with model size
- [x] B) Memory constraints for context length
- [ ] C) Diminishing returns beyond certain parameter counts
- [x] D) Training instability in very large models
- [ ] E) Inability to parallelize training across multiple devices

### Question 7
Which approaches effectively help mitigate bias in generative AI models?
- [x] A) Diverse and balanced training data
- [x] B) Post-training evaluation across demographic groups
- [x] C) Safety guardrails in both pre-training and fine-tuning
- [ ] D) Increasing model size only
- [ ] E) Using exclusively expert-generated content for training

## Section 2: Causal Inference (35 points)

### Question 8
Which statements correctly describe the relationship between association and causation?
- [x] A) Association between variables can exist without causation
- [ ] B) A strong association always implies causation
- [x] C) Causation guarantees association in the absence of other causal factors
- [ ] D) Randomized experiments cannot distinguish association from causation
- [x] E) Causal effects can be masked, creating a situation with causation but no apparent association

### Question 9
In the context of a causal diagram (DAG), when does conditioning on a variable introduce bias rather than reduce it?
- [x] A) When conditioning on a collider
- [ ] B) When conditioning on a direct cause of the exposure
- [x] C) When conditioning on a mediator when estimating total effects
- [x] D) When conditioning on a descendant of a collider
- [ ] E) When conditioning on a common cause of exposure and outcome

### Question 10
For a conditionally randomized experiment, which methods can be used to estimate causal effects?
- [x] A) Stratification by the conditioning variable
- [x] B) Inverse probability weighting
- [x] C) Standardization
- [ ] D) Simple difference in means without adjustment
- [x] E) G-computation

### Question 11
Which statements about counterfactuals in causal inference are correct?
- [x] A) Counterfactuals describe outcomes that would have occurred under different treatments
- [x] B) Individual causal effects require comparing counterfactual outcomes
- [ ] C) Counterfactuals can be directly observed for each individual
- [x] D) Counterfactuals form the basis for defining causal effects
- [ ] E) Counterfactual outcomes can be estimated without assumptions

### Question 12
In which scenarios is the frontdoor criterion applicable for estimating causal effects?
- [x] A) When there are unmeasured confounders between treatment and outcome
- [x] B) When an unconfounded mediator exists between treatment and outcome
- [ ] C) When treatment assignment is fully randomized
- [x] D) When direct effects cannot be estimated using the backdoor criterion
- [ ] E) When the outcome directly causes the treatment

### Question 13
Which of the following are types of selection bias in causal inference?
- [x] A) Self-selection into a study based on health status
- [x] B) Loss to follow-up related to both treatment and outcome
- [x] C) Healthy worker bias in occupational studies
- [ ] D) Random missing data in the outcome variable
- [x] E) Analyzing only complete cases when missingness is related to exposure

### Question 14
Which statements about interaction and effect modification are correct?
- [x] A) Additive interaction occurs when the joint effect of two exposures differs from the sum of their individual effects
- [ ] B) Effect modification and interaction are always equivalent concepts
- [x] C) Qualitative effect modification occurs when effects go in opposite directions across strata
- [x] D) Sufficient cause interaction implies biologic interaction at the mechanistic level
- [ ] E) Interaction can only be assessed on an additive scale

## Section 3: Machine Learning and Data Concepts (30 points)

### Question 15
Which statements about the bias-variance tradeoff are correct?
- [x] A) As model complexity increases, bias tends to decrease while variance increases
- [ ] B) The optimal model should always minimize bias regardless of variance
- [x] C) Cross-validation helps identify the best balance between bias and variance
- [x] D) Regularization techniques help manage the bias-variance tradeoff
- [ ] E) Ensemble methods always increase both bias and variance

### Question 16
For feature selection in machine learning, which approaches are valid?
- [x] A) Filter methods based on statistical measures like correlation or mutual information
- [x] B) Wrapper methods that evaluate feature subsets using the model performance
- [x] C) Embedded methods like LASSO regression that incorporate feature selection within model training
- [ ] D) Selecting features based solely on their individual predictive power
- [ ] E) Always selecting the minimum number of features regardless of model performance

### Question 17
When evaluating a classification model using a confusion matrix, which statements are correct?
- [x] A) High precision means a low false positive rate
- [x] B) High recall means a low false negative rate
- [ ] C) The F1 score equally weights precision and recall for all business problems
- [x] D) AUC-ROC measures discrimination ability across different thresholds
- [ ] E) Accuracy is the most informative metric for highly imbalanced datasets

### Question 18
Which properties correctly describe Principal Component Analysis (PCA)?
- [x] A) Principal components are orthogonal to each other
- [x] B) The first principal component captures the direction of maximum variance
- [ ] C) PCA always improves classification performance
- [x] D) Eigenvalues represent the amount of variance explained by each component
- [ ] E) Principal components have the same interpretation as the original features

### Question 19
In the context of clustering algorithms, which statements are correct?
- [x] A) K-means works best with spherical clusters of similar size
- [ ] B) Hierarchical clustering requires specifying the number of clusters beforehand
- [x] C) DBSCAN can identify clusters of arbitrary shape
- [x] D) The silhouette coefficient is a valid measure of clustering quality
- [ ] E) All clustering algorithms require distance metrics to be Euclidean

### Question 20
Which visualization principles and techniques are effective for communicating complex data?
- [x] A) Choosing chart types based on the specific data relationships you want to highlight
- [ ] B) Maximizing the data-ink ratio by removing all non-data elements
- [x] C) Maintaining consistent scales when comparing multiple charts
- [x] D) Using color strategically to emphasize important findings or group categories
- [ ] E) Always using 3D visualizations to impress the audience

---

# Answer Key with Detailed Explanations

## Section 1: Generative AI and Deep Learning

### Question 1
**Correct answers: B, C, D**

- **B) Multi-head attention mechanisms** ✓
  - Multi-head attention is a fundamental component that allows transformers to attend to different parts of the input simultaneously from different representation subspaces.

- **C) Positional encodings to maintain sequence information** ✓
  - Since transformers process all tokens in parallel, positional encodings are essential to inject information about token position in the sequence.

- **D) Layer normalization and residual connections** ✓
  - These components are crucial for stable training of deep transformer networks by helping with gradient flow and normalization.

- **A) Recurrent connections between encoder and decoder** ✗
  - Transformers specifically avoid recurrent connections, which is a key architectural difference from RNNs/LSTMs.

- **E) Convolutional layers for token processing** ✗
  - While some transformer variants use convolutions, the standard transformer architecture doesn't rely on convolutional layers.

### Question 2
**Correct answers: A, C, D**

- **A) Retrieval-Augmented Generation (RAG)** ✓
  - RAG improves factual accuracy by retrieving relevant information from external sources before generating responses.

- **C) Fine-tuning on domain-specific factual datasets** ✓
  - Domain-specific fine-tuning helps models learn specialized knowledge and correct factual errors in particular domains.

- **D) Adding external knowledge bases for reference** ✓
  - External knowledge bases provide authoritative information that models can access during inference.

- **B) Increasing model size indefinitely** ✗
  - While larger models tend to have better factual recall, size alone doesn't guarantee accuracy and faces diminishing returns.

- **E) Using only greedy decoding strategies** ✗
  - Decoding strategy affects text quality but doesn't directly address factual accuracy issues.

### Question 3
**Correct answers: A, C, E**

- **A) Hallucination rate on benchmark datasets** ✓
  - Measuring the rate of factual errors or hallucinations on standardized datasets helps assess factual accuracy.

- **C) Fact verification against trusted sources** ✓
  - Comparing model outputs to verified facts from trusted sources directly evaluates factual correctness.

- **E) Consistency of answers to related questions** ✓
  - Measuring how consistently a model answers related questions helps assess its factual understanding.

- **B) Perplexity on the training corpus** ✗
  - Perplexity measures language modeling quality but not specifically factual accuracy.

- **D) Token generation speed** ✗
  - Generation speed is a performance metric unrelated to factual accuracy.

### Question 4
**Correct answers: A, C, D**

- **A) Using a learning rate smaller than the pre-training rate** ✓
  - Smaller learning rates during fine-tuning prevent catastrophic forgetting of pre-trained knowledge.

- **C) Evaluating on a held-out validation set during training** ✓
  - Validation sets help monitor performance and prevent overfitting during fine-tuning.

- **D) Using a diverse, high-quality dataset aligned with the target task** ✓
  - Dataset quality and relevance significantly impact fine-tuning success.

- **B) Always fine-tuning all model parameters regardless of dataset size** ✗
  - For small datasets, parameter-efficient fine-tuning methods may be more appropriate to avoid overfitting.

- **E) Using the same hyperparameters as during pre-training** ✗
  - Fine-tuning typically requires different hyperparameters optimized for the specific task.

### Question 5
**Correct answers: A, B, D**

- **A) Zero-shot learning enables models to perform tasks without explicit examples** ✓
  - Zero-shot learning allows models to follow instructions without task-specific examples.

- **B) Few-shot learning provides example inputs and outputs in the prompt** ✓
  - Few-shot learning uses demonstrations within the prompt to guide the model.

- **D) Fine-tuning typically yields better performance than few-shot learning for complex tasks** ✓
  - Fine-tuning typically outperforms few-shot approaches on complex tasks, especially with sufficient task-specific data.

- **C) Zero-shot learning always outperforms fine-tuning for domain-specific tasks** ✗
  - Fine-tuning generally outperforms zero-shot approaches for domain-specific tasks.

- **E) Few-shot learning requires modifying model weights** ✗
  - Few-shot learning operates through prompt engineering without changing model weights.

### Question 6
**Correct answers: A, B, D**

- **A) Computational requirements growing with model size** ✓
  - Computational costs grow significantly with model size, creating resource challenges.

- **B) Memory constraints for context length** ✓
  - Attention computation grows quadratically with sequence length, creating memory bottlenecks.

- **D) Training instability in very large models** ✓
  - Larger models can face optimization challenges including instability during training.

- **C) Diminishing returns beyond certain parameter counts** ✗
  - While scaling laws suggest some diminishing returns, larger models continue to show improved capabilities across many metrics.

- **E) Inability to parallelize training across multiple devices** ✗
  - Techniques like model and data parallelism enable effective distribution of training across multiple devices.

### Question 7
**Correct answers: A, B, C**

- **A) Diverse and balanced training data** ✓
  - Training data diversity helps ensure models learn to represent different perspectives fairly.

- **B) Post-training evaluation across demographic groups** ✓
  - Systematic evaluation across groups helps identify and address bias in model outputs.

- **C) Safety guardrails in both pre-training and fine-tuning** ✓
  - Safety measures throughout training help reduce harmful biases in outputs.

- **D) Increasing model size only** ✗
  - Larger models can sometimes amplify biases if not specifically addressed.

- **E) Using exclusively expert-generated content for training** ✗
  - Expert content alone may not represent diverse perspectives and could introduce its own biases.

## Section 2: Causal Inference

### Question 8
**Correct answers: A, C, E**

- **A) Association between variables can exist without causation** ✓
  - Variables can be associated due to common causes or chance without direct causal relationships.

- **C) Causation guarantees association in the absence of other causal factors** ✓
  - A true causal relationship will produce association unless masked by other factors.

- **E) Causal effects can be masked, creating a situation with causation but no apparent association** ✓
  - Effect modification or competing causal pathways can mask causal effects, creating scenarios with causation but no observed association.

- **B) A strong association always implies causation** ✗
  - Strong associations can result from confounding or other non-causal mechanisms.

- **D) Randomized experiments cannot distinguish association from causation** ✗
  - Properly designed randomized experiments are specifically intended to identify causal effects.

### Question 9
**Correct answers: A, C, D**

- **A) When conditioning on a collider** ✓
  - Conditioning on a collider introduces spurious associations between its causes.

- **C) When conditioning on a mediator when estimating total effects** ✓
  - Controlling for mediators blocks part of the causal pathway, preventing estimation of total effects.

- **D) When conditioning on a descendant of a collider** ✓
  - Conditioning on descendants of colliders can partially condition on the collider, introducing bias.

- **B) When conditioning on a direct cause of the exposure** ✗
  - Conditioning on causes of the exposure typically doesn't introduce bias for the exposure-outcome relationship.

- **E) When conditioning on a common cause of exposure and outcome** ✗
  - Conditioning on common causes (confounders) reduces bias rather than introducing it.

### Question 10
**Correct answers: A, B, C, E**

- **A) Stratification by the conditioning variable** ✓
  - Analyzing each stratum separately and combining results accounts for the conditioning.

- **B) Inverse probability weighting** ✓
  - IPW creates a pseudo-population balancing the conditioning variable across treatment groups.

- **C) Standardization** ✓
  - Standardization calculates the weighted average of stratum-specific effects.

- **E) G-computation** ✓
  - G-computation estimates counterfactual outcomes accounting for the conditioning.

- **D) Simple difference in means without adjustment** ✗
  - This would ignore the conditional randomization, leading to biased estimates.

### Question 11
**Correct answers: A, B, D**

- **A) Counterfactuals describe outcomes that would have occurred under different treatments** ✓
  - This is the fundamental definition of counterfactuals in causal inference.

- **B) Individual causal effects require comparing counterfactual outcomes** ✓
  - Individual effects compare what happened to what would have happened under alternative treatment.

- **D) Counterfactuals form the basis for defining causal effects** ✓
  - Causal effects are defined as comparisons between counterfactual outcomes.

- **C) Counterfactuals can be directly observed for each individual** ✗
  - The fundamental problem of causal inference is that we can never observe all counterfactuals for an individual.

- **E) Counterfactual outcomes can be estimated without assumptions** ✗
  - Estimating counterfactuals requires identifiability assumptions like exchangeability, consistency, and positivity.

### Question 12
**Correct answers: A, B, D**

- **A) When there are unmeasured confounders between treatment and outcome** ✓
  - The frontdoor criterion specifically addresses settings with unmeasured confounding.

- **B) When an unconfounded mediator exists between treatment and outcome** ✓
  - An unconfounded mediator is key to the frontdoor approach.

- **D) When direct effects cannot be estimated using the backdoor criterion** ✓
  - Frontdoor adjustment provides an alternative when backdoor adjustment isn't possible.

- **C) When treatment assignment is fully randomized** ✗
  - With randomization, simpler methods like direct comparison are sufficient.

- **E) When the outcome directly causes the treatment** ✗
  - This would create a cyclic graph, violating DAG assumptions.

### Question 13
**Correct answers: A, B, C, E**

- **A) Self-selection into a study based on health status** ✓
  - This creates non-representative samples based on factors related to outcomes.

- **B) Loss to follow-up related to both treatment and outcome** ✓
  - Differential attrition creates selection bias when related to exposure and outcome.

- **C) Healthy worker bias in occupational studies** ✓
  - This occurs when only healthy individuals remain in certain exposure groups.

- **E) Analyzing only complete cases when missingness is related to exposure** ✓
  - Complete-case analysis creates selection bias when missingness depends on exposure.

- **D) Random missing data in the outcome variable** ✗
  - Truly random (MCAR) missingness doesn't introduce selection bias.

### Question 14
**Correct answers: A, C, D**

- **A) Additive interaction occurs when the joint effect of two exposures differs from the sum of their individual effects** ✓
  - This correctly defines additive interaction in terms of departure from additivity.

- **C) Qualitative effect modification occurs when effects go in opposite directions across strata** ✓
  - Qualitative effect modification involves a change in direction, not just magnitude.

- **D) Sufficient cause interaction implies biologic interaction at the mechanistic level** ✓
  - Sufficient cause interaction reflects mechanistic combination of causal factors.

- **B) Effect modification and interaction are always equivalent concepts** ✗
  - Effect modification involves variables not subject to intervention, while interaction involves two treatment variables.

- **E) Interaction can only be assessed on an additive scale** ✗
  - Interaction can be assessed on additive, multiplicative, or other scales.

## Section 3: Machine Learning and Data Concepts

### Question 15
**Correct answers: A, C, D**

- **A) As model complexity increases, bias tends to decrease while variance increases** ✓
  - This fundamental relationship describes the bias-variance tradeoff.

- **C) Cross-validation helps identify the best balance between bias and variance** ✓
  - Cross-validation estimates generalization performance, helping find optimal complexity.

- **D) Regularization techniques help manage the bias-variance tradeoff** ✓
  - Regularization controls model complexity, helping balance bias and variance.

- **B) The optimal model should always minimize bias regardless of variance** ✗
  - The goal is to minimize total error, which requires balancing bias and variance.

- **E) Ensemble methods always increase both bias and variance** ✗
  - Many ensemble methods (like bagging) reduce variance while maintaining similar bias.

### Question 16
**Correct answers: A, B, C**

- **A) Filter methods based on statistical measures like correlation or mutual information** ✓
  - Filter methods select features based on statistical relationship with the target variable.

- **B) Wrapper methods that evaluate feature subsets using the model performance** ✓
  - Wrapper methods use model performance to evaluate different feature combinations.

- **C) Embedded methods like LASSO regression that incorporate feature selection within model training** ✓
  - Embedded methods perform feature selection during model training.

- **D) Selecting features based solely on their individual predictive power** ✗
  - This ignores feature interactions and redundancy.

- **E) Always selecting the minimum number of features regardless of model performance** ✗
  - Feature selection should optimize performance, not minimize feature count regardless of impact.

### Question 17
**Correct answers: A, B, D**

- **A) High precision means a low false positive rate** ✓
  - Precision = TP/(TP+FP), so high precision means few false positives relative to true positives.

- **B) High recall means a low false negative rate** ✓
  - Recall = TP/(TP+FN), so high recall means few false negatives relative to actual positives.

- **D) AUC-ROC measures discrimination ability across different thresholds** ✓
  - AUC-ROC measures model ability to rank positive instances higher than negative ones.

- **C) The F1 score equally weights precision and recall for all business problems** ✗
  - While F1 equally weights precision and recall mathematically, business contexts may value them differently.

- **E) Accuracy is the most informative metric for highly imbalanced datasets** ✗
  - Accuracy can be misleading for imbalanced data; metrics like precision, recall, and F1 are generally more informative.

### Question 18
**Correct answers: A, B, D**

- **A) Principal components are orthogonal to each other** ✓
  - PCA produces components that are perpendicular to each other in feature space.

- **B) The first principal component captures the direction of maximum variance** ✓
  - PCA finds components in order of variance explained, with the first capturing the most.

- **D) Eigenvalues represent the amount of variance explained by each component** ✓
  - The eigenvalue associated with each component directly measures its variance.

- **C) PCA always improves classification performance** ✗
  - PCA may lose discriminative information since it focuses on variance, not class separation.

- **E) Principal components have the same interpretation as the original features** ✗
  - Principal components are linear combinations of original features with different interpretations.

### Question 19
**Correct answers: A, C, D**

- **A) K-means works best with spherical clusters of similar size** ✓
  - K-means assumes equal-variance spherical clusters and struggles with other shapes.

- **C) DBSCAN can identify clusters of arbitrary shape** ✓
  - DBSCAN defines clusters based on density, allowing it to find irregular shapes.

- **D) The silhouette coefficient is a valid measure of clustering quality** ✓
  - Silhouette measures how similar points are to their cluster compared to other clusters.

- **B) Hierarchical clustering requires specifying the number of clusters beforehand** ✗
  - Hierarchical clustering builds a dendrogram; the number of clusters can be chosen afterward.

- **E) All clustering algorithms require distance metrics to be Euclidean** ✗
  - Many clustering algorithms can use various distance metrics beyond Euclidean distance.

### Question 20
**Correct answers: A, C, D**

- **A) Choosing chart types based on the specific data relationships you want to highlight** ✓
  - Different visualizations are suited for different data relationships and analytical goals.

- **C) Maintaining consistent scales when comparing multiple charts** ✓
  - Consistent scales prevent misleading visual comparisons.

- **D) Using color strategically to emphasize important findings or group categories** ✓
  - Strategic color use enhances information communication and accessibility.

- **B) Maximizing the data-ink ratio by removing all non-data elements** ✗
  - While minimizing chart junk is good, some non-data elements like axes, labels, and legends are essential for understanding.

- **E) Always using 3D visualizations to impress the audience** ✗
  - 3D visualizations often distort perception and should be used selectively, not as a default.