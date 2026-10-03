"""Tests for display helpers."""
from task_cli.display import format_task


def test_format_task_incomplete():
    task = {"title": "Buy milk", "completed": False, "priority": "high", "due_date": ""}
    result = format_task(1, task)
    assert "1." in result
    assert "[ ]" in result
    assert "Buy milk" in result
    assert "HIGH" in result
    assert "Due" not in result  # no due date


def test_format_task_completed():
    task = {"title": "Walk dog", "completed": True, "priority": "low", "due_date": ""}
    result = format_task(2, task)
    assert "[✓]" in result
    assert "Walk dog" in result
    assert "LOW" in result


def test_format_task_with_due_date():
    task = {"title": "Pay bill", "completed": False, "priority": "medium", "due_date": "2026-10-15"}
    result = format_task(3, task)
    assert "Due: 2026-10-15" in result


def test_format_task_priority_is_uppercase():
    task = {"title": "Test", "completed": False, "priority": "high", "due_date": ""}
    result = format_task(1, task)
    assert "HIGH" in result
    assert "high" not in result.replace("HIGH", "")