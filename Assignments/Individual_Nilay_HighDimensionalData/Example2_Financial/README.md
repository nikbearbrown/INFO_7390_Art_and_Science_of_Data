# Example 2: Financial Text Embeddings

**Author:** Nilay Raut  
**Course:** INFO 7390  

## Dataset Description

- **Source**: Manually curated financial news sentences
- **Size**: 20 sentences
- **Categories**: Positive (5), Negative (5), Neutral (5), Mixed (5)
- **Domain**: Financial sentiment analysis
- **Type**: Text data (English)

## Problem Statement

**Objective**: Compare traditional text representation (TF-IDF) with modern neural embeddings (FinBERT) for financial sentiment understanding.

**Research Questions**:
1. Can TF-IDF capture semantic similarity in financial text?
2. How does FinBERT represent nuanced financial sentiment?
3. Which method produces better separation of sentiment categories?

## Methodology

### Data Composition
Curated dataset includes:
- **Positive**: Earnings growth, stock surge, successful launches
- **Negative**: Bankruptcy, sales decline, regulatory issues
- **Neutral**: Meeting schedules, location info, dividend declarations
- **Mixed**: Revenue up but margins compressed, acquisition concerns

### Methods Applied

#### 1. TF-IDF (Term Frequency-Inverse Document Frequency)
- Traditional bag-of-words approach
- Captures word frequency patterns
- Ignores word order and context
- Sparse feature vectors
- Fast computation

#### 2. FinBERT (Financial BERT)
- Pre-trained transformer model
- Domain-specific (financial) language understanding
- Captures semantic relationships
- Dense 768-dimensional embeddings
- Context-aware representations

## Files Generated

- `financial_embeddings.py` - Complete executable code
- `financial_dataset.csv` - Curated financial sentences
- `method_comparison.png` - TF-IDF vs FinBERT visualization
- `similarity_heatmap.png` - Semantic similarity matrix
- `results_summary.csv` - Quantitative comparison

## How to Run

```bash
cd Example2_Financial
python financial_embeddings.py
```

**Note**: First run will download FinBERT model (~440MB) from Hugging Face.

**Requirements**: See parent directory `requirements.txt`

## Expected Results

### Clustering Quality (Silhouette Score)
- **TF-IDF**: Lower score indicating poor separation
- **FinBERT**: Higher score showing better sentiment clustering
- Improvement typically 200-400%

### Semantic Understanding
FinBERT recognizes that:
- "profits rose" and "earnings exceeded" are semantically similar
- "bankruptcy protection" and "debt crisis" share negative context
- Context matters: "margins compressed" is negative despite "increased revenue"

## Key Findings

1. **Dimensionality**: TF-IDF creates sparse ~100-dim vectors vs FinBERT's dense 768-dim embeddings

2. **Semantic Capture**: FinBERT understands synonyms and context; TF-IDF treats each word independently

3. **Sentiment Nuance**: FinBERT correctly identifies mixed sentiments ("revenue up BUT margins down"); TF-IDF struggles with negations and qualifiers

4. **Similarity Patterns**: FinBERT similarity matrix shows clear clustering by sentiment category

## Practical Applications

- **Sentiment Analysis**: Classify financial news as positive/negative/neutral
- **Document Retrieval**: Find semantically similar financial reports
- **Risk Detection**: Identify negative sentiment patterns in earnings calls
- **Trading Signals**: Extract actionable insights from news sentiment
- **Compliance Monitoring**: Detect concerning language patterns

## Technical Insights

### TF-IDF Limitations
- Vocabulary mismatch problem ("profit" ≠ "earnings")
- No understanding of negation ("not good" treated as positive)
- Word order ignored
- Cannot handle synonyms or paraphrasing

### FinBERT Advantages
- Contextualized embeddings
- Domain-specific training on financial corpus
- Handles complex linguistic structures
- Captures subtle sentiment shifts

## Model Information

**FinBERT-tone** (yiyanghkust/finbert-tone):
- Base: BERT-base-uncased
- Training: Financial news and reports
- Parameters: ~110 million
- Output: 768-dimensional dense vectors
- License: MIT

## Academic Context

This example demonstrates the paradigm shift from symbolic (word-level) to distributed (embedding-level) text representations. Neural embeddings capture latent semantic structures that traditional methods miss, enabling more sophisticated NLP applications.

---

**License**: Academic Use Only  
**Year**: 2026
