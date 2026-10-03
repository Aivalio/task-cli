# 📝 Task CLI

A simple command-line task manager written in Python.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/Aivalio/task-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/Aivalio/task-cli/actions/workflows/tests.yml)

---

## ✨ Features

- ➕ **Add** tasks with priority and due date
- 📋 **List** all tasks
- ✅ **Complete** tasks
- 🔄 **Reopen** completed tasks
- ✏️ **Edit** existing tasks
- 🗑️ **Delete** tasks
- 🔍 **Search** tasks by title
- 🎯 **Filter** by status or priority
- 📊 **View statistics**
- 🧹 **Clear** completed tasks
- 💬 **Interactive mode** — menu-driven interface

---

## 📦 Requirements

- Python 3.10+
- No third-party runtime dependencies (uses only the standard library)

---

## 🚀 Installation

```bash
git clone https://github.com/Aivalio/task-cli.git
cd task-cli
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🎮 Usage

### Command-line mode

```bash
# Add a task
python -m task_cli add "Buy groceries" --priority high --due 2026-10-15

# List all tasks
python -m task_cli list

# Mark a task as completed
python -m task_cli complete 1

# Reopen a completed task
python -m task_cli reopen 1

# Edit a task
python -m task_cli edit 2 --title "Buy almond milk" --priority low

# Delete a task
python -m task_cli delete 3

# Search by keyword
python -m task_cli search milk

# Filter by status and priority
python -m task_cli filter --status pending --priority high

# Show statistics
python -m task_cli stats

# Clear all completed tasks
python -m task_cli clear
```

### Interactive mode

Run without any arguments to open the menu:

```bash
python -m task_cli
```

```
============================
       TASK CLI
============================
1. View tasks
2. Add task
3. Complete task
4. Reopen task
5. Delete task
6. Search tasks
7. Statistics
8. Clear completed
9. Exit

Choose an option:
```

---

## 📸 Example Output

**Adding and listing tasks:**

```
$ python -m task_cli add "Buy milk" --priority high --due 2026-10-15
✓ Added: Buy milk

$ python -m task_cli add "Walk dog"
✓ Added: Walk dog

$ python -m task_cli list

--- Tasks ---
1. [ ] Buy milk | Priority: HIGH | Due: 2026-10-15
2. [ ] Walk dog | Priority: MEDIUM
```

**Statistics:**

```
$ python -m task_cli stats

--- Statistics ---
Total tasks:     2
Completed:       1
Remaining:       1

By priority:
  Low      0
  Medium   1
  High     1

Completion rate: 50.0%
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

The project has **33 unit tests** covering storage, task logic, and display helpers.

```bash
pytest tests/test_storage.py -v    # Storage tests
pytest tests/test_tasks.py -v      # Business logic tests
pytest tests/test_display.py -v    # Display tests
```

---

## 📁 Project Structure

```
task-cli/
├── task_cli/
│   ├── __init__.py
│   ├── __main__.py          # Entry point for `python -m task_cli`
│   ├── constants.py         # Configuration constants
│   ├── storage.py           # JSON file storage
│   ├── tasks.py             # Task business logic
│   ├── display.py           # Output formatting
│   └── main.py              # CLI (argparse)
├── tests/
│   ├── __init__.py
│   ├── test_storage.py
│   ├── test_tasks.py
│   └── test_display.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## 💾 Data Storage

Tasks are stored in `tasks.json` in the current working directory:

```json
[
  {
    "title": "Buy milk",
    "completed": false,
    "priority": "high",
    "due_date": "2026-10-15"
  }
]
```

---

## 🗺️ Roadmap

- [ ] Add task categories / projects
- [ ] Support recurring tasks
- [ ] Export tasks to CSV / Markdown
- [ ] Config file (`~/.task-cli/config.json`)
- [ ] Colored output (with `colorama`)

---

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome. Feel free to open an issue.

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

**Built with ☕ by [Aivalio](https://github.com/Aivalio)**