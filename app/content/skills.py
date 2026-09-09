"""Skill matrix, grouped the way the resume groups it.

Levels are self-assessed proficiency, used only to size the bars.
"""

from __future__ import annotations

from app import theme
from app.models import Skill, SkillCategory

CATEGORIES = (
    SkillCategory(
        title="Languages & Core",
        icon="&#9000;&#65039;",
        accent=theme.CARAMEL_MID,
        skills=(
            Skill("Python", 95),
            Skill("SQL", 90),
            Skill("TypeScript", 72),
            Skill("Bash / Shell", 78),
        ),
    ),
    SkillCategory(
        title="Generative AI",
        icon="&#10024;",
        accent=theme.GOLD,
        skills=(
            Skill("LangChain / LangGraph", 92),
            Skill("Model Context Protocol", 88),
            Skill("Azure OpenAI", 92),
            Skill("Anthropic Claude", 90),
            Skill("Prompt Engineering", 90),
        ),
    ),
    SkillCategory(
        title="Retrieval & Vector Search",
        icon="&#128269;",
        accent=theme.AMBER,
        skills=(
            Skill("RAG Pipeline Design", 92),
            Skill("Azure AI Search", 90),
            Skill("pgvector / FAISS", 85),
            Skill("sentence-transformers", 84),
            Skill("Hybrid Search & Re-ranking", 88),
        ),
    ),
    SkillCategory(
        title="ML & Modelling",
        icon="&#129302;",
        accent=theme.BRONZE,
        skills=(
            Skill("scikit-learn / XGBoost", 90),
            Skill("PyTorch", 82),
            Skill("Hugging Face Transformers", 86),
            Skill("spaCy / Clinical NLP", 84),
            Skill("Evaluation Harnesses", 90),
        ),
    ),
    SkillCategory(
        title="Data & MLOps",
        icon="&#9881;&#65039;",
        accent=theme.UMBER,
        skills=(
            Skill("PySpark / Databricks", 90),
            Skill("Delta Lake", 85),
            Skill("Kafka / Airflow", 82),
            Skill("MLflow / Azure ML", 88),
            Skill("Weights & Biases", 80),
        ),
    ),
    SkillCategory(
        title="Platform & Compliance",
        icon="&#128272;",
        accent=theme.HONEY,
        skills=(
            Skill("FastAPI / Flask", 94),
            Skill("Docker / Kubernetes (CKA)", 88),
            Skill("Azure AKS & DevOps", 88),
            Skill("HIPAA / PHI Safeguards", 88),
            Skill("OAuth 2.0 / JWT / RBAC", 85),
        ),
    ),
)

TECH_STACK = (
    "Python", "SQL", "TypeScript", "FastAPI", "Flask", "LangChain", "LangGraph",
    "MCP", "Azure OpenAI", "Anthropic Claude", "Amazon Bedrock", "RAG",
    "Azure AI Search", "pgvector", "FAISS", "sentence-transformers", "PyTorch",
    "scikit-learn", "XGBoost", "Hugging Face", "spaCy", "MLflow", "Azure ML",
    "Weights & Biases", "PySpark", "Pandas", "Databricks", "Delta Lake", "Kafka",
    "Airflow", "Redis", "PostgreSQL", "Azure SQL", "MongoDB", "Cosmos DB",
    "Docker", "Kubernetes", "AKS", "Azure Functions", "Key Vault", "Terraform",
    "GitHub Actions", "Azure DevOps", "Application Insights", "Grafana",
    "HIPAA / PHI", "OAuth 2.0", "pytest",
)
