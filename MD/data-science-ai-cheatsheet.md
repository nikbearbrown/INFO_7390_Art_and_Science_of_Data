## Model Evaluation and Selection

### Classification Metrics
- **Confusion Matrix**: Shows true positives, false positives, true negatives, false negatives
  - Cannot capture probabilistic predictions (only hard classifications)
  - Does not reflect model calibration
  - Can be used for multi-class classification
  - Provides insights for imbalanced datasets

### Bias-Variance Tradeoff
- **Bias**: Simplifying assumptions made by model
  - High bias leads to underfitting
  - Model performs poorly on training data
- **Variance**: Model's sensitivity to fluctuations in training data
  - High variance leads to overfitting 
  - Model performs well on training data but poorly on test data
- Goal is to find optimal balance between bias and variance

## Machine Learning Models

### Decision Trees
- Split nodes based on maximum information gain or minimum Gini impurity
- **Pruning**: Removing nodes with little predictive value
  - Pre-pruning: Stops tree growth early based on criteria
  - Post-pruning: Removes branches after tree is fully grown
  - Improves generalization to unseen data
  - Not based solely on reducing depth
- Used for both classification and regression
- Capture non-linear relationships

### Supervised Learning
- **Logistic Regression**: Useful for binary classification
- **Decision Trees**: Split data using entropy or Gini impurity
- **Neural Networks**: Can be used for both regression and classification
- **Linear Regression**: For continuous numerical values (not discrete data)

### Unsupervised Learning
- **K-Means Clustering**:
  - Minimizes within-cluster sum of squared distances
  - Assumes spherical, equally sized clusters
  - Choice of initial centroids impacts results
  - Sensitive to outliers
  - Doesn't inherently handle missing values
# Data Science and AI Comprehensive Cheat Sheet

## Causal Inference Fundamentals

### Core Concepts
- **Association vs. Causation**: 
  - Association: Pr[Y=1|A=1] ≠ Pr[Y=1|A=0]
  - Causation: Pr[Y^(a=1)=1] ≠ Pr[Y^(a=0)=1]
  - Y^(a) represents counterfactual outcome under treatment a

- **Counterfactuals**:
  - Individual causal effects: Y^(a=1) - Y^(a=0)
  - Population average causal effects: E[Y^(a=1)] - E[Y^(a=0)]
  - Joint counterfactual: Y^(a,e) - outcome if treatment components A=a and E=e

- **Causal Null Hypotheses**:
  - Sharp causal null: Y^(a=1) = Y^(a=0) for all individuals
  - Null of no average effect: E[Y^(a=1)] = E[Y^(a=0)]

### Identifiability Conditions
- **Consistency**: If A = a, then Y^a = Y (observed outcome equals counterfactual)
- **Exchangeability**: Y^a ⫫ A for all a (no unmeasured confounding)
- **Conditional Exchangeability**: Y^a ⫫ A | L for all a (no unmeasured confounding given L)
- **Positivity**: Pr[A=a | L=l] > 0 for all values l (all strata have chance of receiving treatment)

### Experimental Designs
- **Marginally Randomized Experiment**: Single randomization probability for all subjects
- **Conditionally Randomized Experiment**: Different randomization probabilities across strata

### Confounding
- **Backdoor Path**: Noncausal path between treatment and outcome with arrow pointing into treatment
- **Backdoor Criterion**: Identifiability exists if all backdoor paths can be blocked by conditioning on variables not affected by treatment
- **Confounding by Indication**: Treatment more likely prescribed to individuals at higher risk of outcome
- **Frontdoor Criterion**: Method to estimate causal effect when treatment-outcome relationship is confounded but mediated by unconfounded variable

### Causal Diagrams (DAGs)
- **Path**: Sequence of edges connecting two variables 
- **Collider**: Variable where two arrowheads on a path collide (A→Y←L)
- **Blocked Path**: Path containing conditioned noncollider or unconditioned collider
- **d-separation**: All paths between two variables are blocked
- **d-connectedness**: Variables are not d-separated

### Methods for Confounding Adjustment
- **G-Methods**:
  - G-formula, IP weighting, G-estimation
  - Estimate causal effects in entire population
- **Stratification-based Methods**:
  - Stratification, restriction, matching
  - Estimate associations in subsets defined by L

### Selection and Measurement Bias
- **Selection Bias**: Conditioning on common effects
- **Measurement/Information Bias**: Systematic differences due to measurement error
- **Healthy Worker Bias**: Including only subjects healthy enough to participate

### Effect Modification and Interaction
- **Effect Modification**: Treatment effect varies across levels of another variable M
  - Additive effect modification: E[Y^(a=1)-Y^(a=0) | M=1] ≠ E[Y^(a=1)-Y^(a=0) | M=0]
  - Multiplicative effect modification: Ratio of effects differs across strata of M
- **Interaction**: Effect of one treatment component depends on level of another component
  - Sufficient cause interaction: Components appear together in a sufficient cause

### Analysis Methods
- **Standardization**: Calculate marginal effects by weighted average over stratum-specific risks
- **Inverse Probability Weighting**: Weight individuals by inverse probability of treatment received
- **Difference-in-Differences**: Technique to account for unmeasured confounders under specific conditions
- **Intention-to-Treat vs. Per-Protocol Analysis**: 
  - ITT: Effect of treatment assignment regardless of adherence
  - Per-Protocol: Effect if all followed assigned treatment

## Transformer Architecture in Generative AI
- **Attention Mechanism**: Enables models to focus on relevant input tokens
- **Positional Encodings**: Incorporate sequence order information into transformers
- **Self-Attention**: Eliminates need for recurrent layers by allowing parallel processing
- **Multi-Head Attention**: Allows model to focus on different aspects of input simultaneously
- **Encoder-Decoder Architecture**: Used primarily in sequence-to-sequence tasks

## Large Language Models (LLMs)
- **Training Method**: Pre-trained on massive datasets, then fine-tuned for specific tasks
- **Learning Capabilities**: Can perform zero-shot, few-shot, and fine-tuned learning
- **Response Generation**: Generate contextually relevant responses based on pre-trained knowledge
- **Limitations**:
  - Prone to generating hallucinated or incorrect information
  - Training requires significant computational and energy resources
  - Struggle with long-term coherence in multi-turn conversations
  - Inherit biases from training datasets

## Retrieval-Augmented Generation (RAG)
- **Core Function**: Combines generative models with retrieval systems to improve factual accuracy
- **Components**: 
  - Retriever: Fetches relevant documents based on a query
  - Generator: Uses retrieved information plus model knowledge to generate responses
- **Benefits**: Allows integration of domain-specific external knowledge bases

## GenAI Project Lifecycle
- Includes a dedicated phase for augmenting models and building LLM-powered applications
- This phase focuses on enhancing model capabilities and leveraging them in applications

## Data Visualization
### Channels in Visualization
- **Definition**: Control how marks are perceived by mapping data variables to visual properties
- **Examples**: Size, color, position, saturation/opacity, area
- **Application**: Used for encoding both categorical and quantitative variables

### Visualization Analysis
- **Scatterplots**: Useful for showing relationships between variables
  - Positive slopes indicate positive correlations
  - Regression lines show trends but correlation ≠ causation
  - Outliers can be identified visually
- **Histograms**: 
  - Can use stacked bar format to represent multiple variables
  - Bar height represents sum of counts for each category
- **Boxplots**:
  - Shows distribution through quartiles (Q1, median, Q3)
  - Whiskers typically extend to 1.5 × IQR
  - Points beyond whiskers represent outliers
  - IQR (Interquartile Range) = Q3 - Q1
- **Density Plots**:
  - Show distribution of continuous variables
  - Overlapping areas represent similar distributions
  - Narrower curves indicate smaller variance
  - Peak density shows most common values
- **Hans Rosling Plots**:
  - Use bubbles to represent population size
  - Show data for multiple countries over time
  - Often encode multiple dimensions (not histograms)

### Principles of Effective Visualization
- **Simplicity**: Minimize chart elements like gridlines and excessive colors
- **Audience Adaptation**: Tailor visualizations to audience knowledge level
- **Redundant Encoding**: Use both color and shape for clarity and accessibility
- **Titles**: Include descriptive titles even when axes are labeled
- **Avoid 3D Effects**: These distort perception and reduce accuracy

## Statistics and Hypothesis Testing
### Central Limit Theorem
- Allows using normal distribution assumptions in hypothesis testing, even with non-normally distributed data
- Provides basis for confidence intervals and hypothesis testing regardless of population distribution

### t-Distribution
- Used when sample size is small and population standard deviation is unknown
- Symmetric and unimodal
- Has heavier tails than normal distribution (allows for outliers)
- Resembles normal distribution more closely as sample size increases

### Probability Distributions
- **Normal Distribution**: 
  - Symmetric, bell-shaped curve describing many natural phenomena
  - Most data clustered around the mean
- **Binomial Distribution**:
  - Models number of successes in fixed number of independent trials
  - Requires constant probability of success
- **Uniform Distribution**:
  - Gives equal probability to all outcomes in sample space
- **Poisson Distribution**:
  - Models random, independent events in fixed time/space interval
  - Not for predicting events over long time periods

### Bootstrap Methods
- Involves sampling with replacement from original dataset
- Can estimate confidence intervals for any statistic
- Assumes sample is representative of population
- Doesn't require minimum sample size but larger samples give more reliable results
- Not guaranteed to produce unbiased estimates

### Imbalanced Data
- Significantly affects the power of hypothesis tests
- Stratified sampling helps ensure representative samples

### Distance Metrics
- **Euclidean Distance**:
  - Measures straight-line distance between points in n-dimensional space
  - Sensitive to data scale
  - Requires numeric features
  - Not robust to outliers
  - Inappropriate for categorical data without transformation

## Causality and Causal Inference
### Key Concepts
- **Counterfactuals**: 
  - Describe hypothetical scenarios with different decisions/actions
  - Compare actual outcomes to potential outcomes under different treatments
  - Provide framework for estimating causal effects when interventions are infeasible

- **Confounders**: Variables that influence both treatment and outcome
- **Backdoor Criterion**: Ensures confounders are correctly adjusted for

### Examples of True Causality
- Drug reducing cholesterol by inhibiting specific enzyme pathways
- Airbags reducing fatalities in traffic accidents
- Increased school funding improving student performance through better resources

## Feature Engineering and Model Interpretation
### Dimensionality Reduction
- Reduces risk of overfitting
- Improves computational efficiency
- Simplifies understanding of model outputs

### Principal Component Analysis (PCA)
- Reduces dimensionality while preserving important variance
- Projects data onto orthogonal components
- Components ordered by amount of variance explained
- Sensitive to feature scale (requires standardization)
- Helps visualize high-dimensional data
- Works with numeric features, not categorical variables
- Does not guarantee class separability

### Feature Engineering Techniques
- Creating derived features (e.g., price per square foot)
- One-hot encoding categorical variables
- Binning continuous variables into categories
- Creating interaction terms between features
- Standardizing features for distance-based algorithms
- Log transformation to reduce skewness
- For time series: creating features for transaction frequency, time between events
- Feature selection still needed even if all features contain information

### Missing Data Handling
- **K-Nearest Neighbors (KNN) Imputation**: Estimates based on feature similarity
- **Multiple Imputation by Chained Equations (MICE)**: Creates multiple datasets with different plausible values
- **Forward Fill**: Common for time series, fills with most recent non-missing value
- Mean imputation doesn't always improve accuracy
- Removing missing data isn't always best approach

### Interpretable Models
- Causal structures enable counterfactual reasoning for "what-if" scenarios
- Causal knowledge helps models generalize across domains
- Correlation-based models fail with shifting distributions
- Causal models help identify confounding variables
