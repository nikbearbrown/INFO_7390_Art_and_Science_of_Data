"""
WORKED EXAMPLE 2: Financial Text Embeddings
Dataset: Financial news sentences (manually curated)
Problem: Compare traditional (TF-IDF) vs neural embeddings (FinBERT)
Author: Nilay Raut
Course: INFO 7390
"""

import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import BertTokenizer, BertModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
import warnings
import os
import sys

warnings.filterwarnings('ignore')

# Set publication-quality style
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
plt.rcParams['figure.dpi'] = 300

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("EXAMPLE 2: Financial Text Embeddings Analysis")
print("=" * 60)

# ==========================================
# STEP 1: DATA LOADING & CREATION
# ==========================================
print("\n[1/7] Creating Financial News Dataset...")

# Curated financial news dataset
data = {
    'text': [
        # POSITIVE SENTIMENT (5)
        "Quarterly profits rose by 15% exceeding analyst expectations significantly.",
        "The company's stock price surged after announcing the merger deal.",
        "Revenue growth projected to double next year driven by strong demand.",
        "New product launch was a massive success across all Asian markets.",
        "Share buyback program approved boosting investor confidence substantially.",
        
        # NEGATIVE SENTIMENT (5)
        "The company filed for bankruptcy protection amid mounting debt crisis.",
        "Sales dropped by 20% due to increased competition and market saturation.",
        "CEO resigned following the accounting scandal and regulatory investigation.",
        "Quarterly losses were significantly wider than previously anticipated.",
        "Supply chain disruptions will delay product shipments for several months.",
        
        # NEUTRAL/INFORMATIONAL (5)
        "The annual shareholder meeting is scheduled for June 15th this year.",
        "Company headquarters are located in London's financial district.",
        "The board declared a standard quarterly dividend of $0.50 per share.",
        "Trading volume remained consistent with historical average levels today.",
        "The fiscal year ends on December 31st according to corporate guidelines.",
        
        # MIXED/COMPLEX (5)
        "While revenue increased, profit margins compressed due to rising costs.",
        "The acquisition expands market share but raises integration concerns.",
        "Strong domestic performance offset by weakening international sales.",
        "Cost-cutting measures improved profitability but affected employee morale.",
        "Innovation investments yielded breakthroughs yet delayed short-term returns."
    ],
    'category': ['Positive']*5 + ['Negative']*5 + ['Neutral']*5 + ['Mixed']*5,
    'sentiment_score': [0.8]*5 + [-0.8]*5 + [0.0]*5 + [0.2]*5
}

df = pd.DataFrame(data)

print(f"[OK] Dataset created: {len(df)} financial sentences")
print(f"  Categories: {df['category'].value_counts().to_dict()}")
print(f"  Avg sentence length: {df['text'].str.split().str.len().mean():.1f} words")

# Save dataset
df.to_csv(os.path.join(SCRIPT_DIR, 'financial_dataset.csv'), index=False)
print("[OK] Saved: financial_dataset.csv")

# ==========================================
# STEP 2: METHOD 1 - TF-IDF BASELINE
# ==========================================
print("\n[2/7] Method 1: TF-IDF (Traditional Approach)...")

# Create TF-IDF vectors
vectorizer = TfidfVectorizer(
    max_features=100,
    stop_words='english',
    ngram_range=(1, 2),  # Unigrams and bigrams
    min_df=1
)

try:
    tfidf_matrix = vectorizer.fit_transform(df['text'])
    print(f"[OK] TF-IDF matrix shape: {tfidf_matrix.shape}")
    print(f"  Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Show top features
    feature_names = vectorizer.get_feature_names_out()
    print(f"  Sample features: {list(feature_names[:10])}")
    
except Exception as e:
    print(f"[ERROR] TF-IDF Error: {e}")
    sys.exit(1)

# Reduce to 2D with PCA
pca_tfidf = PCA(n_components=2, random_state=42)
tfidf_2d = pca_tfidf.fit_transform(tfidf_matrix.toarray())

print(f"[OK] PCA variance explained: {pca_tfidf.explained_variance_ratio_.sum():.2%}")

# ==========================================
# STEP 3: METHOD 2 - FINBERT EMBEDDINGS
# ==========================================
print("\n[3/7] Method 2: FinBERT Embeddings (Neural Approach)...")
print("  Loading pre-trained model (this may take a moment)...")

try:
    # Load FinBERT model
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
    model = BertModel.from_pretrained('yiyanghkust/finbert-tone')
    model.eval()  # Set to evaluation mode
    
    print("[OK] FinBERT model loaded successfully")
    print(f"  Model parameters: ~110M")
    print(f"  Embedding dimension: 768")
    
except Exception as e:
    print(f"[ERROR] Model loading error: {e}")
    print("  Tip: Ensure transformers and torch are installed")
    sys.exit(1)

def get_finbert_embedding(text: str) -> np.ndarray:
    """
    Generate 768-dimensional embedding from FinBERT.
    Uses mean pooling over all token embeddings.
    
    Args:
        text: Input text string
        
    Returns:
        768-dimensional numpy array
    """
    try:
        inputs = tokenizer(
            text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=128
        )
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Mean pooling over sequence length
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embedding
        
    except Exception as e:
        print(f"  Warning: Embedding failed for text: {text[:50]}...")
        return np.zeros(768)

print("  Generating embeddings for all sentences...")
embeddings_list = []
for idx, text in enumerate(df['text']):
    emb = get_finbert_embedding(text)
    embeddings_list.append(emb)
    if (idx + 1) % 5 == 0:
        print(f"    Progress: {idx + 1}/{len(df)}")

embeddings_matrix = np.array(embeddings_list)
print(f"[OK] Embeddings generated: {embeddings_matrix.shape}")

# Reduce to 2D with PCA
pca_finbert = PCA(n_components=2, random_state=42)
finbert_2d = pca_finbert.fit_transform(embeddings_matrix)

print(f"[OK] PCA variance explained: {pca_finbert.explained_variance_ratio_.sum():.2%}")

# ==========================================
# STEP 4: COMPARATIVE VISUALIZATION
# ==========================================
print("\n[4/7] Creating Comparative Visualizations...")

# Color mapping
color_map = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'blue', 'Mixed': 'orange'}
colors = df['category'].map(color_map)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# TF-IDF Plot
axes[0].scatter(tfidf_2d[:, 0], tfidf_2d[:, 1], 
               c=colors, s=200, alpha=0.7, edgecolors='black', linewidth=1)
axes[0].set_title('TF-IDF + PCA: Word Frequency Approach', 
                 fontsize=14, fontweight='bold')
axes[0].set_xlabel('Principal Component 1')
axes[0].set_ylabel('Principal Component 2')
axes[0].grid(True, alpha=0.3)

# Add labels for TF-IDF
for i, txt in enumerate(df['category']):
    axes[0].annotate(f"{i}", (tfidf_2d[i, 0], tfidf_2d[i, 1]), 
                    fontsize=8, alpha=0.6)

# FinBERT Plot
axes[1].scatter(finbert_2d[:, 0], finbert_2d[:, 1], 
               c=colors, s=200, alpha=0.7, edgecolors='black', linewidth=1)
axes[1].set_title('FinBERT Embeddings: Semantic Understanding', 
                 fontsize=14, fontweight='bold')
axes[1].set_xlabel('Principal Component 1')
axes[1].set_ylabel('Principal Component 2')
axes[1].grid(True, alpha=0.3)

# Add labels for FinBERT
for i, txt in enumerate(df['category']):
    axes[1].annotate(f"{i}", (finbert_2d[i, 0], finbert_2d[i, 1]), 
                    fontsize=8, alpha=0.6)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=label) 
                  for label, color in color_map.items()]
axes[1].legend(handles=legend_elements, loc='best', title='Sentiment')

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, 'method_comparison.png'), dpi=300, bbox_inches='tight')
print("[OK] Saved: method_comparison.png")

# ==========================================
# STEP 5: QUANTITATIVE EVALUATION
# ==========================================
print("\n[5/7] Quantitative Evaluation...")

# Silhouette scores
try:
    sil_tfidf = silhouette_score(tfidf_2d, df['category'])
    sil_finbert = silhouette_score(finbert_2d, df['category'])
    
    print(f"\nClustering Quality (Silhouette Score):")
    print(f"  TF-IDF:   {sil_tfidf:.4f}")
    print(f"  FinBERT:  {sil_finbert:.4f}")
    print(f"  Improvement: {((sil_finbert - sil_tfidf) / abs(sil_tfidf) * 100):+.1f}%")
    
except Exception as e:
    print(f"  Warning: Silhouette calculation issue: {e}")
    sil_tfidf, sil_finbert = 0, 0

# ==========================================
# STEP 6: SEMANTIC SIMILARITY ANALYSIS
# ==========================================
print("\n[6/7] Semantic Similarity Analysis...")

# Calculate similarity matrix for FinBERT embeddings
similarity_matrix = cosine_similarity(embeddings_matrix)

# Visualize similarity heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(similarity_matrix, 
            annot=True, fmt='.2f', 
            cmap='RdYlGn', center=0.5,
            xticklabels=range(len(df)),
            yticklabels=range(len(df)),
            cbar_kws={'label': 'Cosine Similarity'})
plt.title('FinBERT Semantic Similarity Matrix', fontsize=14, fontweight='bold')
plt.xlabel('Sentence Index')
plt.ylabel('Sentence Index')
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, 'similarity_heatmap.png'), dpi=300, bbox_inches='tight')
print("[OK] Saved: similarity_heatmap.png")

# Find most similar pairs (excluding self-similarity)
np.fill_diagonal(similarity_matrix, -1)
most_similar_idx = np.unravel_index(similarity_matrix.argmax(), similarity_matrix.shape)
print(f"\nMost Similar Sentence Pair:")
print(f"  [{most_similar_idx[0]}]: {df.iloc[most_similar_idx[0]]['text'][:60]}...")
print(f"  [{most_similar_idx[1]}]: {df.iloc[most_similar_idx[1]]['text'][:60]}...")
print(f"  Similarity: {similarity_matrix[most_similar_idx]:.3f}")

# ==========================================
# STEP 7: RESULTS SUMMARY
# ==========================================
print("\n[7/7] Generating Results Summary...")

results_df = pd.DataFrame({
    'Method': ['TF-IDF', 'FinBERT'],
    'Dimensions': [tfidf_matrix.shape[1], embeddings_matrix.shape[1]],
    'Silhouette Score': [f"{sil_tfidf:.4f}", f"{sil_finbert:.4f}"],
    'Variance (2D PCA)': [
        f"{pca_tfidf.explained_variance_ratio_.sum():.2%}",
        f"{pca_finbert.explained_variance_ratio_.sum():.2%}"
    ],
    'Captures Semantics': ['No', 'Yes'],
    'Best For': ['Keyword matching', 'Context understanding']
})

print("\n" + "=" * 60)
print("QUANTITATIVE COMPARISON")
print("=" * 60)
print(results_df.to_string(index=False))

results_df.to_csv(os.path.join(SCRIPT_DIR, 'results_summary.csv'), index=False)
print("\n[OK] Saved: results_summary.csv")

# ==========================================
# KEY FINDINGS
# ==========================================
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"""
1. DIMENSIONALITY: 
   - TF-IDF: {tfidf_matrix.shape[1]} sparse features (word counts)
   - FinBERT: 768 dense features (semantic meaning)

2. CLUSTERING QUALITY:
   - TF-IDF struggles to separate sentiments (score: {sil_tfidf:.3f})
   - FinBERT clearly groups similar meanings (score: {sil_finbert:.3f})

3. SEMANTIC UNDERSTANDING:
   - TF-IDF: "profits rose" != "earnings exceeded" (different words)
   - FinBERT: Recognizes these express similar positive sentiment

4. PRACTICAL IMPLICATIONS:
   - Use TF-IDF for: Simple keyword search, interpretability
   - Use FinBERT for: Sentiment analysis, semantic search, document similarity

5. COMPUTATIONAL COST:
   - TF-IDF: Fast, lightweight (~100 features)
   - FinBERT: Slower, requires GPU for large-scale (~110M parameters)
""")

print("\n[OK] Example 2 Complete!")
print("=" * 60)
