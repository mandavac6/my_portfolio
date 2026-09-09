"""Identity, hero, about and contact content."""

from __future__ import annotations

from app.models import Link, PipelineStage, Profile, Section, Stat, TaglineSegment, Ticker

YEAR = 2026

PROFILE = Profile(
    name="Naveen Mandava",
    initials="NM",
    title="AI/ML Engineer",
    tagline=(
        TaglineSegment("From Prompt To", break_after=True),
        TaglineSegment("Production,", gradient=True, break_after=True),
        TaglineSegment("From RAG To"),
        TaglineSegment("Reliability", gradient=True),
    ),
    summary=(
        "AI/ML Engineer with 5+ years shipping production generative AI across healthcare "
        "and financial services — RAG and multi-agent systems on LangChain, LangGraph, and "
        "MCP, served from FastAPI microservices on Azure."
    ),
    availability="Open to Senior AI / ML Engineering Roles",
    location="Greensboro, NC",
    email="naveen.mandava1999@gmail.com",
    phone="937-986-7149",
    # Fill these in and they render automatically in About and Contact.
    linkedin=None,
    github=None,
)

SECTIONS = (
    Section(
        slug="skills",
        nav_label="Skills",
        eyebrow="Capabilities",
        title="Technical",
        title_accent="Skills",
        blurb="The stack I work in daily — grouped by the problem each layer solves.",
    ),
    Section(
        slug="projects",
        nav_label="Projects",
        eyebrow="Selected Work",
        title="Projects &",
        title_accent="Impact",
        blurb="Four systems selected for depth of ownership and a measurable outcome.",
    ),
    Section(
        slug="experience",
        nav_label="Experience",
        eyebrow="Career",
        title="Work",
        title_accent="Experience",
        blurb="Five years across healthcare, banking, applied research, and telecom — each role building on the last.",
    ),
    Section(
        slug="analytics",
        nav_label="Metrics",
        eyebrow="Systems in Motion",
        title="By the",
        title_accent="Numbers",
        blurb="Evaluation and reliability metrics from the systems described above.",
    ),
    Section(
        slug="about",
        nav_label="About",
        eyebrow="Background",
        title="About",
        title_accent="Me",
    ),
    Section(
        slug="contact",
        nav_label="Contact",
        eyebrow="Get In Touch",
        title="Let's",
        title_accent="Connect",
        blurb=(
            "Open to senior AI/ML and GenAI engineering roles where retrieval, agents, and "
            "production reliability meet."
        ),
    ),
)

HERO_STATS = (
    Stat(value="5+", label="Years Experience"),
    Stat(value="88%", label="Retrieval Accuracy"),
    Stat(value="~2s", label="p95 Latency"),
    Stat(value="-35%", label="Hallucination Rate"),
)

HERO_HEADLINE_METRIC = Ticker(
    label="Retrieval Accuracy",
    values=("88.4%", "87.9%", "88.7%", "88.1%"),
    interval_ms=2200,
)

# Relative bar heights for the little sparkline in the hero dashboard.
HERO_SPARKLINE = (2.1, 2.8, 2.4, 4.1, 3.6, 5.9, 5.2, 7.6, 7.1, 9.4)

HERO_TICKERS = (
    Ticker(
        label="p95 Latency",
        icon="&#9889;",
        values=("1.9s", "2.1s", "1.8s", "2.0s"),
        interval_ms=2500,
    ),
    Ticker(
        label="Groundedness",
        icon="&#127919;",
        values=("92.4%", "91.8%", "92.9%", "92.1%"),
        interval_ms=2800,
    ),
    Ticker(
        label="Agent Runs",
        icon="&#129302;",
        values=("31 active", "28 active", "34 active", "30 active"),
        interval_ms=2600,
    ),
    Ticker(
        label="Eval Pass Rate",
        icon="&#10003;",
        values=("99.1%", "98.8%", "99.3%", "99.0%"),
        interval_ms=3000,
    ),
)

HERO_STAGES = (
    PipelineStage(label="Ingest", icon="&#128225;", sub="Databricks", progress=100),
    PipelineStage(label="Embed", icon="&#9881;&#65039;", sub="PySpark", progress=88),
    PipelineStage(label="Retrieve", icon="&#128269;", sub="AI Search", progress=92),
    PipelineStage(label="Generate", icon="&#129302;", sub="Azure OpenAI", progress=95),
)

HERO_BADGES = (
    Stat(value="88%", sub="Retrieval Acc.", label=""),
    Stat(value="~2s", sub="p95 Latency", label=""),
    Stat(value="5 yrs", sub="Experience", label=""),
)

ABOUT_LEAD = "I build the retrieval and agent infrastructure that makes LLMs safe to put in front of clinicians."

ABOUT_PARAGRAPHS = (
    "Five years in, my work sits where generative AI stops being a demo and has to answer to "
    "an audit trail. I design RAG pipelines that combine vector and keyword search with "
    "re-ranking, multi-agent workflows in LangGraph that call real tools with shared memory, "
    "and MCP servers that expose claims data, provider directories, and clinical knowledge "
    "bases to models in a governed, consistent way.",
    "Healthcare and financial services both punish hand-waving, in different currencies. At "
    "Kaiser Permanente that means HIPAA and PHI safeguards, role-based access, and audit "
    "logging across the AI lifecycle; at TD Bank it meant fraud models whose false positives "
    "cost real money and whose lineage had to survive model risk review. That mix shaped how "
    "I build: evaluation harnesses tracking groundedness and hallucination rate before "
    "anything ships, and structured logging and tracing so I can explain a bad answer after "
    "it does.",
)

QUICK_FACTS = (
    Link(label="Location", href="", value="Greensboro, NC", icon="&#128205;"),
    Link(label="Current Role", href="", value="AI Engineer — Kaiser Permanente", icon="&#128188;"),
    Link(label="Education", href="", value="MS CS — Wright State University", icon="&#127891;"),
    Link(
        label="Email",
        href=f"mailto:{PROFILE.email}",
        value=PROFILE.email,
        icon="&#9993;&#65039;",
    ),
    Link(label="Phone", href=PROFILE.tel, value=PROFILE.phone, icon="&#128222;"),
)

ROLE_PREFERENCES = (
    "Senior AI / ML Engineer",
    "GenAI / LLM Engineer",
    "ML Platform Engineer",
    "Staff Applied AI Engineer",
)

SOCIALS = tuple(
    link
    for link in (
        Link(label="Email", href=PROFILE.mailto, value=PROFILE.email, icon="mail"),
        Link(label="Phone", href=PROFILE.tel, value=PROFILE.phone, icon="phone"),
        Link(label="LinkedIn", href=PROFILE.linkedin or "", value="LinkedIn", icon="linkedin")
        if PROFILE.linkedin
        else None,
        Link(label="GitHub", href=PROFILE.github or "", value="GitHub", icon="github")
        if PROFILE.github
        else None,
    )
    if link is not None
)
