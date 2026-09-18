# Core Use Cases

This document details the three primary strategic use cases supported by **InsightForge AI**. Each use case illustrates how internal documents (PDF/TXT) and external web data are processed through the 4-agent LangGraph workflow.

---

## Use Case 1: Market Entry Research

### 1.1 Overview & Persona
* **Target User**: Business / Strategy Analyst
* **Goal**: Evaluate the feasibility, market size, regulatory landscape, and strategic risks of expanding a product or business line into a new geographical or domain market.

### 1.2 User Inputs
* **Natural Language Query**: `"Analyze the strategic feasibility of expanding our cloud enterprise SaaS platform into the Southeast Asian market, focusing on compliance, local competition, and addressable market size."`
* **Internal Documents Uploaded**:
  * `Internal_Financial_Targets_2026.pdf`
  * `Security_Compliance_Capabilities.txt`

### 1.3 Step-by-Step Workflow Execution

```
[User Query + Uploads]
       │
       ▼
1. Planner Agent ──► Formulates sub-queries:
                      - Sub-task A: Query Internal RAG for expansion budget & compliance readiness.
                      - Sub-task B: Execute Web Search for SEA SaaS regulatory policies & market size.
                      - Sub-task C: Run Data Analysis for TAM projections.
       │
       ▼
2. Research Agent ──► Invokes Tools:
                      - RAG Tool: Retrieves pages 4-6 of Internal_Financial_Targets.pdf.
                      - Web Search Tool: Gathers 2025/2026 SEA cloud compliance & market size reports.
                      - Python Tool: Calculates 3-year projected CAGR based on retrieved figures.
       │
       ▼
3. Analysis Agent ──► Synthesizes internal capability vs. external market growth:
                      - Identifies regulatory gap in data residency requirements.
                      - Constructs preliminary market entry recommendation draft.
       │
       ▼
4. Verification Agent ─► Audits claims:
                      - Cross-checks SEA market size claim against retrieved Web Search source.
                      - Validates compliance capability against Security_Compliance_Capabilities.txt.
                      - Pass: Emits finalized structured report.
```

### 1.4 Expected Output Structure
* **Executive Summary**: Strategic recommendation on SEA expansion.
* **Internal Readiness Assessment**: Budget alignment and security compliance gap analysis (cited from `Security_Compliance_Capabilities.txt`).
* **Market Opportunity & TAM Analysis**: Quantified market size and growth forecast (derived via Python tool calculation).
* **Regulatory & Risk Profile**: Key data residency laws and hurdles (cited from web sources).
* **Sources & Citations**: Explicit mapping of claims to internal file page numbers and external URLs.

---

## Use Case 2: Technology Comparison

### 2.1 Overview & Persona
* **Target User**: Product Manager / Technical Strategy Analyst
* **Goal**: Conduct a rigorous comparison between technical frameworks, platforms, or vendor solutions to make an informed architectural or procurement decision.

### 2.2 User Inputs
* **Natural Language Query**: `"Compare Vector Database Option A vs Option B for our internal enterprise AI search infrastructure, factoring in latency, scaling constraints, licensing costs, and compatibility with our existing stack."`
* **Internal Documents Uploaded**:
  * `Current_Architecture_Spec.pdf`
  * `Vendor_Quotes_Comparison.txt`

### 2.3 Step-by-Step Workflow Execution

1. **Planner Agent**:
   * Identifies comparison parameters: Latency, Scalability, Pricing, Integration Overhead.
   * Schedules Internal RAG for architecture constraints and Web Search for external benchmarks.
2. **Research Agent**:
   * Uses **RAG Tool** on `Current_Architecture_Spec.pdf` to identify required throughput (QPS) and cloud provider compatibility.
   * Uses **Web Search Tool** to fetch technical benchmarks and community consensus on Vector DB Option A vs Option B.
   * Uses **Python Data Analysis Tool** to compute total cost of ownership (TCO) across 1M, 10M, and 100M vector index scales.
3. **Analysis Agent**:
   * Constructs comparative matrix highlighting strengths, weaknesses, latency profiles, and cost projections.
4. **Verification Agent**:
   * Evaluates pricing assumptions against `Vendor_Quotes_Comparison.txt`.
   * Flags missing latency benchmark at 100M vectors -> **Triggers Conditional Re-routing** back to Research Agent for dedicated benchmark search.
   * Receives updated evidence and passes verification.

### 2.4 Expected Output Structure
* **Comparison Matrix Table**: Feature-by-feature evaluation.
* **Architectural Compatibility Analysis**: Fit with current stack (cited from `Current_Architecture_Spec.pdf`).
* **Cost & TCO Breakdown**: Python-calculated cost metrics across scale tiers.
* **Risk & Tradeoff Matrix**: Vendor lock-in, open-source vs proprietary tradeoffs.
* **Verified References**: Page-level internal citations + verified web benchmark links.

---

## Use Case 3: Competitive / Strategic Analysis

### 3.1 Overview & Persona
* **Target User**: Startup Founder / Strategy Director
* **Goal**: Perform a comprehensive competitive intelligence analysis evaluating competitor moves, market share shifts, feature gaps, and strategic positioning.

### 3.2 User Inputs
* **Natural Language Query**: `"Evaluate Competitor X's latest product release and pricing tier changes against our internal roadmap to identify strategic defense vectors."`
* **Internal Documents Uploaded**:
  * `Product_Roadmap_Q3_Q4.pdf`
  * `Internal_Pricing_Strategy.txt`

### 3.3 Step-by-Step Workflow Execution

1. **Planner Agent**:
   * Deconstructs query into: Competitor X recent launch features, pricing updates, internal roadmap alignment, counter-strategy formulation.
2. **Research Agent**:
   * Runs **Web Search Tool** to scrap Competitor X press releases, pricing pages, and customer reviews.
   * Runs **RAG Tool** on `Product_Roadmap_Q3_Q4.pdf` and `Internal_Pricing_Strategy.txt` to retrieve upcoming feature milestones and margin requirements.
   * Runs **Python Tool** to model price elasticity and feature parity ratios.
3. **Analysis Agent**:
   * Synthesizes competitor positioning vs. internal roadmap timeline.
   * Highlights feature overlap and identifies key differentiation opportunities.
4. **Verification Agent**:
   * Verifies competitor pricing claims against external URL sources.
   * Verifies internal roadmap launch dates against `Product_Roadmap_Q3_Q4.pdf`.
   * Approves final report structure.

### 3.4 Expected Output Structure
* **Competitor Update Summary**: Key features and pricing shifts announced by Competitor X.
* **Strategic Feature Parity & Gap Analysis**: Comparative grid comparing internal roadmap items with competitor capabilities.
* **Impact & Margin Risk Assessment**: Quantitative insights computed via Python tool.
* **Recommended Counter-Actions**: Prioritized strategic initiatives for product and sales teams.
* **Sources & Attribution**: Full citation list linking internal roadmap pages and external competitor sources.
