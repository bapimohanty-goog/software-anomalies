"""Helper tools for Phase 3: The True Thought Partner (QAC & Risk Assessment)."""

from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import Any


def save_anomaly_report(
    issue_summary: str,
    risk_estimate_summary: str,
    root_cause_classification: str,
    report_markdown: str,
) -> dict[str, Any]:
    """Saves the Phase 3 Comprehensive QAC Recommendation Report to a Markdown file.

    Call this tool once all 4 assessment steps have been completed and synthesized
    into the Comprehensive QAC Recommendation Report, or when the user revises
    details and wants to re-export the report.

    Args:
        issue_summary: Clear, vivid one-line summary of the software anomaly.
        risk_estimate_summary: Summary of Frequency, Severity, and Risk = Frequency x Severity.
        root_cause_classification: Primary root cause category (e.g., "Requirements / Specification",
            "Verification / Implementation", or "Systemic / Process").
        report_markdown: The complete Markdown-formatted Comprehensive QAC Recommendation
            Report ready for Quality Assurance & Compliance review.

    Returns:
        A dictionary containing the status, report_id, saved file path, timestamp,
        risk_estimate_summary, root_cause_classification, and full report markdown.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", issue_summary.lower()).strip("-")[:48] or "anomaly"
    report_id = f"P3-QAC-{timestamp}-{slug[:20]}"
    filename = f"phase3_qac_recommendation_report_{timestamp}_{slug}.md"

    output_dir_str = os.environ.get("ANOMALY_REPORTS_DIR", "reports/phase3")
    output_dir = Path(output_dir_str)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        file_path.write_text(report_markdown.strip() + "\n", encoding="utf-8")
        saved_path = str(file_path.resolve())
    except OSError:
        fallback_dir = Path("/tmp/sw_anomaly_reports/phase3")
        fallback_dir.mkdir(parents=True, exist_ok=True)
        file_path = fallback_dir / filename
        file_path.write_text(report_markdown.strip() + "\n", encoding="utf-8")
        saved_path = str(file_path.resolve())

    return {
        "status": "success",
        "phase": "Phase 3: The True Thought Partner (QAC)",
        "report_id": report_id,
        "issue_summary": issue_summary,
        "risk_estimate_summary": risk_estimate_summary,
        "root_cause_classification": root_cause_classification,
        "saved_file_path": saved_path,
        "created_at_utc": timestamp,
        "report_markdown": report_markdown,
    }
