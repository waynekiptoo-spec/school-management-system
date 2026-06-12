# 📚 School Management System

A production-ready **Command-Line Interface (CLI) School Management System** built with Python 3.10+, following Object-Oriented Programming principles and industry-standard project structure.

---

## Overview

The School Management System allows school administrators, teachers, and parents to manage and view school information from the terminal. Data is persisted automatically to a local JSON database so nothing is lost between sessions.

---

## Features

- **Student Management** — Register, search, update, and delete student records
- **Teacher Management** — Maintain a register of teaching staff with subject specializations
- **Parent/Guardian Management** — Track parents and link them to their children
- **Classroom Management** — Create classrooms with capacity limits and assign students
- **Grade Recording** — Record subject scores; automatic letter grade (A+ through F) computation
- **Attendance Tracking** — Mark Present / Absent / Late with optional date and notes
- **Student Report** — Full per-student report: details, grades, attendance summary
- **School Report** — School-wide summary with student/teacher counts and averages
- **Rich Terminal UI** — Colour-coded tables, panels, and success/error messages via `rich`
- **JSON Persistence** — Atomic writes; graceful handling of missing or corrupt files
- **58 Unit Tests** — Full pytest suite covering all major features

---

## Installation

**Requirements:** Python 3.10 or higher

```bash
# 1. Clone or download the project
git clone https://github.com/your-username/school-management-system.git
cd school-management-system

# 2. (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
# Show all available commands
python app.py --help

# Show help for a specific command
python app.py add-student --help
```

### Quick Start Workflow

```bash
# 1. Add a classroom
python app.py add-classroom --name "Form 4" --capacity 35

# 2. Add a teacher
python app.py add-teacher --name "Mr. Ochieng" --age 35 --subject "Mathematics"

# 3. Register a student
python app.py add-student --name "Wayne Kiptoo" --age 20 --classroom "Form 4"

# 4. Register a parent and link to the student
python app.py add-parent --name "Grace Kiptoo" --age 45 --relationship Mother --phone "+254700123456"

# 5. Record a grade
python app.py record-grade --student 1 --subject Mathematics --score 87

# 6. Mark attendance
python app.py mark-attendance --student 1 --status Present

# 7. View the student's full report
python app.py student-report --student 1
```

---

## CLI Commands

### Students

| Command | Description |
|---|---|
| `add-student` | Register a new student |
| `list-students` | List all registered students |
| `search-student --name <query>` | Search students by name |
| `update-student --id <id> [fields...]` | Update a student's details |
| `delete-student --id <id>` | Delete a student |

```bash
python app.py add-student --name "Alice Njeri" --age 17 --classroom "Form 3" --email "alice@example.com"
python app.py search-student --name "Alice"
python app.py update-student --id 1 --classroom "Form 4"
python app.py delete-student --id 1
```

### Teachers

| Command | Description |
|---|---|
| `add-teacher` | Register a new teacher |
| `list-teachers` | List all teachers |

```bash
python app.py add-teacher --name "Ms. Amara" --age 28 --subject "Biology" --phone "+254711000000"
```

### Parents & Guardians

| Command | Description |
|---|---|
| `add-parent` | Register a parent/guardian |
| `list-parents` | List all parents/guardians |

```bash
python app.py add-parent --name "John Kamau" --age 50 --relationship Father
```

### Classrooms

| Command | Description |
|---|---|
| `add-classroom` | Create a classroom |
| `list-classrooms` | List all classrooms |
| `assign-student` | Assign a student to a classroom |

```bash
python app.py add-classroom --name "Form 4" --capacity 40
python app.py assign-student --student 1 --classroom 1
```

### Grades

| Command | Description |
|---|---|
| `record-grade` | Record a subject grade for a student |
| `view-grades --student <id>` | View all grades for a student |

```bash
python app.py record-grade --student 1 --subject "Mathematics" --score 87
python app.py view-grades --student 1
```

Grade scale:

| Score | Letter |
|---|---|
| 90 – 100 | A+ |
| 80 – 89 | A |
| 70 – 79 | B+ |
| 60 – 69 | B |
| 50 – 59 | C |
| 40 – 49 | D |
| 0 – 39 | F |

### Attendance

| Command | Description |
|---|---|
| `mark-attendance` | Mark a student's attendance |
| `view-attendance --student <id>` | View all attendance records |

```bash
python app.py mark-attendance --student 1 --status Present
python app.py mark-attendance --student 1 --status Absent --date "2025-06-01" --notes "Sick"
```

Valid statuses: `Present`, `Absent`, `Late`

### Reports

| Command | Description |
|---|---|
| `student-report --student <id>` | Full report for one student |
| `school-report` | School-wide summary |

---

## Project Structure

```
school-management-system/
│
├── app.py                    # CLI entry point
│
├── models/
│   ├── person.py             # Base Person class (inheritance root)
│   ├── student.py            # Student(Person) — grades & attendance
│   ├── teacher.py            # Teacher(Person) — subjects & classrooms
│   ├── parent.py             # Parent(Person) — linked students
│   ├── classroom.py          # Classroom — enrollment management
│   ├── grade.py              # Grade — score + letter grade
│   └── attendance.py         # Attendance — Present / Absent / Late
│
├── services/
│   ├── storage.py            # JSON file persistence (atomic writes)
│   └── school_manager.py     # Core business logic — all CRUD + reports
│
├── cli/
│   └── commands.py           # argparse setup + all command handlers
│
├── utils/
│   └── validators.py         # Reusable input validation functions
│
├── tests/
│   ├── conftest.py           # Shared fixtures + in-memory storage stub
│   ├── test_student.py       # Student tests (creation, search, CRUD)
│   ├── test_teacher.py       # Teacher tests
│   ├── test_grade.py         # Grade recording and letter-grade tests
│   └── test_attendance.py    # Attendance marking and summary tests
│
├── data/
│   └── database.json         # Persistent JSON data store
│
├── requirements.txt
└── README.md
```

---

## OOP Design

```
Person (base)
├── Student  — grades, attendance, parent linkage
├── Teacher  — subjects, classroom assignments
└── Parent   — linked student list, relationship type

Supporting classes:
├── Classroom  — enrollment, capacity management
├── Grade      — score + automatic letter grade
└── Attendance — Present / Absent / Late records
```

All model classes implement:
- Private attributes with `@property` accessors
- Validation via `@setter` decorators
- `to_dict()` / `from_dict()` for JSON serialization
- `__str__()` and `__repr__()`

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=. --cov-report=term-missing

# Run a specific test file
python -m pytest tests/test_student.py -v
```

The test suite contains **58 tests** across 4 test files, covering:
- Student creation, validation, search, update, and deletion
- Teacher creation and classroom assignment
- Grade recording, letter grade boundaries, and serialization
- Attendance marking, status validation, and summary counts

All tests use an **in-memory storage stub** — no files are written to disk during testing.

---

## Data Persistence

Data is saved automatically to `data/database.json` after every write operation.

- Missing database file → created fresh on first save
- Empty file → treated as a fresh database
- Corrupt JSON → backed up to `database.json.bak`, fresh database started
- Writes are **atomic** (temp file → replace) to prevent data loss

---

## Future Improvements

- **Authentication** — Role-based access (admin, teacher, parent logins)
- **Export** — Generate PDF or Excel reports with `reportlab` / `openpyxl`
- **Notifications** — Email/SMS alerts for low attendance or failing grades (e.g. via Twilio / Africastalking)
- **Web Interface** — REST API with FastAPI + React frontend
- **Fee Management** — Track school fees, M-Pesa payment integration
- **Timetable** — Subject scheduling per classroom and teacher
- **Bulk Import** — Load students from CSV/Excel files

---

## Dependencies

| Package | Purpose |
|---|---|
| `rich` | Coloured terminal output, tables, panels |
| `python-dateutil` | Flexible date parsing for attendance dates |
| `pytest` | Unit testing framework |
| `pytest-cov` | Test coverage reporting |

---

## License

MIT License — free to use, modify, and distribute.
