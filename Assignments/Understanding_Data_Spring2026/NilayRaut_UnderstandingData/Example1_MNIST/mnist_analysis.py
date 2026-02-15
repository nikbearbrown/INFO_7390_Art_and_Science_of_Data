"""
WORKED EXAMPLE 1: MNIST Dimensionality Reduction
Dataset: MNIST Handwritten Digits
Problem: Compare PCA vs t-SNE for visualization and variance retention
Author: Nilay Raut
Course: INFO 7390
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Tuple, Optional
import warnings
import sys
import os

warnings.filterwarnings('ignore')

# Set publication-quality style
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
plt.rcParams['figure.dpi'] = 300

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("EXAMPLE 1: MNIST Dimensionality Reduction Analysis")
print("=" * 60)

# ==========================================
# STEP 1: DATA LOADING
# ==========================================
print("\n[1/6] Loading MNIST dataset...")
print("Source: OpenML (mnist_784)")
print("Description: 70,000 grayscale images of handwritten digits (0-9)")
print("Original dimensions: 28x28 pixels = 784 features")

try:
    # Load MNIST - use subset for computational efficiency
    mnist = fetch_openml('mnist_784', version=1, parser='auto', as_frame=False)
    X = mnist.data[:5000].astype('float64')  # 5000 samples
    y = mnist.target[:5000].astype('int')
    
    print(f"[OK] Loaded successfully")
    print(f"  Shape: {X.shape}")
    print(f"  Classes: {np.unique(y)}")
    print(f"  Memory: {X.nbytes / 1e6:.2f} MB")
    
except Exception as e:
    print(f"[ERROR] Error loading data: {e}")
    sys.exit(1)

# ==========================================
# STEP 2: DATA EXPLORATION
# ==========================================
print("\n[2/6] Initial Data Exploration...")

# Check for missing values
missing = np.isnan(X).sum()
print(f"Missing values: {missing} ({missing/X.size*100:.2f}%)")

# Visualize sample digits
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for idx, ax in enumerate(axes.flat):
    ax.imshow(X[idx].reshape(28, 28), cmap='gray')
    ax.set_title(f'Label: {y[idx]}')
    ax.axis('off')
plt.suptitle('Sample MNIST Digits', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, 'sample_digits.png'), dpi=300, bbox_inches='tight')
print("[OK] Saved: sample_digits.png")

# ==========================================
# STEP 3: DATA PREPROCESSING
# ==========================================
print("\n[3/6] Data Preprocessing...")

# Normalization: Scale pixel values to [0, 1]
X_normalized = X / 255.0
print(f"[OK] Normalized pixel values: [{X_normalized.min():.2f}, {X_normalized.max():.2f}]")

# Standardization for PCA (mean=0, std=1)
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X_normalized)
print(f"[OK] Standardized: mean={X_standardized.mean():.2e}, std={X_standardized.std():.2f}")

# ==========================================
# STEP 4: METHOD 1 - PCA (LINEAR)
# ==========================================
print("\n[4/6] Applying PCA (Linear Dimensionality Reduction)...")

# Full PCA to analyze variance
pca_full = PCA()
pca_full.fit(X_standardized)

# Calculate cumulative variance
cumvar = np.cumsum(pca_full.explained_variance_ratio_)

# Find components for 95% variance
n_95 = np.argmax(cumvar >= 0.95) + 1
print(f"[OK] Components for 95% variance: {n_95}/{X.shape[1]}")
print(f"  Compression ratio: {n_95/X.shape[1]:.1%}")
print(f"  Top 10 components explain: {cumvar[9]:.1%} of variance")

# Visualize variance explained
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Cumulative variance plot
ax1.plot(range(1, 51), cumvar[:50], 'b-', linewidth=2)
ax1.axhline(y=0.95, color='r', linestyle='--', label='95% Threshold')
ax1.axvline(x=n_95, color='g', linestyle='--', label=f'{n_95} components')
ax1.set_xlabel('Number of Principal Components')
ax1.set_ylabel('Cumulative Explained Variance')
ax1.set_title('PCA: Variance Retention Analysis')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Individual variance per component
ax2.bar(range(1, 21), pca_full.explained_variance_ratio_[:20], color='steelblue')
ax2.set_xlabel('Principal Component')
ax2.set_ylabel('Explained Variance Ratio')
ax2.set_title('Individual Component Contribution (Top 20)')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, 'pca_variance_analysis.png'), dpi=300, bbox_inches='tight')
print("[OK] Saved: pca_variance_analysis.png")

# PCA to 2D for visualization
pca_2d = PCA(n_components=2, random_state=42)
X_pca = pca_2d.fit_transform(X_standardized)
print(f"[OK] 2D PCA variance explained: {pca_2d.explained_variance_ratio_.sum():.2%}")

# ==========================================
# STEP 5: METHOD 2 - t-SNE (NON-LINEAR)
# ==========================================
print("\n[5/6] Applying t-SNE (Non-linear Manifold Learning)...")
print("  Note: This takes approximately 2-3 minutes...")

# Perplexity=30 balances local vs global structure for ~5k samples (van der Maaten, 2008)
tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000, verbose=0)
X_tsne = tsne.fit_transform(X_standardized)
print("[OK] t-SNE transformation complete")

# ==========================================
# STEP 6: COMPARATIVE VISUALIZATION
# ==========================================
print("\n[6/6] Creating Comparative Visualizations...")

# Side-by-side comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PCA Plot
scatter1 = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], 
                          c=y, cmap='tab10', 
                          alpha=0.6, s=20, edgecolors='none')
axes[0].set_title('PCA: Linear Dimensionality Reduction', 
                  fontsize=14, fontweight='bold')
axes[0].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.1%} variance)')
axes[0].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.1%} variance)')
axes[0].grid(True, alpha=0.3)

# t-SNE Plot
scatter2 = axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1], 
                          c=y, cmap='tab10', 
                          alpha=0.6, s=20, edgecolors='none')
axes[1].set_title('t-SNE: Non-linear Manifold Learning', 
                  fontsize=14, fontweight='bold')
axes[1].set_xlabel('t-SNE Dimension 1')
axes[1].set_ylabel('t-SNE Dimension 2')
axes[1].grid(True, alpha=0.3)

# Add shared colorbar
cbar = plt.colorbar(scatter2, ax=axes, orientation='vertical', pad=0.02)
cbar.set_label('Digit Class', rotation=270, labelpad=20)

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, 'method_comparison.png'), dpi=300, bbox_inches='tight')
print("[OK] Saved: method_comparison.png")

# ==========================================
# STEP 7: QUANTITATIVE EVALUATION
# ==========================================
print("\n" + "=" * 60)
print("QUANTITATIVE RESULTS")
print("=" * 60)

# Clustering quality
sil_pca = silhouette_score(X_pca, y)
sil_tsne = silhouette_score(X_tsne, y)

print(f"\nClustering Quality (Silhouette Score):")
print(f"  PCA:   {sil_pca:.4f}")
print(f"  t-SNE: {sil_tsne:.4f}")
print(f"  Winner: {'t-SNE' if sil_tsne > sil_pca else 'PCA'} "
      f"(+{abs(sil_tsne - sil_pca):.4f})")

# Save results summary
results_df = pd.DataFrame({
    'Method': ['PCA', 't-SNE'],
    'Dimensions': [2, 2],
    'Variance Explained': [f"{pca_2d.explained_variance_ratio_.sum():.2%}", "N/A"],
    'Silhouette Score': [f"{sil_pca:.4f}", f"{sil_tsne:.4f}"],
    'Computation Time': ['Fast (~1s)', 'Slow (~120s)'],
    'Best For': ['Quick exploration, preprocessing', 'Final visualization, publication']
})

print("\n" + results_df.to_string(index=False))
results_df.to_csv(os.path.join(SCRIPT_DIR, 'results_summary.csv'), index=False)
print("\n[OK] Saved: results_summary.csv")

# ==========================================
# KEY FINDINGS
# ==========================================
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"""
1. DIMENSIONALITY: Original 784 dimensions can be reduced to {n_95} 
   while retaining 95% of variance - an {(1-n_95/784):.1%} reduction.

2. LINEAR vs NON-LINEAR: 
   - PCA creates overlapping clusters (silhouette: {sil_pca:.3f})
   - t-SNE reveals clear digit separation (silhouette: {sil_tsne:.3f})
   - This proves MNIST has non-linear structure

3. PRACTICAL IMPLICATIONS:
   - Use PCA for: Feature reduction before classification
   - Use t-SNE for: Exploratory visualization, presentations

4. TRADE-OFFS:
   - PCA: Fast, deterministic, interpretable axes
   - t-SNE: Slow, non-deterministic, beautiful clusters
""")

print("\n[OK] Example 1 Complete!")
print("=" * 60)
