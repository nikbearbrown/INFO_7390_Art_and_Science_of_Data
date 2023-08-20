# Introduction to Causal Inference in Data Visualization

## Contents

- [What Is Causal Inference?](#what-is-causal-inference)
- [Case Study](#case-study)
- [Methods for Causal Inference in Data Visualization](#methods-for-causal-inference-in-data-visualization)
- [Importance of Causal Inference in Data Visualization](#importance-of-causal-inference-in-data-visualization)
- [Types of Causal Relationships](#types-of-causal-relationships)
- [Visual Techniques for Understanding Causality](#visual-techniques-for-understanding-causality)
- [Common Pitfalls in Causal Inference](#common-pitfalls-in-causal-inference)
- [Examples of Effective Data Visualizations Using Causal Inference](#examples-of-effective-data-visualizations-using-causal-inference)

 
## What Is Causal Inference?

Causal inference is the process of determining cause-and-effect relationships between variables.
Correlation is not causation.

- **Correlation vs Causation**: 
Correlation identifies a relationship between two variables. Causation is when one variable causes an outcome in the other.

- **Why It Matters**: Causal inference allows us to go beyond identifying correlations in data and pinpoint the exact variables responsible for different outcomes, making data-driven decision-making more accurate and effective.

 

## Case Study

A classic case study of correlational evidence turned on its head by looking at causation.

1. Identify Variables: Smoking & Lung Cancer
2. Observe Data: Collect data on smoking habits and lung cancer rates
3. Check for Correlations: Higher lung cancer rates among smokers
4. Control for Confounders: Exclude other potential causes
5. Establish Causality: Determine smoking as a primary cause
6. Visualize & Interpret: Use graphs to represent data

 

## Methods for Causal Inference in Data Visualization

- **Statistical Models**: Statistical models help establish causal relationships by controlling for extraneous variables and identifying confounding factors and other data biases.
- **Controlled Experiments**: Randomized experiments are ideal for causal inference since they allow for the manipulation of variables to determine cause-and-effect relationships.
- **Machine Learning**: Machine learning tools are used in causal inference by analyzing large amounts of data and identifying patterns and relationships between variables.


## Importance of Causal Inference in Data Visualization

- Beyond Correlation
- Informed Decision making
- Clarity in Complex Systems
- Facilitating Predictive Modeling
- Highlighting Confounders


## Types of Causal Relationships


- **Positive Causation**: An increase in the value of one variable leads to an increase in the value of the other.
- **Negative Causation**: An increase in the value of one variable leads to a decrease in the value of the other.
- **Spurious Correlation**: When two variables show a strong correlation, but there is no causal link.

## Visual Techniques for Understanding Causality


Visual techniques help us conceptualize and understand complex causal relationships in a more natural and effortless way.


- **Confounding**: Confounding occurs when an external factor (the confounder) affects both the independent variable (cause) and the dependent variable (effect), leading to a spurious association between them.
- **Causal Graphs**: Causal graphs are diagrams that depict variables as nodes and causal relationships as directed edges (arrows) between them.
- **Probability Distributions**: DAGs can represent joint probability distributions over the variables they include.

 

## Common Pitfalls in Causal Inference


- **Sampling Bias**: When data samples are not representative of the population being studied. This can lead to misleading conclusions and inaccurate causal relationships.
- **Confounding Variables**: Variables not directly accounted for in the analysis can create a spurious relationship or mask the true causal effect.
- **Reverse Causality**: Mistaking the effect for the cause, leading to misleading conclusions.
- **Overfitting**: Statistics used to generate a model can be too specific to that data set, leading to misleading conclusions and inaccurate causal relationships.


## Examples of Effective Data Visualizations Using Causal Inference

 

- **Before-and-After Comparisons**: Visual representations of how outcomes changed due to a change in one variable, such as weight loss.
- **Scatterplots**: Visualizing the relationship between two variables, such as the number of cups of coffee consumed and productivity.
- **Mapping**: Geographical visualizations that allow us to identify the relationship between location and outcomes like crime rates.


## References
- **1** :https://escholarship.org/uc/item/2183m2cz
- **2** :https://towardsdatascience.com/how-to-visualise-causal-inference-models-with-interactive-directed-acyclic-graphs-8dd648a64915