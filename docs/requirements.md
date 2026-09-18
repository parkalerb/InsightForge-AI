# Project Requirements

## 1. System Overview

InsightForge AI is an Agentic Decision Intelligence Platform designed to automate complex strategic research. The system integrates internal document RAG (PDF/TXT), live web search, quantitative Python data analysis, and multi-agent workflow orchestration via LangGraph.

---

## 2. Functional Requirements (FR)

### FR-1: Document Ingestion & Storage
* **FR-1.1 Document Support**: The system MUST support parsing, chunking, and embedding generation for **PDF** (`.pdf`) and text (`.txt`) documents.
* **FR-1.2 Storage Separation**:
  * Metadata, session history, and report outputs MUST be stored in **PostgreSQL**.
  * Document vector embeddings MUST be indexed and stored in a **Vector Database**.
* **FR-1.3 Ingestion Pipeline**: Extracted document text must be chunked with appropriate chunk size/overlap and indexed with document-level metadata (filename, page numbers).

### FR-2: Multi-Agent Orchestration & Workflow
The workflow MUST be orchestrated using **LangGraph** across 4 core agents:

```
User Question ──► Planner Agent ──► Research Agent ──► Analysis Agent ──► Verification Agent ──► [PASS] ──► Structured Report
                                         ▲                                         │
                                         └─────────── [FAIL: Re-research] ─────────┘
```

* **FR-2.1 Planner Agent**:
  * Deconstructs user business queries into actionable sub-goals and explicit research questions.
  * Formulates search strategies for internal RAG and external web search.
* **FR-2.2 Research Agent**:
  * Invokes research tools to gather relevant evidence.
  * Must utilize internal RAG vector search, live web search, and data processing tools.
* **FR-2.3 Analysis Agent**:
  * Evaluates gathered evidence from both internal and external sources.
  * Synthesizes findings, highlights trends, identifies risks, and drafts the core report sections.
* **FR-2.4 Verification Agent**:
  * Evaluates every key factual claim against retrieved evidence.
  * Performs cross-source attribution and source reliability checks.
  * **Conditional Verification Routing**: If key claims are unverified or evidence is insufficient, triggers a conditional edge in LangGraph to route back to the Research Agent with specific retrieval gaps.
* **FR-2.5 Report Generation**:
  * Report generation MUST NOT be implemented as a separate agent.
  * The final report is generated directly as the structured state output of the verified workflow.

### FR-3: Tool Ecosystem
The system MUST provide 3 core tools to agents:
1. **Web Search Tool**: Fetches live external web data, articles, filings, and industry reports.
2. **RAG / Vector Search Tool**: Performs semantic retrieval across internal indexed PDF/TXT documents.
3. **Python / Data Analysis Tool**: Executes sandboxed Python code for numerical computations, data formatting, or trend calculations.

### FR-4: User Interface & User Experience
* **FR-4.1 Dashboard UI**: Built with **Streamlit** to support:
  * Document upload interface (PDF, TXT).
  * Natural language research query submission.
  * Real-time visibility into active agent execution state and progress.
  * Formatted output rendering for final research reports with interactive source citations.
* **FR-4.2 API Layer**: Built with **FastAPI** exposing RESTful endpoints for:
  * Document upload and indexing status.
  * Research session initialization and execution.
  * History and report retrieval.

---

## 3. Non-Functional Requirements (NFR)

### NFR-1: Factual Accuracy & Citation Traceability
* **Attribution Goal**: The system aims to attach explicit inline citations pointing to internal document page references or external source URLs for all primary factual claims and comparative statistics.

### NFR-2: Observability & Evaluation
* **LangSmith Integration**: System execution traces, prompt calls, agent state transitions, and tool invocations MUST be logged to **LangSmith** for debugging and performance tracking.
* **RAG Evaluation**: Retrieval performance (context recall, precision) and generation quality (faithfulness, answer relevance) MUST be benchmarked using RAG evaluation metrics.

### NFR-3: Containerization & Deployment
* The complete application suite (FastAPI backend, Streamlit frontend, PostgreSQL, Vector DB) MUST be containerized and runnable via **Docker**.

### NFR-4: Scalability & Modularity
* Codebase MUST maintain strict modularity separating API routes, agent node definitions, tools, database access layers, and UI components.
* Provider abstractions MUST allow switching LLM or Vector DB backends without refactoring core agent logic.

---

## 4. Tech Stack Summary Table

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Primary programming language |
| **Backend API** | FastAPI | REST API endpoints & server logic |
| **Frontend UI** | Streamlit | Web interface for analysts |
| **Orchestration** | LangGraph & LangChain | Stateful multi-agent graph orchestration |
| **Relational DB** | PostgreSQL | Session management, metadata & report logs |
| **Vector DB** | Vector Database (Abstracted) | Storing and retrieving document embeddings |
| **Document Formats**| PDF, TXT | Supported input document formats |
| **Observability** | LangSmith | Agent tracing and debug logging |
| **Evaluation** | RAG Evaluation Framework | Quality benchmarking for RAG & agents |
| **Deployment** | Docker | Containerization & local execution |
