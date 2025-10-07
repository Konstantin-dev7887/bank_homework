from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.main import main


def test_main_json_smoke(tmp_path: Path,
                         monkeypatch: pytest.MonkeyPatch,
                         capsys: pytest.CaptureFixture[str]) -> None:
    data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "description": "Перевод организации",
            "from": "Visa Classic 4111 1111 1111 1111",
            "to": "Счет 12345678901234567890",
            "operationAmount": {"amount": "100",
                                "currency":
                                    {"name": "руб.", "code": "RUB"}},
        }
    ]
    json_path = tmp_path / "ops.json"
    json_path.write_text(json.dumps(data), encoding="utf-8")

    user_inputs = iter([
        "1",
        str(json_path),
        "EXECUTED",
        "нет",
        "нет",
        "нет",
    ])
    monkeypatch.setattr("builtins.input", lambda *_: next(user_inputs))

    main()

    out = capsys.readouterr().out

    assert "Привет! Добро пожаловать" in out
    assert "Операции отфильтрованы по статусу" in out
    assert "Распечатываю итоговый список транзакций" in out
    assert "Всего банковских операций в выборке: 1" in out
