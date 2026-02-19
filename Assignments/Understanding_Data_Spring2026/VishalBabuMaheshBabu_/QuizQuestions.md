# Part 4: Quiz Questions

Question 1: Which mechanism allows Lasso (L1 Regularization) to perform automatic feature selection, unlike Ridge (L2 Regularization)?

A) It uses a squared penalty term that shrinks coefficients asymptotically to zero.
B) It uses an absolute value penalty term whose geometric constraint (diamond shape) encourages coefficients to hit exactly zero.
C) It recursively removes features based on p-values.
D) It increases the variance of the model to capture more signal.

Correct Answer: B

Explanation: Lasso uses the L1 norm ($\lambda \sum |\beta_j|$). Geometrically, the constraint region is a diamond (polytope) with corners on the axes. The error contours of the loss function often intersect the constraint region exactly at these corners, setting the coefficient to zero. Ridge uses a circle/sphere (L2 norm), where the intersection almost never occurs exactly on the axis, shrinking coefficients but keeping them non-zero.

Question 2: In the context of Recursive Feature Elimination (RFE), what is the primary risk of its "greedy" search strategy?

A) It cannot handle categorical variables.
B) It assumes that a feature deemed unimportant in the early steps will remain unimportant, potentially discarding a feature that would be useful in a smaller subset.
C) It is computationally cheaper than Filter methods, leading to lower accuracy.
D) It always selects more features than necessary to ensure safety.

Correct Answer: B

Explanation: RFE is a greedy backward selection algorithm. If it removes a feature in step 1 because it seems weak in the presence of 100 other features, it cannot bring it back later. This monotonicity assumption is a key limitation; a feature might be weak individually but strong in a specific interaction that is only revealed after other noise is removed.

Question 3: You have a dataset with two perfectly correlated features, Feature A and Feature B ($Correlation = 1.0$). How does standard Lasso regression handle this situation?

A) It will assign equal weights to both features (e.g., 0.5 to A and 0.5 to B).
B) It will select both features and double the coefficients.
C) It will arbitrarily select one feature (assigning it the full weight) and set the coefficient of the other to zero.
D) It will crash or fail to converge.

Correct Answer: C

Explanation: This is a known instability of Lasso. In the presence of high multicollinearity, the Lasso objective function is indifferent to which of the correlated features is selected. It typically picks one randomly (or based on slight numerical differences) and zeroes the other. Elastic Net is often preferred to fix this (selecting both).

Question 4: Why is "Standardization" (Z-score scaling) a critical preprocessing step before applying Lasso Regularization?

A) To convert categorical data into numeric data.
B) To ensure the data follows a normal distribution for hypothesis testing.
C) To ensure the penalization is applied uniformly, preventing features with large numeric ranges from dominating the penalty term.
D) Standardization is not necessary for Lasso; it is only needed for PCA.

Correct Answer: C

Explanation: The Lasso penalty $\lambda \sum |\beta_j|$ treats all coefficients equally. If Feature X ranges from 0 to 0.1 and Feature Y ranges from 0 to 1000, Feature X needs a massive coefficient to impact the prediction. Lasso would heavily penalize this large coefficient, effectively unfairly suppressing Feature X just because of its scale. Standardization puts all features on the same scale ($mean=0, std=1$).

Question 5: Which of the following best describes the computational complexity difference between Lasso and RFE?

A) RFE is generally faster because it is a wrapper method.
B) Lasso is generally faster because it is solved via a single optimization problem (or path), whereas RFE requires retraining the model multiple times.
C) Both have identical complexity $O(N^2)$
D) RFE is faster on wide datasets ($P \gg N$), while Lasso is faster on long datasets ($N \gg P$).

Correct Answer: B

Explanation: Lasso (using algorithms like Coordinate Descent or LARS) solves the optimization problem efficiently. RFE is a wrapper that must fit the full model, rank features, remove the worst, and refit the model. If removing 1 feature at a time from $P$ features, RFE requires fitting the model $P$ times, making it much more computationally expensive.

Question 6: In a "Large P, Small N" scenario (more features than samples), which issue is most likely to occur if no feature selection is performed?

A) Underfitting due to high bias.
B) Overfitting, where the model learns random noise as signal.
C) The model will converge too quickly to a suboptimal solution.
D) The intercept term will become infinite.

Correct Answer: B

Explanation: This is the definition of the "Curse of Dimensionality." With more features than samples, the model has enough degrees of freedom to perfectly memorize the training data (including noise), leading to a model that fails to generalize (High Variance/Overfitting).

Question 7: What is the function of the hyperparameter $\alpha$ (or $\lambda$) in Lasso Regression?

A) It controls the learning rate of the gradient descent.
B) It determines the number of iterations for the solver.
C) It controls the strength of the regularization; a higher $\alpha$ forces more coefficients to zero.
D) It sets the threshold for the decision boundary in classification.

Correct Answer: C

Explanation: $\alpha$ controls the balance between the RSS (fitting the data) and the L1 Penalty (sparsity). As $\alpha \rightarrow \infty$, the penalty dominates, forcing all coefficients to zero (underfitting). As $\alpha \rightarrow 0$, the penalty vanishes, and Lasso becomes OLS (overfitting).

Question 8: If your goal is strictly "Model Interpretability" in a scientific context (finding the true causal drivers), why might you prefer RFE over Principal Component Analysis (PCA)?

A) PCA is computationally more expensive than RFE.
B) PCA creates new synthetic features (linear combinations) that have no physical meaning, whereas RFE selects a subset of the original, interpretable features.
C) RFE guarantees finding the global optimum feature set.
D) PCA only works on image data.

Correct Answer: B

Explanation: PCA projects data into a new space (Eigenvectors). "Principal Component 1" is a math abstraction (e.g., $0.3*Age + 0.4*Income - 0.2*Height$), which is hard to interpret causally. RFE keeps the original columns (e.g., "Income"), making it easier to say "Income drives the target."

Question 9: What is the purpose of using Cross-Validation (e.g., LassoCV) when performing feature selection?

A) To increase the size of the training set.
B) To determine the optimal regularization strength ($\alpha$) that minimizes error on unseen data, preventing "selection bias."
C) To visualize the coefficients in 2D space.
D) To convert a regression problem into a classification problem.

Correct Answer: B

Explanation: If we pick $\alpha$ based on the training set, we will likely pick a small $\alpha$ that overfits. LassoCV splits the data, trains on one part, and tests on the other for a range of $\alpha$ values. It selects the $\alpha$ that performs best on the validation data, ensuring the selected features are robust.

Question 10: In the context of the "Signal vs. Noise" problem, what does a "False Positive" represent?

A) The model failed to select a truly informative feature.
B) The model selected a noise feature, treating it as informative.
C) The model predicted the target value correctly.
D) The model predicted a negative class when it was positive.

Correct Answer: B

Explanation: In feature selection, the "Positive" class is "Selected Feature." A False Positive means the algorithm selected a feature (Positive) that was actually Noise (False). This reduces interpretability and adds variance.

Question 11: Which Scikit-Learn class allows you to use RFE with any estimator (not just Linear Regression)?

A) sklearn.feature_selection.SelectKBest
B) sklearn.feature_selection.RFE
C) sklearn.linear_model.Lasso
D) sklearn.decomposition.PCA

Correct Answer: B

Explanation: RFE is a meta-estimator (wrapper). It can accept any estimator that exposes a coef_ or feature_importances_ attribute (e.g., Random Forest, SVM, Logistic Regression), making it more flexible than Lasso, which is strictly a linear model.

Question 12: Why is Recall (Sensitivity) a crucial metric when evaluating a feature selection algorithm's performance on synthetic data?

A) It measures how many of the selected features were actually noise.
B) It measures the percentage of the true informative features that the algorithm successfully recovered.
C) It measures the speed of the algorithm.
D) It measures the accuracy of the final predictions.

Correct Answer: B

Explanation: Recall = $TP / (TP + FN)$. In this context, True Positives (TP) are the true signals found. False Negatives (FN) are true signals missed. High recall means the method successfully found all the "Signal" features, even if it also picked up some noise.

Question 13: When using Lasso, if the number of features $P$ is greater than the number of observations $N$ ($P > N$), what is the maximum number of features Lasso can select?

A) Infinite.
B) $P$ (All features).
C) $N$ (The number of samples).
D) $N^2$.

Correct Answer: C

Explanation: This is a theoretical property of the Lasso optimization problem. In the $P > N$ case, the Lasso solution is not unique, but the number of non-zero coefficients is bounded by the number of observations $N$. Elastic Net can overcome this limitation.

Question 14: In the Jupyter Notebook analysis, you observe that RFE selected a Noise feature as one of the "Top 5." What is the most likely reason?

A) The noise feature had a spurious (random) high correlation with the target in the specific training split used.
B) RFE is designed to select noise features.
C) You forgot to standardize the data.
D) The linear model used by RFE cannot handle noise.

Correct Answer: A

Explanation: "Spurious Correlation" is common in small sample sizes. A random noise vector might, by pure chance, align slightly with the target. Because RFE is greedy, if this noise looks slightly better than a real signal at step $K$, RFE will keep it. This highlights the need for larger $N$ or regularization within the RFE base estimator.

Question 15: Which of the following is considered an "Embedded Method" for feature selection?

A) RFE (Recursive Feature Elimination).
B) Filter Method (Correlation Threshold)
C) Lasso (L1 Regularization).
D) Forward Selection.

Correct Answer: C

Explanation: Filter methods select features before training (e.g., based on correlation). Wrapper methods use the model to search the feature space (e.g., RFE, Forward Selection). Embedded methods perform feature selection as part of the model training process itself; Lasso optimizes the weights and performs selection simultaneously during the gradient descent/optimization steps.