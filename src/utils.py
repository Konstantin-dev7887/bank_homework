from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

LOGS_DIRECTORY = Path("logs")
LOGS_DIRECTORY.mkdir(exist_ok=True)

UTILS_LOG_FILE = LOGS_DIRECTORY / "utils.log"

logger = logging.getLogger("src.utils")
logger.setLevel(logging.DEBUG)

_file_handler = logging.FileHandler(UTILS_LOG_FILE, mode="w", encoding="utf-8")
_file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_file_handler.setFormatter(_file_formatter)

if not logger.handlers:
    logger.addHandler(_file_handler)

logger.propagate = False


def read_transactions(path_text: str | Path) -> List[Dict[str, Any]]:
    """
    Прочитать JSON-файл с операциями и вернуть список словарей.
    Если файла нет, он пуст, повреждён или верхний уровень не список -
    вернуть [].
    """
    path = Path(path_text)
    logger.debug("read_transactions called: path=%s", path)

    try:
        if not path.exists():
            logger.error("File not found: %s", path)
            return []

        if path.stat().st_size == 0:
            logger.error("File is empty: %s", path)
            return []

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info("Loaded %d transactions from %s", len(data), path)
            return data

        logger.error("Top-level JSON is not a list: %s", type(data).__name__)
        return []
    except json.JSONDecodeError as exception:
        logger.error("JSON decode error for %s: %s", path, exception)
        return []
    except OSError as exception:
        logger.error("OS error for %s: %s", path, exception)
        return []
