

## Section 2: Causal Inference

### Question 8

Which statements correctly describe the relationship between association and causation?

* [ ] A) Association between variables can exist without causation
* [ ] B) A strong association always implies causation
* [ ] C) Causation guarantees association in the absence of other causal factors
* [ ] D) Randomized experiments cannot distinguish association from causation
* [ ] E) Causal effects can be masked, creating a situation with causation but no apparent association

### Question 9

In the context of a causal diagram (DAG), when does conditioning on a variable introduce bias rather than reduce it?

* [ ] A) When conditioning on a collider
* [ ] B) When conditioning on a direct cause of the exposure
* [ ] C) When conditioning on a mediator when estimating total effects
* [ ] D) When conditioning on a descendant of a collider
* [ ] E) When conditioning on a common cause of exposure and outcome

### Question 10

For a conditionally randomized experiment, which methods can be used to estimate causal effects?

* [ ] A) Stratification by the conditioning variable
* [ ] B) Inverse probability weighting
* [ ] C) Standardization
* [ ] D) Simple difference in means without adjustment
* [ ] E) G-computation

### Question 11

Which statements about counterfactuals in causal inference are correct?

* [ ] A) Counterfactuals describe outcomes that would have occurred under different treatments
* [ ] B) Individual causal effects require comparing counterfactual outcomes
* [ ] C) Counterfactuals can be directly observed for each individual
* [ ] D) Counterfactuals form the basis for defining causal effects
* [ ] E) Counterfactual outcomes can be estimated without assumptions

### Question 12

In which scenarios is the frontdoor criterion applicable for estimating causal effects?

* [ ] A) When there are unmeasured confounders between treatment and outcome
* [ ] B) When an unconfounded mediator exists between treatment and outcome
* [ ] C) When treatment assignment is fully randomized
* [ ] D) When direct effects cannot be estimated using the backdoor criterion
* [ ] E) When the outcome directly causes the treatment

### Question 13

Which of the following are types of selection bias in causal inference?

* [ ] A) Self-selection into a study based on health status
* [ ] B) Loss to follow-up related to both treatment and outcome
* [ ] C) Healthy worker bias in occupational studies
* [ ] D) Random missing data in the outcome variable
* [ ] E) Analyzing only complete cases when missingness is related to exposure

### Question 14

Which statements about interaction and effect modification are correct?

* [ ] A) Additive interaction occurs when the joint effect of two exposures differs from the sum of their individual effects
* [ ] B) Effect modification and interaction are always equivalent concepts
* [ ] C) Qualitative effect modification occurs when effects go in opposite directions across strata
* [ ] D) Sufficient cause interaction implies biologic interaction at the mechanistic level
* [ ] E) Interaction can only be assessed on an additive scale

---

## Section 3: Machine Learning and Data Concepts

### Question 15

Which statements about the bias-variance tradeoff are correct?

* [ ] A) As model complexity increases, bias tends to decrease while variance increases
* [ ] B) The optimal model should always minimize bias regardless of variance
* [ ] C) Cross-validation helps identify the best balance between bias and variance
* [ ] D) Regularization techniques help manage the bias-variance tradeoff
* [ ] E) Ensemble methods always increase both bias and variance

### Question 16

For feature selection in machine learning, which approaches are valid?

* [ ] A) Filter methods based on statistical measures like correlation or mutual information
* [ ] B) Wrapper methods that evaluate feature subsets using the model performance
* [ ] C) Embedded methods like LASSO regression that incorporate feature selection within model training
* [ ] D) Selecting features based solely on their individual predictive power
* [ ] E) Always selecting the minimum number of features regardless of model performance

### Question 18

Which properties correctly describe Principal Component Analysis (PCA)?

* [ ] A) Principal components are orthogonal to each other
* [ ] B) The first principal component captures the direction of maximum variance
* [ ] C) PCA always improves classification performance
* [ ] D) Eigenvalues represent the amount of variance explained by each component
* [ ] E) Principal components have the same interpretation as the original features

### Question 20

Which visualization principles and techniques are effective for communicating complex data?

* [ ] A) Choosing chart types based on the specific data relationships you want to highlight
* [ ] B) Maximizing the data-ink ratio by removing all non-data elements
* [ ] C) Maintaining consistent scales when comparing multiple charts
* [ ] D) Using color strategically to emphasize important findings or group categories
* [ ] E) Always using 3D visualizations to impress the audience


Here are ONLY the questions from Exam #3 that match your INFO 7390 midterm topics (causal inference, stratification/balance, mediation/heterogeneity, DAGs/PS methods, PCA/collinearity, and data visualization).

---

## Section 2: Causal Inference

### Question 8

Which conditions are required for valid causal inference in observational studies?

* [ ] A) No unmeasured confounding between treatment and outcome
* [ ] B) Positivity (non-zero probability of each treatment for all covariate patterns)
* [ ] C) Consistency (well-defined interventions)
* [ ] D) Homogeneous treatment effects across all subpopulations
* [ ] E) Complete absence of measurement error

### Question 9

Which methods can help address unmeasured confounding in causal inference?

* [ ] A) Instrumental variable analysis
* [ ] B) Difference-in-differences designs
* [ ] C) Simple multivariate regression
* [ ] D) Sensitivity analysis for unmeasured confounders
* [ ] E) Increasing sample size without addressing confounding

### Question 10

In the context of mediation analysis, which statements are correct?

* [ ] A) Direct effects measure the impact of treatment not through the mediator
* [ ] B) Indirect effects capture the treatment effect that operates through the mediator
* [ ] C) Mediation analysis requires no additional assumptions beyond those for total effects
* [ ] D) Counterfactual definitions allow for decomposition of total effects
* [ ] E) Mediation analysis cannot be represented in causal diagrams

### Question 11

Which scenarios present threats to internal validity in causal inference studies?

* [ ] A) Differential attrition between treatment groups
* [ ] B) Limited generalizability to other populations
* [ ] C) Measurement error correlated with treatment assignment
* [ ] D) Spillover effects between treatment and control units
* [ ] E) Small sample size with adequate randomization

### Question 12

When working with causal diagrams (DAGs), which operations are valid?

* [ ] A) Determining minimally sufficient adjustment sets
* [ ] B) Identifying instrumental variables
* [ ] C) Testing for conditional independence implications
* [ ] D) Quantifying the magnitude of causal effects
* [ ] E) Proving causation from observational data without assumptions

### Question 13

Which statements about propensity score methods are correct?

* [ ] A) They estimate the probability of treatment given observed covariates
* [ ] B) They can be used for matching, stratification, or weighting
* [ ] C) They eliminate the need for the positivity assumption
* [ ] D) They help balance covariates between treatment groups
* [ ] E) They adjust for unmeasured confounders by design

### Question 14

Which principles apply to causal effect heterogeneity analysis?

* [ ] A) Effect modification can occur without interaction
* [ ] B) Subgroup analyses require no multiple testing adjustment
* [ ] C) Pre-specification of effect modifiers reduces false positives
* [ ] D) Additive interaction may exist without multiplicative interaction
* [ ] E) Post-hoc subgroup analyses have the same validity as pre-specified ones

---

## Section 3: Machine Learning and Data Concepts

### Question 15

Which techniques are appropriate for handling multicollinearity in regression models?

* [ ] A) Principal Component Regression
* [ ] B) Ridge Regression
* [ ] C) Increasing model complexity
* [ ] D) Feature selection to remove redundant predictors
* [ ] E) Ignoring correlation structure entirely

### Question 19

In the context of data visualization, which principles support effective communication?

* [ ] A) Aligning visualization type with the specific analytical question
* [ ] B) Using color intentionally to highlight patterns or categories
* [ ] C) Maximizing the number of variables displayed in a single visualization
* [ ] D) Providing clear context and labels for proper interpretation
* [ ] E) Prioritizing aesthetic appeal over information clarity

Here are ONLY the questions from Exam #3 that match your INFO 7390 midterm topics (causal inference, stratification/balance, mediation/heterogeneity, DAGs/PS methods, PCA/collinearity, and data visualization).

---

## Section 2: Causal Inference

### Question 8

Which conditions are required for valid causal inference in observational studies?

* [ ] A) No unmeasured confounding between treatment and outcome
* [ ] B) Positivity (non-zero probability of each treatment for all covariate patterns)
* [ ] C) Consistency (well-defined interventions)
* [ ] D) Homogeneous treatment effects across all subpopulations
* [ ] E) Complete absence of measurement error

### Question 9

Which methods can help address unmeasured confounding in causal inference?

* [ ] A) Instrumental variable analysis
* [ ] B) Difference-in-differences designs
* [ ] C) Simple multivariate regression
* [ ] D) Sensitivity analysis for unmeasured confounders
* [ ] E) Increasing sample size without addressing confounding

### Question 10

In the context of mediation analysis, which statements are correct?

* [ ] A) Direct effects measure the impact of treatment not through the mediator
* [ ] B) Indirect effects capture the treatment effect that operates through the mediator
* [ ] C) Mediation analysis requires no additional assumptions beyond those for total effects
* [ ] D) Counterfactual definitions allow for decomposition of total effects
* [ ] E) Mediation analysis cannot be represented in causal diagrams

### Question 11

Which scenarios present threats to internal validity in causal inference studies?

* [ ] A) Differential attrition between treatment groups
* [ ] B) Limited generalizability to other populations
* [ ] C) Measurement error correlated with treatment assignment
* [ ] D) Spillover effects between treatment and control units
* [ ] E) Small sample size with adequate randomization

### Question 12

When working with causal diagrams (DAGs), which operations are valid?

* [ ] A) Determining minimally sufficient adjustment sets
* [ ] B) Identifying instrumental variables
* [ ] C) Testing for conditional independence implications
* [ ] D) Quantifying the magnitude of causal effects
* [ ] E) Proving causation from observational data without assumptions

### Question 13

Which statements about propensity score methods are correct?

* [ ] A) They estimate the probability of treatment given observed covariates
* [ ] B) They can be used for matching, stratification, or weighting
* [ ] C) They eliminate the need for the positivity assumption
* [ ] D) They help balance covariates between treatment groups
* [ ] E) They adjust for unmeasured confounders by design

### Question 14

Which principles apply to causal effect heterogeneity analysis?

* [ ] A) Effect modification can occur without interaction
* [ ] B) Subgroup analyses require no multiple testing adjustment
* [ ] C) Pre-specification of effect modifiers reduces false positives
* [ ] D) Additive interaction may exist without multiplicative interaction
* [ ] E) Post-hoc subgroup analyses have the same validity as pre-specified ones

---

## Section 3: Machine Learning and Data Concepts

### Question 15

Which techniques are appropriate for handling multicollinearity in regression models?

* [ ] A) Principal Component Regression
* [ ] B) Ridge Regression
* [ ] C) Increasing model complexity
* [ ] D) Feature selection to remove redundant predictors
* [ ] E) Ignoring correlation structure entirely

### Question 19

In the context of data visualization, which principles support effective communication?

* [ ] A) Aligning visualization type with the specific analytical question
* [ ] B) Using color intentionally to highlight patterns or categories
* [ ] C) Maximizing the number of variables displayed in a single visualization
* [ ] D) Providing clear context and labels for proper interpretation
* [ ] E) Prioritizing aesthetic appeal over information clarity


Here are ONLY the questions from Exam #4 that match your INFO 7390 midterm topics (causal inference, mediation, longitudinal methods, MSM/IPW, selection bias, IVs, and sensitivity analysis).

---

## Section 2: Causal Inference

### Question 8

Which study designs can provide evidence for causal relationships?

* [ ] A) Randomized controlled trials with proper randomization
* [ ] B) Natural experiments with plausible as-if randomization
* [ ] C) Cross-sectional studies without controlling for confounders
* [ ] D) Difference-in-differences designs with parallel trends assumption
* [ ] E) Ecological studies correlating population-level variables

### Question 9

What assumptions are necessary for instrumental variable estimation of causal effects?

* [ ] A) The instrument affects the treatment (relevance)
* [ ] B) The instrument affects the outcome only through the treatment (exclusion restriction)
* [ ] C) The instrument is independent of unmeasured confounders
* [ ] D) Treatment effects must be homogeneous across all subpopulations
* [ ] E) The outcome must be continuous rather than binary

### Question 10

Which statements about marginal structural models (MSMs) and inverse probability weighting are correct?

* [ ] A) MSMs can handle time-varying treatments and confounders
* [ ] B) Inverse probability weighting creates a pseudo-population where treatment is unconfounded
* [ ] C) MSMs require fewer assumptions than standard regression approaches
* [ ] D) Extreme weights can lead to instability in causal effect estimates
* [ ] E) MSMs automatically adjust for unmeasured confounding

### Question 11

What are valid methods to address selection bias in causal inference?

* [ ] A) Inverse probability of censoring weights
* [ ] B) Bounds analysis for partially identified effects
* [ ] C) Simply restricting analysis to complete cases
* [ ] D) Multiple imputation methods with appropriate missingness assumptions
* [ ] E) Ignoring missing data patterns in randomized studies

### Question 12

Which statements about causal effects in longitudinal data are correct?

* [ ] A) Lagged variables can serve as controls for time-varying confounding
* [ ] B) Fixed effects models address time-invariant unobserved confounding
* [ ] C) Standard regression adjustment is sufficient for time-varying confounding
* [ ] D) G-methods can handle treatment-confounder feedback loops
* [ ] E) Longer follow-up always provides more robust causal estimates

### Question 13

In causal mediation analysis, which statements are correct?

* [ ] A) Natural direct and indirect effects require strong assumptions about cross-world counterfactuals
* [ ] B) Controlled direct effects can be identified under weaker assumptions than natural effects
* [ ] C) Baron and Kenny's approach accounts for exposure-mediator interactions
* [ ] D) Sensitive mediation analysis requires no unmeasured mediator-outcome confounding
* [ ] E) The sum of direct and indirect effects always equals the total effect

### Question 14

What are valid methods for sensitivity analysis in causal inference?

* [ ] A) E-values that quantify the minimum strength of unmeasured confounding needed to explain away an effect
* [ ] B) Modeling the potential impact of unmeasured confounders on effect estimates
* [ ] C) Simply comparing results from different study populations
* [ ] D) Bounding approaches that estimate worst-case scenarios under violations of assumptions
* [ ] E) Increasing sample size to eliminate need for sensitivity analysis



