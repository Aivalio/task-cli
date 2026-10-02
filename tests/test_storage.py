"""Tests for the JSON storage module."""
import json
from task_cli.storage import load_tasks, save_tasks


def test_load_missing_file_returns_empty_list(tmp_path):
    """Loading a non-existent file should return an empty list."""
    path = tmp_path / "missing.json"
    assert load_tasks(str(path)) == []


def test_save_and_load_roundtrip(tmp_path):
    """Saving then loading should return the same tasks."""
    path = tmp_path / "tasks.json"
    tasks = [
        {"title": "Buy milk", "completed": False},
        {"title": "Walk dog", "completed": True},
    ]

    save_tasks(tasks, str(path))
    loaded = load_tasks(str(path))

    assert loaded == tasks


def test_load_corrupted_json_returns_empty_list(tmp_path):
    """A corrupted file should not crash — return empty list."""
    path = tmp_path / "corrupted.json"
    path.write_text("{ not valid json", encoding="utf-8")

    assert load_tasks(str(path)) == []


def test_load_non_list_json_returns_empty_list(tmp_path):
    """If the JSON is valid but not a list, return empty list."""
    path = tmp_path / "wrong_type.json"
    path.write_text('{"foo": "bar"}', encoding="utf-8")

    assert load_tasks(str(path)) == []


def test_save_creates_readable_json(tmp_path):
    """Saved file should be valid, pretty-printed JSON."""
    path = tmp_path / "tasks.json"
    tasks = [
        {"title": "Test",
         "completed": False}
    ]

    save_tasks(tasks, str(path))

    content = path.read_text(encoding="utf-8")
    assert "Test" in content
    assert json.loads(content) == tasks