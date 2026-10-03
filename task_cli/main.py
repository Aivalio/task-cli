"""Command-line interface for task-cli."""
import argparse

from task_cli.constants import DEFAULT_PRIORITY, PRIORITIES, TASKS_FILE
from task_cli.display import (
    print_error,
    print_info,
    print_statistics,
    print_success,
    print_tasks,
)
from task_cli.storage import load_tasks, save_tasks
from task_cli.tasks import (
    add_task,
    clear_completed,
    complete_task,
    delete_task,
    edit_task,
    filter_tasks,
    reopen_task,
    search_tasks,
)


# --- Command handlers ---

def cmd_add(args: argparse.Namespace) -> None:
    """Handle `add` command."""
    tasks = load_tasks()
    try:
        task = add_task(tasks, args.title, args.priority, args.due or "")
        save_tasks(tasks)
        print_success(f"Added: {task['title']}")
    except ValueError as error:
        print_error(str(error))


def cmd_list(args: argparse.Namespace) -> None:
    """Handle `list` command."""
    tasks = load_tasks()
    print_tasks(tasks)


def cmd_complete(args: argparse.Namespace) -> None:
    """Handle `complete` command."""
    tasks = load_tasks()
    task = complete_task(tasks, args.number)
    if task is None:
        print_error(f"No task with number {args.number}.")
        return
    save_tasks(tasks)
    print_success(f"Completed: {task['title']}")


def cmd_reopen(args: argparse.Namespace) -> None:
    """Handle `reopen` command."""
    tasks = load_tasks()
    task = reopen_task(tasks, args.number)
    if task is None:
        print_error(f"No task with number {args.number}.")
        return
    save_tasks(tasks)
    print_success(f"Reopened: {task['title']}")


def cmd_delete(args: argparse.Namespace) -> None:
    """Handle `delete` command."""
    tasks = load_tasks()
    task = delete_task(tasks, args.number)
    if task is None:
        print_error(f"No task with number {args.number}.")
        return
    save_tasks(tasks)
    print_success(f"Deleted: {task['title']}")


def cmd_edit(args: argparse.Namespace) -> None:
    """Handle `edit` command."""
    tasks = load_tasks()
    try:
        task = edit_task(
            tasks,
            args.number,
            title=args.title,
            priority=args.priority,
            due_date=args.due,
        )
    except ValueError as error:
        print_error(str(error))
        return

    if task is None:
        print_error(f"No task with number {args.number}.")
        return

    save_tasks(tasks)
    print_success(f"Updated: {task['title']}")


def cmd_search(args: argparse.Namespace) -> None:
    """Handle `search` command."""
    tasks = load_tasks()
    results = search_tasks(tasks, args.keyword)
    print_tasks(results, title=f"Search results for '{args.keyword}'")


def cmd_filter(args: argparse.Namespace) -> None:
    """Handle `filter` command."""
    tasks = load_tasks()

    completed = None
    if args.status == "completed":
        completed = True
    elif args.status == "pending":
        completed = False

    results = filter_tasks(tasks, completed=completed, priority=args.priority)
    print_tasks(results, title="Filtered tasks")


def cmd_stats(args: argparse.Namespace) -> None:
    """Handle `stats` command."""
    tasks = load_tasks()
    print_statistics(tasks)


def cmd_clear(args: argparse.Namespace) -> None:
    """Handle `clear` command."""
    tasks = load_tasks()
    removed = clear_completed(tasks)
    if removed == 0:
        print_info("No completed tasks to clear.")
        return
    save_tasks(tasks)
    print_success(f"Cleared {removed} completed task(s).")


# --- Argument parser ---

def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="task",
        description="A simple CLI task manager.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # add
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument(
        "--priority",
        choices=PRIORITIES,
        default=DEFAULT_PRIORITY,
        help="Task priority (default: medium)",
    )
    p_add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = subparsers.add_parser("list", help="List all tasks")
    p_list.set_defaults(func=cmd_list)

    # complete
    p_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    p_complete.add_argument("number", type=int, help="Task number")
    p_complete.set_defaults(func=cmd_complete)

    # reopen
    p_reopen = subparsers.add_parser("reopen", help="Mark a task as not completed")
    p_reopen.add_argument("number", type=int, help="Task number")
    p_reopen.set_defaults(func=cmd_reopen)

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("number", type=int, help="Task number")
    p_delete.set_defaults(func=cmd_delete)

    # edit
    p_edit = subparsers.add_parser("edit", help="Edit a task")
    p_edit.add_argument("number", type=int, help="Task number")
    p_edit.add_argument("--title", help="New title")
    p_edit.add_argument("--priority", choices=PRIORITIES, help="New priority")
    p_edit.add_argument("--due", help="New due date")
    p_edit.set_defaults(func=cmd_edit)

    # search
    p_search = subparsers.add_parser("search", help="Search tasks by title")
    p_search.add_argument("keyword", help="Search keyword")
    p_search.set_defaults(func=cmd_search)

    # filter
    p_filter = subparsers.add_parser("filter", help="Filter tasks")
    p_filter.add_argument(
        "--status",
        choices=["all", "completed", "pending"],
        default="all",
    )
    p_filter.add_argument("--priority", choices=PRIORITIES)
    p_filter.set_defaults(func=cmd_filter)

    # stats
    p_stats = subparsers.add_parser("stats", help="Show statistics")
    p_stats.set_defaults(func=cmd_stats)

    # clear
    p_clear = subparsers.add_parser("clear", help="Clear all completed tasks")
    p_clear.set_defaults(func=cmd_clear)

    return parser


def main() -> None:
    """Entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()