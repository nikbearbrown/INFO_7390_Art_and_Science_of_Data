## SECTION 1: DATA PREPROCESSING (Questions 1-5)

Question 1: Feature Scaling
Which algorithm REQUIRES feature scaling for optimal performance?
A) Decision Trees
B) Random Forest
C) Logistic Regression
D) Naive Bayes
E) None of the above
Correct Answer: C) Logistic Regression
Explanation: Logistic Regression uses gradient descent optimization which is sensitive to feature scales. When features have different ranges (e.g., Age: 20-90, Income: 20,000-200,000), large-scale features dominate the gradient updates and small-scale features are effectively ignored. StandardScaler normalizes all features to mean=0, std=1, ensuring fair contribution and faster convergence. Tree-based algorithms (Decision Trees, Random Forest) use threshold-based splits that are scale-invariant.


Question 2: Train-Test Split Purpose
What is the primary purpose of splitting data into training and test sets?
A) To make the dataset smaller and easier to work with
B) To evaluate model performance on unseen data and detect overfitting
C) To balance the classes in imbalanced datasets
D) To speed up model training time
E) To create separate datasets for different algorithms
Correct Answer: B) To evaluate model performance on unseen data and detect overfitting
Explanation: The test set acts as a proxy for real-world data that the model has never seen. By holding out a portion of data during training and evaluating on it afterward, we can assess how well the model generalizes to new cases. If a model performs well on training data (98% accuracy) but poorly on test data (60% accuracy), it has overfit—memorizing training patterns that don't generalize. The train-test split is the fundamental technique for detecting overfitting and estimating real-world performance.

Question 3: Handling Missing Values
You have a continuous feature with null values. What is generally the most appropriate imputation strategy?
A) Drop all rows with missing values
B) Fill with 0
C) Fill with the mean or median of the feature
D) Fill with the maximum value
E) Leave as NaN (missing)
Correct Answer: C) Fill with the mean or median of the feature
Explanation: For continuous features with moderate missingness (<20%), imputation with mean or median is standard practice. Median is preferred if the feature has outliers (more robust), while mean works well for normally distributed data. This preserves all samples (important with only 10% missing), maintains the feature's central tendency, and allows algorithms to use the data. With 10% missing, dropping rows loses valuable information, while extreme values (0, max) or leaving as NaN causes algorithm errors or biases.

Question 4: One-Hot Encoding
When should you use One-Hot Encoding for a categorical variable?
A) When the variable has exactly 2 categories
B) When the variable has ordered categories (Low, Medium, High)
C) When the variable has unordered categories (Red, Blue, Green)
D) When the variable has more than 100 unique categories
E) Never; always use Label Encoding instead
Correct Answer: C) When the variable has unordered categories (Red, Blue, Green)
Explanation: One-Hot Encoding is appropriate for nominal (unordered) categorical variables like Color (Red, Blue, Green), Country (USA, Canada, Mexico), or Category types where no inherent ordering exists. It creates separate binary columns for each category, ensuring the model treats all categories equally without imposing false numerical relationships. For example, encoding Color as Red=0, Blue=1, Green=2 would incorrectly suggest Green > Blue > Red, which is meaningless. One-hot encoding avoids this by creating Color_Red, Color_Blue, Color_Green binary indicators.

Question 5: Stratified Sampling
What does stratified train-test splitting ensure?
A) Equal number of samples in training and test sets
B) Random distribution of all features across splits
C) Same class distribution (proportion) in both training and test sets
D) Faster model training by organizing data
E) Removal of outliers from the test set
Correct Answer: C) Same class distribution (proportion) in both training and test sets
Explanation: Stratified splitting (using stratify=y parameter) ensures that both training and test sets maintain the same proportion of each class as the original dataset. For example, if your data has 80% Class 0 and 20% Class 1, stratified splitting guarantees both train and test sets will have exactly 80-20 distribution. This is critical for imbalanced datasets where random splitting could produce inconsistent class distributions (train: 85-15, test: 75-25), leading to unreliable evaluation metrics and models that don't generalize well.

## SECTION 2: DATA VISUALIZATION (Questions 6-8)

Question 6: 
Which plot is MOST useful for visually assessing if a feature follows a normal distribution? 
A) Bar chart
B) Q-Q plot (Quantile-Quantile plot)
C) Scatter plot
D) Pie chart
E) Box plot
Correct Answer: B) Q-Q plot (Quantile-Quantile plot)
Explanation: A Q-Q plot is the gold standard for visually assessing normality. It plots sample quantiles against theoretical normal distribution quantiles. If data is normally distributed, points fall along a straight diagonal line. Deviations from the line indicate non-normality: S-curves suggest skewness, deviations at ends indicate heavy/light tails. While histograms with normal curve overlays provide intuition, Q-Q plots are more precise and better at detecting subtle departures from normality.

Question 7: 
In a correlation heatmap, what does a negative value   between Feature A and Feature B indicate?
A) Feature A and B are unrelated
B) Strong positive relationship: when A increases, B increases
C) Strong negative relationship: when A increases, B decreases
D) Feature A causes Feature B to decrease
E) 85% of values are negative
Correct Answer: C) Strong negative relationship: when A increases, B decreases
Explanation: A correlation of -0.85 indicates a strong negative (inverse) linear relationship. As Feature A increases, Feature B tends to decrease, and vice versa. The correlation coefficient ranges from -1 (perfect negative) to +1 (perfect positive), with 0 meaning no linear relationship. A value of -0.85 is close to -1, indicating a strong inverse association. Important: correlation measures association, not causation—we cannot conclude A causes B to change, only that they vary together inversely.

Question 8: 
What does a box plot primarily show?
A) The exact frequency of each value
B) The correlation between two variables
C) The median, quartiles, and outliers of a distribution
D) The probability density function
E) The time series trend over time
Correct Answer: C) The median, quartiles, and outliers of a distribution
Explanation: A box plot displays five key statistics: minimum (excluding outliers), first quartile (Q1/25th percentile), median (Q2/50th percentile), third quartile (Q3/75th percentile), and maximum (excluding outliers). The "box" spans Q1 to Q3 (interquartile range containing middle 50% of data), with a line at the median. "Whiskers" extend to min/max, and individual points beyond whiskers are outliers (typically beyond 1.5×IQR from quartiles). This compact visualization reveals distribution shape, central tendency, spread, and outliers simultaneously.

## SECTION 3: MACHINE LEARNING ALGORITHMS (Questions 9-12)

Question 9: Logistic Regression Output
What does Logistic Regression output for binary classification?
A) A continuous value between negative and positive infinity
B) A binary prediction (0 or 1) only
C) A probability between 0 and 1, which is then thresholded to produce a binary prediction
D) A distance to the decision boundary
E) A rank ordering of samples

Correct Answer: C) A probability between 0 and 1, which is then thresholded to produce a binary prediction
Explanation: Logistic Regression uses the sigmoid function to transform a linear combination of features (z = β₀ + β₁x₁ + ...) into a probability: P(y=1|x) = 1/(1 + e^(-z)). This probability ranges from 0 to 1. By default, if P ≥ 0.5, the model predicts class 1; otherwise, class 0. The threshold can be adjusted (e.g., 0.3 for higher sensitivity). This probabilistic output is valuable for risk stratification and decision-making beyond simple binary classification.

Question 10:
How does Random Forest make predictions?
A) Averages the predictions from multiple decision trees
B) Takes the majority vote from multiple decision trees
C) Uses the deepest tree's prediction
D) Selects the tree with highest training accuracy
E) Builds a single optimized decision tree

Correct Answer: B) Takes the majority vote from multiple decision trees
Explanation: Random Forest is an ensemble method that builds multiple decision trees (e.g., 100 trees), each trained on a bootstrapped sample of the data with random feature subsets at each split. For classification, when a new instance arrives, each tree votes for a class (0 or 1). The final prediction is the majority vote—whichever class gets more votes wins. For example, if 73 trees vote "disease" and 27 vote "no disease," the prediction is "disease" with 73% confidence. This voting mechanism reduces variance and makes the ensemble more robust than any single tree.

Question 11: 
You have a dataset with 95% Class 0 and 5% Class 1. Which metric is MOST appropriate for evaluation?
A) Accuracy
B) ROC-AUC (Area Under ROC Curve)
C) Mean Squared Error
D) R-squared
E) Training time

Correct Answer: B) ROC-AUC (Area Under ROC Curve)
Explanation: ROC-AUC is the best metric for imbalanced classification because it evaluates model performance across all classification thresholds and is insensitive to class distribution. It measures the model's ability to rank positive cases higher than negative cases. An AUC of 0.5 means random guessing, while 1.0 is perfect. Unlike accuracy (which would be 95% by always predicting Class 0), ROC-AUC cannot be "gamed" by predicting the majority class. Other good alternatives for imbalanced data: F1-Score, Precision-Recall AUC, or class-specific recall/precision.

Question 12: Overfitting
Which scenario indicates overfitting?
A) Training accuracy: 60%, Test accuracy: 62%
B) Training accuracy: 85%, Test accuracy: 83%
C) Training accuracy: 99%, Test accuracy: 55%
D) Training accuracy: 70%, Test accuracy: 70%
E) Training accuracy: 50%, Test accuracy: 50%

Correct Answer: C) Training accuracy: 99%, Test accuracy: 55%
Explanation: Overfitting occurs when a model learns training data too well, including noise and random fluctuations, causing poor generalization to new data. The dramatic gap (99% train vs 55% test) is a clear overfitting signature—the model has essentially memorized the training set but fails on unseen data. This often happens with overly complex models (deep decision trees, too many features) relative to dataset size. Solutions include regularization, reducing model complexity, increasing training data, or using ensemble methods.

## SECTION 4: Model Evaluation and Metrics 
Question 13: 
In a confusion matrix for disease prediction, what is a False Negative?
A) Predicted disease, actually no disease
B) Predicted no disease, actually has disease
C) Correctly predicted disease
D) Correctly predicted no disease
E) An error in the confusion matrix calculation

Correct Answer: B) Predicted no disease, actually has disease
Explanation: A False Negative (FN) occurs when the model predicts the negative class (no disease) but the patient actually has the disease. In medical contexts, false negatives are particularly dangerous because patients who need treatment are told they're healthy. They don't receive necessary interventions, potentially leading to serious health consequences. This is why medical screening models prioritize high recall (sensitivity)—minimizing false negatives is critical even if it means accepting more false positives.

Question 14: Precision vs Recall
A stroke screening model has 90% recall but only 30% precision. What does this mean?
A) The model is excellent; high recall means it's working well
B) The model catches 90% of stroke cases but has many false alarms (70% of stroke predictions are incorrect)
C) The model is 90% accurate overall with 30% error rate
D) 30% of patients have strokes in the dataset
E) The model should not be used because precision is below 50%

Correct Answer: B) The model catches 90% of stroke cases but has many false alarms (70% of stroke predictions are incorrect)
Explanation:

Recall = 90% means the model detects 90% of actual stroke cases (good—we're catching most patients who need help)
Precision = 30% means when the model predicts "stroke," it's only correct 30% of the time (concerning—70% are false alarms)

This trade-off is common in screening: by lowering the threshold to catch more true cases (high recall), we also flag many healthy patients (low precision). In medical screening, this might be acceptable—false alarms can be filtered through follow-up tests, but missing a stroke case could be fatal. The appropriate balance depends on the costs of false positives vs false negatives.

Question 15: 
Your model achieves an ROC-AUC of 0.52 on the test set. What does this indicate?
A) The model is performing excellently with 52% accuracy
B) The model has learned useful patterns and is performing well
C) The model is performing barely better than random guessing
D) The model is 52% confident in its predictions
E) 52% of predictions are correct

Correct Answer: C) The model is performing barely better than random guessing
Explanation: ROC-AUC (Area Under Receiver Operating Characteristic Curve) ranges from 0.5 to 1.0, where:

0.5 = Random classifier (coin flip)
0.7-0.8 = Acceptable discrimination
0.8-0.9 = Good discrimination
0.9-1.0 = Excellent discrimination

An AUC of 0.52 is only marginally better than 0.5 (random chance), indicating the model has barely learned to distinguish between classes. This suggests fundamental problems: weak features, data quality issues, or inappropriate algorithm choice. The model should not be deployed.

