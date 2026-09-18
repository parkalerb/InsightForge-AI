# Project Scope

This document establishes the precise boundaries for **InsightForge AI**. It defines what is explicitly included (In-Scope) and excluded (Out-of-Scope) to ensure focused, real-world execution within the 30-day timeline.

---

## 1. In-Scope Items

### 1.1 Target Users
* **Primary**: Business / Strategy Analyst
* **Secondary**: Product Managers, Startup Founders / Decision Makers

### 1.2 Core Strategic Use Cases
1. **Market Entry Research**: Evaluating new market entry feasibility, market sizing, regulatory considerations, and internal readiness.
2. **Technology Comparison**: Comparing technical solutions, frameworks, vendor options, latency/scaling profiles, and TCO.
3. **Competitive / Strategic Analysis**: Benchmarking competitor announcements, pricing tiers, feature parity, and strategic positioning.

### 1.3 Core Workflow & Agent Structure
* **Workflow**: `User Question ──► Planner Agent ──► Research Agent ──► Analysis Agent ──► Verification Agent ──► Report Output`
* **Agent Count**: Exactly 4 specialized agents:
  1. **Planner Agent**
  2. **Research Agent**
  3. **Analysis Agent**
  4. **Verification Agent**
* **Report Generation**: Integrated as the output of the verified workflow (explicitly **not** a separate agent).
* **Conditional Routing**: LangGraph conditional edges supporting re-routing from Verification Agent back to Research Agent if evidence gaps or unverified claims are detected.

### 1.4 Agent Tools
1. **Web Search Tool**: Real-time web search for market and competitive data.
2. **RAG / Vector Search Tool**: Vector retrieval across indexed internal documents.
3. **Python / Data Analysis Tool**: Numerical computations, market calculations, and data formatting.

### 1.5 Supported Document Formats
* **PDF** (`.pdf`)
* **Text** (`.txt`)

### 1.6 Core Technology Stack
* **Language**: Python
* **Backend**: FastAPI
* **Frontend**: Streamlit
* **Agent Framework**: LangChain & LangGraph
* **Data Storage**: PostgreSQL (Relational & Metadata) + Vector Database (Embeddings)
* **Observability**: LangSmith
* **Quality Assurance**: RAG Evaluation Metrics
* **Containerization**: Docker

---

## 2. Explicitly Out-of-Scope Items

To prevent scope creep and maintain architectural simplicity, the following features and architectures are **strictly out of scope** for this initial implementation:

* 🚫 **Mobile Application**: The interface is strictly a web-based desktop dashboard (Streamlit). No native iOS/Android apps will be built.
* 🚫 **Voice Assistant**: Interface is text and document-driven only. No audio transcription or voice interactions.
* 🚫 **10+ Agents**: System is capped at the 4 defined agents (Planner, Research, Analysis, Verification). No bloated agent hierarchies.
* 🚫 **Multi-Agent Swarm**: No unconstrained, non-deterministic agent swarm topologies. Orchestration is deterministically controlled via LangGraph state machine.
* 🚫 **Multiple LLM Providers**: Multi-provider runtime switching or concurrent multi-vendor LLM routing will not be implemented. Vendor interfaces remain abstracted.
* 🚫 **Custom Model Training**: No fine-tuning or training of custom foundational models. Pre-trained LLM and embedding models will be used exclusively.
* 🚫 **Kubernetes**: Deployment is targeted at Docker / Docker Compose. No complex Kubernetes (k8s) manifests or cluster management.
* 🚫 **Microservices Architecture**: The system will be built as a modular monolith containerized via Docker, avoiding distributed microservice overhead.
* 🚫 **Real-Time Collaboration**: No multi-user live document editing, Google-Docs-style co-presence, or WebSocket collaboration rooms.
* 🚫 **Complex Long-Term Memory**: No long-term episodic vector memory graph across months of user conversations. Focus is on session-level state.
* 🚫 **Autonomous Financial Decisions**: The platform provides research recommendations only; it does NOT execute trades, transfer funds, or authorize financial transactions.
* 🚫 **Autonomous External Actions**: The system does NOT send emails, post to social media, or invoke mutating external APIs.
* 🚫 **Multi-Language Support**: English is the sole supported language for UI, document parsing, and research reports.
* 🚫 **Large Enterprise RBAC System**: No complex multi-tenant Role-Based Access Control (RBAC), SSO/SAML integration, or granular team permission hierarchies.
