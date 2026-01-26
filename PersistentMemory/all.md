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


# Claude's Persistent Memory: A Technical Guide

## Overview

This document explains how Claude's persistent memory system works, based on what Claude itself knows from its system instructions. This is intended for students working on long-term projects who need to understand the limitations and best practices for working with LLM memory.

**Key Takeaway**: Treat LLM memory like cache, not a database. Always maintain external documentation for critical project information.

---

## Architecture

### Two Separate Memory Systems

#### 1. Conversation Context (Short-term)
- **Scope**: Within a single chat session
- **Capacity**: Token-limited (~449K tokens typical)
- **Content**: Full message history of current conversation
- **Behavior**: Gets truncated when token limits reached (older messages drop off)
- **Lifecycle**: Resets when you start a new conversation

#### 2. UserMemories (Long-term)
- **Scope**: Across all conversations
- **Format**: Pre-extracted summaries provided via `<userMemories>` tag
- **Control**: Updated by Anthropic's backend system, not by Claude
- **Access**: Provided at start of each new conversation
- **User Visibility**: Not directly visible to users

---

## How UserMemories Work

### What We Know

**Extraction Process:**
- Has **recency bias** - recent conversations more likely to be included
- Updates **periodically in the background** - there is processing lag
- **Scope-limited** - only conversations within current context (Project vs. non-Project)
- **Deletion handling** - information from deleted conversations removed "eventually nightly"
- **Disabled** in Incognito mode

**Explicit Memory Controls:**
- `memory_user_edits` tool allows explicit memory instructions
- **30 edits maximum**
- **200 characters per edit**
- User can view, add, remove, or replace edits

### What We Don't Know

- Specific extraction algorithm (semantic importance? information density? keyword matching?)
- Why some detailed conversations get captured and others don't
- Exact lag time between conversation and extraction
- Total storage capacity per user
- Whether it uses embeddings, summarization, or another technique
- How long explicit memory edits persist (indefinitely? time-limited?)
- What happens when you hit the 30 edit limit

---

## Memory Tools Available

### 1. conversation_search
Searches past conversations by keywords.

**Usage:**
```
conversation_search(query="keyword1 keyword2", max_results=5)
```

**Capabilities:**
- Returns snippets with links to original chats
- Up to 10 results
- Only searches within current scope (Project vs. non-Project)

**Best for:**
- Finding specific discussions: "What did we decide about database schema?"
- Retrieving technical details from past conversations

### 2. recent_chats
Retrieves most recent conversations.

**Usage:**
```
recent_chats(n=10, before="2025-01-20T00:00:00Z", after="2025-01-01T00:00:00Z")
```

**Capabilities:**
- Retrieves 1-20 most recent conversations
- Can filter by date range
- Provides conversation previews and links
- Supports chronological or reverse-chronological sorting

**Best for:**
- "What did we discuss yesterday?"
- Getting back up to speed after a break

### 3. memory_user_edits
Explicit user control over what Claude remembers.

**Commands:**
- `view` - See current memory edits
- `add` - Add new memory instruction
- `remove` - Delete by line number
- `replace` - Update existing edit

**Limits:**
- 30 edits maximum
- 200 characters per edit
- No whitespace, slashes, or quotes in keys

**Example Usage:**
```
User: "Remember that my capstone project uses React + FastAPI + PostgreSQL"
Claude: [uses memory_user_edits to store this]
```

---

## Real-World Example: The B Wells Problem

### What Happened
A user had an **hours-long conversation** (hundreds of messages) about a complex multi-agent system called "B Wells":
- Detailed architecture (Intelligence Agent → Popper → Publisher)
- Central to their current work
- Highly technical and specific

**Result**: When referenced later, this detailed architecture was **not in Claude's userMemories**.

### Possible Causes
1. Recent conversation - extraction lag hadn't caught up
2. Happened in different context (Project vs. non-Project boundary)
3. Algorithm prioritized other information
4. Lossy summarization compressed away details
5. Unknown system behavior

### Lesson
Even important, detailed, lengthy conversations may not be reliably captured by automatic memory extraction. Critical information needs external storage.

---

## Best Practices for Students

### For Semester-Long Projects

#### 1. Maintain External Context Documents

Create a `project_context.md` file:

```markdown
# Project Name

## Overview (1-2 paragraphs)
Brief description of what you're building and why.

## Technical Architecture
- Frontend: React + TypeScript
- Backend: FastAPI + Python 3.11
- Database: PostgreSQL 15
- Deployment: Docker + AWS

## Key Decisions
- Using JWT for auth (decided 2025-01-15)
- Chose PostgreSQL over MongoDB for relational data
- Material-UI for component library

## Current Status
- Week 8 of 14
- Authentication complete
- Working on: API endpoint implementation
- Next: Frontend integration

## For Claude
When starting new conversations, I'm working on [specific task].
Key context: [paste relevant architecture/decisions from above].
```

**Paste relevant sections** when starting new Claude conversations.

#### 2. Use Version Control

```
semester_project/
├── src/
├── docs/
│   ├── architecture.md
│   ├── decisions/
│   │   ├── 001-tech-stack.md
│   │   └── 002-auth-approach.md
│   └── claude_conversations/  
│       ├── 2025-01-15-initial-architecture.md
│       └── 2025-02-01-database-schema.md
└── context/
    └── for_claude.md  # Master context file
```

**Export important conversations** to markdown and store in repo.

#### 3. Use Explicit Memory Commands

For facts you want reliably remembered:

```
"Remember that my project deadline is April 15, 2025"
"Remember that I'm using the Model-View-Controller pattern"
"Remember that my advisor is Dr. Smith and prefers weekly updates"
```

Claude will use `memory_user_edits` to store these explicitly.

#### 4. Start Each Session With Context

**Good opening message:**
```
I'm continuing work on my semester project (e-commerce platform).

Key context:
- Stack: React/FastAPI/PostgreSQL
- Current task: Implementing shopping cart API
- Last conversation: We designed the cart schema
- Issue: Trying to optimize cart queries for performance

[paste relevant schema/code if needed]
```

**Poor opening message:**
```
"Hey, continue where we left off"
```

---

## Understanding the Probabilistic Nature

### LLMs Are Non-Deterministic

Even with **identical inputs and memories**, responses will diverge because:
- LLMs use sampling (temperature, top-p parameters)
- Multiple valid responses exist
- Generation is inherently probabilistic

### Implications for Students

**Don't expect:**
- Identical responses across sessions for creative tasks
- Consistent code style without explicit instructions
- Same architectural suggestions every time

**Do expect:**
- Consistency for factual/deterministic tasks
- Similar approaches with variation in details
- Need to provide context for critical decisions

**Solution:**
- Document critical decisions externally
- Include them in context when relevant
- Don't rely on "Claude will remember my preferences"

---

## When Memory Works Well vs. Poorly

### ✅ Good Use Cases

- **Preferences**: Communication style, programming language choices
- **Background**: Your role, institution, general project area
- **Ongoing context**: "I'm working on a capstone project in ML"
- **Avoiding repetition**: Not re-explaining basic concepts you've covered

### ❌ Poor Use Cases

- **Detailed specifications**: API schemas, database designs
- **Critical state**: "Where did I leave off in my code?"
- **Complex architectures**: Multi-component system designs
- **Exact previous outputs**: "Regenerate that code from last week"
- **Long-term project management**: Without external documentation

---

## The Engineering Principle

### Treat Memory Like Cache, Not Database

| Aspect | Cache Behavior | Database Behavior |
|--------|---------------|-------------------|
| **Reliability** | May be invalidated | Persistent and reliable |
| **Purpose** | Performance optimization | Source of truth |
| **When to use** | Avoid re-computation | Store critical data |
| **Failure mode** | Graceful degradation | System failure |

**Claude's memory is a cache**: Useful for convenience, but **always keep authoritative source elsewhere**.

---

## Recommended Workflow

### Setup (Start of Semester)

1. **Create Git repository** for project
2. **Create `claude_context.md`** with:
   - Project overview
   - Architecture decisions
   - Tech stack
   - Current status
3. **Use explicit memory commands** for key facts:
   ```
   "Remember my project deadline is [date]"
   "Remember I'm using [tech stack]"
   "Remember my advisor is [name]"
   ```

### Weekly Maintenance

1. **Update context document** with new decisions
2. **Export important conversations** to markdown in repo
3. **Commit to Git** with descriptive messages
4. **Review memory edits** - add/update as needed

### Each Claude Session

1. **Start with context**: Paste relevant sections from `claude_context.md`
2. **State current goal**: "Today I'm working on [specific task]"
3. **Link previous work**: "Last time we discussed [topic]" or link to conversation
4. **Work on task**
5. **Export conversation** if it contains important decisions/code

### End of Project

1. **Export final context document**
2. **Archive all Claude conversations**
3. **Document what worked / what didn't**
4. **Share learnings** with classmates

---

## Testing Memory (Class Exercise)

Have students empirically test memory limitations:

### Exercise Steps

1. **Day 1**: Have detailed conversation about a fake project
   - Complex architecture
   - Multiple components
   - Specific technical decisions
   - Get Claude to summarize it back

2. **Day 2**: Start new conversation
   - Don't mention the project
   - See what Claude remembers unprompted
   - Note: what's present vs. missing

3. **Day 2**: Use `conversation_search`
   - Search for keywords from Day 1
   - Retrieve the original conversation
   - Compare searchable vs. automatically remembered

4. **Week later**: Start new conversation
   - Check what persisted in memory
   - Use explicit memory command to store something
   - Return in another week to verify it persisted

### Learning Outcomes

Students learn:
- Memory extraction is lossy
- Not everything makes it into automatic memory
- Search tools can retrieve what memory doesn't
- Explicit memory commands are more reliable
- External documentation is essential

---

## Memory Persistence Duration

### Known Facts

- **Conversation context**: Persists only within single chat session
- **UserMemories automatic extraction**: Updates periodically, has recency bias
- **Explicit memory edits**: Persist across conversations
- **Deleted conversations**: Information removed "eventually nightly"

### Unknown / Unspecified

- How long explicit edits persist (likely indefinitely, but not guaranteed)
- What happens when hitting 30 edit limit
- Whether automatic extraction can override explicit edits
- Exact processing lag time
- Whether edits expire after account inactivity

### Recommendation

**Treat as persistent but not guaranteed.** For truly critical information, maintain external documentation.

---

## Comparison to Other LLMs

While I can't speak authoritatively about other systems, conceptually:

- **All LLM memory systems** face similar challenges:
  - Extraction vs. storage tradeoffs
  - Recency vs. importance balancing
  - Staleness as context changes
  - Privacy and security considerations

- **All should recommend** external documentation for critical work

- **None should be** sole source of truth for long-term projects

The principles in this guide likely apply broadly, even if implementation details differ.

---

## Common Mistakes to Avoid

### ❌ Don't Do This

1. **Assume memory is perfect**
   - "Claude will remember all the details from last week"

2. **Rely on memory for critical data**
   - Using conversation history as only record of API design

3. **Expect consistency without context**
   - Starting fresh sessions with "continue where we left off"

4. **Skip external documentation**
   - "It's all in our Claude conversations somewhere"

5. **Ignore scope boundaries**
   - Expecting Project conversations to carry into non-Project chats

### ✅ Do This Instead

1. **Verify memory contents**
   - Ask "What do you remember about my project?" periodically

2. **Maintain external source of truth**
   - Git repo with documentation, exported conversations

3. **Provide context explicitly**
   - Paste relevant info at start of each session

4. **Document externally**
   - Markdown files, Git commits, project wiki

5. **Understand scope**
   - Know when conversations are/aren't linked by system

---

## Advanced: Context Compression Strategies

For students working on complex projects, efficiently providing context is crucial.

### Hierarchical Context

```markdown
# Level 1: Always Include (2-3 sentences)
Project: E-commerce platform. Stack: React/FastAPI/PostgreSQL. 
Currently implementing: Shopping cart API.

# Level 2: Include When Relevant (bullet points)
- Using JWT authentication
- Database: PostgreSQL with SQLAlchemy ORM
- Frontend: Material-UI component library
- Deployed: Docker containers on AWS

# Level 3: Include Only When Directly Needed (detailed)
[Paste specific schema, code snippets, error messages only when discussing them]
```

### Decision Log Format

```markdown
## Decision: Use Redis for Session Storage
**Date**: 2025-01-20
**Context**: Need fast session lookup for authenticated users
**Options Considered**: PostgreSQL, Redis, Memcached
**Decision**: Redis
**Rationale**: Best performance/complexity tradeoff for our scale
**Status**: Implemented
```

Only paste relevant decisions when working on related features.

### Code Context Template

```markdown
Working on: [specific function/feature]
File: [path/to/file.py]
Issue: [describe problem]
Context: [paste minimal relevant code, not entire file]
```

---

## Troubleshooting Memory Issues

### "Claude doesn't remember our detailed conversation"

**Diagnosis:**
- Check if conversation was recent (lag?)
- Verify you're in same context (Project vs. non-Project)
- Use `conversation_search` to find original conversation

**Solution:**
- Use explicit memory commands for key facts
- Paste relevant context from external docs
- Link to or export the original conversation

### "Claude remembers wrong information"

**Diagnosis:**
- Memory extraction may have misunderstood context
- Information may be stale
- Could be hallucination filling gaps in memory

**Solution:**
- Use `memory_user_edits` to view current memory
- Remove/replace incorrect information
- Provide correct context explicitly in message

### "Memory seems inconsistent across sessions"

**Diagnosis:**
- Automatic extraction is probabilistic
- Updates may not have propagated
- Different sessions may have different memory snapshots

**Solution:**
- Always provide critical context at session start
- Use explicit memory commands for important facts
- Maintain external documentation as source of truth

---

## Summary

### Key Principles

1. **Memory is convenience, not reliability**
   - Useful for avoiding repetition
   - Cannot be trusted as sole source of truth

2. **External documentation is essential**
   - Git repository with markdown docs
   - Exported conversations
   - Decision logs

3. **Provide context explicitly**
   - Don't assume memory is complete
   - Paste relevant info at session start
   - Use explicit memory commands for key facts

4. **Understand the limitations**
   - Extraction is lossy
   - There is lag
   - Probabilistic nature causes variation

5. **Treat memory like cache**
   - Performance optimization, not data storage
   - May be invalidated
   - Always have authoritative source elsewhere

### For Students: The Bottom Line

**Do this:**
```markdown
1. Create Git repo with documentation
2. Keep `claude_context.md` updated
3. Export important conversations
4. Start each session with relevant context
5. Use explicit memory commands for key facts
```

**Don't rely on:**
```markdown
1. Claude "just remembering" complex details
2. Memory being consistent across sessions
3. Conversation history as project documentation
4. Automatic extraction catching everything important
```

---

## Further Reading

- [Anthropic Documentation](https://docs.anthropic.com) - Official documentation
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) - Best practices for working with Claude
- Your institution's guidelines on AI tool usage in coursework

---

## Document Information

**Created**: January 2025  
**Purpose**: Educational guide for students  
**Maintenance**: Update as Claude's memory system evolves  
**Feedback**: Please submit issues/PRs if you discover additional details about memory behavior

---

## License

This document is provided for educational purposes. Feel free to use, modify, and distribute for teaching and learning about LLM memory systems.# How Gemini's Persistent Memory Actually Works

As of 2026, Gemini's memory architecture is distinct from its competitors (like Claude’s `userMemories`). It utilizes a **Unified Memory Model** that balances an enormous short-term context window with a structured, long-term user profile.

## 🏗️ The Architecture

Gemini operates using two primary layers of information retrieval:

### 1. Short-Term: The Context Window ("RAM")

* **Capacity:** Gemini 1.5 Pro/Flash supports up to **1 million tokens** (with some versions scaling to 2M).
* **Function:** This is the current conversation history. It is volatile and "forgets" once a session ends or the token limit is reached.
* **Strength:** Unlike Claude, which may summarize early messages to save space, Gemini maintains "near-perfect retrieval" (Needle-in-a-Haystack) across its entire window. You can drop a 1,000-page PDF into the chat, and it stays "live" for the duration of that session.

### 2. Long-Term: Personal Context / Saved Info ("Hard Drive")

* **The User Summary:** This is a structured document (`user_context`) that Gemini maintains behind the scenes. It organizes what it knows about you into categories:
* **Demographics:** Career, location, name.
* **Interests:** Hobbies, technical stacks, character preferences.
* **Dated Events:** Ongoing projects (e.g., "80 Days to Stay" or "Humanitarians AI").


* **The Rationale System:** Every memory is stored with a "Rationale"—a timestamped note explaining *why* Gemini knows this (e.g., *"User mentioned they are a Professor in a chat on Oct 22, 2025"*).

---

## 🛠️ Tools for Memory Control

### `memory_user_edits`

This is the "Manual Override" tool. It allows for the most persistent form of memory.

* **Limit:** Maximum of **30 entries**.
* **Size:** Maximum of **200 characters** per entry.
* **Persistence:** Indefinite. These stay until manually deleted by the user.
* **Priority:** These carry the highest weight. If a manual entry says "I use Python," Gemini will ignore search data suggesting you use Java.

### Automatic Extraction

* **Background Updates:** Gemini periodically distills past conversations into the User Summary.
* **Pruning:** When you delete a conversation, the "leaves" (memories) associated with that "root" (chat) are eventually pruned during nightly background syncs.

---

## 🧠 Comparison: Gemini vs. Claude

| Feature | Claude (Anthropic) | Gemini (Google) |
| --- | --- | --- |
| **Persistence** | Background extraction via `<userMemories>` | Structured `user_context` + Manual "Saved Info" |
| **Traceability** | Implicit (Hard to see source) | Explicit (Rationale + Date provided) |
| **Capacity** | Token-based / Periodic lag | 1M - 2M Token window / Real-time Google integration |
| **Control** | Limited edits (30 max) | 30 explicit edits + Google "Saved Info" dashboard |

---

## 🎓 Engineering Best Practices for Students

### 1. Treat Memory as a Cache, Not a Database

Do not rely on Gemini "remembering" a 50-step architectural plan via background memory. **Persistent memory is for identity and preferences; the context window is for data.**

### 2. The "Context Injection" Strategy

Because the context window is so large (1M tokens), the most reliable way to maintain a semester-long project is to:

* Maintain a `project_state.md` file.
* Upload it to every new Gemini session.
* This is faster and more accurate than waiting for background memory to sync.

### 3. Use Explicit Commands

To ensure a fact is stored in the 30-slot persistent memory, use:

> *"Gemini, remember this for my future sessions: [Fact under 200 chars]"*

### 4. Manage Deletion

If you delete a chat to "clean up," be aware that any background learning from that chat will eventually disappear. Use **Saved Info** (Manual Edits) for anything you cannot afford to lose.

