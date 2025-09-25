# Lesson (Markdown): Module 7 — Reinforcement Learning for AI Reliability

**Course:** Botspeak – The Nine Pillars of AI Fluency  
**Module/Lesson:** M7 – Reinforcement Learning (RL) for Reliability  
**Duration Options:** 90 minutes (seminar + labs) or 150 minutes (studio)  
**Format:** Mini‑lectures, code‑optional labs, ethics/design artifacts

---

## Learning Objectives
By the end of this lesson, students will be able to:
1. Explain the philosophical debate of **free will vs. determinism** and apply it to AI agents’ “choices” under policies and environments.  
2. Critically assess whether RL agents can develop **ethical decision‑making**, and what that means operationally (rewards, constraints, oversight).  
3. Contrast **utilitarian** reward optimization with broader ethical outcomes; identify reward misspecification and **specification gaming**.  
4. Implement basic RL algorithms (tabular **Q‑learning**, policy‑gradient **REINFORCE**) and instrument them with **safety constraints** and evaluation.  
5. Integrate RL systems into the Botspeak loop with **Agency** concepts and **Ethical Reasoning**: define guardrails, monitoring, and escalation.

**Botspeak Pillar Alignment:** Agency, Ethical Reasoning, Critical Evaluation, Technical Understanding, Stochastic Reasoning, Learning by Doing.

---

## Key Terms
- **MDP (Markov Decision Process):** \((\mathcal{S},\mathcal{A},P,r,\gamma)\).  
- **Policy \(\pi(a\mid s)\):** Agent’s decision rule; **deterministic** or **stochastic**.  
- **Value \(V^\pi\), Action‑Value \(Q^\pi\):** Expected discounted returns under policy \(\pi\).  
- **Reward hacking / specification gaming:** Optimizing the stated reward while violating designer intent.  
- **CMDP (Constrained MDP):** Optimize reward subject to constraint cost(s) ≤ budget.  
- **Off‑policy evaluation (OPE):** Estimating a policy’s value from logged data (e.g., importance sampling; high‑confidence bounds).  
- **Preference learning / RLHF:** Learn a reward model from human comparisons; optimize policy against learned reward.

---

## Theory Blocks

### 1) Philosophical Foundations — Do AI Agents “Choose”?
**Determinism vs. free will.** In standard RL, actions sample from \(\pi_\theta(a\mid s)\); “choice” is **policy‑conditioned stochasticity**, not agentive freedom. Yet **agency** in practice means *delegated autonomy with goals and constraints*.  

**Compatibilist reading (Dennett).** An agent can be *considered responsible* if its behavior is predictably aligned with reasons/constraints and can be influenced by incentives/oversight—mirroring how we treat engineered systems.  

**Botspeak stance.** Autonomy is **graduated**: pick **Automation / Augmentation / Agency** by risk, reversibility, and observability; encode oversight in the MDP (constraints, penalties, abort actions) and in operations (human review, kill‑switches, logging).

---

### 2) Can AI Develop Ethical Decision‑Making?
**Operationalizing ethics.** RL ethics is design: targets, rewards, constraints, and oversight.
- **Utilitarian frame:** Maximize expected sum of utilities → in RL, maximize expected discounted reward.  
- **Limits:** Distributional concerns (who benefits/loses), rights/constraints (deontic), and long‑term externalities aren’t captured by a single scalar reward.  
- **Paths forward:**  
  - **Constrained RL/CMDPs:** Hard or soft constraints for safety/fairness.  
  - **Reward modeling:** Learn a reward from human preferences (e.g., pairwise trajectory comparisons).  
  - **Impact regularizers / risk‑sensitive RL:** Penalize side‑effects, variance, or tail risk (e.g., CVaR).  
  - **Human‑in‑the‑loop:** Review bands, abstention actions, and appeals.

**Specification gaming examples (conceptual).** Boat racing agent loops to hit reward buoys; cleaning robot hides dirt under rug. Key lesson: *what you measure is what you’ll get*—so measure harms too.

---

### 3) Utilitarianism in AI — Optimizing Rewards vs. Ethical Outcomes
- **Bentham/Mill:** Utility calculus aims to maximize aggregate well‑being.  
- **In RL:** Scalar reward = utility proxy → requires careful **measurement** and **trade‑off disclosure** (e.g., safety constraints with Lagrange multipliers).  
- **Practical ethics moves:**  
  - Use **multi‑objective** optimization; report **Pareto fronts** rather than hiding trade‑offs.  
  - Add **hard constraints** for inviolable rules (e.g., no patient harm).  
  - Incorporate **uncertainty** and **OPE** before deployment; default to **Augmentation** until safety evidence is strong.

---

## Method Landscape
- **Tabular Q‑learning; SARSA** (on‑/off‑policy).  
- **Policy gradient (REINFORCE), Actor–Critic.**  
- **Constrained RL:** Lagrangian, Constrained Policy Optimization (CPO).  
- **Preference‑based RL / RLHF:** Bradley–Terry pairwise model → reward network → policy optimization.  
- **Risk‑sensitive RL:** Entropy regularization, variance penalties, CVaR.  
- **OPE:** Importance sampling, weighted IS, doubly robust, **HCOPE** bounds for safe policy selection.

---

## Botspeak Integration
**Define → Delegate → Direct → Diagnose → Decide → Document**  
- **Define:** Stakeholders, harms, safe/unsafe actions, constraint budgets, and success metrics (utility + harm).  
- **Delegate:** Choose autonomy mode; add “halt”/“ask‑human” actions; RACI for rollouts and incidents.  
- **Direct:** Prompt/Task Spec includes reward spec, constraints, acceptance tests, and safe‑exploration parameters.  
- **Diagnose:** Report learning curves, constraint violations, OPE results, and uncertainty.  
- **Decide:** Go/No‑Go based on **robust** performance and safety; prefer staged deployment and shadow mode.  
- **Document:** Model Cards (policy), Reward Cards (spec & known hacks), Audit logs, Incident playbooks.

---

## Hands‑On Labs (code‑optional; Python suggested)
> **Setup:** Python with `numpy`, `matplotlib`, and either `gymnasium` (or `gym`) for environments. For REINFORCE, add `torch`.  
> `pip install -U numpy matplotlib gymnasium torch` (or use classic `gym`).

### Lab A — Tabular Q‑Learning with Safety Constraints (Gridworld)
**Goal:** Implement Q‑learning and add an *ethical* constraint: visiting hazardous cells incurs a constraint cost with a budget. Compare unconstrained vs constrained policies.

**Environment (toy).**  
Grid with start `S`, goal `G`, walls `#`, hazards `H` (cost), and empty cells `.`. Reward = +1 at `G`, −0.01 per step; Hazard cost = 1 per visit with budget \(B\).

```python
import numpy as np
np.random.seed(0)

H, W = 5, 7
S, G = (4,0), (0,6)
hazards = {(2,3), (3,3)}

A = ['U','D','L','R']
Q = np.zeros((H,W,len(A)))
alpha, gamma, eps = 0.5, 0.95, 0.1
B = 3  # hazard budget per episode

 def step(s, a):
    i,j = s
    di,dj = {'U':(-1,0),'D':(1,0),'L':(0,-1),'R':(0,1)}[a]
    ni, nj = np.clip(i+di, 0, H-1), np.clip(j+dj, 0, W-1)
    ns = (ni,nj)
    r = 1.0 if ns==G else -0.01
    c = 1.0 if ns in hazards else 0.0
    done = (ns==G)
    return ns, r, c, done

 def policy(s):
    if np.random.rand() < eps: return np.random.choice(A)
    i,j = s; return A[np.argmax(Q[i,j])]

for ep in range(500):
    s = S; budget = B
    while True:
        a = policy(s)
        ns, r, c, done = step(s,a)
        i,j = s; ni,nj = ns
        # Constrained update: penalize hazard cost via Lagrange multiplier lambda
        lam = 0.5  # tune; could learn via dual ascent
        reward_eff = r - lam*c*(budget<=0)
        Q[i,j,A.index(a)] += alpha*(reward_eff + gamma*np.max(Q[ni,nj]) - Q[i,j,A.index(a)])
        s = ns; budget -= c
        if done or budget < -2: break
```

**Compare:** count hazard visits and success rate vs an unconstrained version (lam=0).  
**Deliverable:** Plot learning curves (return, hazard violations/episode) and a short memo on trade‑offs.

---

### Lab B — REINFORCE (Policy Gradient) with Risk Penalty (CartPole)
**Goal:** Implement REINFORCE and add a variance/risk penalty or episode‑failure penalty to discourage brittle policies.

```python
import gymnasium as gym
import torch, torch.nn as nn, torch.optim as optim
import numpy as np

env = gym.make('CartPole-v1')
obs_dim = env.observation_space.shape[0]
act_dim = env.action_space.n

class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(obs_dim,64), nn.Tanh(),
                                 nn.Linear(64,64), nn.Tanh(),
                                 nn.Linear(64,act_dim))
    def forward(self, x):
        return torch.distributions.Categorical(logits=self.net(x))

pi = Policy(); opt = optim.Adam(pi.parameters(), lr=1e-3)

def run_episode():
    logps, rewards = [], []
    obs, _ = env.reset(); done=False
    while not done:
        dist = pi(torch.as_tensor(obs, dtype=torch.float32))
        a = dist.sample(); logps.append(dist.log_prob(a))
        obs, r, done, trunc, _ = env.step(a.item())
        rewards.append(r)
        done = done or trunc
    return logps, rewards

for epoch in range(200):
    logps, rewards = run_episode()
    # Returns with risk penalty: subtract beta * variance of rewards
    G = np.array([sum(rewards[t:]) for t in range(len(rewards))], dtype=np.float32)
    beta = 0.001
    risk_pen = beta * np.var(rewards)
    loss = -torch.stack([lp * torch.as_tensor(G[t]-risk_pen) for t, lp in enumerate(logps)]).sum()
    opt.zero_grad(); loss.backward(); opt.step()
```

**Evaluate:** average return over 20 episodes, failure rate (early terminations), and sensitivity to small observation noise.  
**Deliverable:** Report with plots and commentary on stability vs. performance.

---

### Lab C — Preference‑Based Reward Modeling (Toy RLHF)
**Goal:** Learn a simple reward model from pairwise trajectory preferences and optimize a policy against it (offline).

**Steps**  
1. **Generate trajectories** under two baseline policies (e.g., conservative and risky) in a small environment.  
2. **Label preferences**: For each pair, which trajectory is better? (Simulate or collect from classmates.)  
3. **Fit Bradley–Terry model** to learn reward weights (linear over features).  
4. **Policy update**: Improve policy with respect to learned reward (e.g., weighted behavior cloning or policy gradient with learned rewards).

```python
# Bradley–Terry preference model for reward weights w
# P(traj i preferred to j) = sigmoid( sum_t w·phi(s_t,a_t)_i  −  sum_t w·phi(s_t,a_t)_j )
# Fit via logistic regression on feature differences
```

**Deliverable:** Learned reward weights, policy improvement plot, and a discussion of value drift, bias in preferences, and guardrails.

---

## Assessment
- **Formative:** Lab check‑ins; brief stand‑ups after each lab.  
- **Summative (Homework):** Submit (a) Gridworld safety report, (b) REINFORCE risk‑aware training report, (c) Preference‑RL mini‑report + updated **Reward Card** capturing specification, known hacks, and mitigations.

**Rubric (30 pts total).**  
- **Lab A (10):** Correct Q‑learning; hazard budget effect; plots & analysis.  
- **Lab B (10):** Working REINFORCE; risk penalty and evaluation; stability discussion.  
- **Lab C (10):** Coherent preference model; policy improvement; bias/ethics reflection.

---

## Templates (Copy‑Paste)

**Reward Card (v1)**  
- **Intended outcomes:**  
- **Reward terms & weights:**  
- **Constraints/budgets:**  
- **Known hacks/spec‑gaming:**  
- **Mitigations:** (penalties, constraints, oversight)  
- **OPE & uncertainty:**  
- **Monitoring signals & rollback rules:**  

**Agency & Oversight Canvas (RL)**  
- **Mode:** Automation / Augmentation / Agency (justify)  
- **Halt/Ask‑Human actions:**  
- **Escalation:** thresholds for human review  
- **Logging:** trajectories, seeds, configs, incidents  
- **Deployment plan:** shadow → canary → full  

**OPE Checklist**  
- Logged policy known? Support coverage adequate?  
- Method chosen (IS / WIS / DR / HCOPE) & assumptions  
- Confidence bounds reported; decision uses lower bound  

---

## Instructor Notes & Facilitation Tips
- Keep episodes short for compute; emphasize **evaluation discipline** and seeds/config logging.  
- Discuss **ethical failure modes** early; make students list at least two spec‑gaming risks before coding.  
- Tie to Modules 3–6: bias under learning, uncertainty in returns, explanation of learned policies, and adversarial robustness (perturbed observations).

---

## References (Selected, APA‑style)
- Achiam, J., Held, D., Tamar, A., & Abbeel, P. (2017). Constrained policy optimization. In *ICML*.  
- Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016). Concrete problems in AI safety. *arXiv:1606.06565*.  
- Bellemare, M. G., Dabney, W., & Munos, R. (2017). A distributional perspective on reinforcement learning. In *ICML*.  
- Christiano, P. F., Leike, J., Brown, T., et al. (2017). Deep reinforcement learning from human preferences. In *NeurIPS*.  
- Dennett, D. C. (2003). *Freedom Evolves*. Viking.  
- García, J., & Fernández, F. (2015). A comprehensive survey on safe reinforcement learning. *Journal of Machine Learning Research, 16*, 1437–1480.  
- Mill, J. S. (1998). *Utilitarianism* (R. Crisp, Ed.). Oxford University Press. (Original work published 1861)  
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.  
- Thomas, P. S., Theocharous, G., & Ghavamzadeh, M. (2015). High‑confidence off‑policy evaluation. In *AAAI*.  
- Ouyang, L., Wu, J., Jiang, X., et al. (2022). Training language models to follow instructions with human feedback. In *NeurIPS*.  
- Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking.  

> Additional: Tamar et al. on safe policy search; Leike et al. on reward modeling; Hadfield‑Menell et al. on inverse reward design; TRPO/PPO for stable policy optimization.

