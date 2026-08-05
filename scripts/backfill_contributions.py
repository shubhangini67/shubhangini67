#!/usr/bin/env python3
"""Create weekday dev-log commits with backdated author dates for GitHub contributions."""

from __future__ import annotations

import os
import subprocess
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = REPO_ROOT / "logs"
START = date(2025, 5, 16)  # GitHub account creation
END = date(2026, 8, 5)

AUTHOR_NAME = "Shubhangini"
AUTHOR_EMAIL = "shubhangini67@users.noreply.github.com"

MILESTONES: list[tuple[str, str]] = [
    ("PathoVision", "memory-augmented ViT training run and patch indexing pipeline"),
    ("PathoVision", "patient-aware grouped splits and leakage-safe evaluation protocol"),
    ("PathoVision", "Grad-CAM explainability maps and occlusion sensitivity analysis"),
    ("PathoVision", "FastAPI inference service with MC dropout uncertainty"),
    ("PathoVision", "Gradio dashboard wiring and Docker deployment config"),
    ("PathoVision", "focal loss + balanced sampling experiments for class imbalance"),
    ("PathoVision", "temperature scaling calibration and reliability diagrams"),
    ("PathoVision", "ResNet18 and CNN baseline benchmark comparisons"),
    ("CareOps", "LangGraph seven-agent orchestration graph scaffolding"),
    ("CareOps", "Qdrant policy RAG with citation-grounded retrieval"),
    ("CareOps", "safety critic node and human approval queue design"),
    ("CareOps", "Prophet demand forecast + live weather signal integration"),
    ("CareOps", "Next.js dashboard health score and live signals strip"),
    ("CareOps", "Groq function-calling chatbot with planning tools"),
    ("CareOps", "Render deployment fixes — Alembic, CORS, Qdrant Cloud"),
    ("ForgeMind", "NASA C-MAPSS data ingestion and feature engineering"),
    ("ForgeMind", "XGBoost RUL regressor and Isolation Forest anomaly layer"),
    ("ForgeMind", "ten-agent LangGraph workflow for predictive maintenance"),
    ("ForgeMind", "WebSocket real-time risk scoring dashboard"),
    ("ForgeMind", "Tata Steel hackathon finalist submission polish"),
    ("Edge AI", "TensorFlow Lite FP32/FP16/INT8 quantization benchmarks"),
    ("Edge AI", "bearing fault classifier and autoencoder anomaly pipeline"),
    ("PocketWise", "FastAPI expense CRUD with 44 pytest coverage"),
    ("Profile", "GitHub profile README analytics and project showcase"),
    ("Research", "IIT BHU histopathology experiment documentation"),
    ("Tests", "unit test expansion and CI workflow hardening"),
    ("Docs", "architecture diagrams and API reference updates"),
    ("Refactor", "typed Pydantic schemas and service layer cleanup"),
]


def is_weekday(d: date) -> bool:
    return d.weekday() < 5


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    merged = os.environ.copy()
    merged["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    merged["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    merged["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    merged["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL
    if env:
        merged.update(env)
    subprocess.run(cmd, cwd=REPO_ROOT, check=True, env=merged)


def main() -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    day = START
    idx = 0
    created = 0
    skipped = 0

    while day <= END:
        if not is_weekday(day):
            day += timedelta(days=1)
            continue

        log_file = LOGS_DIR / f"{day.isoformat()}.md"
        if log_file.exists():
            skipped += 1
            day += timedelta(days=1)
            continue

        project, detail = MILESTONES[idx % len(MILESTONES)]
        idx += 1

        log_file.write_text(
            f"# Dev log · {day.strftime('%A, %d %B %Y')}\n\n"
            f"**Focus:** {project}\n\n"
            f"- {detail}\n"
            f"- Documented progress and pushed incremental changes\n",
            encoding="utf-8",
        )

        commit_date = f"{day.isoformat()} 18:30:00 +0530"
        env = {
            "GIT_AUTHOR_DATE": commit_date,
            "GIT_COMMITTER_DATE": commit_date,
        }
        run(["git", "add", str(log_file.relative_to(REPO_ROOT))], env=env)
        run(
            ["git", "commit", "-m", f"dev-log: {project} progress ({day.isoformat()})"],
            env=env,
        )
        created += 1
        day += timedelta(days=1)

    print(f"Created {created} commits, skipped {skipped} existing.")


if __name__ == "__main__":
    main()
