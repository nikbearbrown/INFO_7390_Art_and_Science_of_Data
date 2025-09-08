# Lecture: What Is Agentic AI?

These are lecture notes for Nik Bear Brown's July 9, 2025 Northeastern course
* INFO 7375  Prompt Engineering for Generative AI*

**What Is Agentic AI?**
Agentic AI represents the next frontier in artificial intelligence—systems that use sophisticated reasoning and iterative planning to autonomously solve complex, multi-step problems. Unlike traditional AI chatbots that simply provide responses based on single interactions, agentic AI can independently analyze challenges, develop strategies, and execute tasks by ingesting vast amounts of data from multiple sources and third-party applications.

Consider the difference:
- **Traditional AI chatbots** use generative AI to provide responses based on a single interaction. A person makes a query and the chatbot uses natural language processing to reply.
- **Agentic AI systems** go further by maintaining ongoing awareness, making decisions, and taking actions across multiple steps to achieve goals.

For example, an AI agent for customer service could operate beyond simple question-answering. With agentic AI, it could check a user's outstanding balance, recommend which accounts could pay it off, and wait for the user's decision to complete the transaction when prompted—handling the entire workflow autonomously.

This lecture will explore how agentic AI is set to enhance productivity and operations across industries. We'll examine how businesses are implementing agentic AI to personalize customer service, streamline software development, enhance healthcare delivery, and transform various other domains.

In this introductory lecture, we'll cover:
1. The foundations of language models and their evolution into agentic systems
2. The taxonomy of AI agents, from simple reflex to sophisticated learning agents
3. The four-step process (Perceive, Reason, Act, Learn) that powers agentic AI
4. Key design patterns for implementing agentic systems
5. Real-world applications demonstrating agentic AI's transformative potential
6. The critical role of communication protocols in enabling multi-agent systems
7. Implementation strategies for organizations of different sizes
8. Future challenges and directions as the field continues to evolve

By the end of this lecture, you'll understand what sets agentic AI apart from traditional AI approaches and why it represents such a significant advancement in artificial intelligence capabilities.



## 1. The Evolution of AI: From Language Models to Agents

### What are Language Models?
At their core, language models are predictive systems that generate text by determining the most probable next word in a sequence:

- **Example:** Given "The students open their," a model might predict "books" as the next word
- This process continues iteratively to create coherent text
- Modern language models undergo a two-phase development:
  - **Pre-training:** Learning from vast text corpora through unsupervised learning
  - **Post-training:** Specialized training including instruction following and reinforcement learning from human feedback (RLHF)

### The Limitations of Traditional Language Models
Despite their capabilities, language models face several challenges:

- **Hallucination:** Generation of incorrect or fabricated information
- **Knowledge cutoff:** Temporal limits to training data
- **Lack of attribution:** Difficulty in identifying information sources
- **Limited interaction:** Inability to engage with external systems
- **Context constraints:** Maximum input size limitations

### The Emergence of Agentic AI
Agentic AI represents the next frontier—systems that use sophisticated reasoning and iterative planning to autonomously solve complex, multi-step problems:

- Unlike traditional AI chatbots that provide responses based on single interactions
- Can independently analyze challenges, develop strategies, and execute tasks
- Ingest data from multiple sources and third-party applications
- Combine language model reasoning with external tool capabilities

## 2. The Five Types of AI Agents

AI agents are classified based on their intelligence, decision-making processes, and environmental interactions:

### 1. Simple Reflex Agent
- Makes decisions based solely on current perceptions using predefined rules
- No memory of past states or actions
- **Example:** A thermostat that turns on heat when temperature drops below a threshold
- **Characteristics:** Fast execution, effective only in predictable environments

### 2. Model-Based Reflex Agent
- Incorporates an internal model of the world
- Maintains state that tracks aspects not currently visible
- **Example:** A robotic vacuum that remembers cleaned areas and obstacle locations
- **Characteristics:** Functions in partially observable environments, still primarily reactive

### 3. Goal-Based Agent
- Makes decisions to achieve specific objectives
- Simulates future outcomes of possible actions
- **Example:** A self-driving car selecting routes to reach a destination
- **Characteristics:** Plans ahead rather than just reacting, adapts to new situations

### 4. Utility-Based Agent
- Evaluates how desirable different outcomes are
- Assigns utility values to possible future states
- **Example:** Drone delivery system optimizing for speed, safety, and efficiency
- **Characteristics:** Ranks options based on desirability, handles trade-offs

### 5. Learning Agent
- Improves performance over time based on experience
- Contains four components: performance element, critic, learning element, problem generator
- **Example:** AI chess bot analyzing games and refining strategy
- **Characteristics:** Adapts to changing environments, most closely resembles human learning

### Multi-Agent Systems
- Multiple agents operating in a shared environment
- Combines different agent types to leverage respective strengths
- Addresses complex problems single agents cannot solve effectively
- Requires standardized communication protocols

## 3. The Four-Step Process of Agentic AI

Agentic AI operates through a systematic four-step process:

### 1. Perceive
- Gather and process data from various sources
- Extract meaningful features and identify relevant entities
- Connect to databases, APIs, and digital interfaces

### 2. Reason
- Use language models as the orchestration engine
- Understand tasks and generate solutions
- Coordinate specialized models for specific functions
- Apply techniques like retrieval-augmented generation (RAG)

### 3. Act
- Integrate with external tools via APIs
- Execute tasks based on formulated plans
- Implement guardrails to ensure appropriate actions
- Interface with databases, web services, and applications

### 4. Learn
- Continuously improve through feedback loops
- Create a "data flywheel" where interaction data enhances models
- Adapt to become more effective over time
- Refine strategies based on success metrics

## 4. Key Design Patterns for Agentic AI

### Planning
- Break complex tasks into manageable subtasks
- Generate action sequences
- Create explicit plans before execution

### Reflection
- Evaluate and improve outputs
- Generate initial solutions, then critique them
- Produce improved versions based on self-assessment
- Particularly effective for code refactoring and writing improvement

### Tool Usage
- Extend capabilities beyond text generation
- Make API calls to external services
- Generate and execute code in sandboxed environments
- Query databases and retrieve information

### Multi-Agent Collaboration
- Assign specialized agents to different aspects of a task
- Create agents with specific domain expertise
- Implement coordination mechanisms between agents

## 5. Key Design Patterns for Agentic AI

### Planning
- Break complex tasks into manageable subtasks
- Generate action sequences
- Create explicit plans before execution

### Reflection
- Evaluate and improve outputs
- Generate initial solutions, then critique them
- Produce improved versions based on self-assessment
- Particularly effective for code refactoring and writing improvement

### Tool Usage
- Extend capabilities beyond text generation
- Make API calls to external services
- Generate and execute code in sandboxed environments
- Query databases and retrieve information

### Multi-Agent Collaboration
- Assign specialized agents to different aspects of a task
- Create agents with specific domain expertise
- Implement coordination mechanisms between agents

## 6. Real-World Applications of Agentic AI

### Customer Service
- Enhancing self-service capabilities
- Automating routine communications
- Reducing response times and boosting satisfaction
- Implementing digital humans for brand representation

### Content Creation
- Generating initial drafts based on brand guidelines
- Adapting content for different platforms
- Scheduling and distributing across channels
- Saving marketers approximately three hours per content piece

### Software Development
- Analyzing existing codebases
- Identifying bugs and issues
- Generating and testing potential fixes
- Documenting changes and reasoning
- Projected to automate up to 30% of work hours by 2030

### Healthcare
- Distilling critical information from medical data
- Automating administrative tasks
- Providing 24/7 patient support
- Helping with treatment plan adherence

### Video Analytics
- Analyzing live or archived videos
- Responding to natural language requests
- Performing complex operations like video search
- Delivering anomaly alerts and incident reports

### Finance
- Optimizing trading strategies
- Detecting and preventing fraud
- Managing investment portfolios
- Assessing risk in banking applications
- Ensuring regulatory compliance

## 7. What Sets Agentic AI Apart?

The key differentiators of agentic AI from traditional approaches:

1. **Autonomy:** Operating independently without constant supervision
2. **Reasoning capacity:** Adapting to novel situations beyond rule-based systems
3. **Multi-step problem solving:** Breaking down complex tasks methodically
4. **Learning and improvement:** Creating feedback loops for continuous enhancement
5. **Tool integration:** Seamlessly orchestrating multiple external services

## 8. AI Agent Protocols: The Communication Foundation

For AI agents to work together effectively, they need standardized ways to communicate. AI Agent Protocols serve as the universal communication standards that enable different AI agents to interact and collaborate—even if they're built using different technologies or architectures.

These protocols are to AI agents what HTTP is to web browsers and servers: a shared language for coordination. Leading tech companies are investing heavily in these protocols to streamline and automate enterprise workflows.

### Major AI Agent Protocols

#### 1. MCP (Model Context Protocol)
**Developed by Anthropic**

MCP is an open, standardized communication protocol enabling two-way interaction between LLMs (clients) and external tools or services (servers). It functions like a universal connector—seamlessly connecting AI models to any external data or tool.

**Key strengths:**
- Universal compatibility with any LLM or external tool implementing the standard
- Real-time access to external data sources
- Security-first design with built-in authentication mechanisms
- Developer-friendly implementation with extensive documentation

**Limitations:**
- Primarily designed for tool integration rather than inter-agent coordination
- Can introduce latency for simple operations
- Requires understanding of the protocol specification

**Best use cases:** AI assistants needing live external context (weather, market data, sensors), secure standardized tool integration, and real-time decision support systems.

#### 2. A2A (Agent-to-Agent Protocol)
**Developed by Google**

A2A is designed specifically for seamless communication, collaboration, and task execution between AI agents, regardless of vendor, framework, or architecture.

**Key strengths:**
- Cross-platform interoperability across different AI frameworks
- Built-in task state management (created → in-progress → completed)
- Real-time progress updates via streaming support
- Automatic capability discovery through Agent Cards

**Limitations:**
- More complex setup compared to simpler protocols
- Large metadata overhead for simple tasks
- Focuses on agent-to-agent rather than agent-to-tool communication

**Best use cases:** Multi-step enterprise workflows, modular AI systems requiring coordination, and asynchronous task processing across agents.

#### 3. ACP (Agent Communication Protocol)
**Developed by IBM**

ACP is an open, vendor-neutral protocol created by IBM for seamless interactions between AI agents, released under the Linux Foundation through the BeeAI project.

**Key strengths:**
- Familiar RESTful HTTP-based interface for developers
- Support for both synchronous and asynchronous communication
- Robust token-based security and permission system
- Native integration with popular agent frameworks like LangGraph

**Limitations:**
- May favor IBM tools and services
- REST overhead for high-frequency communications
- Complex token management for authorization

**Best use cases:** Complex task management systems, legacy system integration, and enterprise environments requiring robust security.

#### 4. AGP (Agent Gateway Protocol)
**Developed by Cisco**

Part of Cisco's Outshift initiative, AGP aims to power a secure Internet of Agents using gRPC over HTTP/2 for high-performance, scalable agent communication.

**Key strengths:**
- High performance through gRPC over HTTP/2
- Support for multiple patterns: request/response, pub/sub, streaming
- Enterprise-grade security with TLS encryption and authentication
- Optimized for distributed environments

**Limitations:**
- May be overkill for simple local agent interactions
- Steeper learning curve than REST-based protocols
- Requires robust network infrastructure

**Best use cases:** Cross-network agent workflows, high-performance distributed systems, and event-driven architectures.

#### 5. ANP (Agent Network Protocol)
**Developed by ANP Team**

ANP is an open-source protocol designed for seamless interoperability across diverse AI agents using JSON-LD, W3C DIDs, and layered architecture.

**Key strengths:**
- Uses established W3C and JSON-LD standards
- Secure, decentralized authentication through W3C DID
- Rich, linked data representation via JSON-LD
- Truly open-source with no corporate backing

**Limitations:**
- Multiple standards increase implementation complexity
- Fewer development tools and libraries available
- JSON-LD processing can be resource-intensive

**Best use cases:** Cross-domain agent interoperability, research and academic environments, and systems requiring semantic data representation.

#### 6. AGORA Protocol
**Developed at University of Oxford**

AGORA is a scalable communication protocol designed for LLM-based agents that enables natural language protocol negotiation and generation.

**Key strengths:**
- Users can define workflows conversationally through natural language interface
- Creates protocols on-demand based on user intent
- Designed specifically for large language model agents
- Strong academic research foundation

**Limitations:**
- May lack production-ready features
- Requires sophisticated language models to function
- Natural language interpretation can be inconsistent

**Best use cases:** User-centric interaction models, research and prototyping environments, and dynamic workflow generation.

### Multi-Protocol Strategies

Most sophisticated enterprise implementations use multiple protocols together to leverage their respective strengths. Common approaches include:

1. **Layered Architecture**
   - Gateway Layer: AGP for network-level routing and security
   - Agent Layer: A2A for agent-to-agent coordination
   - Tool Layer: MCP for external tool integration

2. **Hybrid Communication Patterns**
   - User Request → AGORA (Natural Language) → A2A (Agent Coordination) → MCP (Tool Access)

3. **Domain-Specific Protocol Selection**
   - Internal Operations: ACP for enterprise task management
   - External Integrations: MCP for third-party tool access
   - Cross-Network: AGP for distributed agent communication

4. **Protocol Translation Bridges**
   - Implementing adapters that translate between different standards
   - A2A ↔ ACP bridge for Google-IBM interoperability
   - MCP ↔ ANP adapter for tool access in semantic environments

The selection of protocols depends on organizational size, use cases, and technical requirements. Small teams might start with one protocol that best fits their primary use case, while large enterprises typically implement multi-protocol strategies with specialized teams and comprehensive translation infrastructure.

## 9. Implementation Strategies

### For Small Teams (1-10 developers)
- Start with one protocol that best fits your primary use case
- Choose based on existing expertise
- Plan for future expansion but avoid over-engineering

### For Medium Organizations (10-100 developers)
- Implement 2-3 protocols for different domains
- Create protocol abstraction layer to hide complexity
- Establish protocol governance and selection criteria

### For Large Enterprises (100+ developers)
- Develop multi-protocol strategy with specialized teams
- Build protocol translation infrastructure
- Implement comprehensive monitoring

### Universal Recommendations
- Invest in protocol abstraction
- Monitor standard evolution
- Participate in the community
- Regularly benchmark performance

## 10. Future Challenges and Directions

### Technical Challenges
- Balancing autonomy and control
- Handling uncertainty in decision-making
- Developing frameworks for ethical decisions
- Ensuring security and robustness
- Standardizing protocols for interoperability

### Future Directions
- Enhanced general reasoning capabilities
- Improved multi-agent coordination
- More intuitive human-AI collaboration
- Development of domain-specific expertise
- Protocol convergence and AI-native protocols
- Quantum-ready security protocols
- Edge computing integration

## 11. Conclusion

Agentic AI represents a natural progression in artificial intelligence capabilities:
- Extends fundamental abilities of language models through structured interaction
- Combines planning, reflection, tool usage, and multi-agent collaboration
- Transforms models from passive text generators into active problem-solvers
- Works best with humans in the loop for complex decisions
- Creates AI systems that not only respond to queries but actively work toward solving complex problems

The emergence of standardized AI agent protocols represents a critical step in the maturation of the agentic AI ecosystem, enabling diverse AI agents to communicate and collaborate effectively regardless of their underlying architecture.

As the field continues to develop, agentic models will become increasingly sophisticated, handling more complex tasks with greater autonomy while maintaining alignment with human intent and values.

