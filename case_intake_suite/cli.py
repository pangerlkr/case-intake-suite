"""CLI for Case Intake Suite."""

import click
from . import storage
from . import packer


CATEGORIES = [
    "spam",
    "impersonation",
    "harassment",
    "hate-speech",
    "privacy-violation",
    "scam",
    "other",
]


@click.group()
def cli():
    """Case Intake Suite — local moderation case management CLI."""
    pass


@cli.command()
def init():
    """Initialise the local database."""
    storage.init_db()


@cli.command()
def new():
    """Create a new case interactively."""
    storage.init_db()
    click.echo("\n=== New Case Intake ===")
    subject_url = click.prompt("Subject profile URL")
    handle = click.prompt("Handle / username", default="")
    click.echo("Categories: " + ", ".join(CATEGORIES))
    category = click.prompt("Category", type=click.Choice(CATEGORIES), show_choices=False)
    description = click.prompt("Brief description")
    reporter_notes = click.prompt("Reporter notes (facts only)")

    case_id = storage.create_case(
        subject_url=subject_url,
        handle=handle,
        category=category,
        description=description,
        reporter_notes=reporter_notes,
    )

    click.echo(f"\nCase created: {case_id}")

    while click.confirm("Add evidence item?", default=False):
        ev_desc = click.prompt("  Evidence description")
        ev_url = click.prompt("  Evidence URL (leave blank if file)", default="")
        ev_file = click.prompt("  File path (leave blank if URL)", default="")
        storage.add_evidence(
            case_id,
            description=ev_desc,
            file_path=ev_file or None,
            url=ev_url or None,
        )
        click.echo("  Evidence added.")

    click.echo(f"\nDone. Case ID: {case_id}")


@cli.command(name="list")
def list_cases():
    """List all cases."""
    cases = storage.get_all_cases()
    if not cases:
        click.echo("No cases found. Run 'init' first.")
        return
    click.echo(f"\n{'ID':<10} {'Status':<12} {'Category':<18} {'Handle':<20} Created")
    click.echo("-" * 75)
    for c in cases:
        click.echo(
            f"{c['id']:<10} {c['status']:<12} {c['category']:<18} "
            f"{(c['handle'] or '-'):<20} {c['created_at'][:10]}"
        )


@cli.command()
@click.argument("case_id")
@click.argument("reviewer_notes")
@click.option("--status", default="reviewed",
              type=click.Choice(["open", "reviewed", "closed", "escalated"]),
              help="New status for the case.")
def review(case_id, reviewer_notes, status):
    """Add reviewer notes and update status for CASE_ID."""
    case = storage.get_case(case_id)
    if not case:
        click.echo(f"Case {case_id} not found.")
        return
    storage.update_case_status(case_id, status, reviewer_notes)
    click.echo(f"Case {case_id} updated to '{status}'.")


@cli.command()
@click.argument("case_id")
def export(case_id):
    """Export a case pack (Markdown + HTML) to exports/CASE_ID/."""
    case = storage.get_case(case_id)
    if not case:
        click.echo(f"Case {case_id} not found.")
        return
    evidence = storage.get_evidence(case_id)
    paths = packer.export_case(case, evidence)
    click.echo(f"Exported to:")
    for p in paths:
        click.echo(f"  {p}")


@cli.command()
@click.argument("case_id")
def show(case_id):
    """Show full details of a case."""
    case = storage.get_case(case_id)
    if not case:
        click.echo(f"Case {case_id} not found.")
        return
    evidence = storage.get_evidence(case_id)
    click.echo(f"\n=== Case {case_id} ===")
    for k, v in case.items():
        click.echo(f"  {k}: {v}")
    if evidence:
        click.echo(f"\n  Evidence ({len(evidence)} items):")
        for e in evidence:
            click.echo(f"    [{e['id']}] {e['description']} | url={e['url']} | file={e['file_path']}")


if __name__ == "__main__":
    cli()
