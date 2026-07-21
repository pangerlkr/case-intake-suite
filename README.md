# Case Intake Suite

> A local-first Python toolkit for moderation case intake, evidence tracking, and exportable review packs.
> Includes a CLI, a Flask web dashboard, and Markdown/HTML evidence pack export.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/platform-local--only-lightgrey)

---

## What This Is

Case Intake Suite is a structured workflow tool for documenting, triaging, and reviewing incidents before any platform action is taken. It is designed for:

- Trust and safety teams managing incident queues locally
- Security researchers documenting findings
- Community managers logging repeat offenders for manual review
- Anyone who needs structured, exportable case dossiers

**This tool does not send reports, automate account actions, or interact with any external platform or API.**
All enforcement actions must be performed manually through official platform reporting flows.

---

## Features

| Feature | Description |
|---|---|
| CLI intake | Interactive case creation, listing, review, and export |
| Flask dashboard | Local web UI with status filters, evidence management, and export buttons |
| SQLite storage | Persistent local case and evidence database |
| Markdown export | Clean `.md` dossier per case |
| HTML export | Printable HTML pack; use browser Print to save PDF |
| Evidence tracking | URL and file-path evidence with timestamps |
| Status workflow | Open > Reviewed > Escalated > Closed |
| Category tagging | Spam, impersonation, harassment, hate-speech, privacy, scam, other |

---

## Project Structure

```
case-intake-suite/
├── app.py                          # Flask dashboard
├── requirements.txt
├── LICENSE
├── README.md
├── SECURITY.md
├── cases/                          # SQLite DB (auto-created)
│   └── cases.db
├── exports/                        # Case pack outputs (auto-created)
│   └── CASE_ID/
│       ├── case-CASE_ID.md
│       └── case-CASE_ID.html
└── case_intake_suite/
    ├── __init__.py
    ├── cli.py                      # Click CLI
    ├── storage.py                  # SQLite CRUD layer
    ├── packer.py                   # Markdown + HTML exporter
    ├── templates/
    │   ├── layout.html
    │   ├── index.html
    │   ├── new_case.html
    │   └── case_detail.html
    └── static/
        └── styles.css
```

---

## Installation

```bash
git clone https://github.com/pangerlkr/case-intake-suite.git
cd case-intake-suite
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## CLI Usage

### Initialise the database

```bash
python -m case_intake_suite.cli init
```

### Create a new case interactively

```bash
python -m case_intake_suite.cli new
```

You will be prompted for:
- Subject profile URL
- Handle / username
- Category (spam, impersonation, harassment, hate-speech, privacy-violation, scam, other)
- Description
- Reporter notes
- Evidence items (URL or file path)

### List all cases

```bash
python -m case_intake_suite.cli list
```

### Show a specific case

```bash
python -m case_intake_suite.cli show CASE_ID
```

### Add reviewer notes and update status

```bash
python -m case_intake_suite.cli review CASE_ID "Reviewed: confirmed spam pattern" --status reviewed
```

Available statuses: `open`, `reviewed`, `closed`, `escalated`

### Export a case pack

```bash
python -m case_intake_suite.cli export CASE_ID
```

Outputs to `exports/CASE_ID/`:
- `case-CASE_ID.md` — Markdown dossier
- `case-CASE_ID.html` — Printable HTML (open in browser, Print > Save as PDF)

---

## Flask Dashboard

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### Dashboard pages

| Route | Description |
|---|---|
| `/` | All cases with status filter |
| `/case/new` | New case intake form |
| `/case/<id>` | Case detail, review panel, evidence manager |
| `/case/<id>/export` | Generate Markdown and HTML pack |
| `/case/<id>/export/download/md` | Download Markdown file |
| `/case/<id>/export/download/html` | Download HTML file |

---

## Scenario Walkthrough

1. **Incident observed** — a user reports a suspicious account.
2. **Open CLI or dashboard** — create a new case with the profile URL, category, and description.
3. **Attach evidence** — add screenshot file paths and direct URL links.
4. **Reviewer triages** — update status to `reviewed`, add reviewer notes.
5. **Export** — generate a clean Markdown dossier and printable HTML pack.
6. **Manual report** — a human reviews the pack and files a report through the platform's official in-app reporting flow.

---

## Safety Model

- No platform API calls or automated reporting.
- No scraping, mass actions, or account enumeration.
- Evidence is stored locally only.
- Exports are for human review, not automation.
- All enforcement decisions are made by a human reviewer.

---

## Requirements

- Python 3.10+
- Flask 3.x
- Click 8.x
- SQLite (built into Python)
- Jinja2 (bundled with Flask)

See `requirements.txt` for the full pinned list.

---

## License

MIT License. See `LICENSE`.

---

*Built by [pangerlkr](https://github.com/pangerlkr) — Kohima, Nagaland, India.*
