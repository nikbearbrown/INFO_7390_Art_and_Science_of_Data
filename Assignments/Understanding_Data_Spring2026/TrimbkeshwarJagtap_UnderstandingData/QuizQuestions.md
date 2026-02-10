# Quiz Questions: Exploratory Data Analysis

**Author:** Trimbkeshwar  
**Course:** INFO 7390 - Understanding Data  
**Topic:** Exploratory Data Analysis (EDA)  
**Total Questions:** 15  
**Date:** January 2026

---

## Instructions

Each question has 4-5 multiple-choice options with one correct answer. Explanations are provided for both the correct answer and why other options are incorrect.

---

## Question 1: EDA Fundamentals

**Who is credited with pioneering Exploratory Data Analysis (EDA) and in what year was the foundational book published?**

A) Edward Tufte, 1983  
B) John Tukey, 1977  
C) William Cleveland, 1993  
D) Leland Wilkinson, 2005  

**Correct Answer: B**

**Explanation:**

John Tukey pioneered Exploratory Data Analysis and published his seminal book "Exploratory Data Analysis" in 1977. This work revolutionized statistical practice by emphasizing visual exploration and flexible investigation over rigid hypothesis testing.

**Why other options are incorrect:**
- **A)** Edward Tufte is famous for data visualization principles (particularly "The Visual Display of Quantitative Information" in 1983), but he did not pioneer EDA
- **C)** William Cleveland contributed to statistical graphics but came after Tukey's foundational work
- **D)** Leland Wilkinson developed the Grammar of Graphics (2005), which is important for visualization theory but not the origin of EDA

---

## Question 2: EDA vs CDA

**What is the primary difference between Exploratory Data Analysis (EDA) and Confirmatory Data Analysis (CDA)?**

A) EDA uses statistical tests while CDA uses visualizations  
B) EDA generates hypotheses from data while CDA tests predefined hypotheses  
C) EDA is only for categorical data while CDA is for numerical data  
D) EDA requires larger sample sizes than CDA  

**Correct Answer: B**

**Explanation:**

The fundamental distinction is that EDA is hypothesis-generating (discovering patterns and forming questions from data), while CDA is hypothesis-testing (using formal statistical tests to confirm or reject predefined hypotheses). EDA comes before CDA in the research process.

**Why other options are incorrect:**
- **A)** Both approaches use statistics and visualizations; the difference is in purpose, not tools
- **C)** Both EDA and CDA can handle any data type (categorical, numerical, mixed)
- **D)** Sample size requirements depend on the specific analysis, not whether it's exploratory or confirmatory

---

## Question 3: Measures of Central Tendency

**In a right-skewed distribution, what is the typical relationship between mean, median, and mode?**

A) Mean < Median < Mode  
B) Mode < Median < Mean  
C) Mean = Median = Mode  
D) Median < Mode < Mean  

**Correct Answer: B**

**Explanation:**

In a right-skewed (positively skewed) distribution, the tail extends to the right, pulling the mean in that direction. The mode is at the peak (leftmost), the median is in the middle, and the mean is pulled furthest right by extreme values. Therefore: Mode < Median < Mean.

**Why other options are incorrect:**
- **A)** This describes a left-skewed distribution where the tail extends left
- **C)** This describes a symmetric distribution (like normal distribution)
- **D)** This ordering doesn't match any standard distribution shape

---

## Question 4: Outlier Detection

**When using the Interquartile Range (IQR) method for outlier detection, values are considered outliers if they fall:**

A) Beyond Q1 - 1.5×IQR or Q3 + 1.5×IQR  
B) Beyond Mean - 2×SD or Mean + 2×SD  
C) Beyond the 5th and 95th percentiles  
D) More than 3 standard deviations from the median  

**Correct Answer: A**

**Explanation:**

The IQR method defines outliers as values that fall below Q1 - 1.5×IQR or above Q3 + 1.5×IQR, where IQR = Q3 - Q1. This is a robust method because it's based on quartiles rather than mean/standard deviation, making it less sensitive to outliers themselves.

**Why other options are incorrect:**
- **B)** This describes the z-score method (specifically the 2-sigma rule), not the IQR method
- **C)** While percentiles can be used for outlier detection, the 5th/95th percentiles are arbitrary thresholds, not the standard IQR method
- **D)** Standard deviations are measured from the mean, not median, and 3 SD is a different outlier detection approach (z-score method)

---

## Question 5: Correlation Coefficients

**What does a Pearson correlation coefficient of -0.85 indicate about the relationship between two variables?**

A) Strong positive linear relationship  
B) Strong negative linear relationship  
C) Weak negative relationship  
D) No relationship exists  

**Correct Answer: B**

**Explanation:**

The Pearson correlation coefficient ranges from -1 to +1. A value of -0.85 indicates a strong negative linear relationship, meaning as one variable increases, the other tends to decrease. The strength is determined by the absolute value (0.85, which is > 0.7), and the negative sign indicates the inverse direction.

**Why other options are incorrect:**
- **A)** The negative sign indicates an inverse relationship, not positive
- **C)** The magnitude of 0.85 indicates a strong relationship, not weak (weak would be |r| < 0.3)
- **D)** A correlation of -0.85 clearly shows a strong relationship; zero or near-zero would indicate no relationship

---

## Question 6: Skewness

**A dataset has a skewness value of +2.3. What does this indicate about the distribution?**

A) The distribution is symmetric  
B) The distribution has a long left tail  
C) The distribution has a long right tail  
D) The distribution is bimodal  

**Correct Answer: C**

**Explanation:**

Positive skewness indicates a right-skewed distribution with a long tail extending to the right. A skewness of +2.3 is substantially positive (|skew| > 1 is considered highly skewed), meaning the distribution has many extreme high values pulling the tail rightward.

**Why other options are incorrect:**
- **A)** Symmetric distributions have skewness near zero (approximately -0.5 to +0.5)
- **B)** Negative skewness would indicate a long left tail
- **D)** Skewness measures asymmetry, not the number of modes; bimodality requires examining the distribution shape directly

---

## Question 7: Missing Data Handling

**When should you consider dropping a variable entirely due to missing values?**

A) When any missing values exist  
B) When more than 50% of values are missing  
C) When exactly 20% of values are missing  
D) Never, always impute all missing data  

**Correct Answer: B**

**Explanation:**

When more than 50% of values are missing, the variable contains insufficient information and any imputation would be largely artificial. Dropping the variable is often the best choice. Alternatively, you might create a "has_variable" indicator variable to capture whether the value was present. The exact threshold can vary (some use 40%, others 60%), but 50% is a reasonable rule of thumb.

**Why other options are incorrect:**
- **A)** Dropping variables at the first sign of missing data is too strict; many datasets have some missingness that can be effectively handled
- **C)** 20% missing is often manageable with proper imputation techniques; there's no hard rule at exactly 20%
- **D)** Some variables with extreme missingness provide no useful information and should be dropped rather than heavily imputed

---

## Question 8: Visualization Selection

**Which visualization is MOST appropriate for showing the distribution of a single continuous numerical variable?**

A) Scatter plot  
B) Bar chart  
C) Histogram  
D) Heatmap  

**Correct Answer: C**

**Explanation:**

A histogram is specifically designed to show the distribution of a continuous numerical variable by dividing the data into bins and displaying the frequency of values in each bin. It reveals the shape, center, spread, and potential outliers of the distribution.

**Why other options are incorrect:**
- **A)** Scatter plots show relationships between TWO variables, not the distribution of one
- **B)** Bar charts are for categorical data or discrete counts, not continuous distributions
- **D)** Heatmaps show relationships across multiple variables (often correlation matrices), not univariate distributions

---

## Question 9: Data Types

**Which of the following is an example of ordinal categorical data?**

A) Customer ID numbers  
B) Blood type (A, B, AB, O)  
C) Education level (High School, Bachelor's, Master's, PhD)  
D) Email addresses  

**Correct Answer: C**

**Explanation:**

Education level is ordinal categorical data because the categories have a natural, meaningful order (High School < Bachelor's < Master's < PhD), but the distances between categories are not necessarily equal. You can rank ordinal data but cannot perform arithmetic operations.

**Why other options are incorrect:**
- **A)** Customer ID numbers are nominal identifiers with no inherent order
- **B)** Blood type is nominal categorical data—the types have no natural ordering
- **D)** Email addresses are nominal identifiers (text strings) with no meaningful order

---

## Question 10: Box Plot Interpretation

**In a box plot, what does the box itself represent?**

A) The full range of the data from minimum to maximum  
B) The middle 50% of the data (IQR)  
C) One standard deviation from the mean  
D) The 95% confidence interval  

**Correct Answer: B**

**Explanation:**

The box in a box plot represents the Interquartile Range (IQR), which contains the middle 50% of the data. The bottom of the box is Q1 (25th percentile), the line inside is the median (Q2, 50th percentile), and the top of the box is Q3 (75th percentile). The box thus spans from the 25th to 75th percentile.

**Why other options are incorrect:**
- **A)** The full range is shown by the whiskers and any outlier points beyond them, not the box
- **C)** Box plots are based on percentiles/quartiles, not mean and standard deviation
- **D)** Box plots show data distribution, not confidence intervals for estimates

---

## Question 11: Correlation vs Causation

**A study finds a strong positive correlation (r = 0.82) between ice cream sales and drowning deaths. What can we conclude?**

A) Ice cream consumption causes drowning  
B) Drowning causes increased ice cream sales  
C) There is a strong association, but correlation does not imply causation  
D) The correlation is spurious and meaningless  

**Correct Answer: C**

**Explanation:**

While there is a strong statistical association (r = 0.82), correlation does not establish causation. Both variables are likely influenced by a confounding variable—warm weather—which increases both ice cream consumption and swimming activity (leading to more drownings). This is a classic example of spurious correlation due to a hidden third variable.

**Why other options are incorrect:**
- **A)** Eating ice cream does not cause drowning; this confuses correlation with causation
- **B)** The causal direction is incorrect; drownings don't cause ice cream purchases
- **D)** The correlation is real and meaningful for prediction, but it reflects a shared cause (temperature/season) rather than direct causation

---

## Question 12: Sample Size and EDA

**Why is EDA particularly important before building models on small datasets (n < 100)?**

A) Small datasets don't need EDA  
B) Small datasets are more prone to outliers having disproportionate influence  
C) Visualizations don't work well with small datasets  
D) Statistical tests are invalid on small datasets  

**Correct Answer: B**

**Explanation:**

With small datasets, individual outliers or unusual observations can have disproportionate influence on model parameters and performance. EDA helps identify these influential points before they distort modeling results. Small datasets also provide less information, making each data point more critical to understand.

**Why other options are incorrect:**
- **A)** Small datasets actually need MORE careful EDA, not less, due to limited information
- **C)** Visualizations work fine with small datasets; in fact, they're easier to inspect thoroughly
- **D)** While some tests have power issues with small samples, many remain valid; this doesn't explain why EDA is important

---

## Question 13: Multicollinearity

**Two predictor variables have a correlation of r = 0.92. What problem does this create for regression modeling?**

A) Underfitting  
B) Multicollinearity  
C) Heteroscedasticity  
D) Non-normality  

**Correct Answer: B**

**Explanation:**

A correlation of 0.92 between predictors indicates severe multicollinearity—the predictors are highly correlated with each other. This makes it difficult to determine the individual effect of each predictor, inflates standard errors, and makes coefficient estimates unstable. One predictor should typically be dropped or the variables combined.

**Why other options are incorrect:**
- **A)** Underfitting refers to models that are too simple to capture patterns; it's unrelated to predictor correlation
- **C)** Heteroscedasticity refers to non-constant variance of residuals, not correlation between predictors
- **D)** Non-normality concerns the distribution of variables or residuals, not relationships between predictors

---

## Question 14: EDA Workflow

**In the systematic EDA workflow, which step should come FIRST?**

A) Build correlation matrices  
B) Create scatter plots for all variable pairs  
C) Load data and perform initial inspection (shape, types, head/tail)  
D) Impute missing values  

**Correct Answer: C**

**Explanation:**

The first step in EDA is always to load the data and perform initial inspection: check dimensions (rows/columns), preview first/last rows, examine data types, and verify successful loading. You need to understand the basic structure before proceeding to any analysis or preprocessing.

**Why other options are incorrect:**
- **A)** Correlation analysis comes later, after understanding data structure and quality
- **B)** Creating visualizations should come after initial inspection and quality checks
- **D)** You should assess missing values before deciding how to handle them; imputation isn't always the first step

---

## Question 15: Practical Application

**You discover that the 'Age' variable in your dataset has 25% missing values. Which approach is LEAST appropriate?**

A) Impute with median age by relevant subgroup (e.g., by gender)  
B) Impute with mean age across all observations  
C) Delete all rows with missing age  
D) Replace all missing values with 0  

**Correct Answer: D**

**Explanation:**

Replacing missing ages with 0 is inappropriate because 0 is not a plausible age for most datasets (except newborns), and it would introduce artificial outliers that distort analysis. Age = 0 would be treated as a real value, misleading any statistical analysis or modeling. This is the worst option among the choices.

**Why other options are incorrect (i.e., why they're more appropriate):**
- **A)** This is actually a good approach—imputing by subgroup preserves group-specific patterns
- **B)** While simple, mean imputation is a reasonable basic approach, better than using 0
- **C)** Deleting rows (listwise deletion) is acceptable when missing data is < 5-10% and MCAR (Missing Completely at Random), though not ideal at 25%

---

## Answer Key

| Question | Answer | Topic |
|----------|--------|-------|
| 1 | B | EDA History |
| 2 | B | EDA Fundamentals |
| 3 | B | Descriptive Statistics |
| 4 | A | Outlier Detection |
| 5 | B | Correlation |
| 6 | C | Skewness |
| 7 | B | Missing Data |
| 8 | C | Visualization |
| 9 | C | Data Types |
| 10 | B | Box Plots |
| 11 | C | Correlation vs Causation |
| 12 | B | Sample Size |
| 13 | B | Multicollinearity |
| 14 | C | EDA Workflow |
| 15 | D | Practical Application |

---

## Question Difficulty Distribution

- **Recall (Easy):** Questions 1, 4, 8, 9, 14 (5 questions)
- **Application (Medium):** Questions 2, 3, 5, 6, 7, 10, 12 (7 questions)
- **Analysis (Hard):** Questions 11, 13, 15 (3 questions)

---

## Topics Covered

✅ EDA History and Fundamentals  
✅ Descriptive Statistics (central tendency, dispersion, shape)  
✅ Outlier Detection Methods  
✅ Correlation and Relationships  
✅ Missing Data Handling  
✅ Data Types and Classification  
✅ Visualization Selection  
✅ Statistical Interpretation  
✅ Practical Application and Decision-Making  
✅ Common Pitfalls and Best Practices  

---

**End of Quiz Questions**