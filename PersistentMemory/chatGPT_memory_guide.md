# How ChatGPT’s Persistent Memory Actually Works  
*(As Far As I Know)*

This document explains how ChatGPT’s memory works in practice, where it is reliable, where it fails, and how to design workflows (especially for students and long-term projects) that **do not depend on opaque AI memory systems**.

This is written from an engineering perspective, not marketing.

---

## 1. The Architecture (Mental Model)

ChatGPT effectively operates with **two distinct memory layers**.

### 1.1 Conversation Context (Short-Term Memory)

- Exists **only within a single conversation**
- Token-limited (large, but finite)
- Contains:
  - Full message history of the current chat
  - System instructions
  - Uploaded files (within limits)
- Behavior:
  - Older messages are **truncated** when token limits are reached
  - Memory is **reset** when a new conversation starts
- Not persistent across chats

**Key takeaway:**  
Conversation context is *fast, detailed, and fragile*.

---

### 1.2 Persistent Memory (Long-Term Memory)

- Exists **across conversations**
- Injected at the **start** of a new conversation
- Consists of:
  - Automatically extracted summaries from past conversations
  - Explicit user-provided memory entries (“remember this”)
- Maintained by the backend system, not by the model itself

**Key takeaway:**  
Persistent memory is *durable, lossy, and selective*.

---

## 2. What Persistent Memory Is (and Is Not)

### What It Is Good At
- Remembering **preferences** (tone, style, recurring tools)
- Remembering **high-level facts** about a user’s work or background
- Reducing the need to re-explain basic context
- Improving conversational continuity

### What It Is Not Good At
- Storing detailed technical specifications
- Preserving complex architectures
- Tracking evolving project state
- Acting as a source of truth

> Treat persistent memory like a **cache**, not a **database**.

---

## 3. Automatic Memory Extraction (What Gets Remembered)

### Known Characteristics

From observed behavior:

- **Recency bias**: recent conversations are more likely to be remembered
- **Lossy summarization**: details are compressed or dropped
- **Selective capture**: not everything “important” is stored
- **Lag**: memory updates may occur well after a conversation ends
- **Deletion lag**: deleting chats removes derived memory *eventually*, not instantly
- **Incognito mode**: disables memory entirely

### Unknowns (Important!)

The following are **not documented**:

- Exact extraction algorithm (semantic importance? heuristics?)
- Storage capacity per user
- Whether embeddings or summaries are used internally
- Why some long conversations are remembered and others are not
- Whether different contexts (projects vs. normal chats) behave differently

**Engineering implication:**  
You cannot reason reliably about *what* will be remembered.

---

## 4. Explicit Memory (User-Controlled Memory)

Users can explicitly instruct ChatGPT to remember things.

### What Explicit Memory Does

- Stores short, user-approved memory entries
- Persists across conversations
- Is more reliable than automatic extraction
- Is editable and removable by the user

### Known Limits

- Maximum number of entries: **~30**
- Maximum length per entry: **~200 characters**
- Entries must be concise
- Designed for **facts**, not documents

### How Long Does Explicit Memory Last?

**What is known with confidence:**
- Persists across conversations
- Remains until explicitly deleted or replaced
- Is tied to the user account

**What is not guaranteed:**
- “Forever” storage
- Immunity to backend changes
- Protection from future system migrations

**Best framing:**
> Explicit memory is *persistent but not guaranteed*.

---

## 5. The B Wells Problem (Real Failure Mode)

### What Happened

- A long, detailed conversation about a major project
- Hundreds of messages
- Central to ongoing work
- Not present in persistent memory later

### Likely Causes

- Extraction lag
- Lossy summarization
- Context prioritization
- Backend heuristics
- Memory capacity limits

### Lesson

**Importance ≠ persistence**

If it matters:
- Document it externally
- Version control it
- Reintroduce it intentionally

---

## 6. The Probabilistic Nature Problem

Even with identical memory and context:

- Responses can vary
- Sampling introduces non-determinism
- Creativity increases variance
- Determinism decreases with abstraction

### What This Means

- Creative tasks → expect variation
- Factual tasks → expect consistency (with verification)
- Planning tasks → always externalize decisions

---

## 7. Recommended Workflow for Students (and Professionals)

### 7.1 External Context Documents (Required)

Create a living document, for example:

```text
project_context.md
├── Project overview
├── Architecture (high level)
├── Key decisions + rationale
├── Current status
└── Next steps
```

Paste relevant sections when starting new conversations.

---

### 7.2 Version Control Everything

```text
repo/
├── code/
├── docs/
│   ├── architecture.md
│   ├── decisions/
│   └── ai_conversations/
└── context/
    └── chatgpt_context.md
```

Treat AI conversations as **artifacts**, not memory.

---

### 7.3 Use Explicit Memory Sparingly

Good candidates:

* Tech stack preferences
* Communication style
* Stable long-term projects

Bad candidates:

* Full architectures
* Changing requirements
* Temporary experiments

---

### 7.4 Start New Conversations With Context

Use a consistent template:

```markdown
Context:
- Project: X
- Architecture: Y
- Current goal: Z
- Last milestone: A
```

This dramatically improves reliability.

---

## 8. Context Compression Strategies

To fit more meaning into fewer tokens:

* Prefer **decisions over discussions**
* Prefer **interfaces over implementations**
* Use bullet points instead of prose
* Replace history with:

  * Decision
  * Reason
  * Tradeoff

This is a transferable engineering skill.

---

## 9. When Memory Works Well

* Remembering preferences
* Maintaining conversational tone
* Light continuity across chats
* Reducing onboarding friction

## 10. When Memory Fails

* Long-term project management
* Complex system design
* Multi-step evolving plans
* Precise technical recall

---

## 11. The Core Engineering Principle

> **LLM memory is a cache, not a database.**

* Useful for performance
* Unsafe as a source of truth
* May be invalidated without notice
* Always subordinate to external documentation

---

## 12. Teaching Exercise (Highly Recommended)

Have students:

1. Discuss a fake project in detail
2. Start a new chat the next day
3. Observe what is remembered
4. Compare with saved documentation

This teaches limitations empirically.

---

## 13. The Honest Truth

AI memory is about **convenience**, not **reliability**.

For anything that matters:

* Store it externally
* Version control it
* Reintroduce it intentionally
* Never assume the system “just remembers”

This isn’t pessimism.

It’s good engineering.


