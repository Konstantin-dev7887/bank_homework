from __future__ import annotations

import logging
from pathlib import Path

MIN_CARD_LENGTH: int = 12
VISIBLE_CARD_PREFIX: int = 6
VISIBLE_CARD_SUFFIX: int = 4
GROUP_SIZE: int = 4

MASK_SYMBOL: str = "*"
ACCOUNT_PREFIX_1: str = "Счет "
ACCOUNT_PREFIX_2: str = "Счёт "
ACCOUNT_MASK_PREFIX: str = "**"

LOGS_DIRECTORY = Path("logs")
LOGS_DIRECTORY.mkdir(exist_ok=True)

MASKS_LOG_FILE = LOGS_DIRECTORY / "masks.log"

logger = logging.getLogger("src.masks")
logger.setLevel(logging.DEBUG)

_file_handler = logging.FileHandler(MASKS_LOG_FILE, mode="w", encoding="utf-8")
_file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_file_handler.setFormatter(_file_formatter)

if not logger.handlers:
    logger.addHandler(_file_handler)

logger.propagate = False


def get_mask_card_number(card_number: str | None) -> str:
    """
    Маскирует номер карты:
    - сохраняет первые 6 и последние 4 цифры,
    - остальное заменяет на '*',
    - возвращает строку в формате 'XXXX XX** **** XXXX'.

    Если входные данные некорректные или слишком короткие (< MIN_CARD_LENGTH) —
    возвращает пустую строку.
    """
    if not card_number:
        logger.error("get_mask_card_number: empty input")
        return ""

    digits = "".join(symbol for symbol in card_number if symbol.isdigit())

    if len(digits) < MIN_CARD_LENGTH:
        logger.error("get_mask_card_number: too short (%d digits)",
                     len(digits))
        return ""

    first_six_symbols = digits[:VISIBLE_CARD_PREFIX]
    last_four_symbols = digits[-VISIBLE_CARD_SUFFIX:]
    middle_symbols = MASK_SYMBOL * (len(digits) -
                                    VISIBLE_CARD_PREFIX -
                                    VISIBLE_CARD_SUFFIX)

    masked = f"{first_six_symbols}{middle_symbols}{last_four_symbols}"

    logger.info("get_mask_card_number: masked card produced")

    return " ".join(masked[i: i + GROUP_SIZE]
                    for i in range(0, len(masked), GROUP_SIZE))


def get_mask_account(account: str | None) -> str:
    """
    Маскирует номер счёта:
    - сохраняет только последние 4 цифры,
    - возвращает строку в формате 'Счет **XXXX' или 'Счёт **XXXX'.

    Если входные данные некорректные или цифр < 4 — возвращает пустую строку.
    """
    if not account:
        logger.error("get_mask_account: empty input")
        return ""

    digits = "".join(symbol for symbol in account if symbol.isdigit())

    if len(digits) < VISIBLE_CARD_SUFFIX:
        logger.error("get_mask_account: less than %d digits",
                     VISIBLE_CARD_SUFFIX)
        return ""

    last_four_symbols = digits[-VISIBLE_CARD_SUFFIX:]

    prefix = ""

    if account.startswith(ACCOUNT_PREFIX_1):
        prefix = ACCOUNT_PREFIX_1
    elif account.startswith(ACCOUNT_PREFIX_2):
        prefix = ACCOUNT_PREFIX_2

    logger.info("get_mask_account: masked account produced with suffix ****%s",
                last_four_symbols)

    return f"{prefix}{ACCOUNT_MASK_PREFIX}{last_four_symbols}"
