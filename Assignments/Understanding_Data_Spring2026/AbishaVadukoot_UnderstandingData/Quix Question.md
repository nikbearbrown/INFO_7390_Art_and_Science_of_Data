# Data Preparation and Interpretation - Multiple Choice Questions

## Question 1: What are the two foundational aspects that this chapter focuses on in data preparation?
A) Data integrity and data merging  
B) Data quality and distributional properties  
C) Missing values and outliers  
D) Temporal dependencies and high dimensionality

**Correct Answer: B**

**Explanation:** The chapter focuses specifically on data quality and distributional properties as foundational aspects: quality issues determine whether data accurately represents reality, while distributional properties determine which statistical methods can be validly applied. Options A and D mention other data preparation challenges that are acknowledged but not the focus of this chapter, while C mentions specific issues rather than the broader foundational aspects.

---

## Question 2: Which missing data mechanism is independent of both observed and unobserved data?
A) MAR (Missing at Random)  
B) MNAR (Missing Not at Random)  
C) MCAR (Missing Completely at Random)  
D) All missing data mechanisms are dependent on observed data

**Correct Answer: C**

**Explanation:** MCAR is defined as missingness that is independent of both observed and unobserved data, exemplified by randomly dropped test tubes. MAR depends on observed data, MNAR depends on unobserved values, making C the correct answer. Option D is incorrect as MCAR exists as an independent mechanism.

---

## Question 3: In the example of younger respondents skipping income questions regardless of their actual income, which missing data mechanism is illustrated?
A) MCAR (Missing Completely at Random)  
B) MAR (Missing at Random)  
C) MNAR (Missing Not at Random)  
D) None of the above

**Correct Answer: B**

**Explanation:** This scenario exemplifies MAR, where missingness depends on observed data but not on the missing values themselves. The missingness depends on age (observed) but not on the actual income value itself. If high earners specifically avoided the question, that would be MNAR instead.

---

## Question 4: Which missing data mechanism is described as nearly impossible to detect without domain knowledge?
A) MCAR  
B) MAR  
C) MNAR  
D) All mechanisms are equally detectable

**Correct Answer: C**

**Explanation:** MNAR depends on the unobserved values themselves (like high earners specifically avoiding income questions) and detecting it is nearly impossible without domain knowledge about why people might hide certain information. MCAR can be tested statistically, and MAR can be identified through understanding behavior, but MNAR requires specific domain knowledge about the reasons behind the missingness.

---

## Question 5: According to the document, why is a body temperature of 110°F significant in discussing data accuracy?
A) It represents the maximum possible human body temperature  
B) It is medically impossible and demonstrates the need for domain expertise in identifying accuracy issues  
C) It is a common data entry error  
D) It indicates a calibration issue with thermometers

**Correct Answer: B**

**Explanation:** This example illustrates how domain expertise is critical for identifying accuracy issues - a body temperature of 110°F is medically impossible. This shows how domain knowledge helps identify impossible values that indicate accuracy problems. While it might result from errors (C or D), the key point is recognizing it as impossible through medical expertise.

---

## Question 6: What is said about a transaction amount of $0 in terms of validity?
A) It is always invalid across all systems  
B) It is always valid in financial systems  
C) Its validity depends on context - invalid in sales but valid in returns/refunds  
D) It should always be treated as a missing value

**Correct Answer: C**

**Explanation:** A transaction amount of $0 might be invalid in a sales system but valid in a returns/refunds context. This exemplifies how validity depends entirely on context and that business rules define validity, not just statistical patterns. Options A and B are too absolute, and D misinterprets the issue.

---

## Question 7: What should be done with an extremely dissatisfied customer who has many support tickets and appears as an outlier?
A) Delete the record as it distorts the analysis  
B) Keep it as it's potentially the most important case to study  
C) Replace it with the median value  
D) Flag it for removal after statistical testing

**Correct Answer: B**

**Explanation:** An extremely dissatisfied customer with many support tickets isn't an outlier to delete but potentially the most important case to study. This emphasizes that valid extremes should be kept and that context determines whether outliers represent errors or valuable information. The other options suggest removal or modification, which would lose important insights about customer dissatisfaction.

---

## Question 8: Which statistical test is described as "most powerful for normality, especially with samples under 5,000"?
A) Kolmogorov-Smirnov  
B) Anderson-Darling  
C) Shapiro-Wilk  
D) Box-Cox

**Correct Answer: C**

**Explanation:** Shapiro-Wilk is identified as the most powerful test for normality, especially with samples under 5,000. Kolmogorov-Smirnov works for any distribution comparison, Anderson-Darling puts more weight on the tails, and Box-Cox is a transformation method, not a test.

---

## Question 9: What type of processes do log-normal distributions typically describe?
A) Additive processes with many small independent effects  
B) Multiplicative processes where growth occurs through percentage changes  
C) Time between independent events  
D) Count data with discrete values

**Correct Answer: B**

**Explanation:** Log-normal distributions describe multiplicative processes where growth occurs through percentage changes rather than fixed amounts, such as income and house prices. Normal distributions arise from additive processes (A), exponential distributions model time between events (C), and Poisson distributions describe count data (D).

---

## Question 10: What do bimodal distributions often indicate?
A) Data collection errors that need to be corrected  
B) The need for logarithmic transformation  
C) Mixture populations representing meaningful structure  
D) Violations of the Central Limit Theorem

**Correct Answer: C**

**Explanation:** Bimodal distributions often indicate mixture populations (such as satisfied vs. dissatisfied customers) and reflect meaningful structure rather than problems. Domain context reveals whether bimodality represents real subgroups that should be analyzed separately. Options A and B suggest treating it as a problem to fix, which contradicts the guidance that bimodal data can't be made unimodal and shouldn't be forced.

---

## Question 11: What is the typical sample size threshold mentioned for the Central Limit Theorem to provide protection against non-normality?
A) n > 10  
B) n > 20  
C) n > 30  
D) n > 100

**Correct Answer: C**

**Explanation:** The Central Limit Theorem provides a safety net with large samples (typically n > 30), where many parametric methods stay reasonably valid even with moderate departures from normality. This is the standard threshold mentioned for when parametric methods become more robust to violations of normality assumptions.

---

## Question 12: Which transformation is mentioned as extending Box-Cox to handle negative values?
A) Logarithmic transformation  
B) Square root transformation  
C) Yeo-Johnson transformation  
D) Power transformation

**Correct Answer: C**

**Explanation:** The Yeo-Johnson transformation extends Box-Cox to handle negative values. While logarithmic, square root, and power transformations are mentioned as common approaches, only Yeo-Johnson is identified as the specific extension that can accommodate negative values in the dataset.

---

## Question 13: If values above 110 are systematically missing (MNAR) from a truly normal variable with mean 100 and SD 15, what will the observed data appear to be?
A) Right-skewed with higher mean  
B) Left-skewed with lower mean and smaller variance  
C) Normally distributed but with higher variance  
D) Bimodal distribution

**Correct Answer: B**

**Explanation:** When high values are systematically missing (MNAR), the observed data will look left-skewed with a lower mean and smaller variance. This illustrates how missing data creates selection bias and distorts the apparent distribution. The missing high values cause leftward skew and reduce both the mean and variance compared to the true underlying distribution.

---

## Question 14: What is described as a "paradoxical effect" of measurement errors on distributions?
A) They always make distributions appear less normal  
B) They can sometimes make non-normal data appear more normal through the Central Limit Theorem  
C) They only affect the mean but not the variance  
D) They convert skewed distributions to bimodal distributions

**Correct Answer: B**

**Explanation:** Measurement errors can have a paradoxical effect: they add noise that sometimes makes non-normal data appear more normal through the Central Limit Theorem. This is counterintuitive because while errors generally distort data, the added randomness can actually help satisfy normality assumptions in some cases by introducing additional variation.

---

## Question 15: What creates the "tricky circular problem" in data preparation?
A) Large datasets require too much computational power to analyze  
B) You need clean data to assess distributions, but assessing quality issues is easier when you know the expected distribution  
C) Statistical tests always contradict domain expertise  
D) Transformations always change the meaning of the data

**Correct Answer: B**

**Explanation:** A circular problem exists because you need clean data to reliably assess distributions, but assessing quality issues is easier when you know what distribution to expect. Outlier detection methods assume distributions, imputation uses distributional assumptions, and breaking this circle requires domain knowledge. The other options don't capture this bidirectional dependency between data quality and distribution assessment.