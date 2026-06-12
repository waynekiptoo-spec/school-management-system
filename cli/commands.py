"""
commands.py — CLI command definitions for the School Management System.

Registers all argparse sub-commands and their handlers.
Uses the rich library for all terminal output (tables, colours, panels).
"""

import sys
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

from services.school_manager import SchoolManager
from utils.validators import (
    validate_age,
    validate_capacity,
    validate_date,
    validate_name,
    validate_score,
    validate_status,
)

console = Console()

# ── Colour palette ───────────────────────────────────────────────────────────
SUCCESS = "bold green"
ERROR   = "bold red"
INFO    = "bold cyan"
WARN    = "bold yellow"
HEADER  = "bold blue"


def _ok(msg: str):
    """Print a success message."""
    console.print(f"[{SUCCESS}]✔  {msg}[/{SUCCESS}]")


def _err(msg: str):
    """Print an error message and exit with code 1."""
    console.print(f"[{ERROR}]✘  {msg}[/{ERROR}]")
    sys.exit(1)


def _info(msg: str):
    """Print an informational message."""
    console.print(f"[{INFO}]ℹ  {msg}[/{INFO}]")


# ══════════════════════════════════════════════════════════════════════════════
# STUDENT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_add_student(args, manager: SchoolManager):
    """Handle: python app.py add-student ..."""
    try:
        name = validate_name(args.name)
        age = validate_age(args.age)
    except ValueError as exc:
        _err(str(exc))

    student = manager.add_student(
        name=name,
        age=age,
        classroom=args.classroom or "",
        email=args.email or "",
        phone=args.phone or "",
    )
    _ok(f"Student '{student.name}' registered successfully with ID {student.id}.")


def cmd_list_students(args, manager: SchoolManager):
    """Handle: python app.py list-students"""
    students = manager.list_students()
    if not students:
        _info("No students registered yet.")
        return

    table = Table(
        title="[bold]Registered Students[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("ID",        style="dim",         width=5)
    table.add_column("Name",      style="bold white",  min_width=20)
    table.add_column("Age",       justify="center",    width=5)
    table.add_column("Classroom", style="cyan",        min_width=12)
    table.add_column("Email",     style="dim",         min_width=20)
    table.add_column("Avg Score", justify="center",    width=10)

    for s in students:
        avg = s.get_average_score()
        avg_str = f"{avg:.1f}" if avg > 0 else "—"
        table.add_row(
            str(s.id),
            s.name,
            str(s.age),
            s.classroom or "—",
            s.email or "—",
            avg_str,
        )

    console.print(table)
    _info(f"Total: {len(students)} student(s).")


def cmd_search_student(args, manager: SchoolManager):
    """Handle: python app.py search-student --name ..."""
    results = manager.search_students(args.name)
    if not results:
        _info(f"No students found matching '{args.name}'.")
        return

    table = Table(
        title=f"[bold]Search Results for '{args.name}'[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("ID",        style="dim",         width=5)
    table.add_column("Name",      style="bold white",  min_width=20)
    table.add_column("Age",       justify="center",    width=5)
    table.add_column("Classroom", style="cyan",        min_width=12)

    for s in results:
        table.add_row(str(s.id), s.name, str(s.age), s.classroom or "—")

    console.print(table)
    _info(f"Found {len(results)} result(s).")


def cmd_update_student(args, manager: SchoolManager):
    """Handle: python app.py update-student --id ..."""
    updates = {}
    try:
        if args.name:
            updates["name"] = validate_name(args.name)
        if args.age:
            updates["age"] = validate_age(args.age)
        if args.classroom is not None:
            updates["classroom"] = args.classroom
        if args.email is not None:
            updates["email"] = args.email
        if args.phone is not None:
            updates["phone"] = args.phone
    except ValueError as exc:
        _err(str(exc))

    if not updates:
        _err("No update fields provided. Use --name, --age, --classroom, --email, or --phone.")

    try:
        student = manager.update_student(args.id, **updates)
        _ok(f"Student ID {student.id} ({student.name}) updated successfully.")
    except ValueError as exc:
        _err(str(exc))


def cmd_delete_student(args, manager: SchoolManager):
    """Handle: python app.py delete-student --id ..."""
    deleted = manager.delete_student(args.id)
    if deleted:
        _ok(f"Student ID {args.id} deleted successfully.")
    else:
        _err(f"No student found with ID {args.id}.")


# ══════════════════════════════════════════════════════════════════════════════
# TEACHER COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_add_teacher(args, manager: SchoolManager):
    """Handle: python app.py add-teacher ..."""
    try:
        name = validate_name(args.name)
        age = validate_age(args.age)
    except ValueError as exc:
        _err(str(exc))

    teacher = manager.add_teacher(
        name=name,
        age=age,
        subject=args.subject or "",
        email=args.email or "",
        phone=args.phone or "",
    )
    _ok(f"Teacher '{teacher.name}' registered successfully with ID {teacher.id}.")


def cmd_list_teachers(args, manager: SchoolManager):
    """Handle: python app.py list-teachers"""
    teachers = manager.list_teachers()
    if not teachers:
        _info("No teachers registered yet.")
        return

    table = Table(
        title="[bold]Teaching Staff[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("ID",      style="dim",        width=5)
    table.add_column("Name",    style="bold white", min_width=20)
    table.add_column("Age",     justify="center",   width=5)
    table.add_column("Subject", style="cyan",       min_width=15)
    table.add_column("Email",   style="dim",        min_width=20)

    for t in teachers:
        table.add_row(
            str(t.id), t.name, str(t.age), t.subject or "—", t.email or "—"
        )

    console.print(table)
    _info(f"Total: {len(teachers)} teacher(s).")


# ══════════════════════════════════════════════════════════════════════════════
# PARENT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_add_parent(args, manager: SchoolManager):
    """Handle: python app.py add-parent ..."""
    try:
        name = validate_name(args.name)
        age = validate_age(args.age)
    except ValueError as exc:
        _err(str(exc))

    parent = manager.add_parent(
        name=name,
        age=age,
        relationship=args.relationship or "Guardian",
        email=args.email or "",
        phone=args.phone or "",
    )
    _ok(f"Parent/Guardian '{parent.name}' registered with ID {parent.id}.")


def cmd_list_parents(args, manager: SchoolManager):
    """Handle: python app.py list-parents"""
    parents = manager.list_parents()
    if not parents:
        _info("No parents/guardians registered yet.")
        return

    table = Table(
        title="[bold]Parents & Guardians[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("ID",           style="dim",        width=5)
    table.add_column("Name",         style="bold white", min_width=20)
    table.add_column("Relationship", style="cyan",       min_width=12)
    table.add_column("Phone",        style="dim",        min_width=15)
    table.add_column("Linked Students", justify="center", width=16)

    for p in parents:
        table.add_row(
            str(p.id),
            p.name,
            p.relationship,
            p.phone or "—",
            str(len(p.student_ids)),
        )

    console.print(table)
    _info(f"Total: {len(parents)} parent(s)/guardian(s).")


# ══════════════════════════════════════════════════════════════════════════════
# CLASSROOM COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_add_classroom(args, manager: SchoolManager):
    """Handle: python app.py add-classroom ..."""
    try:
        capacity = validate_capacity(args.capacity) if args.capacity else 40
    except ValueError as exc:
        _err(str(exc))

    if not args.name or not args.name.strip():
        _err("Classroom name cannot be empty.")

    classroom = manager.add_classroom(
        name=args.name.strip(),
        capacity=capacity,
        teacher_id=args.teacher_id,
    )
    _ok(f"Classroom '{classroom.name}' created with ID {classroom.id} (capacity: {classroom.capacity}).")


def cmd_list_classrooms(args, manager: SchoolManager):
    """Handle: python app.py list-classrooms"""
    classrooms = manager.list_classrooms()
    if not classrooms:
        _info("No classrooms created yet.")
        return

    table = Table(
        title="[bold]Classrooms[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("ID",       style="dim",        width=5)
    table.add_column("Name",     style="bold white", min_width=15)
    table.add_column("Capacity", justify="center",   width=10)
    table.add_column("Enrolled", justify="center",   width=10)
    table.add_column("Status",   justify="center",   width=10)

    for c in classrooms:
        status = "[red]Full[/red]" if c.is_full else "[green]Open[/green]"
        table.add_row(
            str(c.id),
            c.name,
            str(c.capacity),
            str(c.current_enrollment),
            status,
        )

    console.print(table)
    _info(f"Total: {len(classrooms)} classroom(s).")


# ══════════════════════════════════════════════════════════════════════════════
# ASSIGNMENT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_assign_student(args, manager: SchoolManager):
    """Handle: python app.py assign-student --student ... --classroom ..."""
    try:
        success = manager.assign_student_to_classroom(args.student, args.classroom)
        if success:
            student = manager.get_student(args.student)
            classroom = manager.get_classroom(args.classroom)
            _ok(
                f"Student '{student.name}' assigned to classroom '{classroom.name}' successfully."
            )
        else:
            _err(f"Classroom ID {args.classroom} is full or student already enrolled.")
    except ValueError as exc:
        _err(str(exc))


# ══════════════════════════════════════════════════════════════════════════════
# GRADE COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_record_grade(args, manager: SchoolManager):
    """Handle: python app.py record-grade --student ... --subject ... --score ..."""
    try:
        score = validate_score(args.score)
    except ValueError as exc:
        _err(str(exc))

    if not args.subject or not args.subject.strip():
        _err("Subject name cannot be empty.")

    try:
        grade = manager.record_grade(
            student_id=args.student,
            subject=args.subject.strip(),
            score=score,
            teacher_id=args.teacher,
        )
        student = manager.get_student(args.student)
        _ok(
            f"Grade recorded — {student.name} | {grade.subject}: "
            f"{grade.score} ({grade.letter})"
        )
    except ValueError as exc:
        _err(str(exc))


def cmd_view_grades(args, manager: SchoolManager):
    """Handle: python app.py view-grades --student ..."""
    student = manager.get_student(args.student)
    if not student:
        _err(f"No student found with ID {args.student}.")

    grades = student.grades
    if not grades:
        _info(f"{student.name} has no grades recorded yet.")
        return

    table = Table(
        title=f"[bold]Grades — {student.name} (ID: {student.id})[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("Subject",    style="bold white", min_width=18)
    table.add_column("Score",      justify="center",   width=8)
    table.add_column("Grade",      justify="center",   width=8)
    table.add_column("Date",       justify="center",   min_width=12)

    for g in grades:
        letter = g.get("letter", "")
        colour = (
            "green" if letter in ("A+", "A")
            else "yellow" if letter in ("B+", "B")
            else "red" if letter in ("D", "F")
            else "white"
        )
        table.add_row(
            g["subject"],
            str(g["score"]),
            f"[{colour}]{letter}[/{colour}]",
            g.get("date", "—"),
        )

    console.print(table)
    avg = student.get_average_score()
    console.print(
        f"\n  [bold]Average Score:[/bold] {avg:.1f}  |  "
        f"[bold]Total Entries:[/bold] {len(grades)}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# ATTENDANCE COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_mark_attendance(args, manager: SchoolManager):
    """Handle: python app.py mark-attendance --student ... --status ..."""
    try:
        status = validate_status(args.status)
    except ValueError as exc:
        _err(str(exc))

    date_str = None
    if args.date:
        try:
            date_str = validate_date(args.date)
        except ValueError as exc:
            _err(str(exc))

    try:
        record = manager.mark_attendance(
            student_id=args.student,
            status=status,
            date=date_str,
            notes=args.notes or "",
        )
        student = manager.get_student(args.student)
        _ok(
            f"Attendance marked — {student.name}: "
            f"[bold]{record.status}[/bold] on {record.date}"
        )
    except ValueError as exc:
        _err(str(exc))


def cmd_view_attendance(args, manager: SchoolManager):
    """Handle: python app.py view-attendance --student ..."""
    student = manager.get_student(args.student)
    if not student:
        _err(f"No student found with ID {args.student}.")

    records = student.attendance
    if not records:
        _info(f"{student.name} has no attendance records yet.")
        return

    table = Table(
        title=f"[bold]Attendance — {student.name} (ID: {student.id})[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style=HEADER,
    )
    table.add_column("Date",   justify="center", min_width=12)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Notes",  style="dim",      min_width=20)

    for r in records:
        status = r["status"]
        colour = (
            "green" if status == "Present"
            else "red" if status == "Absent"
            else "yellow"
        )
        table.add_row(
            r.get("date", "—"),
            f"[{colour}]{status}[/{colour}]",
            r.get("notes", "") or "—",
        )

    console.print(table)
    summary = student.get_attendance_summary()
    console.print(
        f"\n  [green]Present:[/green] {summary['Present']}  "
        f"[red]Absent:[/red] {summary['Absent']}  "
        f"[yellow]Late:[/yellow] {summary['Late']}  "
        f"[dim]Total: {summary['total']}[/dim]"
    )


# ══════════════════════════════════════════════════════════════════════════════
# REPORT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def cmd_student_report(args, manager: SchoolManager):
    """Handle: python app.py student-report --student ..."""
    report = manager.get_student_report(args.student)
    if not report:
        _err(f"No student found with ID {args.student}.")

    s = report["student"]
    parent = report["parent"]
    grades = report["grades"]
    avg = report["average_score"]
    att = report["attendance_summary"]

    console.print(
        Panel.fit(
            f"[bold white]{s['name']}[/bold white]  |  "
            f"ID: {s['id']}  |  Age: {s['age']}  |  Classroom: {s.get('classroom', '—')}",
            title="[bold blue]Student Report[/bold blue]",
            border_style="blue",
        )
    )

    # Parent info
    if parent:
        console.print(
            f"  [bold]Parent/Guardian:[/bold] {parent['name']} "
            f"({parent.get('relationship', 'Guardian')})  |  "
            f"📞 {parent.get('phone', '—')}"
        )
    else:
        console.print("  [dim]No parent/guardian linked.[/dim]")

    console.print()

    # Grades table
    if grades:
        grade_table = Table(title="Academic Record", box=box.SIMPLE, header_style=HEADER)
        grade_table.add_column("Subject",   style="white",   min_width=18)
        grade_table.add_column("Score",     justify="center", width=8)
        grade_table.add_column("Grade",     justify="center", width=8)
        grade_table.add_column("Date",      justify="center", min_width=12)

        for g in grades:
            letter = g.get("letter", "")
            colour = (
                "green" if letter in ("A+", "A")
                else "yellow" if letter in ("B+", "B")
                else "red" if letter in ("D", "F")
                else "white"
            )
            grade_table.add_row(
                g["subject"],
                str(g["score"]),
                f"[{colour}]{letter}[/{colour}]",
                g.get("date", "—"),
            )

        console.print(grade_table)
        console.print(f"  [bold]Average Score:[/bold] {avg:.1f}\n")
    else:
        console.print("  [dim]No grades recorded.[/dim]\n")

    # Attendance summary
    console.print(
        Panel(
            f"  [green]Present:[/green] {att['Present']}   "
            f"[red]Absent:[/red] {att['Absent']}   "
            f"[yellow]Late:[/yellow] {att['Late']}   "
            f"[dim]Total sessions: {att['total']}[/dim]",
            title="Attendance Summary",
            border_style="green" if att["Absent"] == 0 else "yellow",
            expand=False,
        )
    )


def cmd_school_report(args, manager: SchoolManager):
    """Handle: python app.py school-report"""
    report = manager.get_school_report()

    now = datetime.now().strftime("%d %B %Y, %H:%M")

    console.print(
        Panel.fit(
            f"[bold white]School Management System[/bold white]\n"
            f"[dim]Report generated: {now}[/dim]",
            title="[bold blue]School Summary Report[/bold blue]",
            border_style="blue",
        )
    )

    # Stats table
    stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    stats_table.add_column("Metric", style="bold white", min_width=28)
    stats_table.add_column("Value",  justify="right", style="cyan")

    stats_table.add_row("Total Students",          str(report["total_students"]))
    stats_table.add_row("Total Teachers",           str(report["total_teachers"]))
    stats_table.add_row("Total Parents/Guardians",  str(report["total_parents"]))
    stats_table.add_row("Total Classrooms",         str(report["total_classrooms"]))
    stats_table.add_row("School Average Score",     f"{report['school_average_score']:.1f}")
    stats_table.add_row("Total Present Records",    str(report["total_present_records"]))
    stats_table.add_row("Total Absent Records",     str(report["total_absent_records"]))

    console.print(stats_table)


# ══════════════════════════════════════════════════════════════════════════════
# ARGPARSE SETUP
# ══════════════════════════════════════════════════════════════════════════════

def build_parser(manager: SchoolManager):
    """
    Build and return the top-level argument parser with all sub-commands.

    Args:
        manager: Shared SchoolManager instance passed to each command handler.

    Returns:
        Configured argparse.ArgumentParser.
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="python app.py",
        description=(
            "📚 School Management System — "
            "Manage students, teachers, grades, and attendance from the CLI."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python app.py add-student --name 'Wayne Kiptoo' --age 20 --classroom 'Form 4'\n"
            "  python app.py record-grade --student 1 --subject Mathematics --score 87\n"
            "  python app.py mark-attendance --student 1 --status Present\n"
            "  python app.py student-report --student 1\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # ── add-student ──────────────────────────────────────────────────────────
    p = subparsers.add_parser("add-student", help="Register a new student.")
    p.add_argument("--name",      required=True,  help="Full name of the student.")
    p.add_argument("--age",       required=True,  type=int, help="Age of the student.")
    p.add_argument("--classroom", default="",     help="Classroom name (e.g. 'Form 4').")
    p.add_argument("--email",     default="",     help="Email address.")
    p.add_argument("--phone",     default="",     help="Phone number.")
    p.set_defaults(func=lambda a: cmd_add_student(a, manager))

    # ── list-students ────────────────────────────────────────────────────────
    p = subparsers.add_parser("list-students", help="List all registered students.")
    p.set_defaults(func=lambda a: cmd_list_students(a, manager))

    # ── search-student ───────────────────────────────────────────────────────
    p = subparsers.add_parser("search-student", help="Search students by name.")
    p.add_argument("--name", required=True, help="Name (or partial name) to search for.")
    p.set_defaults(func=lambda a: cmd_search_student(a, manager))

    # ── update-student ───────────────────────────────────────────────────────
    p = subparsers.add_parser("update-student", help="Update an existing student's details.")
    p.add_argument("--id",        required=True, type=int, help="Student ID to update.")
    p.add_argument("--name",      default=None,  help="New name.")
    p.add_argument("--age",       default=None,  type=int, help="New age.")
    p.add_argument("--classroom", default=None,  help="New classroom.")
    p.add_argument("--email",     default=None,  help="New email.")
    p.add_argument("--phone",     default=None,  help="New phone number.")
    p.set_defaults(func=lambda a: cmd_update_student(a, manager))

    # ── delete-student ───────────────────────────────────────────────────────
    p = subparsers.add_parser("delete-student", help="Delete a student by ID.")
    p.add_argument("--id", required=True, type=int, help="Student ID to delete.")
    p.set_defaults(func=lambda a: cmd_delete_student(a, manager))

    # ── add-teacher ──────────────────────────────────────────────────────────
    p = subparsers.add_parser("add-teacher", help="Register a new teacher.")
    p.add_argument("--name",    required=True, help="Full name.")
    p.add_argument("--age",     required=True, type=int, help="Age.")
    p.add_argument("--subject", default="",   help="Primary subject (e.g. Mathematics).")
    p.add_argument("--email",   default="",   help="Email address.")
    p.add_argument("--phone",   default="",   help="Phone number.")
    p.set_defaults(func=lambda a: cmd_add_teacher(a, manager))

    # ── list-teachers ────────────────────────────────────────────────────────
    p = subparsers.add_parser("list-teachers", help="List all teachers.")
    p.set_defaults(func=lambda a: cmd_list_teachers(a, manager))

    # ── add-parent ───────────────────────────────────────────────────────────
    p = subparsers.add_parser("add-parent", help="Register a parent or guardian.")
    p.add_argument("--name",         required=True, help="Full name.")
    p.add_argument("--age",          required=True, type=int, help="Age.")
    p.add_argument("--relationship", default="Guardian",
                   help="Relationship type (Mother, Father, Guardian).")
    p.add_argument("--email",        default="", help="Email address.")
    p.add_argument("--phone",        default="", help="Phone number.")
    p.set_defaults(func=lambda a: cmd_add_parent(a, manager))

    # ── list-parents ─────────────────────────────────────────────────────────
    p = subparsers.add_parser("list-parents", help="List all parents/guardians.")
    p.set_defaults(func=lambda a: cmd_list_parents(a, manager))

    # ── add-classroom ────────────────────────────────────────────────────────
    p = subparsers.add_parser("add-classroom", help="Create a new classroom.")
    p.add_argument("--name",       required=True, help="Classroom name (e.g. 'Form 4').")
    p.add_argument("--capacity",   default=40,    type=int, help="Max students (default 40).")
    p.add_argument("--teacher-id", default=None,  type=int, dest="teacher_id",
                   help="Assign an existing teacher by ID.")
    p.set_defaults(func=lambda a: cmd_add_classroom(a, manager))

    # ── list-classrooms ──────────────────────────────────────────────────────
    p = subparsers.add_parser("list-classrooms", help="List all classrooms.")
    p.set_defaults(func=lambda a: cmd_list_classrooms(a, manager))

    # ── assign-student ───────────────────────────────────────────────────────
    p = subparsers.add_parser("assign-student", help="Assign a student to a classroom.")
    p.add_argument("--student",   required=True, type=int, help="Student ID.")
    p.add_argument("--classroom", required=True, type=int, help="Classroom ID.")
    p.set_defaults(func=lambda a: cmd_assign_student(a, manager))

    # ── record-grade ─────────────────────────────────────────────────────────
    p = subparsers.add_parser("record-grade", help="Record a grade for a student.")
    p.add_argument("--student",  required=True, type=int,  help="Student ID.")
    p.add_argument("--subject",  required=True,            help="Subject name.")
    p.add_argument("--score",    required=True, type=float, help="Numeric score (0–100).")
    p.add_argument("--teacher",  default=None,  type=int,  help="Teacher ID (optional).")
    p.set_defaults(func=lambda a: cmd_record_grade(a, manager))

    # ── view-grades ──────────────────────────────────────────────────────────
    p = subparsers.add_parser("view-grades", help="View all grades for a student.")
    p.add_argument("--student", required=True, type=int, help="Student ID.")
    p.set_defaults(func=lambda a: cmd_view_grades(a, manager))

    # ── mark-attendance ──────────────────────────────────────────────────────
    p = subparsers.add_parser("mark-attendance", help="Mark attendance for a student.")
    p.add_argument("--student", required=True, type=int,  help="Student ID.")
    p.add_argument("--status",  required=True,            help="Present | Absent | Late.")
    p.add_argument("--date",    default=None,             help="Date (default: today).")
    p.add_argument("--notes",   default="",              help="Optional notes.")
    p.set_defaults(func=lambda a: cmd_mark_attendance(a, manager))

    # ── view-attendance ──────────────────────────────────────────────────────
    p = subparsers.add_parser("view-attendance", help="View attendance records for a student.")
    p.add_argument("--student", required=True, type=int, help="Student ID.")
    p.set_defaults(func=lambda a: cmd_view_attendance(a, manager))

    # ── student-report ───────────────────────────────────────────────────────
    p = subparsers.add_parser("student-report", help="Generate a full report for a student.")
    p.add_argument("--student", required=True, type=int, help="Student ID.")
    p.set_defaults(func=lambda a: cmd_student_report(a, manager))

    # ── school-report ────────────────────────────────────────────────────────
    p = subparsers.add_parser("school-report", help="Generate a school-wide summary report.")
    p.set_defaults(func=lambda a: cmd_school_report(a, manager))

    return parser
