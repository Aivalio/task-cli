"""JSON file & task handling."""
import json
import os
from task_cli.constants import TASKS_FILE


def load_tasks(file_path: str = TASKS_FILE) -> list[dict]:
    """Function that loads the tasks from the JSON file.

    Args:
        file_path: The path to the JSON file.
    Returns:
        A list of task dictionaries. Returns an empty list if the file
        does not exist or cannot be parsed.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            response = json.load(file)
    except (json.JSONDecodeError, OSError, FileNotFoundError):
        return []

    if not isinstance(response, list):
        return []

    return response


def save_tasks(tasks: list[dict], file_path: str = TASKS_FILE) -> None:
    """Function that saves the tasks to the JSON file.

    Args:
        tasks: The list of task dictionaries.
        file_path: The path to the JSON file.

    Returns:
        OSError if the file does not exist or cannot be parsed.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)
    except OSError:
        return None