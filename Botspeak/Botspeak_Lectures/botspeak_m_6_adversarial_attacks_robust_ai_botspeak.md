# Lesson (Markdown): Module 6 — Adversarial Attacks & Robust AI Systems

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M6 – Adversarial Attacks & Robustness  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, red‑team/blue‑team labs, evaluation artifacts

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Explain the philosophical lens of **deception** in AI and analyze what adversarial vulnerability implies about “understanding.”  
2. Describe core **threat models** (white‑box, gray‑box, black‑box) and attack classes (evasion, poisoning, backdoor/trojan, privacy attacks).  
3. Implement and evaluate **evasion attacks** (FGSM/PGD) and articulate robust‑accuracy results under \(\ell_p\) constraints.  
4. Design **defensive strategies** (adversarial training, certification, detection, and operational guardrails) and evaluate trade‑offs.  
5. Apply Botspeak pillars **Critical Evaluation** and **Technical Understanding** to produce defense‑ready artifacts: Threat Model Canvas, Robustness Eval Plan, and Incident/Red‑Team report.

**Ethical use note.** All attack implementations in this course are for defensive education and research on local, synthetic datasets. Do not target real users, systems, or models without explicit permission.

---

## Key Terms
- **Adversarial example:** An input modified by a small, often human‑imperceptible perturbation that causes model misprediction.  
- **Threat model:** Attacker’s knowledge and capabilities (white/gray/black‑box; query budget; perturbation norm/size).  
- **\(\ell_p\) norms:** Constraint sets on perturbations, commonly \(\ell_\infty, \ell_2, \ell_0\).  
- **Robust accuracy:** Accuracy measured on worst‑case (or strong attack) inputs within a specified threat model.  
- **Gradient masking:** Defenses that appear to work by obscuring gradients; typically fail under stronger or transfer attacks.  
- **Backdoor/Trojan:** A trigger‑pattern causes targeted misclassification at test time (often from poisoned training data).  
- **Certified robustness:** Provable guarantees that predictions are constant within a perturbation radius (e.g., randomized smoothing).

---

## Theory & Philosophy

### 1) Deception & the Nature of “Understanding”
- **Black‑box deception.** Systems can perform impressively while being exploitable by inputs crafted to exploit decision boundaries.  
- **Does vulnerability negate understanding?** If small, semantically irrelevant changes flip outputs, then representations may rely on **non‑robust features**. Vulnerability does not prove a system lacks any understanding, but it reveals a gap between **statistical correlation** and **semantic grasp** needed for safe deployment.

### 2) Nietzschean Lens: Optimization & Will‑to‑Power
- Nietzsche’s “will to power” can be read (metaphorically) as **relentless optimization**: attack and defense co‑evolve in a competitive game. Adversarial training formalizes this as a **min–max** objective:  
\[ \min_\theta \; \mathbb{E}_{(x,y)}\big[\max_{\delta \in S} \; \ell(f_\theta(x+\delta), y)\big], \]  
where \(S\) is the allowed perturbation set. Robustness emerges from **embracing conflict** in training rather than ignoring it.

### 3) Critical Question
- If an AI can be tricked easily, should we deploy it in **Automation** or **Agency** modes? Botspeak argues for **Augmentation** with strong guardrails in high‑stakes settings until robust evidence justifies autonomy.

---

## Method Landscape

### A. Attack Classes
- **Evasion (test‑time):** FGSM, PGD, CW; universal perturbations; physical attacks (e.g., adversarial patches).  
- **Poisoning (train‑time):** Clean‑label poisoning; label flipping; data poisoning to degrade or steer models.  
- **Backdoor/Trojan:** Inserted trigger makes model misclassify only when trigger present.  
- **Privacy attacks:** Membership inference; model inversion; extraction via query APIs.  
- **LLM‑specific:** Prompt injection, jailbreaks, tool‑use subversion, data‑exfiltration via content leaks.

### B. Defenses
- **Adversarial training:** Empirically robust; expensive; may trade off clean accuracy.  
- **Certified defenses:** Randomized smoothing; convex relaxation/verification; interval bound propagation (provable but limited radius).  
- **Detection & input transformations:** JPEG, bit‑depth reduction, denoising; often brittle.  
- **Ensembles & diversity:** Heterogeneous models to reduce transferability.  
- **Operational guardrails:** Rate limiting, anomaly detection, sandboxing tools, human‑in‑the‑loop review, least‑privilege permissions, and red‑team testing.

---

## Botspeak Integration
**Define → Delegate → Direct → Diagnose → Decide → Document**  
- **Define:** State assets, harms, and acceptable risk; pick threat model(s) and perturbation budgets; set robust‑accuracy targets.  
- **Delegate:** Prefer **Augmentation** for consequential tasks; require human escalation on anomalous inputs.  
- **Direct:** Add adversarial tests to Acceptance Test suite; specify strongest known attacks for eval.  
- **Diagnose:** Evaluate under **AutoAttack/PGD** and measure robust accuracy; check for gradient masking.  
- **Decide:** Ship only if robust criteria met; otherwise mitigate (adversarial training, monitoring).  
- **Document:** Threat Model Canvas, Robustness Eval Plan, Incident reports; update Model Cards with robustness metrics.

---

## Hands‑On Labs
> **Setup:** Python with `torch`, `torchvision`, `numpy`, `matplotlib`. Small datasets (MNIST/CIFAR‑10). If not using GPUs, reduce epochs/batch sizes.

### Lab 1 — Evasion Attacks: FGSM & PGD
**Goal:** Implement Fast Gradient Sign Method (FGSM) and Projected Gradient Descent (PGD) against a CNN; measure clean vs robust accuracy.  

**FGSM idea.** For loss \(\ell(f_\theta(x), y)\), generate \(x' = x + \epsilon\,\mathrm{sign}(\nabla_x\ell)\) and clip to valid range.  

```python
# Minimal FGSM on MNIST (PyTorch)
import torch, torch.nn as nn, torch.nn.functional as F
from torchvision import datasets, transforms

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Data
tf = transforms.Compose([transforms.ToTensor()])
train = datasets.MNIST(root='data', train=True, download=True, transform=tf)
 test = datasets.MNIST(root='data', train=False, download=True, transform=tf)
train_loader = torch.utils.data.DataLoader(train, batch_size=64, shuffle=True)
 test_loader = torch.utils.data.DataLoader(test, batch_size=256)

# Model
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
    def forward(self, x):
        x = F.relu(self.conv1(x)); x = F.relu(self.conv2(x))
        x = F.adaptive_avg_pool2d(x, (12,12)).view(x.size(0), -1)
        x = F.relu(self.fc1(x)); return self.fc2(x)

model = CNN().to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

# Train few epochs for demo
for epoch in range(2):
    model.train()
    for x,y in train_loader:
        x,y = x.to(device), y.to(device)
        opt.zero_grad(); loss = F.cross_entropy(model(x), y)
        loss.backward(); opt.step()

# FGSM attack
def fgsm(x, y, eps=0.25):
    x = x.clone().detach().to(device)
    x.requires_grad_(True)
    loss = F.cross_entropy(model(x), y.to(device))
    loss.backward()
    x_adv = x + eps * x.grad.sign()
    return torch.clamp(x_adv, 0, 1)

# Evaluate clean vs adversarial
model.eval(); correct_clean=correct_adv=total=0
with torch.no_grad():
    for x,y in test_loader:
        x,y = x.to(device), y.to(device)
        pred = model(x).argmax(1); correct_clean += (pred==y).sum().item(); total += y.numel()

for x,y in test_loader:
    x_adv = fgsm(x, y, eps=0.25)
    with torch.no_grad():
        pred = model(x_adv).argmax(1)
    correct_adv += (pred.cpu()==y).sum().item()

print('Clean acc:', correct_clean/total, ' FGSM acc:', correct_adv/total)
```

**PGD (iterative) sketch**  
```python
def pgd(x, y, eps=0.3, alpha=0.03, steps=40):
    x = x.to(device); y = y.to(device)
    x_adv = x + torch.empty_like(x).uniform_(-eps, eps)
    for _ in range(steps):
        x_adv.requires_grad_(True)
        loss = F.cross_entropy(model(x_adv), y)
        grad = torch.autograd.grad(loss, x_adv)[0]
        x_adv = x_adv.detach() + alpha * grad.sign()
        x_adv = torch.max(torch.min(x_adv, x+eps), x-eps)
        x_adv = torch.clamp(x_adv, 0, 1)
    return x_adv
```

**Report:** Clean accuracy, FGSM/PGD robust accuracy at multiple \(\epsilon\) values; short analysis on transferability (attack one model, test on another).

---

### Lab 2 — Adversarial Training (PGD‑AT) vs Standard Training
**Goal:** Train two models—standard and adversarially trained—and compare clean vs robust accuracy.

```python
# PGD adversarial training loop (sketch)
for epoch in range(2):
    for x,y in train_loader:
        x,y = x.to(device), y.to(device)
        x_adv = pgd(x, y, eps=0.3, alpha=0.03, steps=10)
        opt.zero_grad(); loss = F.cross_entropy(model(x_adv), y)
        loss.backward(); opt.step()
```

**Deliverable:** Table of clean and PGD robust accuracies; discussion of trade‑offs (training cost, clean‑robust trade‑off) and evidence against gradient masking (e.g., transfer/black‑box attacks still succeed?).

---

### Lab 3 — Threat Modeling & Defense Playbook (No‑Code + LLM Segment)
**Goal:** Produce a defense plan combining algorithmic and operational controls.

**Part A (Vision/Tabular systems):**  
- Fill a **Threat Model Canvas** (template below).  
- Choose a primary defense (adversarial training or smoothing) and at least **three** operational guardrails (rate limiting, anomaly detection, human review bands, input sanitation, logging & replay).  
- Define **robustness acceptance tests** (attack strength, norms, budgets) and **Go/No‑Go** criteria.

**Part B (LLM‑specific):**  
- Identify **prompt‑injection** and **jailbreak** risks for a tool‑using assistant.  
- Draft a **prompt & tool policy**: content filters, retrieval whitelists, tool sandboxing, output‑bound checks; define red‑team prompts and refusal behaviors.

**Deliverable:** 2‑page Defense Playbook + acceptance tests and escalation/rollback.

---

## Assessment
- **Formative:** Lab check‑ins; quick share‑outs; robustness metrics sanity checks.  
- **Summative (Homework):** Submit (a) Robustness Evaluation Report (Lab 1), (b) Adversarial Training comparison (Lab 2), (c) Defense Playbook with Threat Model Canvas (Lab 3).

**Rubric (30 pts).**  
- **Lab 1 (12):** Correct implementation; multi‑\(\epsilon\) results; discussion of transferability and limitations.  
- **Lab 2 (8):** Clear comparison; discussion of trade‑offs; checks against gradient masking.  
- **Lab 3 (10):** Coherent threat model; practical guardrails; measurable acceptance tests and escalation.

---

## Templates (Copy‑Paste)

**Threat Model Canvas**  
- **Assets & stakes:**  
- **Attacker knowledge/capability:** white/gray/black‑box; query budget  
- **Perturbation set:** norm, radius, physical constraints  
- **Objectives:** targeted/untargeted; availability/stealth  
- **Likely vectors:** evasion/poisoning/backdoor/privacy  
- **Defenses:** training, detection, certification, ops  
- **Acceptance tests:** robust accuracy @ norms; detection ROC; incident SLOs  
- **Escalation & rollback:** thresholds; playbooks  

**Robustness Eval Report**  
- Dataset/model  
- Clean vs robust accuracy (FGSM/PGD/AutoAttack) across \(\epsilon\)  
- Evidence against gradient masking (transfer, BPDA if relevant)  
- Decision & next mitigations  

**Incident/Red‑Team Memo**  
- Attack scenario & threat model  
- Reproduction steps (internal only)  
- Impact & severity  
- Contain/eradicate/recover actions  
- Preventive measures & owners  

---

## Instructor Notes & Facilitation Tips
- Stress **evaluation on strong attacks**; weak attacks inflate a false sense of security.  
- Encourage **small‑scale, repeatable** experiments; track seeds and configs.  
- Cover **physical‑world** pitfalls (printing, angles, lighting) and the gap between digital norms and real perturbations.  
- Tie back to Modules 3–5: fairness under attack, uncertainty bands under adversarial shift, explanation stability for attacked inputs.

---

## References (Selected, APA‑style)
- Athalye, A., Carlini, N., & Wagner, D. (2018). Obfuscated gradients give a false sense of security. In *ICML*.  
- Carlini, N., & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *IEEE S&P*.  
- Cohen, J., Rosenfeld, E., & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *ICML*.  
- Croce, F., & Hein, M. (2020). Reliable evaluation of adversarial robustness with AutoAttack. *arXiv:2003.01690*.  
- Goodfellow, I., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *ICLR*.  
- Gu, T., Dolan‑Gavitt, B., & Garg, S. (2017). BadNets: Identifying vulnerabilities in deep learning models. *arXiv:1708.06733*.  
- Kurakin, A., Goodfellow, I., & Bengio, S. (2017). Adversarial examples in the physical world. In *ICLR Workshop*.  
- Madry, A., Makelov, A., Schmidt, L., Tsipras, D., & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *ICLR*.  
- Papernot, N., McDaniel, P., Goodfellow, I., et al. (2016). The limitations of deep learning in adversarial settings. In *EuroS&P*.  
- Raghunathan, A., Steinhardt, J., & Liang, P. (2018). Certified defenses via convex relaxations. In *NeurIPS*.  
- Szegedy, C., Zaremba, W., Sutskever, I., et al. (2014). Intriguing properties of neural networks. In *ICLR*.  
- Tramèr, F., Papernot, N., Goodfellow, I., et al. (2018). Ensemble adversarial training: Attacks and defenses. In *ICLR*.  
- Shokri, R., Stronati, M., Song, C., & Shmatikov, V. (2017). Membership inference attacks against machine learning models. In *IEEE S&P*.  

> Additional resources: model verification/IBP (Wong & Kolter, 2018); TRADES (Zhang et al., 2019); LLM red‑teaming and prompt‑injection reports (industry whitepapers).

