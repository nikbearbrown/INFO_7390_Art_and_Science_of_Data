# Federated Learning with Differential Privacy: HAR & Credit Risk Analysis

## Project Details

This project implements and analyzes Federated Learning (FL) with Differential Privacy (DP) on two real-world datasets: Human Activity Recognition (HAR) using smartphone sensor data and Credit Risk Assessment using German credit records. The analysis demonstrates privacy-preserving distributed machine learning by training models across simulated clients without centralizing raw data. Key contributions include: (1) comprehensive FedAvg implementation achieving 96%+ accuracy on HAR and 72%+ on credit risk despite non-IID data distributions, (2) quantitative privacy-accuracy tradeoff analysis showing ε-differential privacy costs 3-14% accuracy depending on privacy budget, (3) visual comparisons proving federated learning loses only 2-3% accuracy versus centralized training while preserving 100% data privacy, and (4) production-ready guidance for choosing privacy parameters (ε) based on regulatory requirements (GDPR, HIPAA). The work validates that privacy and performance can coexist in modern ML systems, making federated learning viable for healthcare, finance, and IoT applications where data cannot leave edge devices.

---

## Contents

### Notebooks
- **Analysis.ipynb** – Main analysis pipeline:
  - Data loading and non-IID partitioning (30 HAR subjects, 8 credit subjects)
  - FedAvg algorithm implementation with optional differential privacy
  - Centralized baseline for comparison
  - Convergence analysis and confusion matrices
  - Privacy-accuracy tradeoff visualizations

### Datasets
- **Example1_Dataset/har_federated_extended_12classes.ipynb** – HAR data preprocessing and exploration (12 activity classes including transitions)
- **Example2_Dataset/** – Credit risk dataset (German credit records)

### Generated Outputs
- **federated_learning_results/** – Training curves, accuracy plots, confusion matrices
- **assets/** – High-resolution figures for publication
- **Chapter.pdf** – Comprehensive writeup with theory, methodology, and results

---

## How to Run the Analysis

1. **Clone and navigate to project directory:**
   ```bash
   cd Individual_JahnaviPatel_FederatedLearningAnalysis
   ```

2. **Install dependencies:**
   ```bash
   pip install tensorflow numpy pandas scikit-learn matplotlib seaborn plotly kaleido
   ```
   *(Use `tensorflow-macos` on Apple Silicon Macs)*

3. **Open Analysis.ipynb** in VS Code or Jupyter Notebook:
   ```bash
   jupyter notebook Analysis.ipynb
   ```

4. **Run cells sequentially** (execution time ~10-15 minutes):
   - **Section 1:** Load HAR and credit risk datasets
   - **Section 2:** Partition by subject ID into federated clients
   - **Section 3:** Train global and local models with FedAvg
   - **Section 4:** Compare against centralized baseline
   - **Section 5:** Add differential privacy and analyze tradeoff
   - **Section 6:** Generate visualizations and export results

5. **Outputs** automatically save to:
   - `federated_learning_results/` – Training metrics and plots
   - `assets/` – Publication-ready figures (PNG, 300 dpi)

---

## Key Results

| Metric | HAR Dataset | Credit Risk Dataset |
|--------|-------------|-------------------|
| Federated Accuracy | 96.1% | 72.3% |
| Centralized Accuracy | 98.5% | 74.8% |
| Privacy Cost (Standard FL) | 2.4% | 2.5% |
| DP Cost (ε=1.0) | 3.5% | 4.1% |
| Communication Rounds | 10 | 15 |
| Clients Simulated | 30 | 8 |

---

## Privacy Parameters Guide

| ε (Privacy Budget) | Privacy Level | Use Case | Accuracy Cost |
|------------------|---------------|----------|--------------|
| 0.5 | **STRONG** | Medical records, biometrics | 5-15% |
| 1.0 | **MODERATE** | Recommended for GDPR | 3-5% |
| 10.0 | **WEAK** | Non-sensitive learning | <1% |
| ∞ | **NONE** | Standard federated learning | 0% |

**Recommended:** ε=1.0 balances privacy guarantees with minimal accuracy loss for production systems.

---

## Technical Highlights

### Federated Averaging (FedAvg)
- Client selection: K clients per round from N total clients
- Local training: E epochs on private data
- Aggregation: Weighted averaging of model weights
- No raw data transmission—only ~3 MB weights vs. 40+ MB raw data

### Differential Privacy Implementation
- Gaussian noise calibration: noise ~ N(0, (Δf/ε)²σ²)
- Per-round privacy accounting
- Cumulative privacy budget tracking across rounds

### Non-IID Data Handling
- Quantity skew: 10× sample variation across clients (HAR)
- Label skew: Different activity distributions per subject
- Feature skew: Individual motion pattern differences
- Solution: FedAvg mutual regularization effect

---

## Regulatory Compliance

This implementation provides pathways to compliance with:
- **GDPR** (EU): Raw data never leaves devices ✓
- **HIPAA** (Healthcare): Differential privacy with ε=0.5 provides mathematical guarantees ✓
- **CCPA** (California): User data control and privacy preservation ✓

---

## How to Reproduce Results

All random seeds fixed for reproducibility:
```python
np.random.seed(42)
tf.random.set_seed(42)
```

Run `Analysis.ipynb` end-to-end to regenerate all figures and metrics.

---

## References

- McMahan et al. (2017): "Communication-Efficient Learning of Deep Networks from Decentralized Data" – FedAvg algorithm
- Dwork et al. (2006): "Differential Privacy" – Mathematical privacy foundations
- Li et al. (2020): "Federated Learning on Non-IID Data Silos" – Non-IID convergence analysis

---

## Contact & Questions

For questions or issues, refer to **Chapter.pdf** for detailed methodology and theoretical background.
