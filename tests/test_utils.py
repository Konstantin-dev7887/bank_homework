from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pandas as pd

from src.utils import (read_transactions_csv,
                       read_transactions_excel,
                       read_transactions_json)


def test_read_transactions_ok(tmp_path: Path) -> None:
    data: List[Dict[str, Any]] = [{"id": 1}, {"id": 2}]
    final_path = tmp_path / "operations.json"
    final_path.write_text(json.dumps(data), encoding="utf-8")

    assert read_transactions_json(final_path) == data


def test_read_transactions_empty_file(tmp_path: Path) -> None:
    final_path = tmp_path / "empty.json"
    final_path.write_text("", encoding="utf-8")
    assert read_transactions_json(final_path) == []


def test_read_transactions_not_list(tmp_path: Path) -> None:
    final_path = tmp_path / "obj.json"
    final_path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    assert read_transactions_json(final_path) == []


def test_read_transactions_missing() -> None:
    assert read_transactions_json("no_such_file.json") == []


def _get_data_frame(rows: List[Dict[str, Any]]) -> "pd.DataFrame":
    """Удобный хелпер для сборки DataFrame."""
    return pd.DataFrame(rows)


@patch("src.utils.pd.read_csv")
def test_read_transactions_csv_success(read_csv_mock: Mock) -> None:
    rows = [
        {"id": "1", "amount": "10.50", "currency": "USD"},
        {"id": "2", "amount": "999.00", "currency": "RUB"},
    ]
    read_csv_mock.return_value = _get_data_frame(rows)

    result = read_transactions_csv("data/transactions.csv")

    assert result == rows
    read_csv_mock.assert_called_once()


@patch("src.utils.pd.read_csv")
def test_read_transactions_csv_empty_data_frame(read_csv_mock: Mock) -> None:
    read_csv_mock.return_value = _get_data_frame([])
    assert read_transactions_csv("data/transactions.csv") == []
    read_csv_mock.assert_called_once()


@patch("src.utils.pd.read_csv")
def test_read_transactions_csv_missing_file_returns_empty(
        read_csv_mock: Mock) -> None:
    assert read_transactions_csv("no_such.csv") == []
    read_csv_mock.assert_not_called()


@patch("src.utils.pd.read_csv")
def test_read_transactions_csv_error_returns_empty(read_csv_mock: Mock,
                                                   tmp_path: Path) -> None:
    p = tmp_path / "broken.csv"
    p.write_text("id,amount,currency\n", encoding="utf-8")

    read_csv_mock.side_effect = Exception("boom")
    assert read_transactions_csv(p) == []
    read_csv_mock.assert_called_once()


@patch("src.utils.pd.read_excel")
def test_read_transactions_excel_success(read_excel_mock: Mock) -> None:
    rows = [
        {"id": "3", "amount": "5.00", "currency": "EUR"},
        {"id": "4", "amount": None, "currency": "RUB"},
    ]
    read_excel_mock.return_value = _get_data_frame(rows)

    result = read_transactions_excel("data/transactions_excel.xlsx")

    assert result == rows
    read_excel_mock.assert_called_once()


@patch("src.utils.pd.read_excel")
def test_read_transactions_excel_empty_df(read_excel_mock: Mock) -> None:
    read_excel_mock.return_value = _get_data_frame([])
    assert read_transactions_excel("data/transactions_excel.xlsx") == []
    read_excel_mock.assert_called_once()


@patch("src.utils.pd.read_excel")
def test_read_transactions_excel_missing_file_returns_empty(
        read_excel_mock: Mock) -> None:
    assert read_transactions_excel("no_such.xlsx") == []
    read_excel_mock.assert_not_called()


@patch("src.utils.pd.read_excel")
def test_read_transactions_excel_error_returns_empty(
        read_excel_mock: Mock,
        tmp_path: Path) -> None:
    path = tmp_path / "broken.xlsx"
    path.write_bytes(b"")

    read_excel_mock.side_effect = Exception("fail")
    assert read_transactions_excel(path) == []
    read_excel_mock.assert_called_once()
