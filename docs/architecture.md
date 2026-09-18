# System Architecture

## 1. High-Level Architecture Overview

InsightForge AI is designed as a modular, decoupled decision intelligence platform. The architecture separates the user presentation layer, REST API services, stateful agent orchestration engine, document retrieval pipeline, persistent storage layers, and observability tooling.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          Streamlit User Interface                      │
│        (Query Submission, File Uploads, Agent Progress, Report Viewer)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST / SSE
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                            FastAPI Backend                             │
│       (API Routing, Session Management, Document Ingestion Triggers)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   LangGraph Agent Orchestration Engine                 │
│                                                                        │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐           │
│   │Planner Agent │ ──► │Research Agent│ ──► │Analysis Agent│           │
│   └──────────────┘     └──────┬───────┘     └──────┬───────┘           │
│                               ▲                    │                   │
│                               │ (Re-search Loop)   ▼                   │
│                               └────────────── ┌──────────────┐         │
│                                               │ Verification │         │
│                                               │    Agent     │         │
│                                               └──────┬───────┘         │
│                                                      │ (Verified)      │
│                                                      ▼                 │
│                                            [Structured Report Output]  │
└──────────────┬────────────────────┬──────────────────┬─────────────────┘
               │                    │                  │
               ▼                    ▼                  ▼
      ┌────────────────┐  ┌──────────────────┐  ┌──────────────┐
      │  RAG Search    │  │ Web Search Tool  │  │ Python Data  │
      │  Vector Tool   │  │                  │  │ Analysis Tool│
      └───────┬────────┘  └──────────────────┘  └──────────────┘
              │
              ▼
┌────────────────────────────────────────────────────────────────────────┐
│                             Storage Layer                              │
│  ┌──────────────────────────────────┐  ┌────────────────────────────┐  │
│  │   Vector Database                │  │   PostgreSQL Database      │  │
│  │   (Document Embeddings & Chunks) │  │   (Sessions, Metadata,     │  │
│  │                                  │  │    Report History)         │  │
│  └──────────────────────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Observability & Evaluation                        │
│  ┌──────────────────────────────────┐  ┌────────────────────────────┐  │
│  │   LangSmith                      │  │   RAG Evaluation           │  │
│  │   (Execution Tracing & Logs)     │  │   (Metrics & Benchmarks)   │  │
│  └──────────────────────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Details

### 2.1 User Interface (Streamlit)
* Serves as the interactive dashboard for strategy analysts.
* Features:
  * Document upload drop-zone (PDF and TXT formats).
  * Real-time workflow status display tracking active LangGraph nodes.
  * Markdown-rendered report viewer with interactive source citation drawer.

### 2.2 API Layer (FastAPI)
* Exposes asynchronous REST endpoints handling UI calls.
* Manages document upload endpoints, background indexing jobs, and research task initialization.
* Maintains session states and database connections.

### 2.3 Agent Orchestration Engine (LangGraph)
The stateful core of InsightForge AI orchestrates four distinct agent nodes:

1. **Planner Agent Node**:
   * Inspects the input query and available document indexes.
   * Emits a structured execution plan containing specific research sub-goals.
2. **Research Agent Node**:
   * Evaluates sub-goals and dynamically calls available tools (Internal RAG, Web Search, Python Data Analysis).
   * Accumulates raw text excerpts, financial numbers, and web citations into the graph state.
3. **Analysis Agent Node**:
   * Processes retrieved evidence, resolves conflicting statements, and builds a synthesized report structure.
4. **Verification Agent Node**:
   * Scans generated report drafts against original raw evidence to verify claims.
   * **Conditional Routing Logic**:
     * **Pass**: If claims are backed by solid evidence, routes state to the final report output state.
     * **Fail**: If claims lack citations or evidence is contradictory, appends retrieval feedback to graph state and routes back to the **Research Agent Node** via a conditional edge.

> **Key Architectural Decision**: Report generation is **not** handled by a separate agent. The final structured report is generated as the output of the verified graph state.

---

## 3. Tool Architecture

Agents interact with the environment via three standardized tool interfaces:

```
                  ┌────────────────────────────────────────┐
                  │            Tool Interface              │
                  └───────────────────┬────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│  Internal    │              │  External    │              │ Python / Data│
│  RAG Tool    │              │  Web Search  │              │ Analysis Tool│
├──────────────┤              ├──────────────┤              ├──────────────┤
│ Queries      │              │ Queries live │              │ Executes     │
│ Vector DB    │              │ web search   │              │ sandboxed    │
│ for internal │              │ provider for │              │ code for     │
│ PDF/TXT text │              │ real-time    │              │ data math &  │
│ embeddings.  │              │ data.        │              │ formatting.  │
└──────────────┘              └──────────────┘              └──────────────┘
```

---

## 4. Document Ingestion Pipeline

```
PDF / TXT Document
       │
       ▼
┌───────────────────────┐
│ Document Loader       │ ── Extract raw text & metadata (filename, page #)
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Text Splitter         │ ── Chunk text (e.g., 500-1000 tokens with overlap)
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Embedding Model       │ ── Convert text chunks to vector embeddings
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Vector Database       │ ── Store vectors + metadata payload for similarity search
└───────────────────────┘
```

* **Supported Input Formats**: PDF (`.pdf`), Text (`.txt`).
* **Chunking Strategy**: Semantic chunking preserving paragraph boundaries and metadata tags.
* **Vector Indexing**: Indexed with document ID, page number, and source file path for accurate citations.

---

## 5. Data Persistence & Storage Architecture

### 5.1 PostgreSQL (Relational Storage)
* **Sessions Table**: Stores user session IDs, timestamps, and active configurations.
* **Documents Table**: Tracks uploaded document metadata, file paths, upload dates, and indexing status.
* **Reports Table**: Stores generated final reports, raw graph state logs, and verification audit trails.

### 5.2 Vector Database (Vector Storage)
* Stores high-dimensional vector representations of parsed PDF/TXT chunks.
* Supports cosine similarity / HNSW indexing for rapid semantic RAG retrieval.

---

## 6. Observability, Tracing & Evaluation

* **LangSmith**:
  * Captures full execution traces of LangGraph workflows.
  * Logs agent prompts, raw LLM outputs, tool call parameters, latency, and token consumption.
* **RAG Evaluation**:
  * Evaluates context precision and recall for internal RAG retrieval.
  * Benchmarks report faithfulness and hallucination rate during verification testing.
