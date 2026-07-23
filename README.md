# Case Intake Suite

> A local-first Python toolkit for moderation case intake, evidence tracking, and exportable review packs.  
> Includes a **CLI**, a **Flask web dashboard**, and **Markdown/HTML evidence pack export**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/platform-local--only-lightgrey)

---


## What This Is

Case Intake Suite is a structured workflow tool for documenting, triaging, and reviewing incidents before any platform action is taken. It is designed for:

- **Trust and safety teams** managing incident queues locally
- **Security researchers** documenting findings
- **Community managers** logging repeat offenders for manual review
- **Anyone** who needs structured, exportable case dossiers

**This tool does not send reports, automate account actions, or interact with any external platform or API.**  
All enforcement actions must be performed manually through official platform reporting flows.

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/pangerlkr/case-intake-suite.git
cd case-intake-suite
```

### 2. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## CLI Usage

### Step 1: Initialise the database

```bash
python -m case_intake_suite.cli init
```

This creates `cases/cases.db` with the case and evidence tables.

### Step 2: Create your first case

```bash
python -m case_intake_suite.cli new
```

You'll be prompted for:
- **Subject profile URL** (e.g., `https://instagram.com/username`)
- **Handle / username** (optional)
- **Category**: `spam`, `impersonation`, `harassment`, `hate-speech`, `privacy-violation`, `scam`, `other`
- **Description**: Brief factual description
- **Reporter notes**: Dates, times, context
- **Evidence items** (optional): URLs or file paths

The CLI will output a **Case ID** (e.g., `a3f8c21d`).

### Step 3: List all cases

```bash
python -m case_intake_suite.cli list
```

Output:
```
ID         Status       Category            Handle               Created
---------------------------------------------------------------------------
a3f8c21d   open         spam                @badactor            2026-07-21
```

### Step 4: View case details

```bash
python -m case_intake_suite.cli show a3f8c21d
```

### Step 5: Add reviewer notes and update status

```bash
python -m case_intake_suite.cli review a3f8c21d "Confirmed spam pattern. Ready for escalation." --status reviewed
```

Available statuses: `open`, `reviewed`, `closed`, `escalated`

### Step 6: Export the case pack

```bash
python -m case_intake_suite.cli export a3f8c21d
```

Outputs to `exports/a3f8c21d/`:
- `case-a3f8c21d.md` — Markdown dossier
- `case-a3f8c21d.html` — Printable HTML (open in browser → Print → Save as PDF)

---

## Web Dashboard Usage

### Step 1: Start the Flask server

```bash
python app.py
```

Output:
```
 * Running on http://127.0.0.1:5000
```

### Step 2: Open the dashboard in your browser

```
http://127.0.0.1:5000
```

### Step 3: Create a new case

1. Click **"+ New Case"** in the top-right
2. Fill in the form:
   - Subject Profile URL
   - Handle / Username
   - Category
   - Description
   - Reporter Notes
3. Click **"Create Case"**

You'll be redirected to the case detail page.

### Step 4: Add evidence

On the case detail page, scroll to **"Add Evidence"**:

1. **Description** (required): "Screenshot of spam message"
2. **URL** (optional): `https://example.com/screenshot.png`
3. **File Path** (optional): `evidence/screenshot.png`
4. Click **"Add Evidence"**

### Step 5: Update case status and add reviewer notes

In the **"Review"** panel:

1. **Update Status**: Select `reviewed`, `closed`, or `escalated`
2. **Reviewer Notes**: Add your review summary
3. Click **"Update Case"**

### Step 6: Export the case

Click any of the export buttons:
- **📤 Export** — Generate Markdown + HTML in `exports/CASE_ID/`
- **⬇️ .md** — Download Markdown file
- **⬇️ .html** — Download HTML file (open in browser and Print → Save as PDF)

---

## Features

| Feature | Description |
|---|---|
| **CLI intake** | Interactive case creation, listing, review, and export |
| **Flask dashboard** | Local web UI with status filters, evidence management, and export buttons |
| **SQLite storage** | Persistent local case and evidence database |
| **Markdown export** | Clean `.md` dossier per case |
| **HTML export** | Printable HTML pack; use browser Print to save PDF |
| **Evidence tracking** | URL and file-path evidence with timestamps |
| **Status workflow** | Open → Reviewed → Escalated → Closed |
| **Category tagging** | Spam, impersonation, harassment, hate-speech, privacy, scam, other |

---

## Project Structure

```
case-intake-suite/
├── app.py                          # Flask dashboard
├── requirements.txt                # Dependencies
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
        └── styles.css              # Dark-themed dashboard CSS
```

---

## CLI Command Reference

| Command | Description |
|---|---|
| `python -m case_intake_suite.cli init` | Initialise the SQLite database |
| `python -m case_intake_suite.cli new` | Create a new case interactively |
| `python -m case_intake_suite.cli list` | List all cases |
| `python -m case_intake_suite.cli show CASE_ID` | Show case details |
| `python -m case_intake_suite.cli review CASE_ID "notes" --status reviewed` | Add review and update status |
| `python -m case_intake_suite.cli export CASE_ID` | Export Markdown + HTML pack |

---

## Dashboard Routes

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

- ✅ No platform API calls or automated reporting
- ✅ No scraping, mass actions, or account enumeration
- ✅ Evidence is stored locally only
- ✅ Exports are for human review, not automation
- ✅ All enforcement decisions are made by a human reviewer

---

## Requirements

- Python 3.10+
- Flask 3.x
- Click 8.x
- SQLite (built into Python)
- Jinja2 (bundled with Flask)
- ReportLab, Markdown, Pillow

See `requirements.txt` for the full pinned list.

---

## License

MIT License. See `LICENSE`.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

**Built by [pangerlkr](https://github.com/pangerlkr) — Kohima, Nagaland, India.**
