# Project Roadmap

This roadmap outlines the 30-day development plan for **InsightForge AI**, structured into 4 sequential 1-week sprints.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             30-Day Project Timeline                         │
├───────────────┬───────────────────┬────────────────────┬────────────────────┤
│   Sprint 1    │     Sprint 2      │      Sprint 3      │      Sprint 4      │
│  (Days 1–7)   │    (Days 8–14)    │    (Days 15–21)    │    (Days 22–30)    │
├───────────────┼───────────────────┼────────────────────┼────────────────────┤
│ Foundation +  │  Advanced RAG +   │   Agentic AI +     │    Production +    │
│  Core RAG     │    Research       │    LangGraph       │    Evaluation +    │
│               │   Intelligence    │                    │     Deployment     │
└───────────────┴───────────────────┴────────────────────┴────────────────────┘
```

---

## 📅 Sprint Breakdown

### Sprint 1: Foundation + Core RAG (Days 1–7)
**Goal**: Establish base repository structure, API service, Streamlit UI, document ingestion pipeline, and baseline internal RAG vector retrieval.

* **Key Deliverables**:
  * Project repository initialization, virtual environment, and dependency configuration.
  * FastAPI REST API boilerplate and API route structures.
  * Streamlit basic dashboard for file uploads and text queries.
  * PDF and TXT document ingestion pipeline (parsing, text chunking, vector embedding generation).
  * Vector Database indexing for document chunks with source metadata (filename, page numbers).
  * Baseline single-pass RAG retrieval engine with preliminary context precision check.
* **Sprint Milestone**: Analyst can upload a PDF/TXT file via Streamlit and retrieve relevant text passages via basic RAG.

---

### Sprint 2: Advanced RAG + Research Intelligence (Days 8–14)
**Goal**: Upgrade RAG retrieval strategies and build out external Web Search and Python Data Analysis tools.

* **Key Deliverables**:
  * Advanced RAG retrieval optimizations (chunk overlap tuning, metadata filtering by document/page).
  * Integration of **Web Search Tool** for fetching live external market data and articles.
  * Integration of **Python / Data Analysis Tool** for running math operations, market sizing calculations, and data formatting.
  * Unified context aggregator combining internal vector search results and web search outputs.
  * Initial RAG evaluation benchmarks measuring retrieval recall and context relevance.
* **Sprint Milestone**: System can execute unified queries fetching both internal document snippets and live web search data.

---

### Sprint 3: Agentic AI + LangGraph (Days 15–21)
**Goal**: Implement stateful multi-agent workflow using LangGraph with 4 core agents and conditional verification routing.

* **Key Deliverables**:
  * LangGraph state machine definition (`AgentState` schema, nodes, edges).
  * **Planner Agent**: Decomposes user question into targeted internal/external research sub-tasks.
  * **Research Agent**: Dynamically invokes RAG, Web Search, and Python Data Analysis tools.
  * **Analysis Agent**: Synthesizes evidence into preliminary structured report sections.
  * **Verification Agent**: Checks factual claims against raw evidence sources.
  * **Conditional Verification Routing**: LangGraph conditional edge routing back to Research Agent when claims are unverified or evidence is incomplete.
  * Citation formatting engine attaching source references to report findings (no separate report agent).
* **Sprint Milestone**: End-to-end multi-agent execution in LangGraph with self-correcting verification loops.

---

### Sprint 4: Production + Evaluation + Deployment (Days 22–30)
**Goal**: Add database persistence, LangSmith observability, end-to-end RAG/Agent evaluation, and Docker containerization.

* **Key Deliverables**:
  * **PostgreSQL Integration**: Schema setup for session management, document metadata, and report history.
  * **LangSmith Observability**: Full execution tracing, agent prompt logging, and latency/cost tracking.
  * **RAG & Agent Evaluation**: Running evaluation suites across the 3 Core Use Cases (Market Entry, Tech Comparison, Competitive Analysis).
  * **Docker Containerization**: Multi-container `docker-compose` setup orchestrating FastAPI, Streamlit, PostgreSQL, and Vector DB.
  * End-to-end user testing, UI polishing, and final project documentation.
* **Sprint Milestone**: Fully containerized, interview-defensible platform running via Docker with end-to-end evaluation metrics.

---

## 🎯 Summary of Sprint Outcomes

| Sprint | Core Focus | Key Artifact Produced |
| :--- | :--- | :--- |
| **Sprint 1** | Foundation + Core RAG | PDF/TXT Document Ingestion & Vector Retrieval |
| **Sprint 2** | Advanced RAG + Research Tools | Web Search & Python Data Analysis Tools |
| **Sprint 3** | Agentic AI + LangGraph | 4-Agent Stateful Workflow with Verification Loop |
| **Sprint 4** | Production & Deployment | Dockerized Platform + LangSmith + Evaluation |
