from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from src.utils import read_transactions


def test_read_transactions_ok(tmp_path: Path) -> None:
    data: List[Dict[str, Any]] = [{"id": 1}, {"id": 2}]
    final_path = tmp_path / "operations.json"
    final_path.write_text(json.dumps(data), encoding="utf-8")

    assert read_transactions(final_path) == data


def test_read_transactions_empty_file(tmp_path: Path) -> None:
    final_path = tmp_path / "empty.json"
    final_path.write_text("", encoding="utf-8")
    assert read_transactions(final_path) == []


def test_read_transactions_not_list(tmp_path: Path) -> None:
    final_path = tmp_path / "obj.json"
    final_path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    assert read_transactions(final_path) == []


def test_read_transactions_missing() -> None:
    assert read_transactions("no_such_file.json") == []
