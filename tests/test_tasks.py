"""Tests for task business logic."""
import pytest

from task_cli.tasks import (
    add_task,
    clear_completed,
    complete_task,
    delete_task,
    edit_task,
    filter_tasks,
    find_task,
    get_statistics,
    reopen_task,
    search_tasks,
)


@pytest.fixture
def sample_tasks():
    """A fresh list of sample tasks."""
    return [
        {"title": "Buy milk", "completed": False, "priority": "high", "due_date": ""},
        {"title": "Walk dog", "completed": True, "priority": "low", "due_date": ""},
        {"title": "Read book", "completed": False, "priority": "medium", "due_date": ""},
    ]


# --- find_task ---

def test_find_task_returns_correct(sample_tasks):
    assert find_task(sample_tasks, 1)["title"] == "Buy milk"
    assert find_task(sample_tasks, 3)["title"] == "Read book"


def test_find_task_out_of_range(sample_tasks):
    assert find_task(sample_tasks, 0) is None
    assert find_task(sample_tasks, 99) is None


# --- add_task ---

def test_add_task_appends_and_returns(sample_tasks):
    initial = len(sample_tasks)
    task = add_task(sample_tasks, "New task", priority="high")
    assert len(sample_tasks) == initial + 1
    assert task["title"] == "New task"
    assert task["priority"] == "high"
    assert task["completed"] is False


def test_add_task_strips_title(sample_tasks):
    task = add_task(sample_tasks, "  Trim me  ")
    assert task["title"] == "Trim me"


def test_add_task_empty_title_raises(sample_tasks):
    with pytest.raises(ValueError, match="empty"):
        add_task(sample_tasks, "   ")


def test_add_task_invalid_priority_raises(sample_tasks):
    with pytest.raises(ValueError, match="Priority must be one of"):
        add_task(sample_tasks, "Task", priority="urgent")


def test_add_task_default_priority(sample_tasks):
    task = add_task(sample_tasks, "Task")
    assert task["priority"] == "medium"


# --- complete_task / reopen_task ---

def test_complete_task_marks_done(sample_tasks):
    complete_task(sample_tasks, 1)
    assert sample_tasks[0]["completed"] is True


def test_complete_task_out_of_range(sample_tasks):
    assert complete_task(sample_tasks, 99) is None


def test_reopen_task_marks_undone(sample_tasks):
    reopen_task(sample_tasks, 2)
    assert sample_tasks[1]["completed"] is False


# --- delete_task ---

def test_delete_task_removes_and_returns(sample_tasks):
    deleted = delete_task(sample_tasks, 2)
    assert deleted["title"] == "Walk dog"
    assert len(sample_tasks) == 2


def test_delete_task_out_of_range(sample_tasks):
    assert delete_task(sample_tasks, 99) is None
    assert len(sample_tasks) == 3


# --- edit_task ---

def test_edit_task_changes_fields(sample_tasks):
    edit_task(sample_tasks, 1, title="Updated", priority="low")
    assert sample_tasks[0]["title"] == "Updated"
    assert sample_tasks[0]["priority"] == "low"


def test_edit_task_only_applies_non_none(sample_tasks):
    edit_task(sample_tasks, 1, title="New title")
    assert sample_tasks[0]["title"] == "New title"
    assert sample_tasks[0]["priority"] == "high"  # unchanged


def test_edit_task_empty_title_raises(sample_tasks):
    with pytest.raises(ValueError, match="empty"):
        edit_task(sample_tasks, 1, title="   ")


def test_edit_task_out_of_range(sample_tasks):
    assert edit_task(sample_tasks, 99, title="X") is None


# --- search_tasks ---

def test_search_tasks_matches_case_insensitive(sample_tasks):
    results = search_tasks(sample_tasks, "DOG")
    assert len(results) == 1
    assert results[0]["title"] == "Walk dog"


def test_search_tasks_empty_keyword(sample_tasks):
    assert search_tasks(sample_tasks, "  ") == []


# --- filter_tasks ---

def test_filter_completed(sample_tasks):
    result = filter_tasks(sample_tasks, completed=True)
    assert len(result) == 1
    assert result[0]["title"] == "Walk dog"


def test_filter_by_priority(sample_tasks):
    result = filter_tasks(sample_tasks, priority="high")
    assert len(result) == 1
    assert result[0]["title"] == "Buy milk"


# --- get_statistics ---

def test_statistics_empty():
    stats = get_statistics([])
    assert stats["total"] == 0
    assert stats["completion_rate"] == 0.0


def test_statistics_with_tasks(sample_tasks):
    stats = get_statistics(sample_tasks)
    assert stats["total"] == 3
    assert stats["completed"] == 1
    assert stats["remaining"] == 2
    assert stats["completion_rate"] == 33.3
    assert stats["by_priority"]["high"] == 1


# --- clear_completed ---

def test_clear_completed_removes_done(sample_tasks):
    removed = clear_completed(sample_tasks)
    assert removed == 1
    assert len(sample_tasks) == 2
    assert all(not t["completed"] for t in sample_tasks)


def test_clear_completed_when_none(sample_tasks):
    clear_completed(sample_tasks)  # first clears "Walk dog"
    removed = clear_completed(sample_tasks)  # nothing left to clear
    assert removed == 0