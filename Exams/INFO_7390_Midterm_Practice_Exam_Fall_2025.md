## Practice Exam Questions Fall 2025


### Question 1

Which statements correctly describe the relationship between association and causation?

* [ ] A) Association between variables can exist without causation
* [ ] B) A strong association always implies causation
* [ ] C) Causation guarantees association in the absence of other causal factors
* [ ] D) Randomized experiments cannot distinguish association from causation
* [ ] E) Causal effects can be masked, creating a situation with causation but no apparent association

### Question 2

Which statements about counterfactuals in causal inference are correct?

* [ ] A) Counterfactuals describe outcomes that would have occurred under different treatments
* [ ] B) Individual causal effects require comparing counterfactual outcomes
* [ ] C) Counterfactuals can be directly observed for each individual
* [ ] D) Counterfactuals form the basis for defining causal effects
* [ ] E) Counterfactual outcomes can be estimated without assumptions

### Question 3

In the context of a causal diagram (DAG), when does conditioning on a variable introduce bias rather than reduce it?

* [ ] A) When conditioning on a collider
* [ ] B) When conditioning on a direct cause of the exposure
* [ ] C) When conditioning on a mediator when estimating total effects
* [ ] D) When conditioning on a descendant of a collider
* [ ] E) When conditioning on a common cause of exposure and outcome

### Question 4

Which conditions are required for valid causal inference in observational studies?

* [ ] A) No unmeasured confounding between treatment and outcome
* [ ] B) Positivity (non-zero probability of each treatment for all covariate patterns)
* [ ] C) Consistency (well-defined interventions)
* [ ] D) Homogeneous treatment effects across all subpopulations
* [ ] E) Complete absence of measurement error

### Question 5

Which study designs can provide evidence for causal relationships?

* [ ] A) Randomized controlled trials with proper randomization
* [ ] B) Natural experiments with plausible as-if randomization
* [ ] C) Cross-sectional studies without controlling for confounders
* [ ] D) Difference-in-differences designs with parallel trends assumption
* [ ] E) Ecological studies correlating population-level variables

### Question 6

Which research designs allow for valid causal inference in the presence of unmeasured confounding?

* [ ] A) Regression discontinuity designs with a clear cutoff rule
* [ ] B) Instrumental variable designs with valid instruments
* [ ] C) Simple cross-sectional observational studies
* [ ] D) Difference-in-differences designs with parallel trends
* [ ] E) Case-control studies without adjustment

### Question 7

When working with causal diagrams (DAGs), which operations are valid?

* [ ] A) Determining minimally sufficient adjustment sets
* [ ] B) Identifying instrumental variables
* [ ] C) Testing for conditional independence implications
* [ ] D) Quantifying the magnitude of causal effects
* [ ] E) Proving causation from observational data without assumptions

### Question 8

Which statements about the backdoor criterion in causal inference are correct?

* [ ] A) It identifies sufficient adjustment sets to block all backdoor paths
* [ ] B) It requires a causal graph as input
* [ ] C) It guarantees identification even with unmeasured confounders
* [ ] D) Minimal sufficient adjustment sets may exclude some measured confounders
* [ ] E) It applies only to randomized experiments

### Question 9

Which statements about propensity score methods are correct?

* [ ] A) They estimate the probability of treatment given observed covariates
* [ ] B) They can be used for matching, stratification, or weighting
* [ ] C) They eliminate the need for the positivity assumption
* [ ] D) They help balance covariates between treatment groups
* [ ] E) They adjust for unmeasured confounders by design

### Question 10

What assumptions are necessary for valid application of propensity score methods?

* [ ] A) No unmeasured confounding (conditional exchangeability)
* [ ] B) Positivity (non-zero probability of each treatment for all covariate patterns)
* [ ] C) Consistency (well-defined interventions)
* [ ] D) Homogeneous treatment effects across all subgroups
* [ ] E) Normally distributed outcomes

### Question 11

For a conditionally randomized experiment, which methods can be used to estimate causal effects?

* [ ] A) Stratification by the conditioning variable
* [ ] B) Inverse probability weighting
* [ ] C) Standardization
* [ ] D) Simple difference in means without adjustment
* [ ] E) G-computation

### Question 12

In which scenarios is the frontdoor criterion applicable for estimating causal effects?

* [ ] A) When there are unmeasured confounders between treatment and outcome
* [ ] B) When an unconfounded mediator exists between treatment and outcome
* [ ] C) When treatment assignment is fully randomized
* [ ] D) When direct effects cannot be estimated using the backdoor criterion
* [ ] E) When the outcome directly causes the treatment

### Question 13

Which scenarios present threats to internal validity in causal inference studies?

* [ ] A) Differential attrition between treatment groups
* [ ] B) Limited generalizability to other populations
* [ ] C) Measurement error correlated with treatment assignment
* [ ] D) Spillover effects between treatment and control units
* [ ] E) Small sample size with adequate randomization

### Question 14

Which of the following are types of selection bias in causal inference?

* [ ] A) Self-selection into a study based on health status
* [ ] B) Loss to follow-up related to both treatment and outcome
* [ ] C) Healthy worker bias in occupational studies
* [ ] D) Random missing data in the outcome variable
* [ ] E) Analyzing only complete cases when missingness is related to exposure

### Question 15

What are valid methods to address selection bias in causal inference?

* [ ] A) Inverse probability of censoring weights
* [ ] B) Bounds analysis for partially identified effects
* [ ] C) Simply restricting analysis to complete cases
* [ ] D) Multiple imputation methods with appropriate missingness assumptions
* [ ] E) Ignoring missing data patterns in randomized studies

### Question 16

Which statements about marginal structural models (MSMs) and inverse probability weighting are correct?

* [ ] A) MSMs can handle time-varying treatments and confounders
* [ ] B) Inverse probability weighting creates a pseudo-population where treatment is unconfounded
* [ ] C) MSMs require fewer assumptions than standard regression approaches
* [ ] D) Extreme weights can lead to instability in causal effect estimates
* [ ] E) MSMs automatically adjust for unmeasured confounding

### Question 17

Which statements about causal effects in longitudinal data are correct?

* [ ] A) Lagged variables can serve as controls for time-varying confounding
* [ ] B) Fixed effects models address time-invariant unobserved confounding
* [ ] C) Standard regression adjustment is sufficient for time-varying confounding
* [ ] D) G-methods can handle treatment-confounder feedback loops
* [ ] E) Longer follow-up always provides more robust causal estimates

### Question 18

Which methodological challenges specifically affect causal inference with longitudinal data?

* [ ] A) Time-varying confounding affected by previous treatment
* [ ] B) Selection bias from informative loss to follow-up
* [ ] C) Inability to estimate lagged effects
* [ ] D) Treatment-confounder feedback loops
* [ ] E) Requirement for perfectly balanced repeated measures

### Question 19

In the context of mediation analysis, which statements are correct?

* [ ] A) Direct effects measure the impact of treatment not through the mediator
* [ ] B) Indirect effects capture the treatment effect that operates through the mediator
* [ ] C) Mediation analysis requires no additional assumptions beyond those for total effects
* [ ] D) Counterfactual definitions allow for decomposition of total effects
* [ ] E) Mediation analysis cannot be represented in causal diagrams

### Question 20

In causal mediation analysis, which statements are also correct?

* [ ] A) The product method requires no exposure-mediator interaction
* [ ] B) The controlled direct effect equals the natural direct effect in all cases
* [ ] C) Multiple mediators can be analyzed simultaneously using appropriate methods
* [ ] D) Sensitivity analysis can assess robustness to violations of the no unmeasured mediator–outcome confounding assumption
* [ ] E) Mediation analysis always requires randomized assignment of both exposure and mediator

### Question 21

Which principles apply to causal effect heterogeneity analysis?

* [ ] A) Effect modification can occur without interaction
* [ ] B) Subgroup analyses require no multiple testing adjustment
* [ ] C) Pre-specification of effect modifiers reduces false positives
* [ ] D) Additive interaction may exist without multiplicative interaction
* [ ] E) Post-hoc subgroup analyses have the same validity as pre-specified ones

### Question 22

What approaches can address violations of the positivity assumption in causal inference?

* [ ] A) Trimming the population to regions of common support
* [ ] B) Stabilized weights in inverse probability weighting
* [ ] C) Ignoring areas of limited overlap between treatment groups
* [ ] D) Transportability methods to extrapolate from areas with sufficient data
* [ ] E) Simply assuming positivity holds regardless of data patterns

---

## Section 3: Machine Learning and Data Concepts

### Question 23

Which statements about the bias–variance tradeoff are correct?

* [ ] A) As model complexity increases, bias tends to decrease while variance increases
* [ ] B) The optimal model should always minimize bias regardless of variance
* [ ] C) Cross-validation helps identify the best balance between bias and variance
* [ ] D) Regularization techniques help manage the bias–variance tradeoff
* [ ] E) Ensemble methods always increase both bias and variance

### Question 24

For feature selection in machine learning, which approaches are valid?

* [ ] A) Filter methods based on statistical measures like correlation or mutual information
* [ ] B) Wrapper methods that evaluate feature subsets using the model performance
* [ ] C) Embedded methods like LASSO regression that incorporate feature selection within model training
* [ ] D) Selecting features based solely on their individual predictive power
* [ ] E) Always selecting the minimum number of features regardless of model performance

### Question 25

Which techniques are appropriate for handling multicollinearity in regression models?

* [ ] A) Principal Component Regression
* [ ] B) Ridge Regression
* [ ] C) Increasing model complexity
* [ ] D) Feature selection to remove redundant predictors
* [ ] E) Ignoring correlation structure entirely

### Question 26

Which properties correctly describe Principal Component Analysis (PCA)?

* [ ] A) Principal components are orthogonal to each other
* [ ] B) The first principal component captures the direction of maximum variance
* [ ] C) PCA always improves classification performance
* [ ] D) Eigenvalues represent the amount of variance explained by each component
* [ ] E) Principal components have the same interpretation as the original features

### Question 27

In the context of unsupervised learning, which statements are valid?

* [ ] A) DBSCAN can identify clusters of arbitrary shapes
* [ ] B) K-means always finds the optimal global clustering solution
* [ ] C) Hierarchical clustering provides a dendrogram showing nested cluster relationships
* [ ] D) Dimensionality reduction techniques can improve clustering by removing noise
* [ ] E) Unsupervised learning always requires a predefined number of clusters

### Question 28

Which statements about ensemble methods in machine learning are correct?

* [ ] A) Bagging reduces variance by training models on bootstrap samples
* [ ] B) Boosting reduces bias by focusing on misclassified examples
* [ ] C) Random Forests always outperform single decision trees regardless of data characteristics
* [ ] D) Stacking combines multiple models by training a meta-learner on their predictions
* [ ] E) Ensemble methods always increase model complexity without improving performance

### Question 29

Which visualization principles and techniques are effective for communicating complex data?

* [ ] A) Choosing chart types based on the specific data relationships you want to highlight
* [ ] B) Maximizing the data-ink ratio by removing all non-data elements
* [ ] C) Maintaining consistent scales when comparing multiple charts
* [ ] D) Using color strategically to emphasize important findings or group categories
* [ ] E) Always using 3D visualizations to impress the audience

### Question 30

In the context of data visualization, which principles support effective communication?

* [ ] A) Aligning visualization type with the specific analytical question
* [ ] B) Using color intentionally to highlight patterns or categories
* [ ] C) Maximizing the number of variables displayed in a single visualization
* [ ] D) Providing clear context and labels for proper interpretation
* [ ] E) Prioritizing aesthetic appeal over information clarity


