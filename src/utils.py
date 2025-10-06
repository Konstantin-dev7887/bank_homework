from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def read_transactions(path_text: str | Path) -> List[Dict[str, Any]]:
    """
    Прочитать JSON-файл с операциями и вернуть список словарей.
    Если файла нет, он пуст, повреждён или верхний уровень не список -
    вернуть [].
    """
    path = Path(path_text)

    try:
        if not path.exists() or path.stat().st_size == 0:
            return []

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    return data if isinstance(data, list) else []
