# InsightForge AI

> **Agentic Decision Intelligence Platform**

InsightForge AI is an AI-powered decision intelligence platform designed to help **Business and Strategy Analysts** conduct rigorous research on complex business and technology topics. By synthesizing internal documents (PDFs, TXT) and external web sources, InsightForge AI analyzes evidence, verifies critical claims, and generates structured, source-backed decision research reports.

---

## 📌 Project Overview

* **Project Goal**: Enable data-backed, verified research reports for strategic decision-making.
* **Primary Target User**: Business / Strategy Analyst
* **Secondary Target Users**: Product Managers, Startup Founders / Decision Makers
* **Project Duration**: 30 Days (4 Sprints)

---

## 🔄 Core Workflow

```
User Question
    │
    ▼
┌──────────────┐
│ Planner Agent│ ── (Decomposes research query into targeted sub-tasks)
└──────┬───────┘
       │
       ▼
┌───────────────┐
│Research Agent │ ◄─────────────────────────────────────────────┐
└──────┬────────┘ ── (Executes RAG + Web Search + Data Analysis)│
       │                                                       │
       ▼                                                       │
┌───────────────┐                                              │
│Analysis Agent │ ── (Synthesizes findings & report draft)     │
└──────┬────────┘                                              │
       │                                                       │
       ▼                                                       │
┌──────────────────┐                                           │
│Verification Agent│ ── (Fact-checks claims against evidence)   │
└──────┬───────────┘                                           │
       │                                                       │
       ├────────────── [ FAIL: Re-research Loop ] ─────────────┘
       │
       │ [ PASS: Verification Complete ]
       ▼
┌───────────────────────────────┐
│  Structured Research Report   │
│  with Sources & Citations     │
└───────────────────────────────┘
```

> **Note**: Report generation is **not** a separate agent. It is produced as the final structured artifact of the workflow.

---

## 🤖 Planned Agentic Architecture

The platform uses **LangGraph** to orchestrate four dedicated agents with stateful coordination and conditional routing:

1. **Planner Agent**: Formulates a structured research strategy, identifying necessary internal document retrievals and external web queries.
2. **Research Agent**: Collects evidence using internal RAG (Vector Search), external Web Search, and Python Data Analysis tools.
3. **Analysis Agent**: Evaluates collected evidence, identifies core insights, and drafts a structured analysis.
4. **Verification Agent**: Audits statements, cross-references sources, verifies claims, and conditionally routes back to the Research Agent if gaps or inconsistencies are found.

---

## 🛠️ Tech Stack & Key Technologies

* **Language**: Python
* **API Framework**: FastAPI
* **Orchestration**: LangChain, LangGraph
* **LLM & Embeddings**: Abstracted LLM Interface & Vector Embeddings
* **Database & Storage**: PostgreSQL (Relational/Metadata), Vector Database (Embeddings & Document Indexing)
* **User Interface**: Streamlit
* **Observability & Evaluation**: LangSmith, RAG Evaluation Frameworks
* **Deployment**: Docker

---

## 📚 Project Documentation

Detailed project specification documents are available in the `docs/` directory:

| Document | Description |
| :--- | :--- |
| 📄 [Problem Statement](docs/problem-statement.md) | Business challenges, target audience, and core solution objectives. |
| 📄 [Requirements](docs/requirements.md) | Functional, non-functional, and agent workflow requirements. |
| 📄 [Use Cases](docs/use-cases.md) | End-to-end workflows for Market Entry, Tech Comparison, and Strategic Analysis. |
| 📄 [Architecture](docs/architecture.md) | System design, agent coordination flow, database schema, and tool integration. |
| 📄 [Scope](docs/scope.md) | Clear boundaries detailing explicit in-scope and out-of-scope items. |
| 📄 [Roadmap](docs/roadmap.md) | 30-day implementation plan split into 4 distinct 1-week sprints. |

---

## 🚀 Quick Start (Documentation Phase)

Currently, the project is in the **initial documentation and planning phase**. Application code, agent implementations, and RAG pipelines will be added sequentially following the [Project Roadmap](docs/roadmap.md).