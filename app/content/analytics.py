"""The "By the Numbers" section: counters, charts, rings, and the heatmap.

Geometry is computed here at import time by :mod:`app.charts`, so the templates
receive finished coordinates rather than doing arithmetic in Jinja.
"""

from __future__ import annotations

from app import theme
from app.charts import build_area_chart, build_bar_chart, build_heatmap, build_ring
from app.models import Counter, LatencyRow, PipelineStage

COUNTERS = (
    Counter(
        target=88,
        suffix="%",
        label="Retrieval Accuracy",
        sub="hybrid search + re-ranking",
    ),
    Counter(
        target=35,
        prefix="-",
        suffix="%",
        label="Hallucination Rate",
        sub="after eval-driven fixes",
    ),
    Counter(
        target=30,
        prefix="-",
        suffix="%",
        label="Fraud False Positives",
        sub="vs. rules-based checks",
    ),
    Counter(
        target=2.0,
        decimals=1,
        suffix="s",
        label="p95 Latency",
        sub="LLM microservices under load",
    ),
)

# Where the ~2s p95 budget goes on one grounded answer.
LATENCY_BUDGET = build_bar_chart(
    (
        ("Retrieve", 180.0, "ms"),
        ("Re-rank", 90.0, "ms"),
        ("Generate", 1450.0, "ms"),
        ("Guardrails", 120.0, "ms"),
    )
)

# Groundedness across successive evaluation runs of the clinical RAG pipeline.
GROUNDEDNESS_CURVE = build_area_chart(
    values=(0.61, 0.68, 0.74, 0.79, 0.83, 0.86, 0.885, 0.90, 0.915, 0.924),
    y_labels=("60%", "70%", "80%", "90%"),
)

# The ring stroke doubles as the colour of the percentage inside it, so these
# come from theme.INK rather than the pale fills.
RINGS = (
    build_ring("Python", "Languages", 95, theme.INK[0]),
    build_ring("FastAPI", "Backend", 94, theme.INK[2]),
    build_ring("LangChain", "GenAI", 92, theme.INK[4]),
    build_ring("RAG", "Retrieval", 92, theme.INK[5]),
    build_ring("LangGraph", "Agents", 90, theme.INK[3]),
    build_ring("PySpark", "Data Eng", 90, theme.INK[1]),
    build_ring("MCP", "Tooling", 88, theme.INK[4]),
    build_ring("MLflow", "MLOps", 88, theme.INK[2]),
)

PIPELINE = (
    PipelineStage(label="Ingest", icon="&#128225;", sub="Blob / Databricks"),
    PipelineStage(label="Chunk & Embed", icon="&#9881;&#65039;", sub="PySpark"),
    PipelineStage(label="Retrieve", icon="&#128269;", sub="Azure AI Search"),
    PipelineStage(label="Generate", icon="&#129302;", sub="Azure OpenAI / Claude"),
    PipelineStage(label="Evaluate", icon="&#128202;", sub="Eval harness"),
)

# 48 half-hour buckets across a working day, five weekdays.
HEATMAP = build_heatmap(("Mon", "Tue", "Wed", "Thu", "Fri"), cols=48)

LATENCY_ROWS = (
    LatencyRow(label="Policy lookup", before_s=45 * 60, after_s=2.0),
    LatencyRow(label="Fraud scoring", before_s=8 * 3600, after_s=1.5),
    LatencyRow(label="Document indexing", before_s=24 * 3600, after_s=45 * 60),
    LatencyRow(label="Clinical summary", before_s=20 * 60, after_s=3.0),
)
