"""Command-line interface for the Todo List application.

Provides a CLI for interacting with the task manager.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .manager import TaskManager


def format_task(task) -> str:
    """Format a task for display.

    Args:
        task: Task object to format

    Returns:
        Formatted string representation
    """
    status = "✓" if task.completed else " "
    priority_indicator = {"high": " [HIGH]", "medium": "", "low": " [LOW]"}.get(
        task.priority, ""
    )
    due = f" (Due: {task.due_date})" if task.due_date else ""
    return f"[{status}] #{task.id}: {task.description}{priority_indicator}{due}"


def print_tasks(tasks: List, title: str = "Tasks") -> None:
    """Print a list of tasks with a title.

    Args:
        tasks: List of tasks to print
        title: Title to display
    """
    print(f"\n=== {title} ===")
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(format_task(task))
    print()


def cmd_add(manager: TaskManager, args: argparse.Namespace) -> int:
    """Handle the add command.

    Args:
        manager: TaskManager instance
        args: Parsed arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task = manager.add_task(
            description=args.description,
            priority=args.priority,
            due_date=args.due_date,
        )
        print(f"Added task: {format_task(task)}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_list(manager: TaskManager, args: argparse.Namespace) -> int:
    """Handle the list command.

    Args:
        manager: TaskManager instance
        args: Parsed arguments

    Returns:
        Exit code
    """
    completed_filter = None
    if args.completed:
        completed_filter = True
    elif args.pending:
        completed_filter = False

    priority_filter = args.priority.lower() if args.priority else None
    sort_by = args.sort

    tasks = manager.get_tasks(
        completed=completed_filter,
        priority=priority_filter,
        sort_by=sort_by,
    )

    # Build title
    title_parts = ["Tasks"]
    if completed_filter is True:
        title_parts.append("(Completed)")
    elif completed_filter is False:
        title_parts.append("(Pending)")
    if priority_filter:
        title_parts.append(f"[Priority: {priority_filter}]")

    print_tasks(tasks, " ".join(title_parts))

    # Show stats
    stats = manager.get_stats()
    print(f"Total: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}")
    return 0


def cmd_complete(manager: TaskManager, args: argparse.Namespace) -> int:
    """Handle the complete command.

    Args:
        manager: TaskManager instance
        args: Parsed arguments

    Returns:
        Exit code
    """
    if manager.complete_task(args.task_id):
        print(f"Task #{args.task_id} marked as completed.")
        return 0
    else:
        print(f"Error: Task #{args.task_id} not found.", file=sys.stderr)
        return 1


def cmd_delete(manager: TaskManager, args: argparse.Namespace) -> int:
    """Handle the delete command.

    Args:
        manager: TaskManager instance
        args: Parsed arguments

    Returns:
        Exit code
    """
    if manager.delete_task(args.task_id):
        print(f"Task #{args.task_id} deleted.")
        return 0
    else:
        print(f"Error: Task #{args.task_id} not found.", file=sys.stderr)
        return 1


def cmd_clear_completed(manager: TaskManager, args: argparse.Namespace) -> int:
    """Handle the clear-completed command.

    Args:
        manager: TaskManager instance
        args: Parsed arguments

    Returns:
        Exit code
    """
    count = manager.clear_completed()
    print(f"Cleared {count} completed task(s).")
    return 0


def cmd_search(manager: TaskManager, args: argparse.Namespace) -> int:
    """Handle the search command.

    Args:
        manager: TaskManager instance
        args: Parsed arguments

    Returns:
        Exit code
    """
    tasks = manager.search_tasks(args.query)
    print_tasks(tasks, f'Search results for "{args.query}"')
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo List CLI Application",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument(
        "--priority",
        choices=["high", "medium", "low"],
        default="medium",
        help="Task priority (default: medium)",
    )
    add_parser.add_argument("--due-date", help="Due date in YYYY-MM-DD format")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    status_group = list_parser.add_mutually_exclusive_group()
    status_group.add_argument(
        "--completed", action="store_true", help="Show only completed tasks"
    )
    status_group.add_argument(
        "--pending", action="store_true", help="Show only pending tasks"
    )
    list_parser.add_argument(
        "--priority", choices=["high", "medium", "low"], help="Filter by priority"
    )
    list_parser.add_argument(
        "--sort",
        choices=["id", "priority", "due_date", "created_at"],
        default="id",
        help="Sort by field (default: id)",
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="Task ID to complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    # Clear-completed command
    subparsers.add_parser("clear-completed", help="Remove all completed tasks")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks by description")
    search_parser.add_argument("query", help="Search query")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv)

    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    manager = TaskManager()

    command_handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "complete": cmd_complete,
        "delete": cmd_delete,
        "clear-completed": cmd_clear_completed,
        "search": cmd_search,
    }

    handler = command_handlers.get(args.command)
    if handler:
        return handler(manager, args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
