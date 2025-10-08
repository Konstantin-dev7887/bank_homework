from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

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


def read_transactions_json(path_text: str | Path) -> List[Dict[str, Any]]:
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


def read_transactions_csv(path_text: str | Path) -> List[Dict[str, Any]]:
    """
    Прочитать CSV и вернуть список словарей с транзакциями.
    Любая ошибка чтения -> [].
    Пропуски -> None.
    """
    path = Path(path_text)
    logger.debug("read_transactions_csv called: path=%s", path)

    try:
        if not path.exists():
            logger.error("CSV file not found: %s", path)
            return []

        data_frame = pd.read_csv(path, dtype=str, keep_default_na=True)
        logger.info("CSV file %s successfully read, %d rows",
                    path,
                    len(data_frame))
    except Exception as exception:
        logger.error("Error reading CSV file %s: %s",
                     path,
                     exception)
        return []

    if data_frame.empty:
        logger.warning("CSV file %s is empty",
                       path)
        return []

    data_frame = data_frame.where(pd.notnull(data_frame), None)
    records = data_frame.to_dict(orient="records")
    logger.debug("CSV file %s converted to list of dicts",
                 path)
    return records


def read_transactions_excel(
        path_text: str | Path,
        sheet_name: str | int | None = 0,
) -> List[Dict[str, Any]]:
    """
    Прочитать XLSX и вернуть список словарей с транзакциями.
    По умолчанию читается первый лист (sheet_name=0).
    Любая ошибка чтения -> [].
    Пропуски -> None.
    """
    path = Path(path_text)
    logger.debug("read_transactions_excel called: path=%s, sheet_name=%s",
                 path,
                 sheet_name)

    try:
        if not path.exists():
            logger.error("Excel file not found: %s", path)
            return []

        data_frame = pd.read_excel(path,
                                   sheet_name=sheet_name,
                                   dtype=str,
                                   engine="openpyxl")
        logger.info("Excel file %s successfully read, %d rows",
                    path,
                    len(data_frame))
    except Exception as exception:
        logger.error("Error reading Excel file %s: %s",
                     path,
                     exception)
        return []

    if data_frame.empty:
        logger.warning("Excel file %s is empty",
                       path)
        return []

    data_frame = data_frame.where(pd.notnull(data_frame),
                                  None)
    records = data_frame.to_dict(orient="records")
    logger.debug("Excel file %s converted to list of dicts",
                 path)
    return records
