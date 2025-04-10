# Data Science and AI Practice Exam (100 Points)

## Instructions
- Each question is worth 5 points
- Select all correct answers for each question
- There may be multiple correct answers per question
- A detailed answer key is provided at the end of the exam

## Section 1: Generative AI and Deep Learning (35 points)

### Question 1
Which of the following correctly describe the attention mechanism in transformer models?
- [ ] A) It primarily uses recurrent connections to capture sequential information
- [x] B) It allows the model to focus on different parts of the input simultaneously
- [x] C) It enables transformers to process tokens in parallel rather than sequentially
- [ ] D) It requires fixed-length inputs for all transformer models
- [x] E) It uses positional encodings to maintain sequence order information

### Question 2
What are key limitations of large language models (LLMs)?
- [x] A) They can generate hallucinated or incorrect information
- [x] B) Training them requires significant computational resources
- [ ] C) They cannot generalize to unseen tasks or domains
- [x] D) They inherit biases from their training data
- [ ] E) They can only be used for text generation tasks

### Question 3
Which statements about Retrieval-Augmented Generation (RAG) are correct?
- [x] A) RAG combines generative models with retrieval systems to improve factual accuracy
- [x] B) The retriever component fetches relevant documents based on a query
- [ ] C) RAG eliminates the need for fine-tuning on downstream tasks
- [ ] D) The generator relies solely on retrieved documents to produce outputs
- [x] E) RAG allows integration of domain-specific knowledge bases

### Question 4
In the context of generative AI projects, what is the purpose of the "Augment model and build LLM-powered applications" phase?
- [x] A) To enhance the model's capabilities for specific use cases
- [x] B) To create applications that leverage the underlying model
- [ ] C) To select which model to use based on problem definition
- [ ] D) To perform statistical analysis of model performance
- [ ] E) To gather additional training data

### Question 5
What characteristics are true of transformer neural networks?
- [x] A) They eliminate the need for recurrence through self-attention mechanisms
- [x] B) The multi-head attention mechanism allows focus on different input aspects
- [ ] C) They are inherently more computationally efficient than RNNs for very long sequences
- [x] D) The encoder-decoder architecture is used primarily for sequence-to-sequence tasks
- [ ] E) They cannot process sequential data as effectively as LSTMs

### Question 6
How do counterfactuals function in LLMs and generative AI systems?
- [x] A) They allow models to reason about hypothetical scenarios that didn't occur
- [ ] B) They are only applicable to supervised learning approaches
- [x] C) They enable "what-if" reasoning capabilities in language models
- [x] D) They support complex reasoning in zero-shot learning contexts
- [ ] E) They require explicit causal graphs to be implemented

### Question 7
Which of the following are true about fine-tuning in generative AI models?
- [x] A) It adapts pre-trained models to specific downstream tasks
- [ ] B) It always requires completely retraining the model from scratch
- [x] C) It can be performed with relatively small domain-specific datasets
- [x] D) It helps reduce the occurrence of task-specific errors
- [ ] E) It eliminates the need for prompt engineering

## Section 2: Causal Inference (35 points)

### Question 8
Which of the following are required identifiability conditions for causal inference?
- [x] A) Consistency: If A = a, then Y^a = Y
- [x] B) Exchangeability: Y^a ⫫ A for all a
- [x] C) Positivity: Pr[A=a | L=l] > 0 for all values l with non-zero probability
- [ ] D) Monotonicity: Treatment effects must be in the same direction for all individuals
- [ ] E) Homogeneity: Treatment effects must be identical across all subpopulations

### Question 9
Which statements about confounding are correct?
- [x] A) Confounding occurs when treatment and outcome share a common cause
- [x] B) The backdoor criterion identifies when confounding can be eliminated through adjustment
- [ ] C) Randomization cannot address confounding in experimental settings
- [x] D) Confounding by indication occurs when treatment is more likely for high-risk individuals
- [ ] E) Confounding can only be detected through statistical tests, not through causal diagrams

### Question 10
In causal diagrams (DAGs), which of the following statements are true?
- [x] A) A collider is a variable where two arrowheads on a path collide
- [x] B) Conditioning on a collider can create a spurious association
- [x] C) d-separation means all paths between two variables are blocked
- [ ] D) All associations in a causal DAG imply direct causation
- [ ] E) Backdoor paths must always include mediator variables

### Question 11
Which methods can be used to address confounding in causal inference?
- [x] A) Inverse probability weighting
- [x] B) Standardization by stratification
- [x] C) G-computation formula
- [ ] D) Simple correlation analysis
- [x] E) Matching on confounders

### Question 12
What distinguishes effect modification from interaction in causal inference?
- [x] A) Effect modification involves a variable not subject to intervention
- [ ] B) Interaction always implies qualitative effect modification
- [x] C) In interaction, both variables A and E have equal status as treatments
- [x] D) Effect modifiers are not necessarily causal variables
- [ ] E) Interaction cannot be measured on additive scales

### Question 13
Which statements about the frontdoor criterion are correct?
- [x] A) It allows causal effect estimation when there are unmeasured confounders
- [x] B) It requires an unconfounded mediator variable
- [ ] C) It is more commonly applicable than the backdoor criterion
- [x] D) It uses a two-step standardization process
- [ ] E) It cannot be represented in a causal diagram

### Question 14
What are true statements about selection bias in causal inference?
- [x] A) It occurs when conditioning on common effects
- [x] B) Healthy worker bias is an example of selection bias
- [ ] C) It can always be addressed by collecting more data
- [x] D) It can occur in both observational and experimental studies
- [ ] E) Selection bias always leads to overestimation of causal effects

## Section 3: Machine Learning and Data Concepts (30 points)

### Question 15
Which statements about Principal Component Analysis (PCA) are correct?
- [x] A) It reduces dimensionality while preserving important variance
- [x] B) Components are ordered by the amount of variance they explain
- [ ] C) It works equally well with categorical and numerical variables
- [x] D) It is sensitive to the scale of features
- [ ] E) It guarantees better class separation in classification tasks

### Question 16
What are valid approaches to handling missing data?
- [x] A) K-Nearest Neighbors (KNN) imputation based on feature similarity
- [x] B) Multiple Imputation by Chained Equations (MICE)
- [x] C) Forward fill for time series data
- [ ] D) Always removing observations with any missing values
- [ ] E) Mean imputation always improves dataset accuracy

### Question 17
Which statements about bias and variance in machine learning are correct?
- [x] A) High bias leads to underfitting
- [x] B) High variance leads to overfitting
- [ ] C) High bias implies the model fits training data very well
- [ ] D) High variance means the model generalizes well to new data
- [x] E) The goal is to find an optimal balance between bias and variance

### Question 18
For the K-means clustering algorithm, which statements are true?
- [x] A) It minimizes within-cluster sum of squared distances to centroids
- [x] B) Initial centroid selection can impact final clustering results
- [x] C) It assumes clusters are spherical and equally sized
- [ ] D) It inherently handles missing values
- [x] E) It is sensitive to outliers

### Question 19
Which statements about feature engineering are true?
- [x] A) Log transformation can help reduce skewness in data
- [x] B) One-hot encoding converts categorical variables to numerical form
- [x] C) Creating interaction terms helps capture non-linear relationships
- [ ] D) Feature selection is unnecessary if all features contain information
- [x] E) Standardizing features is useful for distance-based algorithms

### Question 20
Which statements about effective data visualization principles are correct?
- [x] A) Minimize chart elements like gridlines and decorations to reduce cognitive load
- [x] B) Tailor visualizations to the audience's knowledge level
- [ ] C) Adding 3D effects to bar charts improves data interpretation
- [x] D) Use redundant encoding (color + shape) to enhance clarity and accessibility
- [ ] E) Descriptive titles are unnecessary if axes are properly labeled

---

# Answer Key with Detailed Explanations

## Section 1: Generative AI and Deep Learning

### Question 1
**Correct answers: B, C, E**

- **B) It allows the model to focus on different parts of the input simultaneously** ✓
  - The attention mechanism enables transformers to attend to different parts of the input sequence with varying weights, allowing it to focus on relevant tokens.

- **C) It enables transformers to process tokens in parallel rather than sequentially** ✓
  - Unlike recurrent models, transformers process all tokens simultaneously through self-attention, enabling more efficient parallel computation.

- **E) It uses positional encodings to maintain sequence order information** ✓
  - Since transformers process tokens in parallel, they use positional encodings to incorporate sequence order information that would otherwise be lost.

- **A) It primarily uses recurrent connections to capture sequential information** ✗
  - Transformers specifically avoid recurrent connections, which is their key advantage over RNNs/LSTMs.

- **D) It requires fixed-length inputs for all transformer models** ✗
  - Transformers can handle variable-length inputs, although extremely long sequences may have computational limitations.

### Question 2
**Correct answers: A, B, D**

- **A) They can generate hallucinated or incorrect information** ✓
  - LLMs can produce plausible-sounding but factually incorrect information, a phenomenon known as hallucination.

- **B) Training them requires significant computational resources** ✓
  - Training large language models requires substantial computational power, energy, and specialized hardware.

- **D) They inherit biases from their training data** ✓
  - LLMs learn patterns from their training data, including any biases present in that data.

- **C) They cannot generalize to unseen tasks or domains** ✗
  - LLMs can generalize to unseen tasks through techniques like zero-shot and few-shot learning.

- **E) They can only be used for text generation tasks** ✗
  - LLMs can be used for various tasks including classification, summarization, translation, and reasoning.

### Question 3
**Correct answers: A, B, E**

- **A) RAG combines generative models with retrieval systems to improve factual accuracy** ✓
  - RAG systems integrate retrieval mechanisms to ground generative outputs in factual knowledge.

- **B) The retriever component fetches relevant documents based on a query** ✓
  - The retriever in RAG is responsible for finding and retrieving relevant documents or information.

- **E) RAG allows integration of domain-specific knowledge bases** ✓
  - RAG systems can incorporate specialized knowledge bases to enhance relevance for specific domains.

- **C) RAG eliminates the need for fine-tuning on downstream tasks** ✗
  - While RAG improves zero-shot performance, fine-tuning can still be beneficial for domain-specific tasks.

- **D) The generator relies solely on retrieved documents to produce outputs** ✗
  - The generator uses both retrieved documents and its pre-trained knowledge to create responses.

### Question 4
**Correct answers: A, B**

- **A) To enhance the model's capabilities for specific use cases** ✓
  - This phase involves adapting and extending the model's functionality for specific applications.

- **B) To create applications that leverage the underlying model** ✓
  - Building LLM-powered applications is a core purpose of this project phase.

- **C) To select which model to use based on problem definition** ✗
  - Model selection typically occurs earlier in the project lifecycle.

- **D) To perform statistical analysis of model performance** ✗
  - Performance analysis is part of evaluation, not this phase.

- **E) To gather additional training data** ✗
  - Data gathering typically occurs before model training, not during the application building phase.

### Question 5
**Correct answers: A, B, D**

- **A) They eliminate the need for recurrence through self-attention mechanisms** ✓
  - Transformers replace recurrent processing with attention mechanisms, allowing parallel computation.

- **B) The multi-head attention mechanism allows focus on different input aspects** ✓
  - Multi-head attention enables the model to attend to different aspects of the input simultaneously.

- **D) The encoder-decoder architecture is used primarily for sequence-to-sequence tasks** ✓
  - The encoder-decoder structure is commonly used for tasks like translation where input and output are sequences.

- **C) They are inherently more computationally efficient than RNNs for very long sequences** ✗
  - Due to the quadratic complexity of self-attention, transformers can be less efficient for very long sequences without optimizations.

- **E) They cannot process sequential data as effectively as LSTMs** ✗
  - Transformers have generally outperformed LSTMs on sequential tasks, especially for longer sequences.

### Question 6
**Correct answers: A, C, D**

- **A) They allow models to reason about hypothetical scenarios that didn't occur** ✓
  - Counterfactuals enable reasoning about alternative scenarios and outcomes.

- **C) They enable "what-if" reasoning capabilities in language models** ✓
  - "What-if" reasoning is a core counterfactual capability in advanced language models.

- **D) They support complex reasoning in zero-shot learning contexts** ✓
  - Counterfactual reasoning can enhance zero-shot performance on novel tasks.

- **B) They are only applicable to supervised learning approaches** ✗
  - Counterfactual reasoning can be implemented in various learning paradigms.

- **E) They require explicit causal graphs to be implemented** ✗
  - While causal graphs can help formalize counterfactuals, LLMs can perform counterfactual reasoning without explicit graph implementation.

### Question 7
**Correct answers: A, C, D**

- **A) It adapts pre-trained models to specific downstream tasks** ✓
  - Fine-tuning adjusts pre-trained models to perform well on specific tasks or domains.

- **C) It can be performed with relatively small domain-specific datasets** ✓
  - A key advantage of fine-tuning is that it requires much less data than pre-training from scratch.

- **D) It helps reduce the occurrence of task-specific errors** ✓
  - Fine-tuning can help correct model behaviors that are problematic for specific tasks.

- **B) It always requires completely retraining the model from scratch** ✗
  - Fine-tuning specifically refers to adjusting an already trained model, not retraining from scratch.

- **E) It eliminates the need for prompt engineering** ✗
  - Even fine-tuned models can benefit from effective prompt engineering for optimal performance.

## Section 2: Causal Inference

### Question 8
**Correct answers: A, B, C**

- **A) Consistency: If A = a, then Y^a = Y** ✓
  - The consistency assumption links counterfactual outcomes to observed outcomes when treatment matches.

- **B) Exchangeability: Y^a ⫫ A for all a** ✓
  - Exchangeability (no unmeasured confounding) is essential for causal inference.

- **C) Positivity: Pr[A=a | L=l] > 0 for all values l with non-zero probability** ✓
  - Positivity ensures all strata have a chance of receiving each treatment level.

- **D) Monotonicity: Treatment effects must be in the same direction for all individuals** ✗
  - Monotonicity is sometimes assumed but is not a general identifiability condition.

- **E) Homogeneity: Treatment effects must be identical across all subpopulations** ✗
  - Homogeneity is not required; effect modification is allowed under identifiability conditions.

### Question 9
**Correct answers: A, B, D**

- **A) Confounding occurs when treatment and outcome share a common cause** ✓
  - This is the fundamental definition of confounding in causal inference.

- **B) The backdoor criterion identifies when confounding can be eliminated through adjustment** ✓
  - The backdoor criterion provides conditions under which conditioning on variables can remove confounding.

- **D) Confounding by indication occurs when treatment is more likely for high-risk individuals** ✓
  - This describes a common source of confounding in observational healthcare studies.

- **C) Randomization cannot address confounding in experimental settings** ✗
  - Proper randomization is specifically designed to address confounding in experiments.

- **E) Confounding can only be detected through statistical tests, not through causal diagrams** ✗
  - Causal diagrams are powerful tools for identifying potential confounding.

### Question 10
**Correct answers: A, B, C**

- **A) A collider is a variable where two arrowheads on a path collide** ✓
  - This is the definition of a collider in causal diagrams (e.g., A→Y←L).

- **B) Conditioning on a collider can create a spurious association** ✓
  - Conditioning on colliders can create misleading associations between otherwise independent variables.

- **C) d-separation means all paths between two variables are blocked** ✓
  - d-separation indicates that all pathways between variables are blocked, implying conditional independence.

- **D) All associations in a causal DAG imply direct causation** ✗
  - Associations can arise from confounding, selection bias, or direct causation.

- **E) Backdoor paths must always include mediator variables** ✗
  - Backdoor paths need not include mediators; they're non-causal paths with arrows pointing into treatment.

### Question 11
**Correct answers: A, B, C, E**

- **A) Inverse probability weighting** ✓
  - IPW creates a pseudo-population where confounding is balanced through weighted analysis.

- **B) Standardization by stratification** ✓
  - Standardization adjusts for confounding by calculating stratum-specific effects and averaging.

- **C) G-computation formula** ✓
  - The g-formula is a general approach for estimating causal effects under confounding.

- **E) Matching on confounders** ✓
  - Matching creates comparable groups that are balanced on confounding factors.

- **D) Simple correlation analysis** ✗
  - Correlation cannot address confounding as it only measures associations.

### Question 12
**Correct answers: A, C, D**

- **A) Effect modification involves a variable not subject to intervention** ✓
  - Effect modifiers are not considered treatments, unlike interaction variables.

- **C) In interaction, both variables A and E have equal status as treatments** ✓
  - Interaction considers both variables as potential interventions with equal status.

- **D) Effect modifiers are not necessarily causal variables** ✓
  - Effect modifiers may be surrogate variables that don't play a direct causal role.

- **B) Interaction always implies qualitative effect modification** ✗
  - Interaction doesn't necessarily imply effects in opposite directions across strata.

- **E) Interaction cannot be measured on additive scales** ✗
  - Interaction can be measured on both additive and multiplicative scales.

### Question 13
**Correct answers: A, B, D**

- **A) It allows causal effect estimation when there are unmeasured confounders** ✓
  - The frontdoor criterion provides a method to estimate causal effects despite unmeasured confounding.

- **B) It requires an unconfounded mediator variable** ✓
  - The frontdoor criterion relies on an unconfounded mediator between treatment and outcome.

- **D) It uses a two-step standardization process** ✓
  - The frontdoor adjustment involves two standardization steps to identify the causal effect.

- **C) It is more commonly applicable than the backdoor criterion** ✗
  - The frontdoor criterion has more restrictive requirements and is less commonly applicable.

- **E) It cannot be represented in a causal diagram** ✗
  - The frontdoor criterion is explicitly based on specific patterns in causal diagrams.

### Question 14
**Correct answers: A, B, D**

- **A) It occurs when conditioning on common effects** ✓
  - Selection bias happens when conditioning on a collider or its descendants.

- **B) Healthy worker bias is an example of selection bias** ✓
  - Healthy worker bias occurs when only healthy individuals are included in a study population.

- **D) It can occur in both observational and experimental studies** ✓
  - Selection bias can affect both study types, particularly through differential loss to follow-up.

- **C) It can always be addressed by collecting more data** ✗
  - More data won't fix selection bias if the sampling mechanism remains biased.

- **E) Selection bias always leads to overestimation of causal effects** ✗
  - Selection bias can lead to either over- or underestimation depending on the scenario.

## Section 3: Machine Learning and Data Concepts

### Question 15
**Correct answers: A, B, D**

- **A) It reduces dimensionality while preserving important variance** ✓
  - PCA transforms data to capture maximum variance in fewer dimensions.

- **B) Components are ordered by the amount of variance they explain** ✓
  - The first principal component captures the most variance, with decreasing amounts for subsequent components.

- **D) It is sensitive to the scale of features** ✓
  - Features should be standardized before PCA to prevent those with larger scales from dominating.

- **C) It works equally well with categorical and numerical variables** ✗
  - PCA is designed for numerical variables; categorical variables require appropriate encoding first.

- **E) It guarantees better class separation in classification tasks** ✗
  - PCA optimizes for variance preservation, not class separation.

### Question 16
**Correct answers: A, B, C**

- **A) K-Nearest Neighbors (KNN) imputation based on feature similarity** ✓
  - KNN imputation estimates missing values using similar data points.

- **B) Multiple Imputation by Chained Equations (MICE)** ✓
  - MICE creates multiple datasets with different plausible values for missing data.

- **C) Forward fill for time series data** ✓
  - Forward fill replaces missing values with the most recent non-missing value in time series.

- **D) Always removing observations with any missing values** ✗
  - Complete-case analysis can introduce bias and lose valuable information.

- **E) Mean imputation always improves dataset accuracy** ✗
  - Mean imputation can distort relationships and reduce variance.

### Question 17
**Correct answers: A, B, E**

- **A) High bias leads to underfitting** ✓
  - High bias indicates oversimplified models that fail to capture patterns in the data.

- **B) High variance leads to overfitting** ✓
  - High variance indicates models too sensitive to training data, performing poorly on new data.

- **E) The goal is to find an optimal balance between bias and variance** ✓
  - The bias-variance tradeoff aims to minimize both errors for optimal generalization.

- **C) High bias implies the model fits training data very well** ✗
  - High bias actually results in poor training data fit (underfitting).

- **D) High variance means the model generalizes well to new data** ✗
  - High variance leads to poor generalization to new data (overfitting).

### Question 18
**Correct answers: A, B, C, E**

- **A) It minimizes within-cluster sum of squared distances to centroids** ✓
  - K-means iteratively updates cluster assignments to minimize this objective function.

- **B) Initial centroid selection can impact final clustering results** ✓
  - Different initial centroids can lead to different local optima in the final clustering.

- **C) It assumes clusters are spherical and equally sized** ✓
  - K-means performs best when clusters are convex, spherical, and similarly sized.

- **E) It is sensitive to outliers** ✓
  - Outliers can significantly affect centroid positions and clustering results.

- **D) It inherently handles missing values** ✗
  - K-means cannot process data points with missing values without pre-processing.

### Question 19
**Correct answers: A, B, C, E**

- **A) Log transformation can help reduce skewness in data** ✓
  - Log transformations compress high values and expand low values, reducing right skew.

- **B) One-hot encoding converts categorical variables to numerical form** ✓
  - One-hot encoding creates binary columns for each category in a categorical variable.

- **C) Creating interaction terms helps capture non-linear relationships** ✓
  - Interaction terms allow linear models to represent non-linear relationships between variables.

- **E) Standardizing features is useful for distance-based algorithms** ✓
  - Standardization ensures all features contribute equally to distance calculations.

- **D) Feature selection is unnecessary if all features contain information** ✗
  - Feature selection remains important to reduce noise, improve interpretability, and prevent overfitting.

### Question 20
**Correct answers: A, B, D**

- **A) Minimize chart elements like gridlines and decorations to reduce cognitive load** ✓
  - Simplified visualizations focus attention on the data rather than decorative elements.

- **B) Tailor visualizations to the audience's knowledge level** ✓
  - Effective visualizations consider the audience's familiarity with the subject matter.

- **D) Use redundant encoding (color + shape) to enhance clarity and accessibility** ✓
  - Redundant encoding ensures information is accessible to all users, including those with color vision deficiencies.

- **C) Adding 3D effects to bar charts improves data interpretation** ✗
  - 3D effects typically distort perception and make accurate comparisons more difficult.

- **E) Descriptive titles are unnecessary if axes are properly labeled** ✗
  - Descriptive titles provide essential context and improve understanding at first glance.
