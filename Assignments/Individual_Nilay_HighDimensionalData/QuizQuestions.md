# Quiz Questions: Understanding High-Dimensional Data

**Author:** Nilay Raut  
**Course:** INFO 7390  
**Assignment:** Assignment 1  

## Instructions

This document contains 15 multiple-choice questions designed to assess understanding of dimensionality reduction techniques and their applications. Each question includes four options with detailed explanations.

---

## Section 1: Theoretical Foundations

### Question 1: Curse of Dimensionality
What is the primary challenge described by the "curse of dimensionality"?

A) High-dimensional data requires more storage space on disk
B) As dimensions increase, data points become increasingly sparse and distance metrics lose meaning
C) Higher dimensions always lead to better model performance
D) More dimensions mean longer variable names in code

**Answer: B**

**Explanation:** The curse of dimensionality refers to the phenomenon where, as the number of dimensions increases, data points become increasingly sparse in the high-dimensional space, and all points appear roughly equidistant from each other. This makes distance-based algorithms less effective and requires exponentially more samples to maintain the same data density. Option A is trivial (storage is not the main concern), option C is incorrect (more dimensions often hurt performance due to noise), and option D is not a mathematical concern.

---

### Question 2: Manifold Hypothesis
Which statement best describes the manifold hypothesis?

A) All high-dimensional data can be perfectly represented in 2D
B) High-dimensional data often lies on or near a lower-dimensional manifold embedded within the high-dimensional space
C) Dimensionality reduction always preserves 100% of the original information
D) The number of dimensions should always equal the number of samples

**Answer: B**

**Explanation:** The manifold hypothesis states that real-world high-dimensional data often lies on or near a lower-dimensional manifold (curved surface) within the high-dimensional space. This explains why dimensionality reduction works—the data has inherent lower-dimensional structure despite living in high dimensions. Option A is too strong (not always 2D), option C is impossible (some information is always lost), and option D is unrelated to the manifold hypothesis.

---

### Question 3: Covariance Matrix in PCA
What role does the covariance matrix play in Principal Component Analysis?

A) It stores the original pixel values of images
B) Its eigenvalues represent class labels for supervised learning
C) Its eigenvectors define the principal directions of maximum variance in the data
D) It is only used for data normalization before analysis

**Answer: C**

**Explanation:** In PCA, the covariance matrix (Σ) captures how different dimensions vary together. Its eigenvectors represent the principal directions (axes) along which the data has maximum variance, and the corresponding eigenvalues indicate the amount of variance in each direction. By selecting eigenvectors with the largest eigenvalues, PCA finds the most informative projections. Option A confuses covariance with raw data, option B incorrectly relates eigenvalues to labels (PCA is unsupervised), and option D misunderstands its fundamental role.

---

## Section 2: PCA - Principal Component Analysis

### Question 4: Explained Variance Calculation
In the MNIST analysis, the top 2 principal components explained 10.66% of the total variance. What does this percentage represent? (See **Analysis.ipynb**, Section 2.2.)

A) The classification accuracy achieved using only 2 dimensions
B) The proportion of total data variability captured by projecting onto the first 2 principal components
C) The error rate when reconstructing images from 2 components
D) The percentage of pixels that changed during dimensionality reduction

**Answer: B**

**Explanation:** Explained variance measures what proportion of the total variability in the data is captured by the selected principal components. The 10.66% means that projecting the 784-dimensional MNIST data onto the first 2 principal components preserves roughly 11% of the total variation, while the remaining ~89% is lost. Option A confuses variance with accuracy, option C describes reconstruction error (not explained variance), and option D misinterprets variance as pixel changes.

---

### Question 5: Standardization Before PCA
Why is it important to standardize (z-score normalization) data before applying PCA?

A) To make the algorithm run faster on modern computers
B) To ensure features with larger scales don't dominate the principal components
C) Standardization is optional and doesn't affect PCA results
D) To convert categorical variables into numerical format

**Answer: B**

**Explanation:** PCA finds directions of maximum variance, so features with larger numerical scales (e.g., income in dollars vs age in years) will naturally have larger variances and dominate the principal components. Standardization (subtracting mean and dividing by standard deviation) puts all features on the same scale, ensuring each contributes fairly. Option A is incorrect (standardization doesn't significantly affect speed), option C is wrong (it critically affects results), and option D confuses standardization with encoding.

---

### Question 6: Orthogonality of Principal Components
What is the significance of principal components being orthogonal (perpendicular) to each other?

A) Orthogonality ensures the components are correlated and redundant
B) It means the components capture independent, non-redundant directions of variance
C) Orthogonal components always separate data classes perfectly
D) It is a computational artifact with no mathematical meaning

**Answer: B**

**Explanation:** Orthogonality (perpendicularity) of principal components means they are uncorrelated—each component captures a unique, independent direction of variance in the data. This ensures no redundancy between components, maximizing information efficiency. Option A is backwards (orthogonality means uncorrelated, not correlated), option C overstates the claim (orthogonality doesn't guarantee class separation), and option D is incorrect (orthogonality is mathematically fundamental to PCA).

---

## Section 3: t-SNE - Manifold Learning

### Question 7: Perplexity Interpretation
In the MNIST analysis, t-SNE was run with perplexity=30. What does this parameter control?

A) The number of iterations for gradient descent optimization
B) The target number of dimensions in the output (2D or 3D)
C) The effective number of nearest neighbors each point considers, roughly 30 neighbors
D) The random seed for reproducibility of results

**Answer: C**

**Explanation:** Perplexity in t-SNE roughly corresponds to the effective number of nearest neighbors each point considers when computing probability distributions. A perplexity of 30 means each point treats approximately 30 nearby points as its "neighborhood" when preserving local structure. Option A confuses perplexity with iteration count, option B misunderstands it as output dimensionality, and option D confuses it with the random seed parameter.

---

### Question 8: Non-Deterministic Nature
Why does t-SNE produce different results on different runs, even with the same data?

A) The algorithm has bugs that cause inconsistent behavior
B) It uses random initialization and stochastic gradient descent, leading to different local optima
C) The perplexity parameter changes automatically between runs
D) t-SNE always produces identical results when properly implemented

**Answer: B**

**Explanation:** t-SNE initializes the low-dimensional positions randomly and uses gradient descent to optimize the KL divergence cost function. Since this optimization can get stuck in different local optima depending on initialization, each run produces a different (though often qualitatively similar) result. Option A is incorrect (it's by design, not a bug), option C is false (perplexity is fixed), and option D contradicts the non-deterministic nature documented in the chapter.

---

### Question 9: Computational Complexity
The chapter states t-SNE has O(n²) computational complexity. What does this mean for practical applications?

A) Processing time grows linearly with the number of data points
B) Doubling the dataset size roughly quadruples the computation time, limiting scalability
C) t-SNE is faster than PCA for large datasets
D) The complexity is only O(n²) for 2D projections, not 3D

**Answer: B**

**Explanation:** O(n²) complexity means the computation time grows quadratically with the number of samples (n). If you double the dataset size from 5,000 to 10,000 samples, the time increases by a factor of 4 (not 2). This makes t-SNE impractical for very large datasets (>10,000 samples), as seen in the chapter where t-SNE took ~120 seconds versus PCA's ~1 second. Option A describes O(n) not O(n²), option C is backwards (t-SNE is much slower), and option D incorrectly relates complexity to output dimensionality.

---

## Section 4: FinBERT - Neural Embeddings

### Question 10: Self-Attention Mechanism
In the transformer architecture used by FinBERT, what does the self-attention mechanism accomplish?

A) It compresses the vocabulary size to reduce memory usage
B) It allows each word to focus on (attend to) other relevant words in the sentence
C) It removes stop words automatically during preprocessing
D) It translates financial text from one language to another

**Answer: B**

**Explanation:** Self-attention is the core innovation of transformers that allows each word (token) to compute relationships with all other words in the input sequence. The mechanism uses Query, Key, and Value matrices to determine which words are relevant to each other, enabling the model to understand context. For example, in "quarterly profits rose significantly," self-attention helps "rose" attend to "profits" to understand what increased. Option A confuses attention with compression, option C describes preprocessing (not attention), and option D describes a translation task (not the mechanism itself).

---

### Question 11: Dense vs Sparse Embeddings
The chapter compares FinBERT's dense 768-dimensional embeddings to TF-IDF's sparse 100-dimensional vectors. What is the key difference?

A) Dense embeddings have all non-zero values capturing semantic meaning; sparse vectors have mostly zeros representing word presence
B) Dense means more dimensions, sparse means fewer dimensions
C) FinBERT embeddings are sparse, while TF-IDF embeddings are dense
D) There is no meaningful difference between dense and sparse embeddings

**Answer: A**

**Explanation:** Dense embeddings (like FinBERT's 768D vectors) have most or all values non-zero, with each dimension capturing abstract semantic features learned from data. Sparse embeddings (like TF-IDF's 100D vectors) have mostly zero values, with non-zero entries indicating word presence/frequency. FinBERT's dense representation enables semantic similarity (e.g., "profits rose" ≈ "earnings exceeded"), while TF-IDF only matches word overlap. Option B confuses density with dimensionality, option C reverses the methods, and option D ignores the fundamental representational difference.

---

### Question 12: Domain-Specific Pretraining
FinBERT was pretrained on financial text (news, reports, analyst statements) rather than general text. What advantage does this provide?

A) Domain pretraining makes the model smaller and faster
B) It eliminates the need for any fine-tuning on downstream tasks
C) The model learns financial jargon and context, enabling better understanding of domain-specific language
D) General BERT cannot process financial text at all

**Answer: C**

**Explanation:** Domain-specific pretraining exposes FinBERT to millions of financial documents, allowing it to learn that "bankruptcy protection" signals negative sentiment, "quarterly profits rose" indicates positive news, and "guidance" refers to earnings forecasts—nuances that general BERT might miss. This resulted in the 3.4× improvement (0.398 vs -0.163 silhouette score) over generic TF-IDF in the chapter's analysis. Option A is incorrect (size/speed are unchanged), option B overstates the benefit (fine-tuning still helps), and option D is false (general BERT can process financial text, just less effectively).

---

## Section 5: Comparative Analysis

### Question 13: Silhouette Score Interpretation
In the chapter's results, PCA achieved a silhouette score of -0.051 while FinBERT achieved 0.398. What does this difference indicate? (See **Chapter.md**, Figure 4 or **Analysis.ipynb**, Section 3.3.)

A) PCA is 0.398 times slower than FinBERT
B) FinBERT's embeddings create well-separated clusters, while PCA's projection shows poor cluster structure
C) Both methods achieved equally good results since the scores are close to zero
D) Silhouette scores are not meaningful for comparing dimensionality reduction methods

**Answer: B**

**Explanation:** Silhouette scores range from -1 to +1, measuring cluster quality. Negative scores (PCA: -0.051) indicate poor separation—points are closer to neighboring clusters than their own cluster. Positive scores (FinBERT: 0.398) indicate good separation—points are well-grouped with similar items. The 0.449 difference shows FinBERT captures semantic structure much better than PCA's linear projection for financial text. Option A confuses scores with speed, option C misinterprets negative vs positive scores, and option D is incorrect (silhouette scores are standard for comparing clustering quality).

---

### Question 14: Method Selection
A data scientist needs to visualize 50,000 customer reviews to identify complaint patterns for a presentation tomorrow. Which method should they choose? (See timing comparisons in **Analysis.ipynb**, Section 2.3.)

A) t-SNE, because it produces the best visualizations regardless of dataset size
B) PCA, because it's fast enough for 50,000 samples and provides interpretable components
C) FinBERT, because neural embeddings are always superior
D) Random projection, which wasn't covered in the chapter

**Answer: B**

**Explanation:** With 50,000 samples and a tight deadline, PCA is the best choice: it's fast (~seconds even for large datasets), deterministic (same result every run), and produces interpretable components. t-SNE would take hours or fail entirely at this scale (O(n²) complexity), despite producing better visualizations. FinBERT could work but requires GPU resources and more setup time. The decision framework in the chapter recommends PCA for fast, reproducible results with large datasets. Option A ignores scalability, option C ignores time constraints, and option D introduces an irrelevant method.

---

### Question 15: Speed vs Quality Tradeoff
Based on the chapter's comparative analysis, which statement best describes the speed-quality tradeoff?

A) Faster methods always produce lower quality results
B) PCA is fast (1s) but linear; t-SNE is slow (120s) but captures non-linear structure; neural methods balance both with GPU acceleration
C) There is no tradeoff—modern methods are both fast and high-quality
D) Quality doesn't matter if the method is fast enough

**Answer: B**

**Explanation:** The chapter demonstrates a clear tradeoff: PCA processed 5,000 MNIST images in ~1 second but achieved a poor silhouette score (-0.051) due to its linear nature. t-SNE took ~120 seconds but captured non-linear structure (0.125 score, 2.5× better). Neural embeddings like FinBERT achieve the best quality (0.398 score) but require significant compute—though GPU acceleration can make them competitive with t-SNE. Option A is too absolute (PCA can be sufficient for linear data), option C ignores the documented tradeoffs, and option D dismisses quality concerns inappropriately.

---

**End of Quiz Questions**