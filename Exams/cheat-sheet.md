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

# Causal Inference Fundamentals
## What is Causal Inference?
Causal inference is like being a detective for science! It's about figuring out whether one thing actually *causes* another thing to happen, not just whether they happen to occur together.

## Core Concepts

### Association vs. Causation
- **Association**: When two things tend to happen together, but we don't know if one causes the other.
  - **Example**: Students who eat breakfast tend to get better grades (they're associated), but that doesn't prove breakfast *causes* better grades.
  - **Math way**: Pr[Y=1|A=1] ≠ Pr[Y=1|A=0]
    - This means: The probability of an outcome (Y) when exposure (A) is present differs from when exposure is absent.

- **Causation**: When one thing actually *makes* another thing happen.
  - **Example**: Drinking water causes your thirst to be quenched.
  - **Math way**: Pr[Y^(a=1)=1] ≠ Pr[Y^(a=0)=1]
    - This means: The probability of the outcome in the imaginary world where everyone gets the treatment differs from the probability in the imaginary world where no one gets the treatment.

### Counterfactuals
Counterfactuals are "what if" scenarios that didn't actually happen.

- **Individual causal effects**: The difference in what would happen to the same person in two different realities.
  - **Example**: The difference in your test score if you studied versus if you didn't study.
  - **Math way**: Y^(a=1) - Y^(a=0)

- **Population average causal effects**: The average difference across an entire group.
  - **Example**: The average difference in test scores between a world where everyone studied and a world where no one studied.
  - **Math way**: E[Y^(a=1)] - E[Y^(a=0)]

- **Joint counterfactual**: What would happen if we changed two things at once.
  - **Example**: Your test score if you both studied AND got a good night's sleep.
  - **Math way**: Y^(a,e) - outcome if treatment components A=a and E=e

### Causal Null Hypotheses
These are scientific guesses that there is no causal effect.

- **Sharp causal null**: The treatment has absolutely no effect on anyone.
  - **Example**: Taking vitamin C has zero effect on cold duration for every single person.
  - **Math way**: Y^(a=1) = Y^(a=0) for all individuals

- **Null of no average effect**: The treatment might help some people and hurt others, but overall averages out to zero effect.
  - **Example**: A new teaching method helps visual learners but confuses auditory learners, resulting in no change in average test scores.
  - **Math way**: E[Y^(a=1)] = E[Y^(a=0)]

## Identifiability Conditions
These are the conditions we need to accurately determine cause and effect.

### Consistency
If someone actually received treatment A, then their observed outcome equals what would have happened in the hypothetical world where everyone got that treatment.

- **Example**: If Ali actually took the medicine, then Ali's observed recovery time equals what Ali's recovery time would have been in the hypothetical world where everyone took the medicine.
- **Math way**: If A = a, then Y^a = Y

### Exchangeability
The people who got the treatment and those who didn't are similar in all important ways that might affect the outcome.

- **Example**: In a perfect experiment, students randomly assigned to study with flashcards versus textbooks would be similar in intelligence, motivation, and other factors.
- **Math way**: Y^a ⫫ A for all a (the counterfactual outcomes are independent of treatment assignment)

### Conditional Exchangeability
People who got the treatment and those who didn't are similar within specific groups defined by certain characteristics.

- **Example**: Boys who took the medicine might not be similar to girls who didn't take it, but boys who took it are similar to boys who didn't, and girls who took it are similar to girls who didn't.
- **Math way**: Y^a ⫫ A | L for all a (counterfactual outcomes are independent of treatment assignment within levels of L)

### Positivity
Everyone has some chance of receiving each treatment option.

- **Example**: If we're studying the effect of basketball training on height, but only tall people are allowed on the basketball team, we violate positivity.
- **Math way**: Pr[A=a | L=l] > 0 for all values l (every group has a non-zero chance of receiving each treatment)

## Experimental Designs

### Marginally Randomized Experiment
Everyone has the same chance of getting the treatment, like flipping the same coin for each person.

- **Example**: Every student has a 50% chance of being assigned to the new teaching method, regardless of their age, gender, or ability.

### Conditionally Randomized Experiment
Different groups have different chances of getting the treatment.

- **Example**: Younger students might have a 60% chance of getting the new teaching method, while older students have a 40% chance.

## Confounding
Confounding happens when there's another factor that affects both the treatment and the outcome, making it look like there's a causal relationship when there might not be.

### Backdoor Path
A "path" that creates a false association between treatment and outcome.

- **Example**: People who exercise (treatment) tend to have lower heart disease risk (outcome). But people who exercise also tend to eat healthier (confounder), which independently lowers heart disease risk. This creates a "backdoor path" from exercise to heart disease through diet.

### Backdoor Criterion
A rule for identifying which variables we need to control for to get accurate causal estimates.

- **Example**: To properly estimate how exercise affects heart disease, we need to account for diet, smoking status, and age, because they affect both exercise habits and heart disease risk.

### Confounding by Indication
When people receive a treatment specifically because they're at high risk for the outcome.

- **Example**: People who take medicine for headaches are more likely to have headaches than people who don't take the medicine. This doesn't mean the medicine causes headaches!

### Frontdoor Criterion
A method for estimating causal effects when there's unmeasured confounding but there's a clear intermediary step.

- **Example**: We want to know if a medication (A) reduces death (Y), but doctors might prescribe it based on severity we can't measure. If we can measure how the medication affects blood pressure (M), and we know how blood pressure affects death with no confounding, we can estimate the medication's effect on death through its effect on blood pressure.

## Causal Diagrams (DAGs)
Directed Acyclic Graphs are like maps showing how variables affect each other with arrows.

### Path
A sequence of arrows connecting two variables.

- **Example**: In a diagram showing Age → Exercise → Heart Health, there's a path from Age to Heart Health through Exercise.

### Collider
When two arrows point to the same variable, like arrows "colliding."

- **Example**: In Exercise → Athletic Achievement ← Natural Talent, Athletic Achievement is a collider.

### Blocked Path
A path that doesn't create association between variables because of certain conditions.

- **Example**: The path Exercise → Athletic Achievement ← Natural Talent is blocked unless we specifically analyze groups based on Athletic Achievement.

### d-separation
When all paths between two variables are blocked, making them statistically independent.

- **Example**: If we don't account for diet, exercise and heart disease are not d-separated because there's an open path through diet.

### d-connectedness
When variables are not d-separated, meaning there's at least one open path between them.

- **Example**: Exercise and heart disease are d-connected if there's any unblocked path between them.

## Methods for Confounding Adjustment

### G-Methods
Advanced statistical techniques that estimate causal effects for entire populations.

- **G-formula**: Standardizes outcomes across treatment groups.
  - **Example**: Estimating average test scores if everyone studied, by calculating expected scores for each type of student and then averaging.

- **IP weighting**: Gives more weight to individuals who received unusual treatments for their characteristics.
  - **Example**: In a study of exercise and health, giving more statistical weight to sedentary health-conscious people and active unhealthy eaters, since they're less common.

- **G-estimation**: Estimates counterfactual outcomes by modeling how treatment affects outcomes.
  - **Example**: Modeling how each additional hour of study affects test scores, accounting for student characteristics.

### Stratification-based Methods

#### Stratification
Analyzing the treatment effect separately within groups that share similar characteristics.

- **Example**: Looking at the effect of a math app separately for students with high, medium, and low prior math scores.
- **In practice**: Calculate the effect within each group, then combine those estimates (weighted by group size) to get an overall effect.
- **When it works best**: When you have a small number of clearly defined groups that capture all important confounders.
- **Limitations**: Can be impractical with many confounding variables, as the number of strata grows exponentially.

#### Matching
Finding treated and untreated individuals who are similar in all important ways.

- **Example**: For each student who used the study app, find another student with similar grades, age, and motivation who didn't use the app.
- **In practice**: 
  - **1:1 Matching**: Each treated person is matched with exactly one untreated person.
  - **Propensity Score Matching**: Calculate the probability of treatment for each person based on their characteristics, then match people with similar probabilities.
  - **Nearest Neighbor Matching**: For each treated person, find the untreated person most similar to them.
- **When it works best**: When you have a lot of data and can find good matches for most treated individuals.
- **Limitations**: May discard data if good matches can't be found for some treated individuals.

#### Restriction
Limiting analysis to a subset of participants to eliminate confounding.

- **Example**: To study how coffee affects heart health without confounding by smoking, restrict the study to only non-smokers.
- **In practice**: Simply exclude certain groups from your analysis.
- **When it works best**: When focusing on a specific subpopulation is scientifically meaningful and eliminates major confounding.
- **Limitations**: Results only apply to the restricted population; may reduce sample size substantially.

## Observational Data
Studies where researchers observe what happens naturally without controlling who gets the treatment.

- **Example**: Analyzing existing school records to see if students who participated in after-school programs had better grades.
- **Challenges with observational data**:
  - **Self-selection**: People choose treatments based on factors we may not observe.
    - Example: Students who choose to participate in after-school programs might be more motivated.
  - **Unmeasured confounding**: Important factors affecting both treatment and outcome might not be recorded.
    - Example: Parental involvement might affect both program participation and grades.
  - **Missing data**: Incomplete records can bias results.
    - Example: Students who drop out might not have final grades recorded.
  - **Time-varying confounding**: Factors that change over time can be both causes and effects of treatment.
    - Example: Students might join programs because grades started dropping, then grades improve due to the program.

- **How to strengthen causal claims with observational data**:
  - Use multiple adjustment methods and see if results are consistent
  - Conduct sensitivity analyses to estimate how strong unmeasured confounding would need to be to explain away findings
  - Look for natural experiments where treatment assignment was somewhat random
  - Use instrumental variables that affect treatment but not outcomes directly

## Selection and Measurement Bias

### Selection Bias
When the relationship between treatment and outcome is distorted because of how participants were selected.

- **Example**: A study of how music lessons affect math skills that only includes students who stayed in music lessons for at least a year would miss students who quit because they weren't seeing benefits.

### Measurement/Information Bias
When there are systematic errors in how variables are measured.

- **Example**: If students self-report study time, those using the new study app might report longer times to please the researchers.

### Healthy Worker Bias
Including only subjects healthy enough to participate, which can distort results.

- **Example**: A study of job stress that only includes current employees would miss people who left due to high stress, making the workplace appear less stressful than it is.

## Effect Modification and Interaction

### Effect Modification
When the treatment effect varies across levels of another variable.

- **Additive effect modification**: The absolute difference in outcomes varies across groups.
  - **Example**: A study app might improve boys' test scores by 10 points but girls' scores by only 5 points.
  - **Math way**: E[Y^(a=1)-Y^(a=0) | M=1] ≠ E[Y^(a=1)-Y^(a=0) | M=0]

- **Multiplicative effect modification**: The ratio of effects differs across groups.
  - **Example**: A study app might double boys' study time but only increase girls' study time by 50%.

### Interaction
When the effect of one treatment component depends on the level of another component.

- **Sufficient cause interaction**: When components appear together in a sufficient cause.
  - **Example**: Neither studying alone nor getting enough sleep alone guarantees an A on the test, but doing both together guarantees an A.


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
