# Example 1: MNIST Dimensionality Reduction

**Author:** Nilay Raut  
**Course:** INFO 7390  

## Dataset Description

- **Source**: OpenML (mnist_784)
- **Size**: 5,000 samples (subset of 70,000)
- **Features**: 784 (28×28 pixel images)
- **Classes**: 10 digits (0-9)
- **Type**: Grayscale images, pixel values [0-255]

## Problem Statement

**Objective**: Compare linear (PCA) and non-linear (t-SNE) dimensionality reduction techniques for visualizing high-dimensional image data.

**Research Questions**:
1. How many principal components retain 95% of variance?
2. Does MNIST have non-linear structure that PCA cannot capture?
3. Which method produces better visual separation of digit classes?

## Methodology

### Data Preprocessing
1. **Normalization**: Scale pixel values from [0, 255] to [0, 1]
2. **Standardization**: Transform to zero mean and unit variance for PCA
3. **Sampling**: Use 5,000 samples for computational efficiency

### Methods Applied

#### 1. Principal Component Analysis (PCA)
- Linear dimensionality reduction
- Maximizes variance preservation
- Produces orthogonal components
- Fast computation (~1 second)

#### 2. t-Distributed Stochastic Neighbor Embedding (t-SNE)
- Non-linear manifold learning
- Preserves local neighborhood structure
- Minimizes KL divergence between high-D and low-D distributions
- Slower computation (~2-3 minutes)

## Files Generated

- `mnist_analysis.py` - Complete executable code
- `sample_digits.png` - Visual inspection of raw data
- `pca_variance_analysis.png` - Variance retention analysis
- `method_comparison.png` - Side-by-side PCA vs t-SNE
- `results_summary.csv` - Quantitative comparison

## How to Run

```bash
cd Example1_MNIST
python mnist_analysis.py
```

**Requirements**: See parent directory `requirements.txt`

## Expected Results

### Variance Retention
- **95% variance** retained with approximately 154/784 components (80% reduction)
- First 2 PCA components explain approximately 10-12% of total variance
- Diminishing returns after first 50 components

### Clustering Quality (Silhouette Score)
- **PCA**: Lower score (~0.05-0.10) due to linear projection limitations
- **t-SNE**: Higher score (~0.15-0.25) revealing non-linear structure
- Clear visual separation of digit clusters in t-SNE space

## Key Findings

1. **Dimensionality**: MNIST can be effectively compressed - 95% of variance captured by approximately 20% of original features

2. **Non-linear Structure**: t-SNE reveals hidden manifold structure that PCA misses, confirming non-linear relationships between pixel patterns

3. **Method Selection**:
   - **Use PCA when**: Need fast preprocessing, interpretable axes, or feeding into downstream algorithms
   - **Use t-SNE when**: Prioritizing visualization quality, exploring data structure, or creating publication figures

4. **Trade-offs**:
   - **PCA**: Fast, deterministic, mathematically interpretable
   - **t-SNE**: Slow, non-deterministic, better visual separation

## Practical Applications

- **Digit Recognition**: PCA can reduce feature space before classification
- **Anomaly Detection**: Compressed representation speeds up outlier detection
- **Data Visualization**: t-SNE helps humans understand cluster structure
- **Transfer Learning**: Low-dimensional embeddings for downstream tasks

## Academic Context

This example demonstrates the fundamental principle that real-world data often lies on low-dimensional manifolds embedded in high-dimensional space. Linear methods like PCA provide efficient approximations, while non-linear methods like t-SNE better capture intrinsic structure at higher computational cost.

---

**License**: Academic Use Only  
**Year**: 2026
