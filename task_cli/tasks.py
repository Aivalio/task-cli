"""Business logic for the task operations."""
from task_cli.constants import DEFAULT_PRIORITY, PRIORITIES


def find_task(tasks: list[dict], index: int) -> dict | None:
    """Find a task by its 1-based index.

    Args:
        tasks: List of tasks.
        index: 1-based index of the task.

    Returns:
        The task dict, or None if the index is out of range.
    """
    if index < 1 or index > len(tasks):
        return None
    return tasks[index - 1]


def add_task(
    tasks: list[dict],
    title: str,
    priority: str = DEFAULT_PRIORITY,
    due_date: str = "",
) -> dict:
    """Add a new task to the list.

    Args:
        tasks: List of tasks.
        title: The title of the task.
        priority: Priority of the task.
        due_date: Optional due date of the task.

    Returns:
        The task dict.

    Raises:
        ValueError: If title is empty or priority invalid.
    """
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")

    priority = priority.lower()
    if priority not in PRIORITIES:
        raise ValueError(f"Priority must be one of {PRIORITIES}")

    task = {
        "title": title,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
    }
    tasks.append(task)
    return task


def complete_task(tasks: list[dict], index: int) -> dict | None:
    """Function that completes a task.

    Args:
        tasks: List of tasks.
        index: 1-based index of the task.

    Returns:
        The updated task or None if out of range.
    """
    task = find_task(tasks, index)
    if task is None:
        return None
    task["completed"] = True
    return task


def reopen_task(tasks: list[dict], index: int) -> dict | None:
    """Function that marks a task as not completed.

    Returns:
        The updated task or None if out of range.
    """
    task = find_task(tasks, index)
    if task is None:
        return None
    task["completed"] = False
    return task


def delete_task(tasks: list[dict], index: int) -> dict | None:
    """Function that deletes a task.

    Returns:
        The deleted task or None if out of range.
    """
    if index < 1 or index > len(tasks):
        return None
    return tasks.pop(index-1)


def edit_task(
        tasks: list[dict],
        index: int,
        title: str | None = None,
        priority: str | None = None,
        due_date: str | None = None,
) -> dict | None:
    """Function that edits a task.
    Args:
        tasks: The task list.
        index: 1-based position.
        title: New title (optional).
        priority: New priority (optional).
        due_date: New due date (optional).

    Returns:
        The updated task, or None if index is out of range.

    Raises:
        ValueError: If new title is empty or priority is invalid.
    """
    task = find_task(tasks, index)
    if task is None:
        return None

    if title is not None:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        task["title"] = title

    if priority is not None:
        priority = priority.lower()
        if priority not in PRIORITIES:
            raise ValueError("Priority must be one of {}".format(PRIORITIES))
        task["priority"] = priority

    if due_date is not None:
        task["due_date"] = due_date.strip()

    return task


def search_tasks(tasks: list[dict], keyword: str) -> list[dict]:
    """Function that searches for tasks matching the given keyword."""
    keyword = keyword.lower().strip()
    if not keyword:
        return []
    return [task for task in tasks if keyword in task["title"].lower()]


def filter_tasks(
    tasks: list[dict],
    *,
    completed: bool | None = None,
    priority: str | None = None,
) -> list[dict]:
    """Filter tasks by completion status and/or priority."""
    result = tasks
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    if priority is not None:
        result = [t for t in result if t["priority"] == priority]
    return result


def clear_completed(tasks: list[dict]) -> int:
    """Function that clears completed tasks.

    Returns:
        The number of completed tasks.
    """
    original = len(tasks)
    tasks[:] = [task for task in tasks if not task["completed"]]
    return original - len(tasks)


def get_statistics(tasks: list[dict]) -> dict:
    """Return aggregate statistics about the tasks."""
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    remaining = total - completed

    by_priority = {p: 0 for p in PRIORITIES}
    for t in tasks:
        by_priority[t["priority"]] += 1

    percentage = (completed / total * 100) if total else 0.0

    return {
        "total": total,
        "completed": completed,
        "remaining": remaining,
        "by_priority": by_priority,
        "completion_rate": round(percentage, 1),
    }