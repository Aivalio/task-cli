# 📝 Task CLI

A simple command-line task manager written in Python.

## Features

- ➕ Add tasks with priority and due date
- 📋 List all tasks
- ✅ Mark tasks as completed
- ✏️ Edit existing tasks
- 🔍 Search tasks by title
- 🎯 Filter by status or priority
- 📊 View statistics
- 🗑️ Delete tasks
- 🧹 Clear completed tasks

## Requirements

- Python 3.10+

## Installation

```bash
git clone https://github.com/Aivalio/task-cli.git
cd task-cli
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```


## Usage

```bash
python -m task_cli add "Buy groceries" --priority high --due 2026-10-15
python -m task_cli list
python -m task_cli complete 1
python -m task_cli stats
```

Or run interactively:

```bash
python -m task_cli
```

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT