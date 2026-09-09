"""Selected projects, drawn from the work described in the resume."""

from __future__ import annotations

from app import theme
from app.models import Metric, Project

PROJECTS = (
    Project(
        slug="clinical-rag",
        title="Clinical Knowledge RAG Platform",
        domain="Healthcare / Retrieval",
        accent=theme.CARAMEL_MID,
        summary=(
            "Hybrid vector and keyword retrieval with re-ranking over medical policies, "
            "formularies, and provider guidelines, lifting retrieval accuracy to around 88% "
            "and grounding answers in cited source documents."
        ),
        tags=("RAG", "Azure AI Search", "Azure OpenAI", "PySpark", "Databricks", "FastAPI"),
        metrics=(
            Metric(value="88%", label="Retrieval Accuracy", sub="hybrid + re-rank"),
            Metric(value="-35%", label="Hallucination Rate", sub="vs. first release"),
        ),
        problem=(
            "Member services and care management teams were reading through medical policies, "
            "formularies, and provider guidelines by hand to answer questions that had to be "
            "correct the first time."
        ),
        contribution=(
            "Built the retrieval layer — chunking, embedding, and metadata enrichment on "
            "PySpark and Databricks, then hybrid vector and keyword search with a re-ranking "
            "stage — and wired it behind a FastAPI service with per-answer citations."
        ),
        outcome=(
            "Retrieval accuracy reached roughly 88%, and an evaluation harness tracking "
            "groundedness and hallucination rate drove iterative fixes that cut hallucinations "
            "by about 35%."
        ),
    ),
    Project(
        slug="mcp-gateway",
        title="MCP Server Suite for Governed Tool Access",
        domain="Healthcare / Agent Infrastructure",
        accent=theme.GOLD,
        summary=(
            "Reusable Model Context Protocol servers exposing claims data, provider "
            "directories, and clinical knowledge bases to LLMs through one governed contract "
            "instead of bespoke per-team integrations."
        ),
        tags=("MCP", "Python", "FastAPI", "RBAC", "Audit Logging", "Key Vault"),
        metrics=(
            Metric(value="3", label="Shared Domains", sub="claims, providers, knowledge"),
            Metric(value="100%", label="Audited Tool Calls", sub="access + logging"),
        ),
        problem=(
            "Every squad wiring an LLM to internal data was writing its own integration, each "
            "with a different auth story and no consistent audit trail."
        ),
        contribution=(
            "Contributed to standardizing agent-to-tool integration on MCP: reusable servers "
            "per data domain, role-based access on every tool, and structured audit logging "
            "of each call."
        ),
        outcome=(
            "New agents consume claims, provider, and clinical knowledge tools without "
            "rebuilding access control, and every tool call lands in the audit log the "
            "compliance reviews ask for."
        ),
    ),
    Project(
        slug="langgraph-ops",
        title="Multi-Agent Clinical Operations Workflows",
        domain="Healthcare / Agents",
        accent=theme.AMBER,
        summary=(
            "LangGraph workflows with tool calling and shared memory that carry clinical and "
            "operational tasks end to end, replacing steps that previously required manual "
            "review at each handoff."
        ),
        tags=("LangGraph", "LangChain", "Tool Calling", "Shared Memory", "Redis", "AKS"),
        metrics=(
            Metric(value="~2s", label="p95 Latency", sub="cached + async"),
            Metric(value="Multi-step", label="Task Automation", sub="was manual review"),
        ),
        problem=(
            "Operational tasks spanned several systems and a person had to shepherd each one, "
            "re-reading the same context at every handoff."
        ),
        contribution=(
            "Implemented multi-agent workflows in LangGraph and LangChain with tool calling "
            "and shared memory, shipped as FastAPI microservices with caching and async "
            "processing on AKS."
        ),
        outcome=(
            "Tasks that needed manual review now run as governed agent workflows, holding p95 "
            "latency around two seconds and degrading gracefully under load."
        ),
    ),
    Project(
        slug="fraud-scoring",
        title="Near-Real-Time Fraud Scoring Engine",
        domain="Banking / Streaming ML",
        accent=theme.BRONZE,
        summary=(
            "Supervised and unsupervised models on Kafka and Spark Structured Streaming "
            "scoring millions of transactions a day, surfacing fraud signals in seconds "
            "instead of overnight batch."
        ),
        tags=("XGBoost", "scikit-learn", "Kafka", "Spark Streaming", "Delta Lake", "Azure ML"),
        metrics=(
            Metric(value="-30%", label="False Positives", sub="vs. rules-based checks"),
            Metric(value="Millions/day", label="Transactions Scored", sub="seconds, not nightly"),
        ),
        problem=(
            "Rules-based checks flagged too much legitimate activity, and nightly batch runs "
            "meant analysts saw fraud signals long after the transaction cleared."
        ),
        contribution=(
            "Built the models and the feature pipelines behind them — PySpark and Databricks "
            "into Delta Lake — then moved scoring onto Kafka and Spark Structured Streaming "
            "with drift monitoring and a scheduled retraining cadence."
        ),
        outcome=(
            "False positives fell roughly 30% against the earlier rules, and fraud signals now "
            "reach risk analyst dashboards within seconds of the transaction."
        ),
    ),
)
