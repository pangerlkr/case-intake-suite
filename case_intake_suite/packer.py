"""Evidence pack exporter for Case Intake Suite.

Exports:
  - Markdown dossier (.md)
  - Printable HTML pack (.html) — open in browser and Print -> Save as PDF
"""

from pathlib import Path
from datetime import datetime

EXPORTS_DIR = Path("exports")


def _md_content(case, evidence):
    lines = [
        f"# Case Dossier: {case['id']}",
        f"",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        f"",
        f"## Subject",
        f"",
        f"| Field | Value |",
        f"|---|---|",
        f"| Case ID | `{case['id']}` |",
        f"| Profile URL | {case['subject_url']} |",
        f"| Handle | {case.get('handle') or '-'} |",
        f"| Category | {case['category']} |",
        f"| Status | {case['status']} |",
        f"| Created | {case['created_at']} |",
        f"| Updated | {case['updated_at']} |",
        f"",
        f"## Description",
        f"",
        f"{case.get('description') or 'No description.'}",
        f"",
        f"## Reporter Notes",
        f"",
        f"{case.get('reporter_notes') or 'None.'}",
        f"",
        f"## Reviewer Notes",
        f"",
        f"{case.get('reviewer_notes') or 'Pending review.'}",
        f"",
        f"## Evidence ({len(evidence)} items)",
        f"",
    ]
    if evidence:
        for i, e in enumerate(evidence, 1):
            lines.append(f"### {i}. {e['description']}")
            lines.append(f"")
            if e.get('url'):
                lines.append(f"- **URL:** {e['url']}")
            if e.get('file_path'):
                lines.append(f"- **File:** `{e['file_path']}`")
            lines.append(f"- **Added:** {e['added_at']}")
            lines.append(f"")
    else:
        lines.append("_No evidence items attached._")
        lines.append("")

    lines += [
        f"---",
        f"",
        f"*This document is for human review only. Do not submit automated reports.*",
        f"*All platform reports should be filed through the platform's official reporting flow.*",
    ]
    return "\n".join(lines)


def _html_content(case, evidence, md_text):
    rows = "".join(
        f"<tr><td><strong>{k.replace('_', ' ').title()}</strong></td><td>{v}</td></tr>\n"
        for k, v in case.items()
    )
    ev_html = ""
    if evidence:
        for i, e in enumerate(evidence, 1):
            ev_html += f"<div class='evidence-item'><h3>{i}. {e['description']}</h3>\n"
            if e.get('url'):
                ev_html += f"<p><strong>URL:</strong> <a href='{e['url']}'>{e['url']}</a></p>\n"
            if e.get('file_path'):
                ev_html += f"<p><strong>File:</strong> <code>{e['file_path']}</code></p>\n"
            ev_html += f"<p><strong>Added:</strong> {e['added_at']}</p></div>\n"
    else:
        ev_html = "<p><em>No evidence items attached.</em></p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Case Dossier: {case['id']}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         max-width: 860px; margin: 40px auto; padding: 0 20px; color: #222; }}
  h1 {{ border-bottom: 2px solid #d00; padding-bottom: 8px; }}
  h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 36px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  td {{ padding: 8px 12px; border: 1px solid #ddd; }}
  tr:nth-child(even) {{ background: #f9f9f9; }}
  .evidence-item {{ background: #f5f5f5; border-left: 4px solid #d00;
                    padding: 12px 16px; margin: 16px 0; border-radius: 4px; }}
  .footer {{ font-size: 0.85em; color: #888; margin-top: 48px; border-top: 1px solid #eee; padding-top: 12px; }}
  @media print {{ body {{ margin: 20px; }} }}
</style>
</head>
<body>
<h1>Case Dossier: {case['id']}</h1>
<p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
<h2>Subject Details</h2>
<table>{rows}</table>
<h2>Description</h2>
<p>{case.get('description') or 'No description.'}</p>
<h2>Reporter Notes</h2>
<p>{case.get('reporter_notes') or 'None.'}</p>
<h2>Reviewer Notes</h2>
<p>{case.get('reviewer_notes') or 'Pending review.'}</p>
<h2>Evidence ({len(evidence)} items)</h2>
{ev_html}
<div class="footer">
  <p>This document is for human review only. Do not submit automated reports.<br>
  All platform reports should be filed through the platform's official reporting flow.</p>
</div>
</body>
</html>
"""


def export_case(case, evidence):
    """Export Markdown and HTML packs. Returns list of output paths."""
    out_dir = EXPORTS_DIR / case['id']
    out_dir.mkdir(parents=True, exist_ok=True)

    md_text = _md_content(case, evidence)
    html_text = _html_content(case, evidence, md_text)

    md_path = out_dir / f"case-{case['id']}.md"
    html_path = out_dir / f"case-{case['id']}.html"

    md_path.write_text(md_text, encoding="utf-8")
    html_path.write_text(html_text, encoding="utf-8")

    return [str(md_path), str(html_path)]
