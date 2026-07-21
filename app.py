"""Flask dashboard for Case Intake Suite."""

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_file
)
from pathlib import Path
import os

from case_intake_suite import storage, packer

app = Flask(
    __name__,
    template_folder="case_intake_suite/templates",
    static_folder="case_intake_suite/static",
)
app.secret_key = os.urandom(24)

CATEGORIES = [
    "spam", "impersonation", "harassment",
    "hate-speech", "privacy-violation", "scam", "other",
]
STATUSES = ["open", "reviewed", "closed", "escalated"]


@app.before_request
def ensure_db():
    storage.init_db()


@app.route("/")
def index():
    cases = storage.get_all_cases()
    return render_template("index.html", cases=cases, statuses=STATUSES)


@app.route("/case/new", methods=["GET", "POST"])
def new_case():
    if request.method == "POST":
        case_id = storage.create_case(
            subject_url=request.form["subject_url"],
            handle=request.form.get("handle", ""),
            category=request.form["category"],
            description=request.form.get("description", ""),
            reporter_notes=request.form.get("reporter_notes", ""),
        )
        flash(f"Case {case_id} created.", "success")
        return redirect(url_for("case_detail", case_id=case_id))
    return render_template("new_case.html", categories=CATEGORIES)


@app.route("/case/<case_id>")
def case_detail(case_id):
    case = storage.get_case(case_id)
    if not case:
        flash(f"Case {case_id} not found.", "error")
        return redirect(url_for("index"))
    evidence = storage.get_evidence(case_id)
    return render_template(
        "case_detail.html",
        case=case,
        evidence=evidence,
        statuses=STATUSES,
    )


@app.route("/case/<case_id>/update", methods=["POST"])
def update_case(case_id):
    storage.update_case_status(
        case_id,
        status=request.form["status"],
        reviewer_notes=request.form.get("reviewer_notes", ""),
    )
    flash("Case updated.", "success")
    return redirect(url_for("case_detail", case_id=case_id))


@app.route("/case/<case_id>/evidence", methods=["POST"])
def add_evidence(case_id):
    storage.add_evidence(
        case_id,
        description=request.form["description"],
        url=request.form.get("url") or None,
        file_path=request.form.get("file_path") or None,
    )
    flash("Evidence added.", "success")
    return redirect(url_for("case_detail", case_id=case_id))


@app.route("/case/<case_id>/export")
def export_case(case_id):
    case = storage.get_case(case_id)
    if not case:
        flash(f"Case {case_id} not found.", "error")
        return redirect(url_for("index"))
    evidence = storage.get_evidence(case_id)
    paths = packer.export_case(case, evidence)
    flash(f"Exported {len(paths)} files to exports/{case_id}/", "success")
    return redirect(url_for("case_detail", case_id=case_id))


@app.route("/case/<case_id>/export/download/<fmt>")
def download_export(case_id, fmt):
    ext = "md" if fmt == "md" else "html"
    path = Path(f"exports/{case_id}/case-{case_id}.{ext}")
    if not path.exists():
        case = storage.get_case(case_id)
        evidence = storage.get_evidence(case_id)
        packer.export_case(case, evidence)
    return send_file(str(path.resolve()), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
