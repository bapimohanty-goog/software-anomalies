"""Helper tools for Phase 2: Contextual SW Depth Anomaly Thought Partner."""

from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import Any


def save_anomaly_report(
    issue_summary: str,
    report_markdown: str,
) -> dict[str, Any]:
    """Saves the synthesized Phase 2 Detailed Technical Anomaly Report to a Markdown file.

    Call this tool once all 5 contextual assessment questions have been answered and
    synthesized into the Detailed Technical Anomaly Report, or when the user updates
    details and wants to re-export the report.

    Args:
        issue_summary: Short one-line title or summary of the software anomaly.
        report_markdown: The complete Markdown-formatted Detailed Technical Anomaly Report
            with clear headings for all 5 contextual assessment areas.

    Returns:
        A dictionary containing the status, report_id, saved file path, timestamp,
        and formatted report markdown ready for engineering and QA handoff.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", issue_summary.lower()).strip("-")[:48] or "anomaly"
    report_id = f"P2-{timestamp}-{slug[:20]}"
    filename = f"phase2_technical_anomaly_report_{timestamp}_{slug}.md"

    output_dir_str = os.environ.get("ANOMALY_REPORTS_DIR", "reports/phase2")
    output_dir = Path(output_dir_str)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        file_path.write_text(report_markdown.strip() + "\n", encoding="utf-8")
        saved_path = str(file_path.resolve())
    except OSError:
        fallback_dir = Path("/tmp/dexcom_anomaly_reports/phase2")
        fallback_dir.mkdir(parents=True, exist_ok=True)
        file_path = fallback_dir / filename
        file_path.write_text(report_markdown.strip() + "\n", encoding="utf-8")
        saved_path = str(file_path.resolve())

    return {
        "status": "success",
        "phase": "Phase 2: Contextual SW Depth",
        "report_id": report_id,
        "issue_summary": issue_summary,
        "saved_file_path": saved_path,
        "created_at_utc": timestamp,
        "report_markdown": report_markdown,
    }
