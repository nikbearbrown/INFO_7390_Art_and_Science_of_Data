# Computational Skepticism for Data Understanding — QC System (Detect → Fix → Communicate)

This repo implements a repeatable **data QC system** grounded in **computational skepticism**: *treat the dataset as untrusted until it passes evidence-based checks*.  
It standardizes a **Detect → Fix → Communicate** workflow with an extensible **QC Core + plugin** design.

## Navigation
- **Chapter / Conceptual Writeup**
  - `Chapter.md` — research question, theory, system design, and references
- **Implementation Notebook (Chapter → Code)**
  - `Analysis.ipynb` — implements the chapter’s QC pipeline (core workflow + reporting)
- **Worked Examples (Live Datasets)**
  - `Example1_WorkedExample_Claims.ipynb` — claims-style dataset (QC Core + claims rules)
  - `Example2_WorkedExample_Housing.ipynb` — housing/Ames-style dataset (QC Core + housing rules)

## Outputs (Generated)
Each worked example writes auditable artifacts to its dataset folder:
- `*/processed/*_clean.csv` — cleaned data + `__was_*` quality flags  
- `*/processed/*_fixlog.csv` — deterministic change log (impute/winsorize/dedupe/etc.)  
- `*/processed/*_qc_report.csv` — severity-ranked QC findings (where applicable)

## How to Run (Quick)
1. Put raw CSVs in:
   - `Example1_Dataset/raw/`
   - `Example2_Dataset/raw/`
2. Run:
   - `Analysis.ipynb` (chapter implementation)
   - `Example1_WorkedExample_Claims.ipynb`
   - `Example2_WorkedExample_Housing.ipynb`
3. Check outputs in `Example*_Dataset/processed/`.

## Author
Akash Arokianathan
