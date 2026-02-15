## Part 4 — Quiz Questions (Chapter Topic: Computational Skepticism QC System)

### Question 1: What is the core idea of **computational skepticism** in the chapter?
A) Trust the dataset if it comes from a reputable source  
B) Assume data is correct unless a model performs poorly  
C) Treat the dataset as untrusted until it passes evidence-based checks  
D) Validate only after building visualizations  

**Correct Answer: C**

**Explanation:**  
C is correct: the chapter defines computational skepticism as treating data as untrusted until systematic checks support trust.  
- A is wrong: reputable sources can still have duplicates, missingness artifacts, and parsing errors.  
- B is wrong: model performance doesn’t prove data validity.  
- D is wrong: validation should happen before inference/modeling, not only after visuals.

---

### Question 2: Which workflow does the chapter propose to operationalize QC?
A) Collect → Model → Report  
B) Normalize → Encode → Train  
C) Inspect → Clean → Deploy  
D) Detect → Fix → Communicate  

**Correct Answer: D**

**Explanation:**  
D is correct: the proposed QC pipeline is **Detect–Fix–Communicate**.  
- A/B/C are plausible workflows but not the chapter’s specific QC system.

---

### Question 3: Which item is explicitly described as an **optional module** in the Detect stage (depending on metadata availability)?
A) Missingness analysis  
B) Duplicate/integrity checks  
C) Schema and type checks  
D) Drift checks (when a time column exists)  

**Correct Answer: D**

**Explanation:**  
D is correct: drift checks are optional and require a time column.  
- A/B/C are core QC checks described as part of QC Core.

---

### Question 4: Why does the chapter recommend a **QC Core + plugin** design?
A) Because common failure modes repeat across domains, and plugins add domain-specific rules  
B) Because plugins eliminate the need for general checks like missingness and duplicates  
C) Because domain semantics are irrelevant to validation  
D) Because every dataset can share the same fixed schema and constraints  

**Correct Answer: A**

**Explanation:**  
A is correct: the chapter argues for standardized core checks plus modular domain rules.  
- B is wrong: plugins complement the core; they don’t replace it.  
- C is wrong: domain semantics matter for constraints/derived validations.  
- D is wrong: datasets differ in schema and meaning.

---

### Question 5: Why does the chapter emphasize **severity scoring** in QC reports?
A) To make all issues equally important  
B) To prioritize issues by potential impact and urgency  
C) To remove the need for evidence in reporting  
D) To ensure fixes are applied randomly across columns  

**Correct Answer: B**

**Explanation:**  
B is correct: severity helps rank failures so effort focuses on high-impact problems first.  
- A is wrong: the whole point is *not* treating all issues equally.  
- C is wrong: evidence is required; skepticism is evidence-based.  
- D is wrong: fixes must be deterministic and justified, not random.

---

### Question 6: Which statement best describes why the chapter separates **Detect** from **Fix**?
A) Detection is only needed after building a model  
B) Fixing first always increases trust scores  
C) Detection tests assumptions and surfaces evidence before any transformations change the data  
D) Detect and Fix are interchangeable stages  

**Correct Answer: C**

**Explanation:**  
C is correct: separating stages prevents “hiding” problems by cleaning too early and supports reproducibility.  
- A is wrong: QC is required before inference/modeling.  
- B is wrong: fixing first can hide root causes and distort evidence.  
- D is wrong: they are intentionally distinct stages.

---

### Question 7: What is the chapter’s main reason for preferring **robust anomaly methods** (IQR/MAD) over naive z-scores in heavy-tailed data?
A) Robust methods require normal distributions  
B) Naive z-scores are always meaningless  
C) Robust methods are less distorted by skew/heavy tails and extreme leverage points  
D) Robust methods prove that every outlier is an error  

**Correct Answer: C**

**Explanation:**  
C is correct: robust methods reduce false alarms caused by skew and heavy tails.  
- A is wrong: robust methods *do not* require normality.  
- B is wrong: z-scores can work sometimes, but are often misleading here.  
- D is wrong: anomaly scoring flags suspicion; it does not prove error.

---

### Question 8: Why does the chapter insist on checking **missingness by subgroup** (not only overall missingness)?
A) Because overall missingness is never informative  
B) Because missingness can be structured and correlated with groups, biasing comparisons  
C) Because subgroup checks replace schema/type validation  
D) Because subgroup missingness only matters if there is a time column  

**Correct Answer: B**

**Explanation:**  
B is correct: subgroup missingness can reveal collection/mapping gaps that distort inference.  
- A is wrong: overall missingness is still useful.  
- C is wrong: subgroup checks are additive, not a replacement.  
- D is wrong: subgroup bias can exist without time.

---

### Question 9: The chapter says duplicates are “not always trivial.” What’s the recommended approach?
A) Deduplicate deterministically and document the rule (auditability)  
B) Always keep all duplicates to preserve sample size  
C) Randomly keep one row from each duplicate group  
D) Drop every record that shares any value with another record  

**Correct Answer: A**

**Explanation:**  
A is correct: deterministic deduplication (e.g., keep most complete record) + logging is emphasized.  
- B is wrong: duplicates can inflate metrics and mislead decisions.  
- C is wrong: randomness harms reproducibility and auditability.  
- D is wrong: that would remove valid data and is not a sensible integrity rule.

---

### Question 10: What is the chapter’s recommended default handling for **outliers**?
A) Delete them immediately to stabilize statistics  
B) Replace them with the mean to normalize distributions  
C) Assume they are all errors  
D) Prefer flagging and conservative handling (e.g., capping/winsorizing) over silent deletion  

**Correct Answer: D**

**Explanation:**  
D is correct: outliers may be valid; the system prefers flags + explainable handling.  
- A is wrong: deletion can remove true signal and hide analyst choices.  
- B is wrong: mean replacement can distort distributions and is not conservative.  
- C is wrong: outliers are suspicious, not automatically wrong.

---

### Question 11: Which is a **QC Core Detect-stage** module that is dataset-agnostic?
A) Hyperparameter tuning  
B) Model training  
C) Feature embedding generation  
D) Duplicate/integrity checks on key fields  

**Correct Answer: D**

**Explanation:**  
D is correct: duplicates/integrity checks are explicitly part of QC Core.  
- A/B/C are modeling/ML steps, not QC detection fundamentals.

---

### Question 12: What makes a Fix step **auditable** according to the chapter?
A) Each fix is reproducible and recorded (what changed, why, and impact)  
B) Fixes are applied manually and not written down to avoid clutter  
C) Fixes are done by deleting rows so nothing needs to be tracked  
D) Fixes are chosen to maximize the QCScore regardless of meaning  

**Correct Answer: A**

**Explanation:**  
A is correct: auditability requires deterministic transformations + fix logs/flags.  
- B is wrong: undocumented manual fixes are the opposite of auditable.  
- C is wrong: deletion without documentation hides decisions and uncertainty.  
- D is wrong: gaming the score violates evidence-based skepticism.

---

### Question 13: Which output best matches the chapter’s definition of `D_clean`?
A) A dataset where all suspicious rows are removed  
B) A cleaned dataset plus quality flags (not silent deletion)  
C) A dataset converted into visualizations only  
D) A dataset that must be perfectly complete (no missing values allowed)  

**Correct Answer: B**

**Explanation:**  
B is correct: `D_clean` includes cleaned values *and* flags to preserve uncertainty and auditability.  
- A is wrong: the chapter discourages silent deletion as the default.  
- C is wrong: visuals are outputs, not the cleaned dataset itself.  
- D is wrong: missingness can be meaningful; QC should make it explicit, not pretend it can’t exist.

---

### Question 14: Which statement best reflects the chapter’s goal in criticizing ad hoc validation (“tribal knowledge”)?
A) Ad hoc validation is ideal because it’s fast and personal  
B) Ad hoc validation is fine because it always catches all failure modes  
C) Ad hoc validation slows analysis, reduces reproducibility, and increases artifact-driven decisions  
D) Ad hoc validation removes the need for communication artifacts  

**Correct Answer: C**

**Explanation:**  
C is correct: the chapter argues ad hoc checks are scattered, non-reusable, and risky.  
- A is wrong: ad hoc methods often slow teams long-term and create inconsistency.  
- B is wrong: ad hoc checks frequently miss structured issues.  
- D is wrong: communication is essential; QC shouldn’t be invisible.

---

### Question 15: In Detect–Fix–Communicate, what is the purpose of **Communicate**?
A) Hide uncertainty to avoid confusion  
B) Replace the QC report with a single trust score  
C) Present issues and improvements clearly (tables/plots), including remaining uncertainty  
D) Focus only on aesthetics of charts  

**Correct Answer: C**

**Explanation:**  
C is correct: communication makes QC actionable by summarizing evidence, impact, and remaining uncertainty.  
- A is wrong: the chapter emphasizes honesty and explicit uncertainty.  
- B is wrong: the score must be explainable and supported by evidence.  
- D is wrong: chart design matters, but clarity and actionability are the point.
