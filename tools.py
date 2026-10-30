
from database import (
    add_task,
    list_tasks,
    complete_task,
)


def add_task_tool(title: str) -> str:
    """Add a new task to the user's task list.

    Args:
        title: Description of the task to add.
    """

    return add_task(title)


def list_tasks_tool() -> str:
    """List all saved tasks and show their status."""

    return list_tasks()


def complete_task_tool(task_id: int) -> str:
    """Mark an existing task as completed.

    Args:
        task_id: Numeric ID of the task to complete.
    """

    return complete_task(task_id)


# Available tools that Gemini can select.

TOOL_FUNCTIONS = {
    "add_task_tool": add_task_tool,
    "list_tasks_tool": list_tasks_tool,
    "complete_task_tool": complete_task_tool,
}
