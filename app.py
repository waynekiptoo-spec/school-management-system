"""
app.py — Entry point for the School Management System CLI.

Usage:
    python app.py --help
    python app.py add-student --name "Wayne Kiptoo" --age 20 --classroom "Form 4"
    python app.py school-report
"""

import sys

from rich.console import Console

from cli.commands import build_parser
from services.school_manager import SchoolManager

console = Console()


def main():
    """Initialize the school manager and dispatch the requested CLI command."""
    try:
        manager = SchoolManager()
    except RuntimeError as exc:
        console.print(f"[bold red]✘  Failed to start: {exc}[/bold red]")
        sys.exit(1)

    parser = build_parser(manager)

    # Show help when no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
