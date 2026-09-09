"""Professional experience, education, and certifications."""

from __future__ import annotations

from app import theme
from app.models import Certification, Education, Role

ROLES = (
    Role(
        title="AI Engineer",
        company="Kaiser Permanente",
        location="Greensboro, NC",
        period="Aug 2025 - Present",
        domain="Healthcare",
        accent=theme.CARAMEL_MID,
        highlights=(
            "Built generative AI features across member services, care management, and clinical "
            "operations, working with product managers and clinicians to turn requirements into "
            "production systems.",
            "Developed RAG pipelines for healthcare knowledge retrieval combining vector and "
            "keyword search with re-ranking, lifting retrieval accuracy to around 88% and "
            "improving grounding across medical policies, formularies, and provider guidelines.",
            "Implemented multi-agent workflows in LangGraph and LangChain with tool calling and "
            "shared memory to automate clinical and operational tasks that previously needed "
            "manual review.",
            "Contributed to standardizing agent-to-tool integration on Model Context Protocol "
            "(MCP), building reusable servers that expose claims data, provider directories, and "
            "clinical knowledge bases to LLMs in a governed, consistent way.",
            "Shipped LLM capabilities as Python and FastAPI microservices with caching and async "
            "processing, holding p95 latency around two seconds and degrading gracefully under "
            "load.",
            "Built evaluation harnesses tracking retrieval accuracy, groundedness, hallucination "
            "rate, and latency, pairing results with user feedback to cut hallucination rate by "
            "around 35%.",
            "Deployed AI services to Azure Kubernetes Service with Docker, managed model "
            "lifecycle with MLflow and Azure DevOps, and applied HIPAA and PHI safeguards "
            "including role-based access, audit logging, and encryption across the AI lifecycle.",
        ),
        tags=(
            "Python",
            "FastAPI",
            "LangGraph",
            "LangChain",
            "MCP",
            "Azure OpenAI",
            "Anthropic Claude",
            "Azure AI Search",
            "Databricks",
            "MLflow",
            "AKS",
            "HIPAA",
        ),
    ),
    Role(
        title="Machine Learning Engineer",
        company="TD Bank",
        location="Charlotte, NC",
        period="Jan 2023 - Aug 2025",
        domain="Banking",
        accent=theme.GOLD,
        highlights=(
            "Built fraud and anomaly detection models with scikit-learn and XGBoost on large "
            "transaction datasets, blending supervised and unsupervised techniques to cut false "
            "positives by around 30% versus the earlier rules-based checks.",
            "Engineered feature pipelines with PySpark, Pandas, and Azure Databricks that turned "
            "raw transaction data into model-ready features for fraud detection and credit risk "
            "scoring, with Delta Lake tables backing training and inference.",
            "Built near-real-time scoring pipelines on Kafka and Spark Structured Streaming that "
            "processed millions of transactions a day and surfaced fraud signals within seconds "
            "instead of waiting on nightly batch runs.",
            "Exposed model inference as secure FastAPI microservices with OAuth2 and JWT, backed "
            "by Redis caching and async processing to keep p95 latency responsive for risk "
            "analyst dashboards.",
            "Trained, tracked, and deployed models on Azure Machine Learning with MLflow, "
            "containerized services with Docker on AKS, and shipped releases through Azure "
            "DevOps pipelines.",
            "Set up drift and performance monitoring with Azure Monitor and Application "
            "Insights, running a scheduled retraining cadence so detection stayed accurate as "
            "fraud patterns shifted.",
            "Applied NLP with spaCy and Hugging Face Transformers for complaint classification "
            "and customer-feedback sentiment analysis feeding compliance review and reporting.",
        ),
        tags=(
            "scikit-learn",
            "XGBoost",
            "PySpark",
            "Kafka",
            "Spark Streaming",
            "Delta Lake",
            "FastAPI",
            "OAuth 2.0",
            "Redis",
            "Azure ML",
            "MLflow",
            "spaCy",
        ),
    ),
    Role(
        title="ML Research Assistant",
        company="Wright State University",
        location="Dayton, OH",
        period="Jan 2022 - Dec 2022",
        domain="Research",
        accent=theme.AMBER,
        highlights=(
            "Supported a faculty-led research group in Computer Science and Engineering on "
            "applied machine learning in healthcare and clinical NLP, contributing to "
            "experiments, dataset preparation, and internal write-ups.",
            "Preprocessed and curated research datasets with Python, Pandas, and NumPy, "
            "handling missing values, class imbalance, and label consistency so downstream "
            "models trained on clean, reproducible inputs.",
            "Trained and evaluated classical and deep learning models with scikit-learn, "
            "XGBoost, and PyTorch on clinical and behavioral data, tracking experiments in "
            "Weights and Biases so results stayed comparable across runs.",
            "Built NLP pipelines with spaCy and Hugging Face Transformers for text "
            "classification and information extraction on unstructured clinical notes, "
            "fine-tuning BERT-based models for domain-specific tasks.",
            "Developed lightweight Flask and FastAPI services letting collaborators run "
            "inference on trained models and browse experiment results through simple React "
            "dashboards.",
            "Containerized experiment environments with Docker so pipelines ran the same way on "
            "lab workstations and shared servers, and presented weekly progress to the research "
            "group.",
        ),
        tags=(
            "PyTorch",
            "scikit-learn",
            "XGBoost",
            "spaCy",
            "Hugging Face",
            "BERT",
            "Weights & Biases",
            "Flask",
            "PySpark",
            "Docker",
        ),
    ),
    Role(
        title="Python Developer",
        company="Reliance",
        location="Hyderabad, India",
        period="Nov 2019 - Jul 2021",
        domain="Telecom",
        accent=theme.BRONZE,
        highlights=(
            "Built web applications and internal automation tools with Python, Django, and "
            "Flask for telecom business processes, building out CRUD features and REST "
            "endpoints.",
            "Wrote Python and shell scripts automating log parsing, data migration, and report "
            "generation, cutting manual effort for the team by roughly 40%.",
            "Built scraping and data-extraction scripts with BeautifulSoup, Requests, and "
            "Selenium to collect, clean, and validate telecom data for reporting dashboards.",
            "Wrote and tuned SQL on MySQL and PostgreSQL, including stored procedures and "
            "triggers, to support reporting and daily operations.",
            "Tested with unittest and Selenium, used Git and Jenkins for version control and "
            "builds, and helped deploy and troubleshoot applications on Linux (RHEL) servers.",
        ),
        tags=(
            "Python",
            "Django",
            "Flask",
            "REST APIs",
            "BeautifulSoup",
            "Selenium",
            "PostgreSQL",
            "MySQL",
            "Jenkins",
            "Linux",
        ),
    ),
)

EDUCATION = (
    Education(
        degree="M.S. Computer Science",
        school="Wright State University",
        location="Dayton, OH",
        period="Aug 2021 - May 2023",
    ),
    Education(
        degree="B.Tech Computer Science & Engineering",
        school="Vignan University",
        location="Guntur, AP, India",
        period="May 2016 - May 2020",
    ),
)

CERTIFICATIONS = (
    Certification(name="Azure AI Fundamentals", issuer="Microsoft"),
    Certification(name="Certified Kubernetes Administrator", issuer="CNCF"),
)
