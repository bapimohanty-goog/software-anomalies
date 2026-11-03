"""Helper tools for Phase 1: Core Triage Anomaly Thought Partner."""

from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import Any


def save_anomaly_report(
    issue_summary: str,
    report_markdown: str,
) -> dict[str, Any]:
    """Saves the synthesized Phase 1 Core Bug Report to a Markdown file for ticketing handoff.

    Call this tool once all 3 core triage questions have been answered and synthesized,
    or when the user confirms they want to export/copy the Core Bug Report.

    Args:
        issue_summary: Short one-line title or summary of the software anomaly.
        report_markdown: The complete Markdown-formatted Core Bug Report containing
            Issue Summary, Manifestation, Trigger, and Steps to Reproduce.

    Returns:
        A dictionary containing the status, report_id, saved file path, timestamp,
        and formatted report markdown ready to paste into Jira or QAC ticketing systems.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", issue_summary.lower()).strip("-")[:48] or "anomaly"
    report_id = f"P1-{timestamp}-{slug[:20]}"
    filename = f"phase1_core_bug_report_{timestamp}_{slug}.md"

    output_dir_str = os.environ.get("ANOMALY_REPORTS_DIR", "reports/phase1")
    output_dir = Path(output_dir_str)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        file_path.write_text(report_markdown.strip() + "\n", encoding="utf-8")
        saved_path = str(file_path.resolve())
    except OSError:
        # Fallback to /tmp when running inside a read-only Vertex AI Agent Engine container
        fallback_dir = Path("/tmp/dexcom_anomaly_reports/phase1")
        fallback_dir.mkdir(parents=True, exist_ok=True)
        file_path = fallback_dir / filename
        file_path.write_text(report_markdown.strip() + "\n", encoding="utf-8")
        saved_path = str(file_path.resolve())

    return {
        "status": "success",
        "phase": "Phase 1: Core Triage",
        "report_id": report_id,
        "issue_summary": issue_summary,
        "saved_file_path": saved_path,
        "created_at_utc": timestamp,
        "report_markdown": report_markdown,
    }
