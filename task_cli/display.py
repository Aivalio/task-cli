"""Display helpers for printing tasks and messages."""
from task_cli.tasks import get_statistics


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"✗ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"i {message}")


def format_task(index: int, task: dict) -> str:
    """Format a single task as a one-line string.

    Args:
        index: 1-based position in the list.
        task: The task dict.

    Returns:
        A formatted string like:
            1. [ ] Buy milk | Priority: HIGH
            2. [✓] Walk dog  | Priority: LOW  | Due: 2026-10-15
    """
    status = "✓" if task["completed"] else " "
    priority = task["priority"].upper()

    line = f"{index}. [{status}] {task['title']} | Priority: {priority}"

    if task["due_date"]:
        line += f" | Due: {task['due_date']}"

    return line


def print_tasks(tasks: list[dict], title: str = "Tasks") -> None:
    """Print a list of tasks with a header.

    If the list is empty, prints a friendly message.
    """
    if not tasks:
        print(f"\nNo {title.lower()} found.")
        return

    print(f"\n--- {title} ---")
    for index, task in enumerate(tasks, start=1):
        print(format_task(index, task))


def print_statistics(tasks: list[dict]) -> None:
    """Print statistics about the tasks."""
    stats = get_statistics(tasks)

    print("\n--- Statistics ---")
    print(f"Total tasks:     {stats['total']}")
    print(f"Completed:       {stats['completed']}")
    print(f"Remaining:       {stats['remaining']}")

    print("\nBy priority:")
    for priority, count in stats["by_priority"].items():
        print(f"  {priority.capitalize():<8} {count}")

    if stats["total"] > 0:
        print(f"\nCompletion rate: {stats['completion_rate']}%")